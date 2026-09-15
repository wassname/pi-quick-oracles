---
name: quick-oracles
description: "Quick second opinions for open questions, uncertain decision branches and reviews. Uses neutral one-page briefs, independent answers and iterative clarification."
---

# Quick oracles

Use the `pi-quick-oracles` agent through Nico's `subagent` tool. Consult one oracle at an uncertain branch, or use different model families for independent perspectives. Respect the user's chosen models and budget; discover available models rather than guessing names. Oracles can help during exploration, not only at final review.

## Brief and answer

Write a neutral one-page brief and request about one page back, roughly 500 words each. Include the question, goals, constraints, observations, contrary evidence and known gaps. Attach necessary source excerpts or code separately. Separate observations from interpretation.

Do not lead the witness. Withhold your preferred answer, suspected cause and peer verdicts from initial oracles unless that hypothesis is explicitly the question being examined. Ask each oracle to reconstruct the situation in its own terms. For separate branches, supply the shared facts and each branch's question; keep the first answers independent.

## Clarify and iterate

Check claims against their sources. If there is confusion or missing information, quote the disputed claim, supply the relevant evidence, and request a revised assessment in a new bounded run. If the brief was leading, correct it and test a fresh oracle. Do not coach a desired conclusion.

Repeat until material confusion, leading framing and missing information are resolved. If evidence is unavailable or the agreed budget is exhausted, report what remains unresolved rather than claiming completion. Agreement is not the stopping criterion. Label follow-ups and peer discussion as such, not as independent evidence.

## Budget

Each run shares 4000 generated tokens, including reasoning, across its tool-using turns. At the cutoff, the same child preserves its native conversation, disables tools and gets one final-answer call with minimum supported thinking and a separate 2000-token allowance. A second truncation is incomplete; do not retry it automatically.

`PI_REVIEW_TOKENS` and `PI_ANSWER_TOKENS` can set these allowances before starting Pi; both must be integers of at least 16. Each new run receives a new allowance. Input tokens and external tool costs are not capped.

Load the TypeScript extension only through the child agent, never in the parent session. Unknown APIs and incompatible explicit Anthropic thinking budgets stop with an error. Do not replace native signed/encrypted state with visible text or change backends silently.

-- Pi/OpenAI
