---
title: "Auto-Research Is Only as Good as Its Exam"
date: 2026-09-26
draft: true
description: "Agents now design, run and log most of my model experiments overnight. What made that loop useful was not more autonomy but a good exam: a fixed benchmark that tells the agents, and me, what better actually means."
tags: ["AI", "MrCogito", "Auto-Research", "Agents", "Evaluation", "Long Context", "Research Methodology"]
categories: ["AI Research"]
showReadingTime: true
---

{{< lead >}}
My research agents can now design an experiment, write the code, train the model on my GPU servers and log the result while I sleep. The part they cannot do for me is decide what "better" means. When I tried to explore new model architectures without a good exam, the loop just produced confident mistakes faster.
{{< /lead >}}

## TL;DR

**What you will learn:**

- How my auto-research loop works: agents design, implement, run and record experiments on two GPU servers, and I decide the direction
- Why the standard training metric (next-token loss) was the wrong goal for exploring new memory architectures, and how it fooled me once in public
- How a synthetic exam with an exact score in bits turned vague progress into numbers the agents and I could trust
- What that exam revealed about three memory designs, including one that was not the model I thought I had built
- Six rules I now follow before letting agents explore on their own

## The loop works. That was never the hard part.

Look at the commit history of my research repo for September. Most commits were not written by me. Cursor agents made 176 of them; I made fewer than a hundred. Over three days in the middle of the month, agents ran one exam campaign almost around the clock and made 115 commits to its log, many of them between midnight and six in the morning, while my two GPU servers (seven RTX 3090 cards in total) stayed busy.

This is the auto-research approach I described when [MrCogito](/projects/concept-reasoning/) entered its second phase. I build agents during the day at work. At night the same kind of agents run my own research. They read the experiment log, propose the next test, write the code, launch the training over SSH, watch the logs, evaluate the result and write it up. I pick the direction, approve the plans and read the reports.

Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) shows the same idea in its simplest form: an agent edits one training script, trains for exactly five minutes, checks whether validation bits per byte went down, and keeps or reverts the change. About a hundred experiments while you sleep.

Two design choices in that repo matter more than the agent. The metric is fixed (`val_bpb`). And the evaluation code is explicitly off limits: the agent may change anything in the training file, but never the data preparation or the evaluation.

It took me a few weeks, and one public correction, to understand why those two choices are the whole game.

## What I am trying to build

The research question behind MrCogito is about efficiency. A standard transformer lets every token look at every earlier token. That is powerful, and its cost grows with the square of the text length. At a million tokens it gets very expensive.

I am exploring models that work more like a student preparing for an exam with a long book. The student cannot keep the whole book in view, so they write a **notebook** while reading: a small set of dense vectors (I call them concepts) that summarise what they have read. Later, when a question comes, they look things up in the notebook instead of rereading every page. If the notebook holds the right things, the model can handle much longer texts at a fraction of the cost, and the notebook becomes a natural place to reason.

The opposite student is the one allowed to reread any page at any moment. That is a normal transformer with full attention. It is expensive, it loses nothing, and it is the student I have to match more cheaply.

So every new design I try is a different way of **writing the notebook**. And the only question that matters is simple to say and hard to measure:

**Does the notebook actually hold the facts the model needs later?**

## The metric my agents were optimising was the wrong one

The natural goal for a language model is next-token loss: how surprised the model is by the next word. It is what autoresearch optimises. It is what I used for months.

For my question, it is almost blind.

In July I published [a promising result](/posts/gemma-with-concepts/): a concept notebook grafted into Google's Gemma-3 model seemed to take over the long-range work. When I scrambled the notebook, the loss on distant tokens got much worse. A few weeks later, an audit of my own code found a leak. In that design, later layers could read notebook entries written from the current stretch of text, including a little of what came next. The loss signal was real, but part of it was not memory. When the model had to generate text on its own, it fell into repetition loops.

Then two experiments measured how much the objective cares about memory at all. In one, I trained a 125M model with a single long-range lookup and a copy of it with that lookup removed. Their final losses were 4.090 and 4.091. In another, I measured what the notebook's distant entries were worth on ordinary text: about **0.05 nats**, the same at 1,000 tokens and at 32,000.

That number explains a lot. On natural text, at the scale I can afford, predicting the next word needs almost nothing from far away. Nearby words carry most of the signal. A model can reach a good loss while its notebook is decoration, and an agent optimising that loss will happily report progress.

**An agent optimises whatever you measure, faster than you can check it. If the measure does not reward memory, the loop will not find memory.**

## Giving the loop a real goal: an exam with an exact price

So I stopped asking agents to make the loss go down, and built an exam instead.

The idea comes from a 2025 paper by Schnabel et al. that treats a transformer's view of earlier text as a narrow communication channel, and asks which tasks need more bandwidth through that channel. I rebuilt its task families in the simplest possible form:

- The "book" is a long string of random letters from a four-letter alphabet, like DNA.
- Somewhere far back, the generator plants a fact: a marker, a two-letter key and a 32-letter value.
- At the end comes a question, and the model has to produce the value.

Because the value is random, it cannot be guessed. Each letter is worth exactly 2 bits, so a 32-letter value is a **64-bit prize**. A model that recovers 40 bits has carried 40 bits of real information across the book. Zero means chance. No language priors, no tokenizer effects, no arguing about what a score means.

That one change gave the agents something they never had before: a goal where "better" is unambiguous.

Every exam trains four models side by side, on identical data:

| model | why it is there |
|---|---|
| **full-attention model** (rereads any page) | if it cannot reach 75% accuracy, the exam is not learnable at this size and budget, and nothing else on it counts |
| **uncompressed notebook** | the same architecture without compression, to show what compression costs |
| **no notebook** (only the nearby text) | if this model beats chance, the answer leaks through local context and the exam is broken |
| **the candidate** | the new design being tested |

The exams form a ladder, from easy to hard:

| level | the question it asks |
|---|---|
| 0 · learns at all | can it copy or look something up in a short text? |
| 1 · carries a fact | does a whole fact survive the notebook at 256–512 tokens? |
| 2 · ignores a lookalike | can it pick the real fact when a decoy of the same shape is planted too? |
| 3 · long reach | can it look up a fact 1,000–2,000 tokens back? |
| 4 · multi-step reasoning | can it follow a chain of four facts, each pointing to the next? |
| 5 · language-like noise | same skills when the filler looks like plausible text |
| 6 · hard stretch | tasks a narrow channel should not solve easily (reported, never gating) |

Every design runs this ladder at four model sizes, from 5M to 50M parameters, and gets a verdict from written rules: **scale up**, **promising, fix first**, or **not ready**. Scaling up requires, among other things, passing levels 0–2 at 30M parameters or more, matching or beating the best earlier design on at least one long-reach or reasoning exam, and not getting worse as the model grows.

{{< mermaid >}}
flowchart TB
  I["Idea"] --> S["Frozen spec:<br/>pass and kill criteria"]
  S --> R["Agents implement<br/>and train overnight"]
  R --> E["Fixed exam ladder,<br/>full-attention ceiling in every run"]
  E --> V["One-page scorecard<br/>and verdict"]
  V --> H{"I read, question<br/>and decide"}
  H -->|next idea| I
{{< /mermaid >}}

The agents do everything except the two boxes that matter most: the exam stays fixed, and the decision stays mine.

## What the exam showed about three notebook designs

Here is what happened when three ways of writing the notebook went through the exam. The details are in the [open repo](https://github.com/ksopyla/MrCogito); the numbers below are what matters.

### Design 1: the averaged notebook

The simplest notebook: average every 16 tokens into one note. At a million tokens, that shrinks the memory to around 64 MB.

The exam gave a sharp, two-sided answer. Copying a span from far back survived the averaging well: **54 of 64 bits** at 1,024 tokens. Looking up a fact by its key did not. With finer notes (one per 8 tokens) the lookup got **60 bits** at 1,024 tokens and then **0 bits** at 1,280, while the uncompressed notebook still got all 64.

An average keeps what a page is *about*. It loses the one detail you will be asked about later. The agents then worked through a queue of repairs: an extra loss to reconstruct each page from its note, and keeping the key tokens uncompressed next to the average. They recovered **1 and 3 bits** where the uncompressed notebook got about 47. Each repair had its kill criterion written in advance, so each one ended in a day instead of dragging on.

### Design 2: a learned note-taker

The second design replaced the average with learned attention. The book is covered by overlapping windows of 256 tokens, and each window has 32 learned "questions" that pick what to write into its notes.

This was the first design that looked genuinely better on hard exams. At 31M parameters:

- On a four-step chain across 1,024 tokens, it recovered **40 bits**. The averaged notebook recovered 4.
- On a lookup 1,024 tokens back, it got **26 bits**. Every other model, the full-attention one included, stayed at zero at that budget.

Then I noticed a pattern. The lookup at 31M parameters: 25.7 bits. At 50M: 24.3. At 2,048 tokens with finer windows: 25. The lookalike exam: 25.9. Different sizes, lengths and tasks, and all of them stopped near **26 bits out of 64**.

That was not a result. It was a fingerprint.

### The model I tested was not the model I designed

The regularity sent me back to the code, reading it line by line against my original design notes. The design called for real memory cells that read their window and keep what matters. The implementation wrote something much narrower: each note was a weighted average of token vectors, chosen by fixed learned queries that could only see **16 tokens back**.

That limit explains the fingerprint. A note-taker looking at a letter can only tell it belongs to the fact if the fact's marker is within its 16-token view. After the marker and the two-letter key, that covers the first 13 letters of the value. The other 19 look like random filler. Thirteen letters at 2 bits each is **26 bits**.

The review also found a latent leak, similar in spirit to the one from July: in some configurations the notebook could include tokens from the answer side. It never triggered on the recorded exams, but it would have in language training.

On a loss curve, this flaw would have looked like "a bit worse than I hoped". On the exam, it was a number that repeated itself until I asked why. I still have to confirm the explanation: the next run measures accuracy for each answer letter, and the 13-versus-19 split should be visible directly.

### Design 3: real memory cells, running now

The third design builds what the notes asked for in the first place. Each window is written by 32 memory vectors with their own state, their own width and an address saying where in the book they read from. They read the window in both directions, so a note-taker sees the whole fact in context. There are two variants of how that context is built, and a control that only widens the 16-token view, to separate "more context" from "better memory".

The pass marks were written before the first run: at least 40 of 64 bits on the 1,024-token lookup (the previous design stopped at 26), and at least 75% of the full-attention model's score on the lookalike and the four-step chain. If both variants stay below 32 bits after a doubled training budget, I record that the idea did not break the plateau and move on.

It started training this week. I do not have results yet.

## Six rules before letting agents explore

Most of what I learned in the last six weeks did not come from any one architecture. It came from the exam catching mistakes, many of them in the loop itself.

### 1. Write the goal and the kill criteria before the run

Every experiment starts as a frozen spec: the hypothesis, the one thing that changes, what counts as success, what counts as failure. An agent will always find a reason to extend a run or add one more tweak. The written criteria are what let a failed idea die in a day. The repairs to the averaged notebook each ended within a day or two, instead of dragging on for weeks.

### 2. Train the "can this be learned at all?" model next to every candidate

When the new design's first exam run came back this week, the full-attention model had failed some of the long exams too. Because it trains next to every candidate, the scorecard marked those cells as "not learnable at this budget", not as a failure of the new design. The fix took less than a day: the training budget gave about 38,000 examples at 1,024 tokens and 19,000 at 2,048, fewer than every model needs before it starts learning at that length. Without the ceiling in the same run, I would have killed a design because my exam was underfed.

### 3. Freeze and version the exam, and keep agents out of it

A saved configuration for the long exams once quietly became a **16-bit** exam instead of the recorded **64-bit** one: an override shortened the planted value from 32 letters to 8. Nothing crashed. The numbers would just have meant something else. Now every exam carries its expected prize in bits, a test fails if a configuration changes it, and any change to the exam bumps its version so old and new scores are never mixed. This is the same reason autoresearch forbids the agent to touch the evaluation code.

### 4. Most "failed" ideas are failed training runs

Training settings do not carry over across text lengths at this scale. The step size that trains 128-token exams kills the longer ones. At 1,024 tokens, a step three times larger made **every** architecture score zero on two exams. At 50M parameters, the uncompressed notebook "collapsed" on the chain exam; with a smaller step and more patience it scored 99%. Small models also often sit at chance for a long time and then jump. So the exam now fixes the step size per model size and length, and extends a run once if the loss is still falling, instead of letting an impatient schedule kill an idea.

### 5. A strange regularity means read the code

Twenty-six bits across every setting was the most useful number of the month, because it was too regular to be a coincidence. An exact score makes that kind of pattern visible. Next-token loss would have smeared it into noise.

### 6. The output of the loop should be one page

The exam produces a scorecard: bits per exam, the highest level passed, the comparison with every earlier design at the same size, and the verdict. My job in the morning is to read one page, ask why, and decide the next direction, not to scroll through forty training logs. That is the division of labour that makes auto-research work for me: agents are fast and tireless, and I am the one who has to stay suspicious.

## What the exam does not prove

- **It is not language.** Random letters with an exact score are a controlled test of the mechanism. My earlier experiments showed that natural text pays far less for memory. The next rung plants facts in real prose, and the exam will not call a design ready until it passes there.
- **It is small.** Everything here is 50M parameters or less, and the gating exams stop at 2,048 tokens. At 4,096 tokens none of the notebooks I tried, including the uncompressed one, found the fact. A million tokens is still an ambition, not a result.
- **It can be gamed.** A fixed exam invites designs that are good at the exam. The language-like noise level and the hard stretch exams, which never gate, are my guard against that, not a guarantee.
- **The rules are judgment calls.** A 75% pass mark and "no loss of more than 2 bits with size" are choices. I made them before seeing the new design's results, so at least they cannot bend toward it.
- **My results can still change.** The July result changed after an audit. Anything here can too. The log keeps old numbers next to their corrections.

## What I believe now

Auto-research is real, and for a solo researcher with evenings and seven GPUs it changes what is possible. Most of this month's experiments ran while I was asleep or at work.

But autonomy is the cheap part. The expensive part is the goal. Karpathy's loop works because validation loss is the right measure for his question. For mine, it was nearly blind, and a tireless loop pointed at a blind metric just produces well-documented noise.

If you want agents to explore new architectures for you, build the exam first:

- an exact score, so "better" is not a matter of opinion
- a ceiling model and a leak check trained in every run
- pass and kill criteria written before the run
- a frozen, versioned exam that the agents cannot touch
- a verdict that fits on one page

Then let them run all night.

## What comes next

1. Finish the first full exam run of the memory-cell design and publish the scorecard, whatever it says.
2. Check the 26-bit explanation directly with per-letter accuracy.
3. Add the language rung: facts planted in real prose, plus a short next-token test where the notebook has to earn its place.
4. Only if a design passes those, spend the compute on longer texts and bigger models.

## References

1. Karpathy, A. (2026). [**autoresearch**](https://github.com/karpathy/autoresearch). GitHub repository.
2. Schnabel, T. et al. (May 2025). [**Lost in Transmission: When and Why LLMs Fail to Reason Globally**](https://arxiv.org/abs/2505.08140). Microsoft Research. NeurIPS 2025. arXiv:2505.08140
3. Hsieh, C.-P. et al. (Apr 2024). [**RULER: What's the Real Context Size of Your Long-Context Language Models?**](https://arxiv.org/abs/2404.06654). NVIDIA. COLM 2024. arXiv:2404.06654
4. Kuratov, Y. et al. (Jun 2024). [**BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack**](https://arxiv.org/abs/2406.10149). NeurIPS 2024. arXiv:2406.10149
5. Sopyla, K. (Jul 2026). [**Replacing Gemma-3 Global Attention with Concepts (Toward Longer Context)**](https://ai.ksopyla.com/posts/gemma-with-concepts/). ai.ksopyla.com
6. Sopyla, K. (Mar 2026). [**Quicker Failures lead to better questions: How AI Helped Me Steer my research forward**](https://ai.ksopyla.com/posts/quicker-failures-better-questions/). ai.ksopyla.com
7. MrCogito sources: [the exam ladder spec](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/capability_suite.md) · [training rules for small models](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/small_model_capability_protocol.md) · [averaged notebook report](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/run_reports/e25_e21_dna_capability_report_20260916.md) · [learned note-taker and its code review](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E30_sliding_window_perceiver.md) · [memory-cell design](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E31_sliding_window_latent_memory.md) · [agent skills](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills) · [experiment log](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/master_experiment_log.md)

*All numbers are from my own runs on two servers with 3 and 4 RTX 3090 GPUs. Models are discarded after each exam. The memory-cell results are pending. Independent reproduction has not been published.*
