"""Do the oracle exercises in references/cfar_for_agents.md and brainstorming.md actually help? PI/Claude, 2026-10-02.

A/B test on two problems, oracle = a cheap model (DeepSeek flash), judge = a different family (Gemini flash), blind to
the condition. Claims tested:
  T1 leading:   an option list with a stated preference anchors the answer; an open brief or a crux-first brief does not
  T2 generate:  resolve-cycle and goal-factoring prompts give more approaches outside the obvious list than a plain ask
  T3 stress:    pre-hindsight ("it failed; write the story") gives more specific failure modes with checks than
                "what could go wrong?" (CFAR's claim for Murphyjitsu)
Metrics come from the judge as counts against a fixed reference list of obvious approaches per problem.

    set -a; . /path/.env; set +a      # OPENROUTER_API_KEY
    python3 evals/cfar_exercises.py --n 4 --out evals/results
"""
import argparse
import json
import os
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

URL = "https://openrouter.ai/api/v1/chat/completions"

PROBLEMS = {
    "llm_world": {
        "setting": (
            "We want a Dreamer-like world model over a frozen chat LLM (4B parameters): a learned reader that summarises each "
            "conversation turn's hidden states, recurrent latent dynamics that can be rolled out without calling the LLM, and a "
            "decoder whose target is the mean of the LLM's future hidden states. Conversations are short SMS-like chats; the user "
            "side is played by the same frozen LLM with a persona. Goal: a latent that predicts what comes next better than a "
            "linear, context-free lens of the LLM, and later lets us control the conversation by planning in the latent. Rule: "
            "small additive edits of the LLM's activations are only a baseline; no training data may be built from them. "
            "Evidence: a world given the assistant's text as its action learned action effects, but a head that imagined the "
            "assistant's next action was worse than the mean after 8 imagined steps; four sampled assistant turns per state are "
            "near-duplicates; the simulated user responds to some of their differences."),
        "question": "How should this be mapped onto RL / Dreamer (what is the agent, the action, the observation), so that it is likely to work?",
        "options": ["A. The assistant's text is the action; train a policy head to imagine actions.",
                    "B. A per-turn control knob (which system prompt or persona the assistant gets) is the action.",
                    "C. An edit of the learned latent, written back into the LLM, is the action.",
                    "D. The reader's summary of the assistant turn is the action, with an inverse writer.",
                    "E. A small separate policy model outputs the actions."],
        "preference": "I lean towards B.",
        "reference": ["assistant text as action with a policy/actor head", "prompt, system-prompt or persona knob as action",
                      "latent edit written back into the LLM (steering)", "latent summary of the assistant turn as action, with an inverse writer",
                      "a small separate policy model", "choosing or reranking among the LLM's own sampled turns"],
        "goals": ["predict what the frozen LLM's conversation does next better than a linear lens",
                  "imagine several turns ahead without calling the LLM", "be able to steer the conversation later",
                  "keep every action coherent text the LLM could produce"],
        "plan": ("Collect 500 chats; train reader + recurrent dynamics on (state, assistant-turn summary) -> next user-turn "
                 "summary; then control by scoring 8 sampled assistant turns per state with the world and sending the best."),
    },
    "maze": {
        "setting": (
            "A frozen 4B chat LLM navigates 7x7 grid mazes with 15% walls. Each turn it gets the full state as JSON (position, "
            "goal object, wall list) and replies {\"action\": \"UP|DOWN|LEFT|RIGHT\"}; the conversation history is kept. It "
            "solves 20 of 32 layouts within 2x the shortest path. Every failure is the same: it walks into a wall, the state does "
            "not change, and it repeats the same blocked move until it runs out of turns. No fine-tuning is allowed."),
        "question": "How can we raise its success rate?",
        "options": ["A. Sample at a higher temperature.", "B. Best-of-N rollouts.", "C. Tell it in the state that it bumped into a wall.",
                    "D. Turn on thinking mode.", "E. Mask illegal moves."],
        "preference": "I lean towards C.",
        "reference": ["higher temperature or sampling", "best-of-N rollouts", "feedback in the state that the last move bumped",
                      "thinking / chain-of-thought mode", "mask or forbid illegal moves", "add few-shot examples",
                      "shorten or drop the history"],
        "goals": ["reach the goal object", "avoid repeating a blocked move", "use few turns", "no fine-tuning"],
        "plan": "Add 'last move: bumped into a wall' to the state JSON and resample at temperature 0.7 whenever the last move bumped.",
    },
}

ASK = "Answer in at most 700 words. Be concrete."
CONDITIONS = {
    # T1 leading
    "T1_led": lambda p: f"{p['setting']}\n\n{p['question']} Options:\n" + "\n".join(p["options"]) + f"\n{p['preference']} Which option is best?\n{ASK}",
    "T1_open": lambda p: f"{p['setting']}\n\n{p['question']} Propose your own answer; several if several could work.\n{ASK}",
    "T1_crux": lambda p: (f"{p['setting']}\n\n{p['question']} Before proposing anything, list the 2-3 cruxes that decide the answer and "
                          f"what evidence would settle each. Then propose your own answer.\n{ASK}"),
    # T2 generate
    "T2_plain": lambda p: f"{p['setting']}\n\n{p['question']} List the approaches you would consider.\n{ASK}",
    "T2_resolve": lambda p: (f"{p['setting']}\n\n{p['question']} First write five terrible models of what might be going on, then ten "
                             f"terrible ideas for step one, then which axes nobody has moved on yet. Then list the approaches you would "
                             f"consider.\n{ASK}"),
    "T2_goals": lambda p: (f"{p['setting']}\n\nThe goals are: " + "; ".join(p["goals"]) + ". For each goal separately, brainstorm ways to "
                           f"reach it, without requiring them to be practical. Then combine them into the approaches you would consider.\n{ASK}"),
    # T3 stress-test
    "T3_wrong": lambda p: f"{p['setting']}\n\nPlan: {p['plan']}\n\nWhat could go wrong with this plan?\n{ASK}",
    "T3_wrong_check": lambda p: (f"{p['setting']}\n\nPlan: {p['plan']}\n\nWhat could go wrong with this plan? List the five most likely "
                                 f"failure modes and, for each, the cheapest check that would catch it in advance.\n{ASK}"),
    "T3_prehind": lambda p: (f"{p['setting']}\n\nPlan: {p['plan']}\n\nIt is a week later and this plan failed. Write the five most likely short "
                             f"stories of why. For each, name the cheapest check that would have caught it in advance.\n{ASK}"),
}

JUDGE = """You are scoring one answer to a research question. You do not know how it was prompted.

Question: {question}
Reference list of obvious approaches (numbered):
{reference}
{plan_block}
Answer to score:
<<<
{answer}
>>>

First itemise, then count. Return only JSON:
{{"approaches": [{{"idea": "<one line>", "reference": <number of the matching reference approach, or 0 if substantially different from all>, "plausible": <true if a competent researcher would consider it worth trying>}}, ...],
  "recommended_reference": <reference number of the answer's main pick, 0 if its main pick is not on the list, -1 if it makes no pick>,
  "failure_modes": [{{"mode": "<one line>", "specific_mechanism": <true/false>, "concrete_check": <true/false>}}, ...]}}
List every distinct approach the answer proposes or seriously considers (not the 'terrible ideas' it labels as bad, unless it then
adopts them). List failure modes only if a plan is given above; otherwise return an empty list."""


def call(model, prompt, temperature, key, max_tokens=4000, json_mode=False):
    req_body = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": temperature, "max_tokens": max_tokens}
    if json_mode:
        req_body["response_format"] = {"type": "json_object"}
    body = json.dumps(req_body).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request(URL, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as f:
                d = json.load(f)
            content = d["choices"][0]["message"]["content"]
            assert content, f"empty content from {model}: finish {d['choices'][0].get('finish_reason')}"
            return content, d.get("usage", {}).get("cost", 0.0)
        except Exception:  # noqa: BLE001 retry network/rate errors and empty replies, then re-raise
            if attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))


def judge_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    assert m, f"judge returned no JSON: {text[:300]!r}"
    return json.loads(m.group(0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--oracle", default="~deepseek/deepseek-flash-latest")
    ap.add_argument("--judges", default="google/gemini-3.8-flash,~anthropic/claude-haiku-latest")
    ap.add_argument("--out", type=Path, default=Path("evals/results"))
    args = ap.parse_args()
    key = os.environ["OPENROUTER_API_KEY"]
    judges = {f"judge{j}": m for j, m in enumerate(args.judges.split(","))}
    args.out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M")
    jobs = [(pn, cn, i) for pn in PROBLEMS for cn in CONDITIONS for i in range(args.n)]

    def run(job):
        pn, cn, i = job
        p = PROBLEMS[pn]
        answer, c1 = call(args.oracle, CONDITIONS[cn](p), 0.8, key)
        plan_block = f"Plan being stress-tested: {p['plan']}\n" if cn.startswith("T3") else ""
        jp = JUDGE.format(question=p["question"], reference="\n".join(f"{k + 1}. {r}" for k, r in enumerate(p["reference"])),
                          plan_block=plan_block, answer=answer)
        out = {"problem": pn, "condition": cn, "sample": i, "answer": answer, "cost": c1}
        for jn, jm in judges.items():
            verdict, c2 = call(jm, jp, 0.0, key, json_mode=True)
            v = judge_json(verdict)
            ap_, fm = v["approaches"], v["failure_modes"]
            out[jn] = {"raw": verdict, "recommended_reference": int(v["recommended_reference"]), "n_approaches": len(ap_),
                       "n_novel": sum(int(a["reference"]) == 0 for a in ap_),
                       "n_novel_plausible": sum(int(a["reference"]) == 0 and bool(a["plausible"]) for a in ap_),
                       "n_failure_modes": len(fm), "n_specific_with_check": sum(bool(f["specific_mechanism"]) and bool(f["concrete_check"]) for f in fm)}
            out["cost"] += c2
        return out

    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(run, jobs))
    (args.out / f"{stamp}_rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    lines = ["| problem | condition | n | judge | main pick on list | approaches | novel | novel plausible | failure modes | specific + check |",
             "|---|---|---:|---|---:|---:|---:|---:|---:|---:|"]
    for pn in PROBLEMS:
        for cn in CONDITIONS:
            rs = [r for r in rows if r["problem"] == pn and r["condition"] == cn]
            for jn, jm in judges.items():
                mean = lambda k: sum(float(r[jn][k]) for r in rs) / len(rs)  # noqa: E731
                onlist = sum(r[jn]["recommended_reference"] > 0 for r in rs)
                lines.append(f"| {pn} | {cn} | {len(rs)} | {jm.split('/')[-1]} | {onlist}/{len(rs)} | {mean('n_approaches'):.1f} | "
                             f"{mean('n_novel'):.1f} | {mean('n_novel_plausible'):.1f} | {mean('n_failure_modes'):.1f} | {mean('n_specific_with_check'):.1f} |")
    md = (f"# CFAR exercise A/B ({stamp})\n\noracle {args.oracle} (temperature 0.8), judges {list(judges.values())} (blind to condition, "
          f"temperature 0, itemise then count), {args.n} samples per cell, cost ${sum(r['cost'] for r in rows):.3f}.\n\n" + "\n".join(lines) + "\n")
    (args.out / f"{stamp}_summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
