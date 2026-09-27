---
title: "A Memory That Reads by Content: Trained on Short Books, Still Finding Facts at 128K Tokens"
date: 2026-09-27
draft: false
description: "Three attempts at a compressed memory for long context: an average that cannot hold a key, learned notes that hit a wall, and memory cells that find a planted fact in 128K-token books after training on 16K."
tags: ["AI", "MrCogito", "Concept Reasoning", "Long Context", "Memory", "Research"]
categories: ["AI Research"]
featureImage: "feature_memory_reads_by_content.png"
featureAlt: "Abstract digital art: a warm stream of text-like particles compresses into a small bright constellation of concept nodes, held up by a lone silhouette, while cool blue streams weave through a grid of glowing cells"
showReadingTime: true
---

{{< lead >}}
Can a model read a long book, keep only a small notebook of dense concepts, and still find a single fact when asked about it at the end? After three attempts, I have the first design in my project that does this at 128,000 tokens, after training on books of at most 16,000. Getting there took an average that could not hold a key, a wall I could explain to the bit, and a control experiment that humbled me.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why compressed memory is the hard part of making long context affordable, and how I test it with an exact score in bits
- Why averaging tokens into notes keeps what a page is about but loses the fact you will be asked about
- Why learned notes stalled at 26 of 64 bits, and how giving the writer the whole window broke that wall
- The result that matters: a memory that reads by content stays above 95% up to 64K tokens and reaches 80% at 128K, while memories that read by position fall to chance by 16K
- What this does and does not prove, and why a million tokens will need a two-level memory

## Why memory is the hard part

A standard transformer lets every token look at every earlier token, so its cost grows with the square of the text length. At a million tokens that is expensive even for large labs. At ten million it is out of reach.

[MrCogito](/projects/concept-reasoning/) is my open research project exploring another path. The model compresses a long input into a much smaller set of **concepts** (dense vectors), reasons over those concepts, and only then decodes the answer. If that works, three things follow:

- **Long context becomes a question of compression, not brute force.** Attention between N tokens and C concepts costs O(C·N) instead of O(N²). With the number of concepts growing with the text, one million tokens becomes tractable on hardware I can actually afford.
- **Reasoning gets a wider channel.** A text token carries roughly 15 bits. A 2,048-dimensional concept vector can carry thousands of times more. Reasoning in concept space, instead of writing every thought as text, is a higher-bandwidth way to think.
- **Models could exchange concepts, not text.** Eventually, cooperating agents could pass concept vectors to each other directly.

The picture I keep in mind is a student preparing for an exam with a long book. The student cannot keep the whole book in view, so they write a **notebook** while reading. When the question comes, they look it up in the notebook instead of rereading every page. The opposite student is allowed to reread any page at any moment: a normal transformer with full attention. It is expensive, it loses nothing, and it is the student I have to match more cheaply.

Every design in this post is a different way of writing the notebook. The only question that matters is:

**Does the notebook actually keep the facts needed later?**

## How I measure a memory

Next-token loss on ordinary text is almost blind to this question: in my experiments, the memory's distant entries were worth about 0.05 nats. So I test memory with an exam where the answer has an exact price. I describe the exam, and how it became the goal of an agent-run research loop, in [the companion post](/posts/auto-research-and-human-ideas/). In short:

- The book is a long string of random letters from a four-letter alphabet.
- Far back, a fact is planted: a marker, a two-letter key and a 32-letter value.
- At the end, the model is asked for the value. Each letter is worth 2 bits, so the full answer is a **64-bit prize**, and chance is 25% per letter.

A full-attention model, the same model with an uncompressed memory, and a model with no memory at all train next to every candidate, on the same data. If full attention cannot learn the exam, it does not count. If the no-memory model beats chance, the exam leaks.

## Attempt 1: an average cannot hold a key

The simplest notebook averages every 16 tokens into one note. At a million tokens, that shrinks the memory to about 64 MB.

The exam gave a sharp, two-sided answer. Copying a span from far back survived the averaging well: **54 of 64 bits** at 1,024 tokens. Looking up a fact by its key did not. With finer notes (one per 8 tokens), lookup got **60 bits** at 1,024 tokens and then **0 bits** at 1,280, while the uncompressed memory still got all 64.

An average keeps what a page is *about*. It loses the one detail you will be asked about. In information-bottleneck terms, the notebook should keep what predicts the answer, not what describes the page. Repairs on top of the average, a reconstruction loss and keeping key tokens uncompressed, recovered 1 and 3 bits where the uncompressed memory got 47.

## Attempt 2: learned notes, and a wall at 26 bits

The second design replaced the average with learned attention. The book is covered by overlapping windows of 256 tokens, and each window has 32 learned "questions" that pick what to write into their notes.

It was clearly better. It followed a four-step chain of facts across 1,024 tokens (40 bits, against 4 for the average) and was the only model above zero on the 1,024-token lookup, where even full attention stayed at zero at that training budget.

Then it stopped at **26 bits**: at 31M and 50M parameters, at 1,024 and 2,048 tokens, on the plain lookup and on the one with a decoy. The reason turned out to be the implementation, not the idea. Each note-taker could only see 16 tokens back, so it could recognise just the first 13 value letters as part of the fact. Thirteen letters at 2 bits each is 26 bits. How I found that is the story of [the companion post](/posts/auto-research-and-human-ideas/).

## Attempt 3: memory cells that read the whole window

The third design is the one the idea note asked for in the first place. Each 256-token window is written by **32 memory vectors**, and each vector is a real memory cell rather than a weighted mix of tokens:

- it is 512 dimensions wide, four times the token embedding;
- it has its own state, refined through attention and a feed-forward layer;
- it keeps 8 attention heads separate instead of averaging them;
- it carries an address: which cell it is, and where in the window it read from.

Most importantly, the cells write from **two-way context**. Before they read, a small two-layer encoder lets every token in the window see every other token, so a value letter "knows" it belongs to a fact even when the marker is far from it. A second variant, where cells and tokens refine each other in rounds (in the style of BiXT), learned too slowly at this budget and was marked not ready.

At 30M parameters the design passed every gating level of the exam, including the level where the filler looks like plausible text, and got the verdict **scale up**. On the 1,024-token lookup it recovered **94%** of the answer letters (57.6 of 64 bits), up from 54%. Accuracy was flat across all 32 letters. The 26-bit wall was gone.

## The control that humbled me

The experiment plan included a cheap control: the old note-taker from attempt 2 with a single change, a wider 64-token view. It was there to separate "more context" from "better memory".

On the short exams, the control **matched or beat** the new design: 99% against 94% on the lookup with a decoy, and 99% against 89% on the 2,048-token lookup. Most of the gain came from context, not from the memory cells I was proud of.

If the story ended at 2,048 tokens, the honest conclusion would be: widen the old writer's view and move on. It did not end there.

## Train short, test long

Short exams check whether a memory works. They do not check whether it keeps working when the book grows, which is the entire point of a long-context memory. So the next test trained on 2,048-token books and evaluated on books up to 128K tokens.

![Line charts of accuracy versus book length from 2K to 128K tokens. The content-addressed memory with a short curriculum stays above 95% up to 64K and reaches 80% at 128K on lookup and 82% on a 4-step chain; position-addressed memory, the wider-context note-taker and full attention fall to chance.](memory_length_generalization.png "Train short, test long. The memories that read by position fall to chance within 8× of their training length; the content-addressed memory holds.")

The picture changed completely:

- **The memory cells as first built, and the wider-context control, both fell to chance by 16K tokens.** Trained on 2K books, they reached roughly twice their training length and failed on the farthest facts first. Even trained up to 64K, the first version dropped to 53% at 128K.
- **A variant without an absolute address held.** Its slots carry no "this came from window 37" label, and their positions are counted from the question rather than from the start of the book. Trained on 2K books only, it held 91% at 8K (median of three seeds). After two short extra stages at 8K and 16K, it held **98%** at 32K, **95%** at 64K and **80%** at 128K. A second seed replicated it (81% at 128K).
- **The four-step chain transferred too.** Full attention trained on 2K books dropped to chance at 4K. The content-addressed memory held **82%** at 128K after one extra stage at 8K.
- **The cost grows linearly.** Evaluating a 128K-token book takes 1.35 seconds and 3.4 GB on one RTX 3090.

This is also where the humbling control stopped being a threat: the wider-context note-taker scored 29% at 16K. At the length that matters, context alone did not carry over.

## Why reading by content generalises

My reading of these results, as a hypothesis rather than a proof: a memory that learns **where** a fact sits learns something that is only true at the training length. "The key was around position 1,400" has nothing useful to say at position 90,000. A memory that learns **what** to look for, the slot whose content matches the key, has the same job at 2K and at 128K. There are just more slots to search.

Two details support that reading:

- **Where the memories fail.** The position-reading memories failed on distant facts first. The content-reading memory lost accuracy evenly across the book as it grew, which looks like dilution (more slots competing for one lookup), not like forgetting.
- **Where the chain works.** Models that read by position learned a chain solution tied to one length. Trained at 8K, one worked at 8K (92%) and failed at 16K (29%). Trained at 16K, it worked at 16K and failed at 8K.

One more practical lesson: the content-reading memory **could not learn the chain from scratch** in two attempts. Starting from its lookup weights, it learned it quickly. It has to learn to find a fact before it can learn to follow a chain of them.

## What this does not prove

- **It is not language yet.** Random letters with an exact score are a controlled test of the mechanism. The next rung plants facts in real prose, and adds a next-token test where the memory has to earn its place.
- **It is small.** 30M-class models, trained on books of at most 16K tokens. 128K is evaluation only. The memory cells also add about 14% parameters over the baselines, more than my exam's usual 5% tolerance.
- **Seeds vary.** One of three seeds reached only 65% even at 2K tokens. Takeoff at 2K is still stochastic.
- **One level of memory is not enough for a million tokens.** A coarser version (512-token windows with 8 cells each, the density a million tokens would need) dropped from 93% to 39% on the 2K lookup. The 1M design will need **two levels**: coarse notes to find the right pages, fine notes to read them.

## What comes next

1. Facts planted in real prose, and a next-token test where the memory has to lower the loss on tokens whose evidence is far away.
2. The two-level memory for the million-token setting.
3. Reasoning loops over the concepts: the part of the vision this memory was built to support.

For the first time in this project, the memory is not the thing I am unsure about at short lengths. The open question has moved to where I wanted it: language, and scale.

## References

1. Schnabel, T. et al. (May 2025). [**Lost in Transmission: When and Why LLMs Fail to Reason Globally**](https://arxiv.org/abs/2505.08140). Microsoft Research. NeurIPS 2025. arXiv:2505.08140
2. Tishby, N., Pereira, F. C., Bialek, W. (Apr 2000). [**The information bottleneck method**](https://arxiv.org/abs/physics/0004057). arXiv:physics/0004057
3. Jaegle, A. et al. (Mar 2021). [**Perceiver: General Perception with Iterative Attention**](https://arxiv.org/abs/2103.03206). ICML 2021. arXiv:2103.03206
4. Hiller, M. et al. (Feb 2024). [**Perceiving Longer Sequences With Bi-Directional Cross-Attention Transformers**](https://arxiv.org/abs/2402.12138). arXiv:2402.12138
5. Hsieh, C.-P. et al. (Apr 2024). [**RULER: What's the Real Context Size of Your Long-Context Language Models?**](https://arxiv.org/abs/2404.06654). NVIDIA. COLM 2024. arXiv:2404.06654
6. Kuratov, Y. et al. (Jun 2024). [**BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack**](https://arxiv.org/abs/2406.10149). NeurIPS 2024. arXiv:2406.10149
7. Sopyla, K. (Sep 2026). [**Auto-Research Can Run the Experiments. It Cannot Have the Idea.**](https://ai.ksopyla.com/posts/auto-research-and-human-ideas/). ai.ksopyla.com
8. MrCogito sources: [project vision](https://github.com/ksopyla/MrCogito/blob/dev/docs/1_Strategy_and_Plans/vision_and_goals.md) · [averaged-notebook report](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e25_e21_dna_capability_report_20260916.md) · [learned-notes design and review](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E30_sliding_window_perceiver.md) · [memory-cell design and results](https://github.com/ksopyla/MrCogito/blob/e31-latent-memory/docs/experiments_specs/ahead/E31_sliding_window_latent_memory.md)

*All numbers are from my own runs on two servers with 3 and 4 RTX 3090 GPUs. Models are discarded after each exam. Independent reproduction has not been published.*
