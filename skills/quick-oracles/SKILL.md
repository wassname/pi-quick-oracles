---
name: quick-oracles
description: "Runs iterative frontier-model consultations. Required reruns for echoed primer bias, no surprising insight or viable disagreement, and confused or unworkable answers. Finds alternate providers when credits run out."
---

# Quick oracles

A consultation has two purposes: to obtain perspectives that you do not have, and to test whether
your explanation of the problem can be understood. Each has one failure signal, and both failures
are faults of the brief, not of the oracles.

> If the models have uniform opinions the setup failed to brainstorm. If they misunderstand it
> failed to inform. -- wassname, 2026-11-16 (spelling corrected)

> We are searching for a new perspective or concepts or insights. Not more of the same or clinging
> to existing ideas. -- wassname, 2026-11-16

Do not report that oracles agree. Agreement between readers of one brief measures the brief.
Agreement with the user's stated view is the usual result of a brief that contains that view.

What counts as new: a different mechanism, a different way to state the problem, a concept from
another field, or an observation that the current explanation does not predict. What does not
count: a restatement of the brief, or a refinement of the current approach (another setting of the
same method, one more control, a larger sample).

## What to do

| when | steps, in order |
|---|---|
| before you send a brief | BRIEF |
| after every round of answers | ECHO, COMPREHENSION, VERIFY |
| ECHO or COMPREHENSION failed | REPAIR, then a new round with fresh readers |
| you report to the user | the block under [Your report](#your-report), one entry per round |

## The steps

### BRIEF

One page, about 500 words. Request about one page back. Attach source excerpts and code separately.

1. An open question. No list of options to choose from, and no preferred answer.
2. The goal and the constraints, in the user's words.
3. Observations, separate from interpretation. Include an "already measured" list: every earlier
   result that bears on the question, with its numbers. Search the journal and the logs for them
   first. An oracle cannot use what the brief omits.
4. Evidence against your current view, and the known gaps.
5. Background claims as hypotheses: "J-lens may be more causal", not "J-lens is causal by
   construction". An oracle repeats a stated framing; it does not test it.
6. Withhold your diagnosis, your suspected cause and the verdicts of other oracles, unless that
   hypothesis is the question.
7. The user's own opinions, when the oracle will read them (project instructions, quoted
   preferences): mark them as claims under test, and ask for the strongest case against each.
8. Ask the oracle to restate the problem in its own words before it answers. COMPREHENSION reads
   that restatement.
9. Ask for other ways to see the problem, not for improvements to the current approach: "What
   would explain these observations if our explanation is wrong?", "How would a different field
   state this problem?", "Which question should we ask instead?". With several oracles, give each
   a different position to argue from (for example: a sceptic of the method, a specialist of
   another field, a reader who assumes a bug).
10. Name the files to read. Tell the oracle not to explore beyond them: an oracle that spends its
   token budget on reading returns no answer.

| leading | neutral |
|---|---|
| "We think the loss weights are unbalanced. Do you agree?" | "The slope error is 0.94 at step 1,000; the reference run had 0.92. What could cause this?" |
| "Which is better, option A or option B?" | "What approaches could reach the goal under these constraints?" |

### ECHO: did the brief fail to brainstorm?

List the main claims of each answer. Classify each one: restatement (the brief contained it),
refinement (an adjustment of the current approach), or new perspective (a different mechanism,
framing, concept or unpredicted observation). The round failed if no answer has a new perspective,
and no answer disagrees with another answer or with you in a way that could be true. A round that
returns only refinements failed.

A failed round is not consensus. Using several model families does not prevent it: all of them
read the same brief.

Do not demand novelty or dissent for its own sake. An incoherent objection is not a viable
disagreement.

Your own attachment to the current idea is the second cause of an echo. State each new
perspective in its strongest form before you judge it. Do not answer it with the reasons why the
current plan was chosen; check it (VERIFY).

### COMPREHENSION: did the brief fail to inform?

Read every answer in full, including the confident ones. Compare each oracle's restatement, and
the mechanism its recommendation relies on, with the paper, the code or a small worked example.
Read the primary source yourself until you can explain the mechanism.

- One confused reader is sufficient to require investigation. A majority does not resolve a
  misunderstanding.
- An objection that rests on a mistaken concept is not evidence against the user's idea. Example:
  "J-lens is sensitivity, not prediction" does not refute a proposal that uses its linearised
  prediction of an intervention's effect. Identify the input, the target, the horizon and the
  mapping before you judge the comparison.
- Check that each recommended solution is internally coherent and can work under the user's
  constraints.

### VERIFY

A new claim is not yet a finding. Before you use one, check it against the source, the code or a
small computation, and record the check. For a disputed claim, send the quotation and the evidence
to the oracle, request a revised assessment, and check the reply.

### REPAIR

Change the brief, not the question to the same readers.

- After a failed ECHO: compare the brief with the user's goals and the primary observations.
  Remove your diagnosis, loaded descriptions, the answer menu and assumed constraints. Add missing
  observations, source excerpts and evidence against your view. Keep the user's real constraints:
  widen the perspective, not the goal.
- After a failed COMPREHENSION: correct the explanation of the concept and add the missing
  context. Do not paste the desired verdict into the correction.
- Send the repaired brief to fresh readers that have not seen the earlier answers. A request to
  the same readers to defend their answers repeats the anchoring.

Repeat until a round adds a checked, substantive perspective. If the budget or missing evidence
prevents the repair, report a failed or incomplete consultation. An explicit one-shot request
limits the number of calls, not the standard of evidence.

## Your report

Return findings that you checked and their effect on the decision. Then this block. The user reads
it to decide how much weight the consultation has. It states how many rounds ran and what happened
in each one.

```
quick-oracles: <n> rounds
round 1  <model A>, <model B>; brief: <path>
         BRIEF          my view in the brief: "<quote>" | withheld
                        user's views in the reading: marked as claims under test | not present
         ECHO           new perspective: <oracle> "<a different mechanism, framing or concept>" | none
                        refinements only: "<adjustment of the current approach>" | none
                        disagreement: <A> "<quote>" against <B or me> "<quote>" | none
                        passed | FAILED TO BRAINSTORM
         COMPREHENSION  <oracle> restated the problem as "<quote>": correct | wrong: <what>, per <file:line>
                        passed | FAILED TO INFORM
         VERIFY         "<claim>" checked against <file:line or computation>: holds | does not hold | not checked
         REPAIR         for round 2: removed "<text>"; added <observation or source>; fresh readers <models>
                        | none needed | not repaired: <reason>
round 2  ...            (the same lines for every round that ran)
DECISION <what changes in the plan, and which checked claim caused it> | nothing changes
```

- One `round` entry for every round that ran, including a failed one. Do not merge rounds, and do
  not report only the last one.
- Write `none` where it is true. `new perspective: none` with `disagreement: none` is a failed
  round, also when there are refinements; report it as one.
- A single round with a failed check and no repair is reported as a failed consultation, with the
  reason that the repair was not done.
- Do not write "the oracles agree", "consensus", "independently confirmed" or "3 of 4 oracles".
- Do not report an oracle's credence as evidence. Report the argument and your check of it.
- Label follow-up answers and replies to peer answers as such; they are not independent of the
  first round.
- A rerun that you promised is not a rerun that you executed.

Example of a failed first round and its repair:

```
quick-oracles: 2 rounds
round 1  gpt-6-astra, kimi-k3; brief: slop/briefs/20261116_why_small_gain.md
         BRIEF          my view in the brief: "the gain is small because the labels are few" (not withheld)
         ECHO           new perspective: none
                        refinements only: "use more direction sets", "train for longer"
                        disagreement: none
                        FAILED TO BRAINSTORM
         COMPREHENSION  astra restated the problem as "a lens fitted to predict later states": wrong:
                        the model is fitted to Qwen's gradient, per src/lucid3/probe_loss.py:41
                        FAILED TO INFORM
         VERIFY         not checked
         REPAIR         for round 2: removed my diagnosis and the two options; added the label formula
                        and the table of earlier results; asked "what would explain this if our
                        explanation is wrong?"; fresh readers glm-5.3 (sceptic), muse-spark-1.3 (control theory)
round 2  glm-5.3, muse-spark-1.3; brief: slop/briefs/20261116_why_small_gain_v2.md
         BRIEF          my view in the brief: withheld
         ECHO           new perspective: glm "the dose is chosen on 2 items, so the comparison is dominated by dose noise"
                        refinements only: none
                        disagreement: muse "the evaluation is too small to rank methods" against glm "the fit is the limit"
                        passed
         COMPREHENSION  both restatements correct
         VERIFY         "dose chosen on 2 items" checked against outputs/runs/<run>/calibration.json: holds
         REPAIR         none needed
DECISION calibrate the dose on 8 items before the next comparison (from glm's claim, verified)
```

Keep the same record in the review file, with the brief of each round and each answer in full.

## Running

Use the `pi-quick-oracles` agent through the `subagent` tool. Consult one oracle at an uncertain
branch, or several model families for different perspectives. Respect the user's choice of models
and budget. Find available models with `subagent({action: "models"})`; do not guess a model name.
Oracles are useful during exploration, not only at a final review. For separate branches, give
the shared facts and each branch's question, and keep the first answers separate.

## Provider credits are a routing problem

- On an exhausted subscription, a credit limit or an unavailable provider: read the exact error,
  then find another configured provider for the same model with `subagent({action: "models"})`.
  A model in the catalogue is not proof of credits or authentication; test the replacement through
  the same tool.
- Use the replacement within the approved budget. State the provider change and record the failed
  route. Do not repeat a known credit failure, invent a model ID, or use another project's
  credentials.
- If the exact model is unavailable, use an allowed equivalent of the same family. If the user
  fixed the model or the provider, ask before a substitution that matters.
- A different provider is a fresh run: reuse the neutral brief and the evidence, not signed or
  encrypted state from another backend. Record it as a replacement, not as an additional opinion.
- Report a routing blocker only after you have checked the permitted alternatives. Do not change
  the model tier or increase spending without saying so.

## Budget

- Each run has 4,000 generated tokens, reasoning included, shared across its tool-using turns.
- At the limit the same child keeps its conversation, loses its tools, and gets one final-answer
  call with minimum thinking and a separate allowance of 2,000 tokens. A second truncation is an
  incomplete answer; do not retry it automatically.
- `PI_REVIEW_TOKENS` and `PI_ANSWER_TOKENS` set the two allowances before Pi starts; each is an
  integer of at least 16. Every new run gets a new allowance. Input tokens and external tool
  costs have no limit.
- Load the TypeScript extension only through the child agent, never in the parent session.
  Unknown APIs and incompatible explicit Anthropic thinking budgets stop with an error. Do not
  replace signed or encrypted state with visible text, and do not change backends without
  saying so.

<!-- First version: Pi/OpenAI. Rewritten 2026-11-16 by Claude (PI, Fable) at wassname's request as
steps with a report block, after an agent reported "they agree with each other, and with your two
points" as the result of a consultation. The content of the two failure checks, the routing rules
and the budget is unchanged. Not yet tested on real consultations. -->
