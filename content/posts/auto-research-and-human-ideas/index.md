---
title: "Auto-Research Can Run the Experiments. It Cannot Have the Idea."
date: 2026-09-27
draft: false
description: "Notes from a month of letting agents run my model research: strong at implementation, optimisation and test harnesses, but the unusual ideas still came from me."
tags: ["AI", "MrCogito", "Auto-Research", "Agents", "Evaluation", "Research Methodology"]
categories: ["AI Research"]
featureImage: "feature_auto_research_human_ideas.jpg"
featureAlt: "Abstract digital painting at night: a lone person raises a glowing spark that lights a constellation of concept nodes; a warm stream of particles pours into it from the left, while blue rivers of light wind through a city where small robots tend glowing glass cubes of experiments"
showReadingTime: true
---

{{< lead >}}
For the last month, agents have run most of my model research: they implement my designs, build the test harness, tune the training and run experiments on my GPU servers while I sleep. They are very good at it. But every idea that actually moved the project came from me, and at least once the agents quietly built a more ordinary version of the idea than the one I asked for. This is what I learned about dividing the work between a researcher and a research loop.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Where auto-research helped most (implementation, optimisation, test harnesses, running experiments around the clock) and where it did not (original ideas)
- How an unusual idea drifts back into an ordinary one, one reasonable decision at a time, without anything crashing
- Why next-token loss is the wrong goal for a research loop that explores new architectures, and what a better exam looks like
- The habit that kept me aligned with the agents: an interactive diagram of what was actually built, reviewed before every launch
- Six rules I now follow before letting agents explore on their own

## Twenty-six bits, every time

The number was 26.

My agents had built a new memory design for my research model, tested it, trained it on my two GPU servers and scored it on a fixed exam where the full answer is worth 64 bits. At 31M parameters it scored 25.7 bits. At 50M, 24.3. On books twice as long, 25. On a harder exam with a decoy fact, 25.9.

Different sizes, different lengths, different exams. The same number.

The reports recorded it faithfully, run after run. Nothing had crashed, the training curves looked healthy, and the design did beat the previous one. By every signal the loop was built to check, things were fine.

A number that refuses to move across every setting is not a result. It is a fingerprint. It took me a few days, and one habit I did not have yet, to find out whose fingerprint it was.

## Why I let agents run my research

[MrCogito](/projects/concept-reasoning/) is my open research project on models that compress a long input into a small set of dense vectors, which I call **concepts**, and reason over those instead of attending to every token. If it works, long context becomes a question of compression rather than brute force, and a million-token input becomes affordable on hardware like mine. I explain the architecture side in a separate post: [A Memory That Reads by Content](/posts/memory-that-reads-by-content/).

It is an evenings-and-weekends project, run on two servers with seven RTX 3090 GPUs. I build agent systems by day. For the second phase of the project I decided to let the same kind of agents run the research at night.

The loop is a set of agent skills in the [MrCogito repo](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills), each owning one step:

1. **Design:** turn my idea into one falsifiable experiment spec, with success and kill criteria written before any code.
2. **Plan and implement:** map the spec onto the existing codebase and write the model, with tests.
3. **Run:** sync the code to the servers, launch training in persistent sessions, watch the logs, recover from crashes.
4. **Evaluate and record:** score the result, update the experiment log and write a short report.
5. **Communicate:** explain the result to me in plain language, with every number explained.

Helper agents check server health, read training curves from Weights & Biases and search for papers. Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) shows the same idea in its simplest form: an agent edits one training script, trains for five minutes, keeps the change if validation loss improved, and runs about a hundred experiments overnight.

It works. In September, agents made 176 commits to the research repo and I made fewer than a hundred. Over three days in the middle of the month, one exam campaign ran almost around the clock, with 115 commits to its log, many between midnight and six in the morning.

## What agents are good at

These are my observations from a month of working this way, not a benchmark of agents.

**Implementation.** When I approved a new design one evening, the agents had the model written, tested and the previous design's bugs fixed within hours. That includes a causality test that perturbs future tokens and checks that earlier predictions do not change, which I would have skipped when tired.

**Optimisation.** The agents found the training settings that make small models learn at long lengths: step sizes that change with text length, budgets large enough for late takeoff, when to extend a run instead of killing it. Tedious work, done thoroughly.

**Harness.** The test suite described below (a ladder of exams, four model sizes, scoring rules, a scorecard) was built by agents in about a day. When its first real run exposed a budget that was too small, they fixed it overnight, twice.

**Persistence.** Agents do not get bored of running the same exam at eight lengths with three seeds.

What they did not do was produce the ideas that changed direction. My opinion after this month: **agents are strong at the moves that already exist in the literature, and weak at the move that does not.** When an early design failed, the repairs they queued were the textbook ones: add a reconstruction loss, keep key tokens uncompressed. Each was a reasonable choice, and each failed.

## Before the loop can find anything, it needs the right goal

The first problem was not the agents. It was what I asked them to optimise.

Karpathy's autoresearch optimises validation loss, and the agent may not touch the evaluation code. For improving a training recipe, that is exactly right. For testing a new memory architecture, the standard loss is almost blind.

Two experiments showed me why. I trained a 125M model whose only long-range path was a single lookup into earlier text, and an identical model with that lookup removed. Their final losses: **4.090** and **4.091**. In another experiment, the memory's distant entries were worth about **0.05 nats** of loss on ordinary text, the same at 1,000 tokens as at 32,000. At the scale I can afford, predicting the next word needs almost nothing from far away. A model can reach a good loss while its memory is decoration, and an agent optimising that loss will happily report progress.

It had already fooled me once in public. In July I reported that a concept memory grafted into Gemma-3 [seemed to take over long-range work](/posts/gemma-with-concepts/). A later audit of my code found that later layers could read memory written from the current stretch of text, including a little of what came next. The loss signal was real, but part of it was not memory.

**An agent optimises whatever you measure, faster than you can check it. If the measure does not reward memory, the loop will not find memory.**

So I built an exam where "better" cannot be argued about, based on a 2025 framework by Schnabel et al. that treats a transformer's view of earlier text as a narrow communication channel:

- The "book" is a long string of random letters from a four-letter alphabet, like DNA.
- Somewhere far back, a fact is planted: a marker, a two-letter key and a 32-letter value.
- At the end comes a question, and the model has to write the value.

The value is random, so it cannot be guessed. Each letter is worth exactly 2 bits, so the full answer is a **64-bit prize**. A model that recovers 40 bits has carried 40 bits across the book. Zero means chance. No language priors, no tokenizer effects.

Every exam trains four models on identical data:

| model | why it is there |
|---|---|
| **full attention** (rereads any page) | if it cannot reach 75%, the exam is not learnable at this budget, and nothing else counts |
| **uncompressed memory** | shows what compression costs |
| **no memory** | if it beats chance, the answer leaks and the exam is broken |
| **the candidate** | the new design |

The exams form a ladder: learn at all, carry a whole fact, ignore a decoy that looks like the fact, reach 1,000–2,000 tokens back, follow a four-step chain of facts, and do all of that when the filler looks like plausible text. Every design runs at four sizes, from 5M to 50M parameters, and gets a verdict from rules written in advance: **scale up**, **promising, fix first**, or **not ready**. The exam is versioned, every cell carries its expected prize in bits, and a test fails if anyone, human or agent, changes it by accident. That last rule exists because it happened once: a saved configuration quietly turned a 64-bit exam into a 16-bit one.

The exam gave the agents a goal worth optimising. It is also the exam that kept returning 26 bits.

## Back to the 26 bits: the model I tested was not the model I designed

After those runs, I asked the agents for something new: an interactive page showing how information flows through the model, step by step, as the code actually implements it.

Clicking through it, I saw the first clue: each note was described as "a weighted pick of the tokens in its own window". I asked for a full review of the code against my original idea note. It came back the same day.

The design came from an idea note I had written in my own words. Two of its lines (typos fixed):

> "slots where r token vectors are averaged is not a good idea, we want something which picks the signal from noise in each window"
>
> "TinyHashed Embeddings: I didn't see much difference ... by default do not implement that, keep it simple"

In the code, each memory slot was, in effect, **a weighted average of token vectors**, and the hashed embeddings were switched on. Each slot was written by a note-taker that could only see **16 tokens back**.

That last detail explained the fingerprint. A note-taker looking at a letter can only tell it belongs to the fact if the fact's marker is within its 16-token view. After the marker and the two-letter key, that covers the first 13 letters of the value. The other 19 look like random filler. Thirteen letters at 2 bits each is **26 bits**.

The implementation had drifted back towards the common pattern, the one my note explicitly rejected. Nothing crashed. The model trained and scored reasonably. It just was not my idea.

This is the risk of auto-research that I did not expect: not wrong code, but **ordinary code**. An unusual idea is, by definition, far from the patterns an agent has seen most often, and it gets pulled back towards them one reasonable decision at a time. Tests do not catch it, because the tests check the code the agent wrote, not the idea you had.

## The habit: no launch without a diagram

Since then, after implementation and before any run or harness launch, I ask the agents for **an interactive diagram of what the code actually implements.** Not the design I described. The forward pass that will run, step by step, with tensor shapes, and with a toggle to compare it against the previous design.

For the next design, the agents produced two pages before launch: an architecture page with a checklist of open design decisions that were not part of the experiment until I confirmed them, and a wiring page where I can click any cell and see everything it depends on, down to the token embeddings.

![Interactive wiring page generated before launch: every layer and token of a small example, showing the memory path, the main path, and where the answer prediction gets its information from.](interactive_wiring_page.png "The wiring page the agents generated before launch. Clicking the answer prediction (top row) highlights its full route: through the global read, into the memory slots, down to the fact's tokens. A toggle switches to the previous design, where most of the value letters never see the fact's marker.")

Why this works better than reading the code:

- **It shows what is built, not what was intended.** The agent has to trace the real forward pass to draw it, so the drift from the idea note becomes visible.
- **It is fast to review.** Fifteen minutes of clicking beats reading a thousand lines of diff at 11 pm.
- **It is a shared language.** When I say "this latent should not see the answer side", we are both looking at the same picture.
- **It catches leaks.** A dependency line from the answer back into the memory is hard to miss when it is drawn in orange.

The design built this way passed every level of the exam at 30M parameters. The 26-bit wall disappeared: the model recovered 94% of the answer letters, and accuracy was flat across all 32 of them.

My rule now: **no launch until I have clicked through the diagram and it matches my idea.**

## The control that corrected me

One more lesson came from the same run, and it was about me rather than the agents.

The spec included a cheap control: the old note-taker with a single change, a wider 64-token view. It was there to separate "more context" from "better memory".

On the short exams, the control **matched or beat** my new design. Most of the gain came from context, not from the part of the idea I was proudest of. Only one version of the new design pulled ahead, and only when the books got much longer, which is the story of the [companion post](/posts/memory-that-reads-by-content/).

Without that boring control, I would have credited the wrong idea. It is an easy control to skip, because it can only make your idea look smaller. Ask for it anyway.

## Six rules before letting agents explore

1. **Keep the idea yours, and write it down in your own words.** An idea note with explicit "do not do this" lines is the reference you will need when the implementation drifts.
2. **Give the loop an exam, not a loss.** Exact scores, a full-attention ceiling and a no-memory leak check in every run, criteria written before the run, and an exam the agents cannot edit.
3. **Ask for an interactive diagram of what was built, before every launch.** Review it against the idea note. It is the cheapest alignment check I have found.
4. **Always include the boring control.** The cheapest alternative explanation, run in the same job, tells you which part of your idea matters.
5. **Treat a number that never moves as a question, not a result.** Regularity across settings usually points at the implementation, not at the idea.
6. **Most failed ideas are failed training runs.** Step size, budget and late takeoff killed more designs in my logs than bad architecture did. Let the agents handle this, and keep the rules in the exam.

## What this does not prove

- **It is one month and one project.** Other people will see different strengths and failure modes, and agents improve quickly.
- **The drift is one clear case, not a statistic.** I saw it once in full and suspect it in smaller decisions elsewhere.
- **The exam is synthetic.** Random letters with an exact score test the mechanism, not language. The next rung plants facts in real prose.

## What I believe now

Auto-research is real. For a solo researcher with evenings and seven GPUs, it changes what is possible: most of this month's experiments ran while I was asleep or at work, and the harness they run on was built by agents.

But the loop amplifies what you give it. Give it a blind metric and it produces well-documented noise. Give it an unusual idea without a way to check the build, and it returns a more common idea. Give it a good exam, a frozen spec, a diagram to review and a boring control, and it becomes the best research assistant I have had.

The ideas, the questions and the suspicion are still the researcher's job. I do not think that is a temporary limitation to wait out. It is the division of labour I want.

## What comes next

The research result this loop produced, a memory that keeps finding facts at 128K tokens after training on much shorter books, has its own write-up: [A Memory That Reads by Content](/posts/memory-that-reads-by-content/). Next for the loop itself: an exam rung with facts planted in real prose, so the agents optimise against language and not only against letters.

## References

1. Karpathy, A. (2026). [**autoresearch**](https://github.com/karpathy/autoresearch). GitHub repository.
2. Schnabel, T. et al. (May 2025). [**Lost in Transmission: When and Why LLMs Fail to Reason Globally**](https://arxiv.org/abs/2505.08140). Microsoft Research. NeurIPS 2025. arXiv:2505.08140
3. Sopyla, K. (Jul 2026). [**Replacing Gemma-3 Global Attention with Concepts (Toward Longer Context)**](https://ai.ksopyla.com/posts/gemma-with-concepts/). ai.ksopyla.com
4. Sopyla, K. (Mar 2026). [**Quicker Failures lead to better questions: How AI Helped Me Steer my research forward**](https://ai.ksopyla.com/posts/quicker-failures-better-questions/). ai.ksopyla.com
5. MrCogito sources: [agent skills](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills) · [the exam ladder](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/capability_suite.md) · [the review that found the drift](https://github.com/ksopyla/MrCogito/blob/dev/docs/experiments_specs/ahead/E30_sliding_window_perceiver.md) · [experiment log](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/master_experiment_log.md)

*All numbers are from my own runs on two servers with 3 and 4 RTX 3090 GPUs. Independent reproduction has not been published.*
