---
title: "Healthy concepts that the model ignores"
date: 2026-07-26
platform: linkedin
status: draft
content_score: 4.6
related_blog_post: "https://ai.ksopyla.com/posts/gemma-with-concepts/"
---

Healthy concept geometry is not the same thing as a working long-range memory.

I grafted a recurrent concept bank onto frozen Gemma-3 1B and replaced its global-attention layers with concept reads/writes. The idea: keep local windows for fluency, move long-range state into C=128 concepts, and open a path toward longer context without full N×N attention.

For a while the runs looked fine and failed quietly.

RankMe stayed high (often 60–100 / 128).
Loss went down.
Gates were open.

Then I ablated the concepts on beyond-local positions. Delta CE was ~0.001 nats. The model was solving short-context CE from local windows. Concepts were present. Unused.

What finally moved the needle was not another tiny calibration. It was making forgetting expensive:

→ same architecture
→ seq 2048 → 4096
→ long-document mix
→ Muon
→ 100M → 1B tokens

Beyond-local causal use jumped from ~0.003 to ~2.35 nats. RankMe stayed ~101. Concepts started doing the job global attention used to do.

This is not a 10M-context demo. It is one validated step: the replacement channel can become load-bearing.

Practical lesson if you are building latent memory:
if local context can finish the objective, your fancy global replacement will stay ornamental.

Full write-up with architecture, metrics, and WandB runs:
https://ai.ksopyla.com/posts/gemma-with-concepts/

If you train long-context or memory modules: do you measure causal use, or only geometry and loss?

#AIResearch #AIEngineering #MachineLearning
