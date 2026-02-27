---
title: "MrCogito Research Log #1 — February 2026"
date: 2026-02-27
platform: linkedin
status: draft
content_score: 4.20
related_blog_post: ""
---

MrCogito Research Log #1

I'm building a ConceptEncoder — a novel transformer architecture that replaces expensive O(n²) self-attention with cross-attention through a small set of learnable concept tokens. I'm sharing my research journey openly. Here's what happened in February 2026.

What I tried:
→ Redesigned the diffusion decoder — removed O(n²) self-attention, added AdaLN-Zero timestep conditioning. ~4x speedup per training step.
→ Compared diffusion vs MLM training objectives head-to-head. Diffusion gave 2x better concept geometry (rank 10.1 vs 5/128) but near-random semantic quality (STS-B: 0.138).
→ Implemented ViaDecoder evaluation — a fairer way to evaluate concept encoders that preserves their internal structure. Consistent +0.65-2.3% improvement over the naive CLS-query approach.
→ Added VICReg regularization with warmup to combat concept collapse.

What surprised me:
→ Better geometry doesn't automatically mean better semantics. You can spread concepts apart in space without them capturing different meanings.

What's next:
→ TSDAE (denoising autoencoder) training — forces concepts to reconstruct from corrupted input
→ Prefix generation — the decoder must generate text the encoder never saw

Full project (open source): github.com/ksopyla/MrCogito

#AIResearch #OpenScience #ConceptEncoder #ResearchLog #MachineLearning
