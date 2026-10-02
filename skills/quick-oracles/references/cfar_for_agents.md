# CFAR Handbook techniques for agents

Source: the CFAR Handbook by Duncan Sabien for the Center for Applied Rationality (CFAR), as republished (lightly
edited, 2022) in the LessWrong sequence <https://www.lesswrong.com/s/KAv8z6oJCTxjR8vdR>, posted as CFAR!Duncan. One
file per post in `cfar_handbook_lw/` (index in its README); file numbers are cited below as [NN].

<!-- PI/Claude 2026-10-02. Techniques were first extracted per handbook range by DeepSeek subagents, then re-quoted from
the LessWrong files; every quote below was checked against those files by script. Body- and emotion-only material
(Focusing felt senses, Againstness, Taste & Shaping) is left out. -->

Use: pick the situation, run the technique, and when asking oracles turn its steps into the brief's question.

Tested 2026-10-02 (`evals/cfar_exercises.py`, results in `evals/results/20261002T1545_summary.md`): DeepSeek flash as the
oracle, two blind judges (Gemini 3.8 Flash, Claude Haiku), two problems, 6 samples per cell. The judges disagree on
absolute counts, so only directions that held for both judges on both problems count as support. Exploratory, not proof.
Each "Oracle use" line says what the test found, or that it is untested.

## 1. Generate options (diverge)

**Goal factoring** [16]. Assume "that there might be a way to get everything we want, and achieve all of the good with
none of the bad." Steps: choose an action; prepare to accept all worlds; factor the action into the goals it serves (a
button test checks the list is complete: if a button gave all those goals without the action, would you press it?);
brainstorm replacement actions one goal at a time; reality check, which runs Murphyjitsu.

Oracle use: give the goals the current approach serves, not the approach, and ask for other ways to reach each goal.
Tested: the strongest generator; on the maze problem more novel ideas than a plain ask for both judges (4.3 vs 2.8;
13.7 vs 4.0), and the main pick left the obvious list in 6 of 6.

**Resolve cycles** [24]. "Try to solve the problem—in five minutes. Yes, actually. No, don’t just make a plan; try to
completely solve it." Then "spend five minutes brainstorming five-minute next actions" and do the most promising one.
"Even complex and intractable-seeming problems often turn out to have short or simple solutions".

Oracle use (refined): ask for a complete solution in one short attempt, or, after listing what has been tried, ask
"What do all my ideas and efforts so far have in common? What axes am I not moving on?" Tested against a plain "what
else could we try?" with the same tried list (`evals/results/20261002T1738_spread_summary.md`): preferred on the maze problem by both judges (4/6,
5/6), not on the other (2/6, 3/6); mixed. The grimoire prompt
"Five terrible models of what might be going on" plus "Ten terrible ideas for step one" was tested and gave mixed
results (more novel ideas for one judge, fewer for the other), so it is not recommended.

## 2. Ask without leading

**Socratic ducking** [05]. "You’re there so that they can clarify their own understanding, not to provide them with an
outside solution." Ways to do it: counter vagueness ("Ask for specific examples"), draw out their experience, map out
the parts of the problem, breadth-first before depth.

**Double crux** [27] and the jargon entry [10]: participants seek "cruxes" for their argument, "provable/falsifiable
binary statements". Seek your own cruxes independently, then compare; state what would change your mind.

Oracle use: ask each oracle for its own cruxes before showing yours; when two oracles disagree, ask what would change
each one's mind, not who is right. Tested: a crux-first brief picked the obvious option less often than an open brief
(both judges, both problems) but did not produce more novel ideas. A brief with an option list and a stated preference
made the main pick come from the list in 6 of 6 for both judges on both problems, with fewer novel ideas than an open
brief.

## 3. Stress-test a plan

**Murphyjitsu** [14], "a process for bulletproofing your strategies and plans": select a goal; outline the plan with
concrete steps; "Surprise-o-meter. Imagine you get a message from the future—it’s been months, and it turns out the
plan failed"; "Pre-hindsight. Try to construct a plausible narrative for what kept you from succeeding."; bulletproof;
"Iterate steps 2-4" until the failure would shock you.

Glossary [10]: **Outside view**, "The “common sense” view, as derived from base rates, past experience, and observations
of similar phenomena." **Planning fallacy**, "The tendency to model only best-case scenarios when generating plans".

Oracle use: *it is a week later and this plan failed; write the five most likely stories of why, and for each the
cheapest check that would have caught it.* Tested: most of the gain comes from asking for a check per failure (specific
failures with checks rose from about 1-2 to 4-5 with the stricter judge); the pre-hindsight framing added a small
further gain on one problem for both judges and tied on the other.

## 4. Debug

**Frame-by-frame debugging** [05]: pick a bug; "Describe a recent, concrete example of it."; "Where did it go wrong?";
"Zero in on the exact moment."; "Check for awareness" (did the alternative occur to you at all?); "Reality check".

**OODA loops** [05]: "think deliberately about what step of the OODA loop you are on, given a specific bug or problem."

**Bucket errors** [28] and **question substitution**: beliefs bundled together so that evidence about one forces
updates on others; a hard question silently swapped for an easier one. Read [28] before reviewing a surprising result.

**Gears-level understanding** [06]: knowing from trusted sources versus seeing why it could not be otherwise.

## 5. Stay on track, decide what to work on

**Hamming questions** [09]: "What are the most important problems in my life, and what's stopping me from working on
them?" and "what's your bottleneck?"

**Polaris** [04]: "There should be some sort of guiding light, some sort of known overall objective that serves as a
check for whether or not you’re still pointed in the right direction."

**The strategic level** [06], **policy-level decisionmaking** and **saving state** [08], **area under the curve** [07].

## 6. Calibrate

Glossary [10]: **Metacognitive blindspot**, "An area of one’s self-reflection or introspection which does not exist or
returns inaccurate results". **Sphexishness**, "the execution of rigid algorithms which create the appearance (but not
the advantages) of intelligent thought or action." **Chesterton's fence**, "if one comes across a seemingly-purposeless
fence in the middle of the desert, one should not take it down." **Bayesian updating**.
