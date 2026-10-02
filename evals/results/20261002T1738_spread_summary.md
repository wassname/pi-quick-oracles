# Provocations and axes (20261002T1738)

oracle ~deepseek/deepseek-flash-latest (temperature 0.8), judges ['google/gemini-3.8-flash', '~anthropic/claude-haiku-latest'] (blind, temperature 0), 4 groups of 4 per problem for T4, 6 pairs per problem for T5, cost $0.800.

## T4 provocations: spread across 4 oracles (group judge)

| problem | judge | condition | groups | union of approaches | plausible in union | mean pairwise Jaccard overlap |
|---|---|---|---:|---:|---:|---:|
| llm_world | gemini-3.8-flash | T4_same | 4 | 5.0 | 4.5 | 0.60 |
| llm_world | gemini-3.8-flash | T4_provoked | 4 | 6.8 | 6.2 | 0.34 |
| llm_world | claude-haiku-latest | T4_same | 4 | 16.8 | 16.0 | 0.50 |
| llm_world | claude-haiku-latest | T4_provoked | 4 | 14.0 | 12.8 | 0.28 |
| maze | gemini-3.8-flash | T4_same | 4 | 10.2 | 10.2 | 0.77 |
| maze | gemini-3.8-flash | T4_provoked | 4 | 10.8 | 10.2 | 0.60 |
| maze | claude-haiku-latest | T4_same | 4 | 17.8 | 17.8 | 0.65 |
| maze | claude-haiku-latest | T4_provoked | 4 | 15.8 | 15.0 | 0.47 |

## T4 provocations: pairwise (provoked group vs same-brief group)

| problem | judge | provoked wins | ties | other wins |
|---|---|---:|---:|---:|
| llm_world | gemini-3.8-flash | 4/4 | 0 | 0 |
| llm_world | claude-haiku-latest | 2/4 | 0 | 2 |
| maze | gemini-3.8-flash | 2/4 | 1 | 1 |
| maze | claude-haiku-latest | 0/4 | 3 | 1 |

## T5 axes: pairwise (axes prompt vs 'what else could we try?', both given the tried list)

| problem | judge | axes wins | ties | other wins |
|---|---|---:|---:|---:|
| llm_world | gemini-3.8-flash | 2/6 | 0 | 4 |
| llm_world | claude-haiku-latest | 3/6 | 0 | 3 |
| maze | gemini-3.8-flash | 4/6 | 0 | 2 |
| maze | claude-haiku-latest | 5/6 | 0 | 1 |
