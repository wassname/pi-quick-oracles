# Brainstorming with oracles

<!-- PI/Claude 2026-10-02, after a led oracle round (LUCID3): I listed 5 options including my own preference; all 4
oracles picked from the list. De Bono via the LessWrong post below; CFAR in cfar_for_agents.md. -->

## The failure this prevents

An option list in the brief turns a brainstorm into a multiple-choice test. The oracles pick from your list, agree
with each other, and you learn nothing you did not already think. Agreement among oracles that saw the same framing
is one sample, not four.

## Diverge first: provocations (De Bono, via LessWrong)

From [How to brainstorm effectively](https://www.lesswrong.com/posts/PrPk5ogJNK7QcPead/how-to-brainstorm-effectively),
summarising Edward de Bono's *Serious Creativity*:

> "A provocation is a seemingly random or nonsensical sentence or phrase. Movement is the process of going forward
> with a provocation and actually generating an idea."

Ways to make a provocation, each a sentence prefixed "po" (provoking operation):

| method | what you do | example from the post |
|---|---|---|
| escape | negate something taken for granted | "Po, restaurants do not have food" |
| reversal | reverse a standard relationship | "Po, the orange juice has me for breakfast" |
| exaggeration | push a dimension far outside its range (not to zero) | "Po, every household has 100 phones" |
| distortion | switch arrangements or time order | "Po, you close the letter after you post it" |
| wishful thinking | an impossible fantasy | "Po, the pencil should write by itself" |

Movement from a provocation: extract a principle, focus on the difference, moment to moment, positive aspects,
circumstances where it would have value. The post warns: "try to avoid saying 'oh, but this is just like this other
existing product' ... Saying an idea is 'the same as' something else gives the illusion of having fully explored the
idea" and "do not take too many steps when moving from a provocation. This will just lead you to an existing idea."

Use with oracles: give different oracles different provocations about the same problem (one per oracle), or ask one
oracle for several framings each starting from a different provocation. Tested 2026-10-02 (`evals/spread_axes.py`,
`evals/results/20261002T1738_spread_summary.md`): with 4 oracles per group, provocations cut the mean pairwise overlap of their ideas for both judges on
both problems (Jaccard 0.60 to 0.34, 0.50 to 0.28, 0.77 to 0.60, 0.65 to 0.47), but the total number of distinct ideas went
up for one judge and down for the other. Use them for independence between oracles, not for more ideas. Write the provocations from the problem's
own assumptions ("po, the user is the agent", "po, the frozen model is the controller"), not random ones.

## CFAR techniques

See `cfar_for_agents.md`: resolve cycles and goal factoring to generate options, Socratic ducking and double crux to
ask without leading, Murphyjitsu to stress-test a plan, with verified quotes from the LessWrong sequence in `cfar_handbook_lw/`.

## Signals that a round failed

- Every answer picks from options you supplied, or restates your preferred option.
- All oracles converge on one answer from one framing. Convergence counts only after independent framings.
- Nobody proposes something you had not considered.

Then change the framing (remove options, give provocations, swap who is the agent, invert the goal) and run a new
round. Report which round was led.
