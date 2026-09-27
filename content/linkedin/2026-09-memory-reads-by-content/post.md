---
title: "Train short, test long: WHERE vs WHAT memory"
date: 2026-09-30
platform: linkedin
status: draft
content_score: 4.4
related_blog_post: "https://ai.ksopyla.com/posts/memory-that-reads-by-content/"
visual: "memory_length_generalization.png (the length chart)"
first_comment: "Full write-up with the three attempts, the chart and the caveats: https://ai.ksopyla.com/posts/memory-that-reads-by-content/"
sequence: "Post 2 of 2. Post 1 (auto-research) goes first."
---

Trained on texts up to 16K tokens. Still finds the fact at 128K.

My research question is simple: can a small model squeeze a long text into a short memory, and still find one planted fact at the end?

On short texts, several of my designs said yes. So I stopped testing at the length I trained on.

Train short. Test long.

→ memory that learns WHERE the fact sits, trained on 2K: near chance by 16K
→ the same memory trained all the way up to 64K: still breaks at 128K (53%)
→ memory that learns WHAT the fact looks like, trained up to 16K: 98% at 32K, 80% at 128K

That difference is the whole lesson.

"The fact was around token 1,400" is useless at token 90,000.
"The slot that matches this key" is the same job at 2K and at 128K.

If you only test a long-context model at the length you trained it on, you cannot tell which of the two it learned.

Still a small model (30M parameters) on synthetic text. Next: real prose, and a million tokens.

How do you test long-context models: at the training length, or beyond it?

#AIResearch #MachineLearning #LongContext
