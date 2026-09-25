---
title: "Build the Exam Before the Architecture: E21, E30, E31 and a Capability Test Bench"
date: 2026-09-25
draft: true
description: "Six weeks of exploring compressed-memory architectures for efficient long-context reasoning. The architectures kept changing; the thing that made progress possible was a fixed, graded capability test bench with exact information scores and a dense model trained next to every candidate."
tags: ["AI", "MrCogito", "Concept Reasoning", "Evaluation", "Long Context", "Research Methodology"]
categories: ["AI Research"]
showReadingTime: true
---

{{< lead >}}
A new architecture has no track record. Your loss curve is not sure what it is measuring, and your intuition is biased toward the idea you just spent a week building. Over the last six weeks of MrCogito I tried three memory designs for efficient long-context reasoning. The most useful thing I built in that time was not one of them. It was the exam I now run them all through.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why next-token loss on natural text is a weak instrument for testing a new memory architecture (in my runs, far context was worth about **0.05 nats**)
- How synthetic exams with an exact information prize (in bits) turned "it seems to work" into numbers I could compare across weeks
- What three designs taught me: **E21** (an averaged notebook), **E30** (a learned sliding-window notebook), and **E31** (addressed latent memory, now running)
- How the test bench caught my own mistakes: false kills from the wrong step size, an exam that silently lost three quarters of its prize, and a model that was not the one I designed
- The rules I now use to decide whether an architecture has earned more compute

This is a progress report from [MrCogito — Concept Reasoning Model](/projects/concept-reasoning/). It follows [Replacing Gemma-3 Global Attention with Concepts](/posts/gemma-with-concepts/), and it starts with a correction to that post.

## How this started: my own headline number needed a correction

In July I reported that a concept bank grafted into Gemma-3 1B had started to "do the long-range job global attention used to do". Shuffling the concepts raised the loss on far tokens by about 2.4 nats. It looked like the clearest positive result the project had produced.

Three weeks later, an architecture and evaluation audit found a problem in my own measurement. In that design, later layers in the same block could read concept writes made from the *current* block, so part of the "memory" signal could come from nearby future tokens rather than from earlier ones. The large teacher-forced ΔCE was real, but it was not clean evidence of causal memory. Free-running generation from the same checkpoint told the same story: it looped (distinct-1 0.04, REP-3 0.94), while the unmodified model did not.

The model was not the only problem. The instrument I trusted had let a leak through.

The next four experiments (E17c–E17e and E18) kept moving the same way. E18 was a 125M model trained from scratch whose only long-range path was a single global read. That read cost nothing (eval loss **3.790** vs **3.786** for a matched dense model) and could copy exactly from 16K tokens back (**99.9998%**). But a copy of the model with the read removed reached the same loss (**4.091** vs **4.090**). When I added supervised retrieval rows (E18b), first-token accuracy moved from 2.4% to **4.49%**, while the dense control on the identical task reached **99.33%** ([E18 verdict](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e18_family_verdict_20260912.md)).

E22, a Perceiver-style concept LM trained at 32K tokens, closed the argument. Its concept array was alive and diverse (RankMe 265), yet the far slots were worth **0.05 nats**, flat from 1K to 32K tokens ([E22 root cause](https://github.com/ksopyla/MrCogito/blob/dev/docs/4_Research_Notes/e22_root_cause_20260912.md)). On natural text at this scale, next-token prediction pays almost nothing for remembering far facts. A memory that learns exactly what the objective pays for learns almost nothing. I had been testing memory architectures with an objective that barely rewards memory.

So I changed the exam before changing the architecture again.

## The exam: facts with an exact price in bits

The project glossary has a picture I keep returning to. A **student** reads a long **book** for an exam. The book is too long to keep in view, so the student writes a **notebook** (the concept slots) while reading. The **dense model** is a student allowed to reread any page at any time. It is expensive and loses nothing. That is the student to beat, or at least to match more cheaply.

The exams are synthetic, generated on the fly, and built around one property: **every answer has an exact information content**. The book is written in a 4-letter alphabet (like DNA) with random filler. A planted fact looks like `keymark · 2-letter key · 32-letter value`. Since the value is random, the model cannot guess it; predicting it correctly means carrying it across the book. A 32-letter value over 4 letters is a **64-bit prize**, and the floor is exactly `ln 4` nats per letter.

That gives a score I can trust across architectures and months:

```text
recovered_bits   = max(0, floor − CE) × answer_len / ln 2
information_flow = recovered_bits / prize_bits      # 0 = chance, 1 = the whole fact
```

The task families come from the BAPO framework (Schnabel et al., NeurIPS 2025), which models a transformer's view of the past as two bounded channels: a compressed summary and a small number of raw tokens it can attend to. Re-implemented over the DNA alphabet, the families become:

| exam | what it asks | BAPO class |
|---|---|---|
| copy | reproduce a marked span far back | INDEX |
| lookup | find the value for one planted key | MATCH |
| lookalike | same, with a decoy fact of the same shape | MATCH + decoy |
| chain | follow A→B→C→D in reading order | multi-hop |

Every job trains four students on identical rows:

- **dense**: full attention everywhere. If it cannot reach 75% accuracy, the exam is not learnable at this size and budget, and nothing else on that row is scored.
- **E18 (full read)**: the same platform with an uncompressed global read, as the ceiling for "the same model, no compression".
- **local-only**: the global read removed. If this student beats chance, the exam leaks through the local window.
- **the candidate**.

The 75% dense gate is the rule I break least. Without it, a failed exam looks like a failed architecture.

## E21: the averaged notebook

E21 was the most ambitious framing in the project: one model split into a sender and a receiver that may only talk through a compressed message. At a `QUERY` boundary the local attention is cut. After that point, the only way to see the earlier text is through **slots**, one per 16 tokens. At the planned geometry that is about 64 bytes per token: 2 MB for a 32K-token document, 64 MB for a million. The same object would be a long-context cache, a reasoning state, and a message between agents.

The 125M language-model run never answered that question. It stopped around step 2,084 (about 3% of its budget) and its weights were lost. So I put E21's mechanism on the DNA ladder instead (E25), with models under 11M parameters, and mapped where it breaks ([E25 report](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e25_e21_dna_capability_report_20260916.md)):

| exam | what the averaged notebook did | where it broke |
|---|---|---|
| copy (16 tokens per slot) | **53.8 of 64 bits** at 1024 tokens (dense 64, full read 63.1) | 1536, where the uncompressed full read also fails |
| lookup (8 tokens per slot) | **60.4 bits** at 1024 | **0 bits** at 1280, while the full read still got 64 |
| lookup (no compression, 1 token per slot) | **63.9 bits** at 1280 | 1536 |
| lookalike | **62.8 bits** at 692 tokens | **0 bits** at 696 |

Two things stood out. Copy survives an average; lookup does not. A lookup key is not a typical summary of 16 tokens, and averaging smears exactly the letters you need to find it. And when I let the model *learn* the pooling from the answer loss, the channel went to zero. It learned a document average.

I then queued a set of repairs to the averaged notebook, each with its own spec and kill criteria. A reconstruction loss on each slot (E26) recovered **1.03 bits** where the full read got about 47. Keeping key tokens uncompressed next to an averaged summary (E27) recovered **3.03 bits**. On a new dataset family with a 40-bit prize (E28), the *dense* model itself reached only 6.5% accuracy, so that exam was not calibrated and the averaged notebook recovered 0 bits anyway.

Lesson from E21: the average is the wrong sufficient statistic for a fact. In information-bottleneck terms, the notebook should keep what predicts the answer, not what describes the page.

## E30: a learned sliding-window notebook

E30 replaced the average with a learned write. The book is covered by overlapping windows (256 tokens, stride 192). Each window has 32 learned queries that cross-attend its tokens and write 32 slots, so the notebook grows with the book, at about 8 tokens per slot. The reader and the exclusive cut are unchanged from E21, so the write is the only difference.

The width sweep went from 0.6M to 50M parameters on the same exams ([31M report](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e30_30m_gpu_odra_polonez_20260922.md), [length limits](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e30_length_hardness_limits_20260922.md), [coverage](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e30_coverage_and_breadth_20260922.md)):

| exam (31M, bits recovered) | full read | E21 average | E30 learned windows |
|---|---:|---:|---:|
| lookup, 512 tokens (48-bit prize) | 48.0 | 44.0 | **47.6** |
| lookalike, 128 tokens (32-bit prize) | 31.3 | 8.8 | **27.8** |
| in-order 4-hop chain, 1024 tokens | 63.3 | 4.0 | **40.1** (77%) |
| lookalike, 1024 tokens | 62.6 | 18.7 | 25.9 |
| lookup, 1024 tokens | 0 | 0 | **25.7** |
| lookup, 4096 tokens | 0 | 0 | 0 |

At 9M parameters E30 already beat the average on copy (37 vs 14 bits). At 31M it matched the uncompressed read at 512 tokens and was the only notebook to follow a 4-hop chain at 1024. On the 1024-token lookup it was the only architecture above zero, including the full read.

The coverage sweep taught me something I had not expected. A 128-token window (about 3 tokens per slot) passed the 1024-token chain. A 512-token window wrote nothing useful on any exam, even with 64 queries per window. The limit is the window, not the slot count. And the chain that passed at 1024 tokens was **0 bits** at 2048 for every notebook, while the full read still solved it.

Then the numbers started to look suspicious. Lookup at 1024 settled at **25.7** bits. At 50M it was **24.3**. At 2048 with finer windows, **25**. The lookalike: **25.9**. Different widths, lengths and exams all stopped near 26 bits of 64.

### The review: the model I ran was not the model I designed

On 2026-09-24 I compared the code against the idea note it came from ([built vs intended](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E30_sliding_window_perceiver.md#built-vs-intended-review-2026-09-24)). The note asked for latent vectors that pick facts out of their window and carry an address. The code built something narrower:

- Each slot was a **weighted average of token keys and values**. The query only chose the weights and added nothing of its own. No residual, no feed-forward layer, and a stored width of 64.
- The write scored tokens after **one causal layer with a 16-token reach**. The queries were static.
- The position bias was **shared by all 32 queries**, so no query had its own part of the page, and the attention heads were averaged into one distribution.
- A **future-token leak** existed in the pooling mask. It did not fire on any recorded exam (answers were short, one question per row), but it would have fired on multi-question rows or language pretraining.

The 16-token reach also explains the plateau, as a hypothesis. A static query looking at a token can only tell it belongs to the fact if the `keymark` is within its 16-token view. After the marker and the 2-letter key, that covers value letters 1–13. Letters 14–32 look like filler. Thirteen letters at 2 bits each is **26 bits**. The measured plateaus were 25.7, 26, 24.3, 25 and 25.9.

I call this the **salience wall**: a write that cannot see context can only keep what looks important locally. Whether it explains the plateau is tested directly before E31's main runs: per-letter answer accuracy should show letters 1–13 above 75% and letters 14–32 near chance, and widening only the writer's reach to 64 tokens should lift the second group.

What E30 does show is still worth keeping: a learned filter beats an average on the exclusive read (chain 40 vs 4 bits, lookalike 28 vs 9). What it does not test is the design I wanted to test.

## E31: addressed latent memory, written from two-way context

E31 builds the design from the note ([spec](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E31_sliding_window_latent_memory.md)). Each 256-token window is written by **32 latent vectors** that are real memory cells: width 512 (4× the 128-dim token embedding), their own residual state and feed-forward layer, 8 attention heads kept separate, and an address made of a latent ID, the window start, a learned position prior over part of the window, and a position stamp where the latent actually read.

The main change is context. Every write from E18 to E30 saw a 16-token causal state. E31 writes from **two-way context over the whole window**, in two arms:

- **Page encoder (arm A):** two bidirectional attention layers inside the window, then the latents read it. Writer: 4.15M parameters.
- **Latent↔token iteration (arm B):** no encoder. Three BiXT-style rounds in which latents and tokens refine each other, with Slot-Attention competition so two latents do not store the same thing. Writer: 3.62M parameters.

A **context-only control** (E30 with a 64-token writer reach) separates "more context" from "real latents". The leak is fixed and covered by a causality test.

The gates were written before any run. At 1024 tokens: lookup **≥ 40 bits** (E30: 25.7), lookalike **≥ 47 bits** (0.75 × the full read's 62.6), chain **≥ 47 bits**; lookup at 2048 **≥ 32 bits**; and the best latent arm must beat the context-only control by 8 bits. If both arms stay under 32 bits on lookup after a doubled budget over three seeds, I record that addressed latents from two-way context do not break the plateau, and the next bet moves to the read side.

E31 is implemented and its first runs started last night. I do not have results yet, and I will not guess them here. The first thing the run did was find a problem in the exam, which leads to the main part of this post.

## The test bench: one ladder of exams for every architecture

Until last week, every architecture was scored with its own flag combinations. Each E-number had its own recipes, eval sizes and training settings. Comparing E21 in mid-September with E30 a week later meant reading two reports carefully and hoping nothing else had changed.

The [capability suite](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/capability_suite.md) fixes one ladder of exams, one set of model sizes, one training policy and one set of scoring rules. It answers three questions in order: can the architecture learn to pick the right information and reason over it; is it better than what I already had; and does it improve with size?

| level | question | cells (tokens) |
|---|---|---|
| **L0** learns at all | can it copy and look up at all? | copy-128, lookup-128 |
| **L1** carries a fact | does a whole fact survive the channel? | copy / lookup at 256 and 512 |
| **L2** picks signal over a lookalike | keep the fact, ignore a same-shaped decoy | lookalike-128, lookalike-1k |
| **L3** long reach | retrieval in a long book | lookup-1k, lookup-2k |
| **L4** multi-step reasoning | follow a 4-hop chain | chain-1k, chain-2k |
| **L5** language-like noise | same skills when the filler looks like plausible text | Glyph fact / story / chain at 512 and 1K |
| **L6** BAPO-hard stretch | tasks a bounded channel should not solve easily (reported, never gating) | shuffled chain, unique fact |

Every candidate runs at four width-matched sizes (**5M, 10M, 30M, 50M**, all four-layer and all fitting on one RTX 3090), in one of three tiers:

| tier | levels | seeds | use | rough cost per candidate |
|---|---|---|---|---|
| screen | L0–L2 | 1 | does it learn at all? (5M and 10M) | 1–2 GPU-hours per size |
| standard | L0–L4 | 2 | the comparison run at 30M, then 50M | one night on 3 GPUs per size |
| full | L0–L6 | 3 | a claim run | 1–2 nights on both servers |

{{< mermaid >}}
flowchart LR
  C[New architecture<br/>registered as config] --> S[Screen<br/>5M · 10M · L0–L2]
  S -->|reaches L1| T[Standard<br/>30M · L0–L4 · 2 seeds]
  T --> SC[Scorecard<br/>bits per cell · frontier level<br/>vs dense, E18, E21, E30]
  SC --> V{Scale-up rule}
  V -->|all 5 conditions| U[Scale up]
  V -->|some levels pass,<br/>a rule fails| P[Promising — fix first]
  V -->|otherwise| N[Not ready]
  D[Dense model trained<br/>next to every job] -.ceiling.-> SC
{{< /mermaid >}}

The scorecard gives a verdict from rules, not from how I feel about the idea late at night. "Scale up" requires all of:

1. a run at 30M or larger;
2. every L0–L2 cell passing at the largest size;
3. at least one L3/L4 cell that passes or ties the best past architecture;
4. no cell losing more than 2 bits as the model grows;
5. training speed at least half the dense model's.

A level where the candidate missed only on cells the dense model *also* missed is marked **uncalibrated**, not failed. That is no evidence against the candidate.

Under these rules at 30M, the past architectures look like this: dense passes L0–L2 and the 1024 chain but scores 0 on the 1024 and 2048 lookups (a trainability wall, not a capacity one); E30 passes L0–L1 and the 1024 chain and misses the 1024 lookalike and lookup, so it lands at **"promising — fix before scaling"**; E21 fails L2 and L4.

## Why the bench mattered more than any single architecture

This is the part I would tell anyone starting to explore a new architecture on a small budget. Most of what I learned in these six weeks came from the bench catching mistakes, including mine.

### 1. The step size killed more ideas than the ideas did

Step sizes do not transfer across sequence lengths at this scale: 3e-3 trained 128-token rows, 1e-3 256, 3e-4 512 and 1e-4 1024. At 1024 tokens, a 3e-4 step scored **zero for every architecture** on both the lookup and the lookalike, the full read included. At 256, a 1e-3 step with zero-initialised residuals made the full read and the averaged notebook look dead on copy; 3e-4 with warm residuals brought them back. A 50M "collapse" of the full read on the chain was just too few steps at 1e-4; at 5e-5 it scored 99%.

Each of these would have been a wrong conclusion about an architecture. The bench now fixes the step size per size and length, and runs a second one (half the step) the first time a size is tried.

### 2. Late takeoff is not failure

At these sizes, models often sit at chance and then jump. One run stalled at 49% on a copy exam because the one-cycle learning-rate schedule had decayed to almost nothing; the same number of examples under a live schedule reached 99.9%. The probe now extends a run once if eval loss is still falling (by at least 0.2 nats in the last third), and compressed models always get at least as many steps as the dense model used.

### 3. The exam can change without anyone noticing

A frozen preset for the E30 limit runs quietly resolved to a **16-bit** exam instead of the recorded **64-bit** one: a short-value override replaced the 32-letter packing. I caught it while preparing E31, by checking the preset against the saved probe files on the server. Every frozen cell now carries its expected prize in bits, and the tests fail if a preset changes the exam. Any change to a cell, size, policy or scoring rule bumps a suite version, and the scorecard compares only like with like.

### 4. The dense ceiling must train on the same run

The first E31 suite run (last night) had the dense model at chance on some 1024-token seeds. The v1 budget gave ~38K examples at 1024 tokens and ~19K at 2048, below the ~20–32K every architecture needs before it starts to learn at that length. Because dense trains next to the candidate in every job, that showed up as "uncalibrated", not as "E31 failed". Two fixes within a day: v2 raised the batch; v3 runs 2048-token cells at batch 32 in two micro-batches with 6× the steps (~230K examples), because v2's ~77K left everything, dense included, at chance on the 2048 lookup.

Without the ceiling, I would have read that run as a verdict on E31.

### 5. The bench audits the implementation, not only the idea

The 26-bit plateau was a number, repeated across widths and lengths, that a plausible design should not produce. That regularity is what sent me to read the E30 code against its design note. On a language-model loss curve, the same flaw would have looked like "a bit worse than hoped".

### 6. Small numbers need honest error bars

Earlier runs at 1024 tokens used 16–32 eval rows and one seed. The suite uses 256 rows, reports accuracy ± standard error, accuracy per answer letter, and examples to 75% (confirmed over two evaluations). Per-letter accuracy is what makes the salience test possible at all.

### 7. A fixed bench makes new ideas cheap

Registering a new architecture means adding it as a config option on the shared model factory. The screen tier costs 1–2 GPU-hours per size. That changes which ideas I can afford to try. It also fits the way the project now runs: agents launch the suite on the two servers overnight, the scorecard produces the verdict, and I read one page in the morning instead of forty log files. The bench is what makes that loop trustworthy. An agent can run experiments faster than I can check them; it cannot fix a wrong ruler.

## What the bench does not prove

- **It is not language.** Passing L0–L6 means the mechanism works in a controlled setting, with an exact floor and known noise. E22 showed natural text pays far less for far context. A rung with planted facts in real prose and a 512-token next-token check is specified for E31 (L7), but the generator does not exist yet.
- **It is small.** Everything here is 50M parameters or less, on a platform with one global read and up to 2K tokens in the gating cells. At 4K and 16K tokens, every architecture I tried, the full read included, recovered nothing on the lookup. Million-token context is untested.
- **It can be overfit.** A fixed exam invites architectures that are good at the exam. Stretch cells that never gate (L6), the language-like noise level (L5) and the planned text rung are my guard against that, not a guarantee.
- **Rules can be wrong.** The 75% bar, the 2-bit regression threshold and the 0.5× speed rule are judgment calls. I made them before seeing E31's results so they cannot bend toward it.
- **My own past results can still move.** The Gemma result moved after an audit. Anything in this post can too, and the ledger keeps the old numbers next to the corrections.

## Takeaway

When the architecture is new, the evaluation is the part you can make trustworthy first. For me that meant exams with an exact price in bits, a dense ceiling and a leak check trained next to every candidate, gates written before the run, and one versioned ladder that every idea has to climb. E21 taught me that an average cannot hold a key. E30 taught me that a learned write beats it, and that the model I ran was not the one I meant to build. E31 is the first design that tests the idea as intended, and whatever it scores, I will be able to compare it with everything before it.

If you are exploring a new architecture on a small budget: build the exam before the model, and keep the model that would pass it trivially (dense) in every run.

## References

1. Schnabel, T. et al. (May 2025). [**Lost in Transmission: When and Why LLMs Fail to Reason Globally**](https://arxiv.org/abs/2505.08140). Microsoft Research. NeurIPS 2025. arXiv:2505.08140
2. Tishby, N., Pereira, F. C., Bialek, W. (Apr 2000). [**The information bottleneck method**](https://arxiv.org/abs/physics/0004057). arXiv:physics/0004057
3. Hsieh, C.-P. et al. (Apr 2024). [**RULER: What's the Real Context Size of Your Long-Context Language Models?**](https://arxiv.org/abs/2404.06654). NVIDIA. COLM 2024. arXiv:2404.06654
4. Kuratov, Y. et al. (Jun 2024). [**BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack**](https://arxiv.org/abs/2406.10149). NeurIPS 2024. arXiv:2406.10149
5. Jaegle, A. et al. (Mar 2021). [**Perceiver: General Perception with Iterative Attention**](https://arxiv.org/abs/2103.03206). ICML 2021. arXiv:2103.03206
6. Hiller, M. et al. (Feb 2024). [**Perceiving Longer Sequences With Bi-Directional Cross-Attention Transformers**](https://arxiv.org/abs/2402.12138). arXiv:2402.12138
7. Locatello, F. et al. (Jun 2020). [**Object-Centric Learning with Slot Attention**](https://arxiv.org/abs/2006.15055). NeurIPS 2020. arXiv:2006.15055
8. Sopyla, K. (Jul 2026). [**Replacing Gemma-3 Global Attention with Concepts (Toward Longer Context)**](https://ai.ksopyla.com/posts/gemma-with-concepts/). ai.ksopyla.com
9. MrCogito experiment sources: [capability suite spec](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/capability_suite.md) · [small-model protocol](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/small_model_capability_protocol.md) · [BAPO DNA ladder](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/bapo_capability_ladder.md) · [E25/E21 report](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e25_e21_dna_capability_report_20260916.md) · [E30 spec and review](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E30_sliding_window_perceiver.md) · [E31 spec](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E31_sliding_window_latent_memory.md) · [E18/E21 diagnosis](https://github.com/ksopyla/MrCogito/blob/dev/docs/4_Research_Notes/e18_e21_dense_baseline_diagnosis_20260916.md) · [master experiment log](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/master_experiment_log.md)

*All numbers are from my own runs on Odra (3× RTX 3090) and Polonez (4× RTX 3090), with models discarded after each probe. E31 results are pending. Independent reproduction has not been published.*
