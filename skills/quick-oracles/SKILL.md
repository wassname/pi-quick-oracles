---
name: quick-oracles
description: "Runs iterative frontier-model consultations. Required reruns for echoed primer bias, no surprising insight or viable disagreement, and confused or unworkable answers. Finds alternate providers when credits run out."
---

# Quick oracles

## Required: detect and repair these two failures

The parent must enforce these checks before accepting oracle advice. “They all agreed” is not a successful consultation. Do not act on a failed consultation as if it validated a plan or disproved a method.

### 1. The primer returns your own perspective

If the answers provide neither a surprising insight nor genuinely viable disagreement, the framing test has failed. Do not explain it away as consensus. It is easy to put your perspective into the primer and get it back from every model, even across model families.

Re-read the actual primer against the user's goals and primary observations. Remove your preferred diagnosis, loaded descriptions, suggested answer menu and assumed constraints. Add missing observations, source excerpts and context, including evidence against your view. Ask an open question that permits different mechanisms and tractable approaches beyond your proposals. Preserve the user's real constraints; widen the perspective, not the goal. Then rerun with fresh readers who have not seen the old verdicts. Merely asking the same readers to defend their answers repeats the anchoring.

Repeat until the consultation adds a substantive perspective rather than echoing the primer. Do not demand novelty or dissent for its own sake: an incoherent objection is not viable disagreement, and a surprising claim still needs checking. If budget or missing evidence blocks repair, report failed framing or an incomplete consultation, not success.

### 2. A reader is confused, but the parent accepts the answer

Read every answer carefully, including confident ones. Check whether it reconstructs the actual mechanism, whether its recommendation is internally coherent, and whether the proposed solution can work under the user's constraints. One confused reader is enough to require investigation; a majority vote does not resolve a misunderstanding.

Quote the suspect claim and compare it with the paper, code or a small worked example. Read the primary source yourself until you can explain the relevant mechanism. For example, “J-lens is sensitivity, not prediction” does not refute a proposal using its linearized prediction of intervention effects: identify the input, target, horizon and mapping before judging the comparison. Distinguish predicting a perturbation's effect from forecasting unperturbed states or exact generated text.

An objection resting on a mistaken concept is invalid evidence, not a negative result for the user's idea. Correct the concept explanation and missing context in the primer, then rerun a fresh comprehension check. Resolve other material confusion with evidence-directed follow-ups. Do not paste the desired verdict into the correction or accept an incoherent solution because a frontier model proposed it.

Use the `pi-quick-oracles` agent through Nico's `subagent` tool. Consult one oracle at an uncertain branch, or use different model families for independent perspectives. Respect the user's chosen models and budget; discover available models rather than guessing names. Oracles can help during exploration, not only at final review.

## Brief and answer

Write a neutral one-page brief and request about one page back, roughly 500 words each. Include the question, goals, constraints, observations, contrary evidence and known gaps. Attach necessary source excerpts or code separately. Separate observations from interpretation.

Do not lead the witness. Withhold your preferred answer, suspected cause and peer verdicts from initial oracles unless that hypothesis is explicitly the question being examined. Ask each oracle to reconstruct the situation in its own terms. For separate branches, supply the shared facts and each branch's question; keep the first answers independent.

Include an "already measured" list: every earlier result that bears on the question, with numbers. Oracles cannot use what the brief leaves out; search your journal and logs for it before sending. Write background claims as hypotheses, not facts ("J-lens may be more causal", not "J-lens is causal by construction"); oracles repeat a stated framing instead of testing it. Give models with long reasoning (for example Fable) a larger final-answer budget, so a truncated answer does not lose the round. -- PI/Claude, 2026-10-12, from a 3-round, 4-family brainstorm where the deciding fact was in the journal but not in the brief

## Iterate and record what happened

Enforce the two required checks above after every round. For a disputed claim, send its quote and the relevant evidence, request a revised assessment, and check the reply again. For failed framing or comprehension, repair the primer and test fresh readers. An explicit one-shot request limits the calls, not the standard of evidence; label unchecked or failed advice accordingly.

In the existing review artifact, retain the initial claim, source/check and observed result, changed primer or actual follow-up prompt, new answer, remaining uncertainty and evidence-based stopping reason. A promised rerun is not an executed rerun. Return checked findings and their effect on the parent's decision, not a vote tally. Label follow-ups and peer discussion as such, not as independent evidence.

## Provider credits are a routing problem

In Pi, use `subagent({action: "models"})` to find provider-qualified alternatives. Catalog presence is not proof of usable credits or authentication; test the replacement through the same tool.

On an exhausted subscription, credit limit or unavailable provider, read the exact error and discover another configured provider for the same model. Use that route within the approved budget; announce the provider change and record the failed route. Do not give up because one provider is exhausted, repeat a known credit failure, invent model IDs or obtain another project's credentials. If the exact model is unavailable, use an allowed same-family equivalent; respect an explicitly fixed model/provider or ask for a consequential substitution.

Stay in the same governed tool workflow. A different provider is a fresh run: reuse the neutral brief and necessary evidence, not signed/encrypted state from another backend. Record it as a replacement, not an independent extra vote. Only report a routing blocker after checking the permitted alternatives; do not silently change model tier or expand spending.

## Budget

Each run shares 4000 generated tokens, including reasoning, across its tool-using turns. At the cutoff, the same child preserves its native conversation, disables tools and gets one final-answer call with minimum supported thinking and a separate 2000-token allowance. A second truncation is incomplete; do not retry it automatically.

`PI_REVIEW_TOKENS` and `PI_ANSWER_TOKENS` can set these allowances before starting Pi; both must be integers of at least 16. Each new run receives a new allowance. Input tokens and external tool costs are not capped.

Load the TypeScript extension only through the child agent, never in the parent session. Unknown APIs and incompatible explicit Anthropic thinking budgets stop with an error. Do not replace native signed/encrypted state with visible text or change backends silently.

-- Pi/OpenAI
