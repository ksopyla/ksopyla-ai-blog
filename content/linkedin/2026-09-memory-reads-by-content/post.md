---
title: "Trained on 16K tokens, finds the fact at 128K"
date: 2026-09-30
platform: linkedin
status: draft
content_score: 4.4
related_blog_post: "https://ai.ksopyla.com/posts/memory-that-reads-by-content/"
visual: "memory_length_generalization.png (the length chart)"
first_comment: "Full write-up with the three attempts, the chart and the caveats: https://ai.ksopyla.com/posts/memory-that-reads-by-content/"
sequence: "Post 2 of 2. Post 1 (auto-research) goes first."
---

Trained on books of 16K tokens. Still finds the fact at 128K.

That is the first result in my research project that points straight at the goal.

MrCogito is my attempt at models that compress a long text into a small notebook of dense concepts, instead of attending to every token. The hard question is always the same: does the notebook keep the facts?

Three attempts:

1. Average every 16 tokens into one note. Copying survives. Looking up a fact dies at 1,280 tokens. An average keeps what a page is about, not the detail you will be asked about.
2. Learned notes. Better, but stuck at 26 of 64 bits, because the writer could only see 16 tokens back.
3. Memory cells that read the whole window in both directions. Passed every level of my exam at 30M.

Then a cheap control humbled me: the old design with a wider view matched it on short texts.

The difference only showed up when I trained short and tested long:
→ memories that read by position: chance by 16K
→ full attention trained on 2K: chance at 4K on a 4-step chain
→ the memory that reads by content: 98% at 32K, 80% at 128K (82% on the chain)

A memory that learns WHERE a fact sits only knows its training length. A memory that learns WHAT to look for has the same job at 2K and at 128K.

Still synthetic, still 30M parameters. Next: facts in real prose, and a two-level memory for a million tokens.

If you work on long context: do you test train-short-test-long, or only at the training length?

#AIResearch #MachineLearning #LongContext
