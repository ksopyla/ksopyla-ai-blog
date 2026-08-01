---
title: "Replacing Gemma-3 global attention with concepts"
date: 2026-07-26
platform: linkedin
asset_type: carousel
status: draft
related_blog_post: "https://ai.ksopyla.com/posts/gemma-with-concepts/"
---

## Slide 1 - cover
Replacing Gemma-3 global attention with concepts
Toward longer context

## Slide 2 - the problem
Global layers still attend all N tokens
That is the expensive part as context grows

## Slide 3 - the bet
Keep local windows for fluency
Put long-range state in a recurrent concept bank (C ≪ N)

## Slide 4 - the surgery
Before: global layers → full attention over N
After: those layers → concepts + local window

## Slide 5 - complexity
From global N×N terms
To O(N · (K + C)) with fixed block size K

## Slide 6 - evidence so far
At 4K, concepts became load-bearing for beyond-local CE
Not a 10M demo — a working replacement channel

## Slide 7 - takeaway
Longer context as an architectural consequence
Replace the global path. Then prove the model uses it.

Full notes: ai.ksopyla.com/posts/gemma-with-concepts/
