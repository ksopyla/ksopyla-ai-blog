---
title: "Replace global attention with concepts"
date: 2026-07-26
platform: linkedin
asset_type: carousel
status: draft
related_blog_post: "https://ai.ksopyla.com/posts/gemma-with-concepts/"
---

## Slide 1 - cover
Replace Gemma-3 global attention with concepts
Toward longer context — without full N×N attention

## Slide 2 - the problem
Healthy concepts can still be unused
High RankMe + falling loss ≠ the model needs your memory

## Slide 3 - the bet
Keep local windows for fluency
Put long-range state in a small recurrent concept bank (C ≪ N)

## Slide 4 - the surgery
Stock Gemma: global layers attend all tokens
Graft: those layers attend concepts + local window instead

## Slide 5 - what failed
At 2K, local windows still finished next-token CE
Beyond-local ΔCE stayed ~0.001 despite open gates

## Slide 6 - what worked
Same architecture, harder regime:
4K + long docs + Muon + 1B tokens
Beyond-local ΔCE → ~2.35 nats

## Slide 7 - takeaway
If local context can solve the objective, memory stays ornamental
Measure causal use — not only geometry

Full notes: ai.ksopyla.com/posts/gemma-with-concepts/
