# Evals

`cfar_exercises.py`: A/B test of the oracle exercises in `skills/quick-oracles/references/` (PI/Claude, 2026-10-02).
Oracle DeepSeek flash via OpenRouter, two blind judges from other families, two problems, itemise-then-count judging.
Needs `OPENROUTER_API_KEY`. Runs in about 10 minutes for about $1.3 at `--n 6`.

Results: `results/20261002T1545_summary.md` (main run) and `results/20261002T1535_summary.md` (first run; its judge
undercounted and two comparisons were unfair: the pre-hindsight prompt alone asked for checks, and the resolve-cycle
prompt ran out of its 400-word budget). Raw answers and judge outputs are in the matching `_rows.jsonl`.

Findings and limits are summarised in `skills/quick-oracles/references/cfar_for_agents.md`. Judges disagree on absolute
counts (Haiku itemises 3-5x more than Gemini on the same answers); only directions shared by both judges on both
problems are reported as support.

`spread_axes.py`: provocations per oracle (spread across 4 oracles, group and pairwise judging) and the refined
resolve-cycle "which axes are we not moving on?" prompt vs "what else could we try?" (pairwise). Results:
`results/20261002T1738_spread_summary.md`. Oracle answers are cached in `results/spread_answers_*.json` so judging can be rerun.
