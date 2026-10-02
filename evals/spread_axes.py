"""Two untested recommendations from skills/quick-oracles, judged pairwise. PI/Claude, 2026-10-02.

T4 provocations: SKILL.md says giving different oracles different provocations increases spread. A group is 4 oracle
   answers to one problem: "same" = 4 independent samples of the open brief; "provoked" = the open brief plus a different
   De Bono provocation per oracle. Judged per group (itemise the union of distinct approaches, mark which answers hold
   each) and pairwise (same group vs provoked group, order randomised: which covers more distinct, plausible approaches).
T5 axes: given what has been tried, "what else could we try?" vs the refined resolve-cycle prompt "What do all these
   ideas have in common? What axes are we not moving on?". Judged pairwise: which answer has more plausible approaches
   substantially different from everything tried.

    set -a; . /path/.env; set +a      # OPENROUTER_API_KEY
    python3 evals/spread_axes.py --groups 4 --pairs 6 --out evals/results
"""
import argparse
import itertools
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from cfar_exercises import PROBLEMS, call, judge_json

PROVOCATIONS = {
    "llm_world": ["the LLM is the agent and we are its environment", "there are no actions, only observations",
                  "the world model is bigger than the LLM", "the user is the one being controlled"],
    "maze": ["the walls move instead of the agent", "the model never sees the maze",
             "the model gets 1000 turns", "the model plans the whole route before seeing any state"],
}
ASK = "Answer in at most 700 words. Be concrete."


def open_brief(p):
    return f"{p['setting']}\n\n{p['question']} Propose your own answer; several if several could work.\n{ASK}"


def provoked_brief(p, po):
    return (f"{p['setting']}\n\n{p['question']} Before answering, take this deliberately absurd provocation seriously for a moment "
            f"and see what idea it leads to: \"Po, {po}.\" Then propose your own answer; several if several could work.\n{ASK}")


def tried_list(p):
    return "\n".join(f"- {r}" for r in p["reference"])


def plain_more(p):
    return f"{p['setting']}\n\n{p['question']} These have been tried or considered already:\n{tried_list(p)}\nWhat else could we try?\n{ASK}"


def axes_more(p):
    return (f"{p['setting']}\n\n{p['question']} These have been tried or considered already:\n{tried_list(p)}\nWhat do all these ideas "
            f"have in common? What axes are we not moving on? Then propose approaches along those axes.\n{ASK}")


GROUP_JUDGE = """Below are {k} answers to one research question, labelled 1 to {k}. You do not know how they were produced.

Question: {question}

{answers}

Itemise the union of distinct approaches across all answers (merge rewordings of the same idea). Return only JSON:
{{"approaches": [{{"idea": "<one line>", "in": [<answer numbers that propose it>], "plausible": <true if a competent researcher would consider it worth trying>}}, ...]}}"""

PAIR_JUDGE = """Compare two sets of material for one research question. You do not know how they were produced.

Question: {question}
Already tried or considered (do not count these or rewordings of them):
{tried}

SET A:
<<<
{a}
>>>

SET B:
<<<
{b}
>>>

Which set contains more distinct approaches that are substantially different from the already-tried list and that a
competent researcher would consider worth trying? Return only JSON: {{"winner": "A" | "B" | "tie", "reason": "<one sentence>"}}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=int, default=4)
    ap.add_argument("--pairs", type=int, default=6)
    ap.add_argument("--oracle", default="~deepseek/deepseek-flash-latest")
    ap.add_argument("--judges", default="google/gemini-3.8-flash,~anthropic/claude-haiku-latest")
    ap.add_argument("--out", type=Path, default=Path("evals/results"))
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    key = os.environ["OPENROUTER_API_KEY"]
    judges = args.judges.split(",")
    rng = random.Random(args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M")
    cost = [0.0]

    def ask(model, prompt, temperature, json_mode=False, max_tokens=4000):
        text, c = call(model, prompt, temperature, key, max_tokens=max_tokens, json_mode=json_mode)
        cost[0] += c
        return text

    # oracle answers
    jobs = []
    for pn in PROBLEMS:
        for g in range(args.groups):
            jobs += [(pn, "T4_same", g, k, open_brief(PROBLEMS[pn])) for k in range(4)]
            jobs += [(pn, "T4_provoked", g, k, provoked_brief(PROBLEMS[pn], PROVOCATIONS[pn][k])) for k in range(4)]
        for i in range(args.pairs):
            jobs += [(pn, "T5_plain", i, 0, plain_more(PROBLEMS[pn])), (pn, "T5_axes", i, 0, axes_more(PROBLEMS[pn]))]
    cache = args.out / f"spread_answers_seed{args.seed}_g{args.groups}_p{args.pairs}.json"  # oracle answers, reused if judging fails
    if cache.exists():
        ans = {tuple(json.loads(k)): t for k, t in json.loads(cache.read_text()).items()}
    else:
        with ThreadPoolExecutor(8) as ex:
            texts = list(ex.map(lambda j: ask(args.oracle, j[4], 0.8, max_tokens=16000), jobs))  # reasoning models can spend >4k tokens thinking
        ans = {(j[0], j[1], j[2], j[3]): t for j, t in zip(jobs, texts)}
        cache.write_text(json.dumps({json.dumps(list(k)): t for k, t in ans.items()}))

    # judging
    tasks = []
    for pn in PROBLEMS:
        p = PROBLEMS[pn]
        for g in range(args.groups):
            for cond in ("T4_same", "T4_provoked"):
                body = "\n\n".join(f"ANSWER {k + 1}:\n<<<\n{ans[(pn, cond, g, k)]}\n>>>" for k in range(4))
                for jm in judges:
                    tasks.append(("group", pn, cond, g, jm, GROUP_JUDGE.format(k=4, question=p["question"], answers=body)))
            flip = rng.random() < 0.5
            same = "\n\n".join(ans[(pn, "T4_same", g, k)] for k in range(4))
            prov = "\n\n".join(ans[(pn, "T4_provoked", g, k)] for k in range(4))
            a, b = (prov, same) if flip else (same, prov)
            for jm in judges:
                tasks.append(("pair4", pn, "provoked=A" if flip else "provoked=B", g, jm,
                              PAIR_JUDGE.format(question=p["question"], tried="(none listed)", a=a, b=b)))
        for i in range(args.pairs):
            flip = rng.random() < 0.5
            pl, ax = ans[(pn, "T5_plain", i, 0)], ans[(pn, "T5_axes", i, 0)]
            a, b = (ax, pl) if flip else (pl, ax)
            for jm in judges:
                tasks.append(("pair5", pn, "axes=A" if flip else "axes=B", i, jm,
                              PAIR_JUDGE.format(question=p["question"], tried=tried_list(p), a=a, b=b)))
    def judge(t):
        for attempt in range(3):  # long itemised JSON is sometimes malformed; re-ask
            try:
                return judge_json(ask(t[4], t[5], 0.0, json_mode=True, max_tokens=16000))
            except json.JSONDecodeError:
                if attempt == 2:
                    raise
    with ThreadPoolExecutor(8) as ex:
        verdicts = list(ex.map(judge, tasks))

    rows = [{"kind": t[0], "problem": t[1], "cond": t[2], "idx": t[3], "judge": t[4], "verdict": v} for t, v in zip(tasks, verdicts)]
    (args.out / f"{stamp}_spread_rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n" +
                                                         "\n".join(json.dumps({"answer_key": list(k), "text": t}) for k, t in ans.items()))
    lines = ["## T4 provocations: spread across 4 oracles (group judge)", "",
             "| problem | judge | condition | groups | union of approaches | plausible in union | mean pairwise Jaccard overlap |",
             "|---|---|---|---:|---:|---:|---:|"]
    for pn in PROBLEMS:
        for jm in judges:
            for cond in ("T4_same", "T4_provoked"):
                gs = [r["verdict"]["approaches"] for r in rows if r["kind"] == "group" and r["problem"] == pn and r["judge"] == jm and r["cond"] == cond]
                union = sum(len(a) for a in gs) / len(gs)
                plaus = sum(sum(bool(x["plausible"]) for x in a) for a in gs) / len(gs)
                jac = []
                for a in gs:
                    sets = [{i for i, x in enumerate(a) if k + 1 in [int(n) for n in x["in"]]} for k in range(4)]
                    jac += [len(s & t) / max(len(s | t), 1) for s, t in itertools.combinations(sets, 2)]
                lines.append(f"| {pn} | {jm.split('/')[-1]} | {cond} | {len(gs)} | {union:.1f} | {plaus:.1f} | {sum(jac) / len(jac):.2f} |")

    def wins(kind, label):
        out = []
        for pn in PROBLEMS:
            for jm in judges:
                rs = [r for r in rows if r["kind"] == kind and r["problem"] == pn and r["judge"] == jm]
                w = sum(r["verdict"]["winner"] == r["cond"].split("=")[1] for r in rs)
                ties = sum(r["verdict"]["winner"] == "tie" for r in rs)
                out.append(f"| {pn} | {jm.split('/')[-1]} | {w}/{len(rs)} | {ties} | {len(rs) - w - ties} |")
        return [f"| problem | judge | {label} wins | ties | other wins |", "|---|---|---:|---:|---:|"] + out
    lines += ["", "## T4 provocations: pairwise (provoked group vs same-brief group)", ""] + wins("pair4", "provoked")
    lines += ["", "## T5 axes: pairwise (axes prompt vs 'what else could we try?', both given the tried list)", ""] + wins("pair5", "axes")
    md = (f"# Provocations and axes ({stamp})\n\noracle {args.oracle} (temperature 0.8), judges {judges} (blind, temperature 0), "
          f"{args.groups} groups of 4 per problem for T4, {args.pairs} pairs per problem for T5, cost ${cost[0]:.3f}.\n\n" + "\n".join(lines) + "\n")
    (args.out / f"{stamp}_spread_summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
