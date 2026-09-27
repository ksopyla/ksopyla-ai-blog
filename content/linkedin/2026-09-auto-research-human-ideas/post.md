---
title: "Auto-research can run the experiments. It cannot have the idea."
date: 2026-09-27
platform: linkedin
status: draft
content_score: 4.5
related_blog_post: "https://ai.ksopyla.com/posts/auto-research-and-human-ideas/"
visual: "feature_auto_research_human_ideas.jpg (the Canva image)"
first_comment: "Full write-up with the exam, the diagrams and the results: https://ai.ksopyla.com/posts/auto-research-and-human-ideas/"
---

Last month my AI agents made 176 commits to my research repo. I made fewer than 100.

The ideas that moved the project were still mine.

I run MrCogito, a side project on models that compress long text into a small set of concepts. In September I let agents run most of it. They wrote the code, built the test harness, tuned training and ran experiments on my 7 GPUs while I slept.

What they were great at:
→ implementing a new design, with tests, in a few hours
→ finding training settings that work for long sequences
→ running the same exam at 8 lengths and 3 seeds without getting bored

What they didn't do: come up with the unusual idea.

Worse, when I gave them one, they quietly built a more common version. My note said "don't average the tokens". The code built a weighted average of the tokens. Tests passed. Nothing crashed. It just wasn't my idea.

Two habits fixed it:

1. A fixed exam with an exact score, so "better" is not a matter of opinion.
2. Before every launch, I ask the agents for an interactive diagram of what they actually built. 15 minutes of clicking beats reading 1,000 lines of diff.

With both in place, the loop found something real: a memory trained on texts up to 16K tokens that still finds the planted fact 80% of the time at 128K.

Agents run the experiments. The idea, the questions and the suspicion are still my job.

If you use agents for research or engineering: what is the most "ordinary" thing they built instead of what you asked for?

#AIResearch #AIAgents #MachineLearning
