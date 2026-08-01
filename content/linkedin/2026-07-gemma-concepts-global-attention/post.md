---
title: "Replacing Gemma-3 global attention with concepts"
date: 2026-07-26
platform: linkedin
status: draft
content_score: 4.7
related_blog_post: "https://ai.ksopyla.com/posts/gemma-with-concepts/"
---

A bit like Batman, minus the cape 🦇: by day ☀️ I lead AI work at Pearson and ship agent systems. At night 🌙 I still chase one stubborn idea: long-range state should not have to live in full global attention.

Why I keep training this: agents need memory that survives tools, turns, and long documents. Stuffing more tokens into the window works until KV-cache and latency say no. I want a compact concept workspace the model can read and write — something closer to reusable internal state than another RoPE trick.

That is why I started grafting concepts onto Gemma-3 1B.

Gemma already separates the stack: mostly local sliding-window layers, plus a few global ones. I remove the global-attention channel and put a recurrent concept bank in its place. Frozen backbone + LoRA. C=128 concepts. Block size K=512. Former global layers attend concepts + local window. Complexity becomes O(N·(K+C)) instead of full N×N global terms.

Phase 1 of MrCogito taught me concept collapse the hard way. So this time I refused to re-learn English on every ablation. Start from a pretrained decoder. Replace only the long-range path. Measure whether concepts actually take that job.

For two weeks short-context CE almost lied to me 😅. The concept bank looked diverse and healthy. Gates were open. Loss fell. Then beyond-local concept ablations stayed near zero. Local windows were still finishing the prediction. The graft existed. The transfer had not happened.

What helped was making forgetting expensive: seq 4096, long documents, Muon, 1B tokens. Same architecture. Harder regime. Beyond-local ΔCE jumped from ~0.003 to ~2.35 nats. Concepts started doing what global attention used to do ✅

Useful for me personally: I finally have one validated path where the replacement channel is load-bearing — not just present in the graph. That is enough to keep going toward longer context, instead of restarting from scratch again.

This post is also a reminder to myself: in research you cannot give up too early. Curiosity has to outlast the quiet failures — the runs that look fine and teach you nothing until you dig deeper.

Full write-up with architecture and WandB:
https://ai.ksopyla.com/posts/gemma-with-concepts/

If you design long-context systems: do you scale global attention, or try to replace it?

#AIResearch #AIEngineering #MachineLearning
