---
title: "Concept Collapse — 128 concepts collapsed to 5"
date: 2026-02-27
platform: linkedin
status: draft
content_score: 4.70
related_blog_post: ""
---

My 128 concept tokens collapsed to just 5 effective dimensions during training.

I'm building a ConceptEncoder — a transformer that uses cross-attention between a small set of learnable "concept" tokens and the input sequence, instead of expensive self-attention between all tokens. The theory is promising: 1000x memory reduction for long contexts.

But when I analyzed the concept embedding space after training, I found that out of 128 concepts, only ~5 were doing meaningful work. The effective rank was 5.45/128 — meaning 96% of my concept capacity was wasted.

After digging into the root cause, I identified 5 structural problems, all pointing to the same issue:

→ The training objective (masked language modeling) lets the encoder get away with surface-level pattern matching
→ The decoder sees the same content as the encoder, so concepts can "cheat" by hashing token positions instead of compressing semantics
→ Regularization (VICReg, variance terms) can spread concepts apart in space but can't force them to capture different meanings

The deeper lesson: if your decoder can reconstruct the input without needing rich representations, it will learn the laziest path. The fix isn't more regularization — it's changing what the decoder has to produce.

I'm now testing approaches where the decoder must generate content the encoder never saw (denoising, prefix generation). Early signs suggest this forces genuinely different concepts to emerge.

Has anyone else run into representation collapse in their encoder architectures? How did you diagnose and fix it?

github.com/ksopyla/MrCogito

#AIResearch #MachineLearning #ConceptEncoder #RepresentationLearning #OpenScience
