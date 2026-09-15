# Pi Quick Oracles

Short, independent second opinions: a neutral page in, about a page back, then clarify misunderstandings and missing information. Useful at decision branches as well as for reviews.

Uses [Nico's pi-subagents](https://github.com/nicobailon/pi-subagents): 4000 generated tokens across review turns, then one 2000-token final answer with native conversation state retained.

```sh
pi install git:github.com/wassname/pi-quick-oracles
```

Requires Pi ≥0.85.1 and pi-subagents ≥0.66.0. Reload, then ask Pi to use `pi-quick-oracles`. The extension loads only in the oracle child. [Workflow](skills/quick-oracles/SKILL.md).

-- Pi/OpenAI
