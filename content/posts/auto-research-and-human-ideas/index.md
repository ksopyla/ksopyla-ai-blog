---
title: "Auto-Research Can Run the Experiments. It Cannot Have the Idea."
date: 2026-09-27
draft: false
description: "Notes from a month of letting agents run my model research: strong at implementation, optimisation and test harnesses, but the unusual ideas still came from me."
tags: ["AI", "MrCogito", "Auto-Research", "Agents", "Evaluation", "Long Context", "Research Methodology"]
categories: ["AI Research"]
featureImage: "feature_auto_research_human_ideas.png"
featureAlt: "Abstract digital art of a lone human silhouette raising a glowing spark at night; a warm stream of text particles compresses into it from the left while cool blue streams of agents weave through a grid of glowing experiment cells on the right"
showReadingTime: true
---

{{< lead >}}
For the last month, agents have run most of my model research: they implement my designs, build the test harness, tune the training and run experiments on my GPU servers while I sleep. They are very good at it. But every idea that actually moved the project came from me, and at least once the agents quietly built a more ordinary version of the idea than the one I asked for. This is what I learned about dividing the work between a researcher and a research loop.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why I am building MrCogito: models that compress long text into dense concepts and reason over them, instead of attending to every token
- Where auto-research helped most (implementation, optimisation, test harnesses, running experiments around the clock) and where it did not (original ideas)
- Why next-token loss is the wrong goal for testing new memory architectures, and what a better exam looks like
- The habit that kept me aligned with the agents: an interactive diagram of what was actually built, reviewed before every launch
- What the loop found: a memory design that holds a fact at 128K tokens after training on books of at most 16K, and a control experiment that showed me which part of my own idea mattered

## Why I am doing this

Most of today's progress in language models comes from scale: more parameters, more data, longer context windows paid for with more GPUs. I think this is only part of the answer. A standard transformer lets every token look at every earlier token, so its cost grows with the square of the text length. At a million tokens, that becomes expensive even for large labs. At ten million, it is out of reach.

[MrCogito](/projects/concept-reasoning/) is my open research project exploring a different path. The model compresses a long input into a much smaller set of **concepts** (dense vectors), reasons over those concepts, and only then decodes the answer. Three things follow if that works:

- **Long context becomes a question of compression, not brute force.** Attention between N tokens and C concepts costs O(C·N) instead of O(N²). With the number of concepts growing with the text, one million tokens becomes tractable on hardware I can actually afford.
- **Reasoning gets a wider channel.** A text token carries roughly 15 bits. A 2,048-dimensional concept vector can carry thousands of times more. Reasoning in concept space, instead of writing every thought as text, is a higher-bandwidth way to think.
- **Models could exchange concepts, not text.** Eventually, cooperating agents could pass concept vectors to each other directly, which is the kind of agent communication I care about in my day job.

I also believe AI has to become much more efficient to be widely useful, and that small, well-designed experiments still matter. That is why this is a project run on evenings and weekends, on two servers with seven RTX 3090 GPUs, with models between 5M and 50M parameters. I build agent systems by day; at night I train my own models.

The hard part of this vision is memory. If the model compresses a long book into a small notebook of concepts, **does the notebook actually keep the facts needed later?** Every design in this post is a different answer to that question.

## My auto-research setup

In the second phase of the project I stopped running experiments by hand. The loop is a set of agent skills in the [MrCogito repo](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills), each owning one step:

1. **Design:** turn my idea into one falsifiable experiment spec, with success and kill criteria written before any code.
2. **Plan and implement:** map the spec onto the existing codebase and write the model, with tests.
3. **Run:** sync the code to the servers, launch training in persistent sessions, watch the logs, recover from crashes.
4. **Evaluate and record:** score the result, update the experiment log and write a short report.
5. **Communicate:** explain the result to me in plain language, with every number explained.

Helper agents check server health, read training curves from Weights & Biases and search for papers. Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) shows the same idea in its simplest form: an agent edits one training script, trains for five minutes, keeps the change if validation loss improved, and runs about a hundred experiments overnight.

It works. In September, agents made 176 commits to the research repo and I made fewer than a hundred. Over three days in the middle of the month, one exam campaign ran almost around the clock, with 115 commits to its log, many between midnight and six in the morning.

## What agents did well, and what they did not

These are my observations from a month of working this way, not a benchmark of agents.

**Implementation.** When I approved a new design one evening, the agents had the model written, tested and the previous design's bugs fixed within hours. That includes a causality test that perturbs future tokens and checks that earlier predictions do not change, which I would have skipped when tired.

**Optimisation.** The agents found the training settings that make small models learn at long lengths: step sizes that change with text length, budgets large enough for late takeoff, when to extend a run instead of killing it. Tedious work, done thoroughly.

**Harness.** The test suite described below (a ladder of exams, four model sizes, scoring rules, a scorecard) was built by agents in about a day. When its first real run exposed a budget that was too small, they fixed it overnight, twice.

**Persistence.** Agents do not get bored of running the same exam at eight lengths with three seeds.

What they did not do was produce the ideas that changed direction. My opinion after this month: **agents are strong at the moves that already exist in the literature, and weak at the move that does not.** When an early design failed, the repairs they queued were the textbook ones: add a reconstruction loss, keep key tokens uncompressed. Each was a reasonable choice, and each failed.

The more surprising failure went the other way. I wrote an idea note for a new memory design, in my own words. Two of its lines (typos fixed):

> "slots where r token vectors are averaged is not a good idea, we want something which picks the signal from noise in each window"
>
> "TinyHashed Embeddings: I didn't see much difference ... by default do not implement that, keep it simple"

The agents built it, tests passed, runs started, results came in. A few days later I found that each memory slot was, in effect, **a weighted average of token vectors**, and the hashed embeddings were switched on. The implementation had drifted back towards the common pattern, the one the note explicitly rejected. Nothing crashed. The model trained and scored reasonably. It just was not my idea.

This is the risk of auto-research that I did not expect: not wrong code, but **ordinary code**. An unusual idea is, by definition, far from the patterns an agent has seen most often, and it gets pulled back towards them one reasonable decision at a time.

## The goal problem: next-token loss is nearly blind to memory

Before I could trust any of this, I had to fix the loop's goal.

Karpathy's autoresearch optimises validation loss, and the agent may not touch the evaluation code. For improving a training recipe, that is exactly right. For testing a new memory architecture, the standard loss is almost blind.

Two experiments showed me why. I trained a 125M model whose only long-range path was a single lookup into earlier text, and an identical model with that lookup removed. Their final losses: **4.090** and **4.091**. In another experiment, the notebook's distant entries were worth about **0.05 nats** of loss on ordinary text, the same at 1,000 tokens as at 32,000. At the scale I can afford, predicting the next word needs almost nothing from far away. A model can reach a good loss while its memory is decoration, and an agent optimising that loss will happily report progress.

It had already fooled me once in public. In July I reported that a concept memory grafted into Gemma-3 [seemed to take over long-range work](/posts/gemma-with-concepts/). A later audit of my code found that later layers could read memory written from the current stretch of text, including a little of what came next. The loss signal was real, but part of it was not memory.

**An agent optimises whatever you measure, faster than you can check it. If the measure does not reward memory, the loop will not find memory.**

## Giving the loop a real goal: an exam with an exact score

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

The exam gave the agents a goal worth optimising. It did not stop them from building the wrong model. For that I needed something else.

## The habit that kept me in line with the agents: diagram before launch

After implementation, and before any run or harness launch, I now ask the agents for one more thing: **an interactive diagram of what the code actually implements.** Not the design I described. The forward pass that will run, step by step, with tensor shapes, and with a toggle to compare it against the previous design.

I started this by accident. After the second memory design's runs (described below), I asked for an interactive page showing how information flows through it. Clicking through it, I could see that each note was a weighted pick of tokens, written by a note-taker that could only see 16 tokens back. That became a full review the same day, and the review explained a number that had been puzzling me for days.

Every run of that design had stopped near **26 bits out of 64**: at different model sizes, different lengths, different exams. A note-taker that sees 16 tokens back can only recognise a value letter as part of the fact if the fact's marker is within view. After the marker and the two-letter key, that covers the first 13 letters of the value. The other 19 look like random filler. Thirteen letters at 2 bits each is **26 bits**.

For the next design I did it on purpose. Before launch, the agents produced two pages: an architecture page with a checklist of open design decisions that were not part of the experiment until I confirmed them, and a wiring page where I can click any cell and see everything it depends on, down to the token embeddings.

![Interactive wiring page generated before launch: every layer and token of a small example, showing the memory path, the main path, and where the answer prediction gets its information from.](interactive_wiring_page.png "The wiring page the agents generated before launch. Clicking the answer prediction (top row) highlights its full route: through the global read, into the memory slots, down to the fact's tokens. A toggle switches to the previous design, where most of the value letters never see the fact's marker.")

Why this works better than reading the code:

- **It shows what is built, not what was intended.** The agent has to trace the real forward pass to draw it, so the drift from the idea note becomes visible.
- **It is fast to review.** Fifteen minutes of clicking beats reading a thousand lines of diff at 11 pm.
- **It is a shared language.** When I say "this latent should not see the answer side", we are both looking at the same picture.
- **It catches leaks.** A dependency line from the answer back into the memory is hard to miss when it is drawn in orange.

My rule now: **no launch until I have clicked through the diagram and it matches my idea.**

## What the exam and the loop found

With a real goal and a way to check the build, the loop started producing results I trust.

### An average cannot hold a key

The first memory design averaged every 16 tokens into one note. At a million tokens that would shrink the memory to about 64 MB. Copying a far span survived the averaging (54 of 64 bits at 1,024 tokens). Looking up a fact by its key did not: with one note per 8 tokens, lookup got 60 bits at 1,024 tokens and **0 bits** at 1,280, while the uncompressed memory still got all 64. An average keeps what a page is about. It loses the one detail you will be asked about.

### Learned notes beat averages, and hit a wall I could explain

The second design used overlapping windows with 32 learned "questions" each, choosing what to write. It followed a four-step chain across 1,024 tokens (40 bits, against 4 for the average) and was the only model above zero on a lookup at that length. Then it stopped at 26 bits everywhere, the salience wall from the diagram.

### Real memory cells passed the whole exam

The third design is the one the idea note asked for: 32 memory vectors per window, each with its own state, width and address, reading the whole window in both directions before writing. At 30M parameters it passed every gating level of the exam, including the level with language-like noise, and got the verdict **scale up**. On the 1,024-token lookup it recovered **94%** of the answer letters, up from 54%, and accuracy was flat across all 32 letters. The 13-letter wall was gone, which also confirmed the diagnosis.

### The control told me which part of my idea mattered

Here is the humbling part. The spec included a cheap control: the old note-taker with only one change, a wider 64-token view. It was there to separate "more context" from "better memory".

On the short exams, the control **matched or beat** my memory cells: 99% against 94% on the lookup with a decoy, 99% against 89% on the 2,048-token lookup. Most of the gain came from context, not from my elegant latent design. Without that control, I would have credited the wrong idea.

### Then the length test separated them

Short exams check whether a memory works. They do not check whether it keeps working when the book grows. So the next test trained on 2,048-token books and evaluated on books up to 128K tokens.

![Line charts of accuracy versus book length from 2K to 128K tokens. The content-addressed memory with a short curriculum stays above 95% up to 64K and reaches 80% at 128K on lookup and 82% on a 4-step chain; position-addressed memory, the wider-context note-taker and full attention fall to chance.](memory_length_generalization.png "Train short, test long. The memories that read by position fall to chance within 8× of their training length; the content-addressed memory holds.")

The picture changed completely:

- The memory design as first built, and the wider-context control, both fell to chance by 16K tokens. Both had learned **where** facts sit, not **what** they are: trained at length L, they reach roughly 2L and fail on the far facts first.
- A variant of the memory without an absolute address, where slots are matched by content rather than by their position in the book, held **98%** at 32K and **80%** at 128K after two short extra stages at 8K and 16K. A second seed replicated it (81% at 128K).
- On the four-step chain, full attention trained on 2K books dropped to chance at 4K. The content-addressed memory, starting from its lookup weights, held **82%** at 128K after one extra stage at 8K. Trained from scratch on the chain, it did not take off in two attempts: it has to learn lookup before it can learn to follow a chain.
- Evaluating a 128K-token book costs 1.35 seconds and 3.4 GB on one RTX 3090. The cost grows linearly with length.

This is the first result in the project that points directly at the long-context goal from the beginning of this post. It is also a result the short exams alone would have hidden: at 2K tokens, the position-reading models looked just as good.

## What I would tell another researcher using agents

1. **Keep the idea yours, and write it down in your own words.** An idea note with explicit "do not do this" lines is the reference you will need when the implementation drifts.
2. **Give the loop an exam, not a loss.** Exact scores, a full-attention ceiling and a no-memory leak check in every run, criteria written before the run, and an exam the agents cannot edit.
3. **Ask for an interactive diagram of what was built, before every launch.** Review it against the idea note. It is the cheapest alignment check I have found.
4. **Always include the boring control.** The cheapest alternative explanation, run in the same job, told me which part of my own idea mattered.
5. **Train short, test long.** Position shortcuts look perfect at the training length. Length generalisation is where memory designs actually differ.
6. **Most failed ideas are failed training runs.** Step size, budget and late takeoff killed more designs in my logs than bad architecture did. Let the agents handle this, and keep the rules in the exam.

## What this does not prove

- **It is not language yet.** Random letters with an exact score are a controlled test of the mechanism. The next rung plants facts in real prose and adds a next-token test where the memory has to earn its place.
- **It is small.** 30M parameters, training books up to 16K tokens. 128K is evaluation only.
- **Seeds vary.** One of three seeds reached only 65% even at 2K tokens. The chain needs a lookup-first curriculum.
- **One level of memory is not enough for a million tokens.** A coarser version (512-token windows, 8 slots each) dropped from 93% to 39% on the 2K lookup, so the 1M design will need a two-level memory: coarse notes to find the right pages, fine notes to read them.
- **My view of agents is one month, one project.** Other people will see different strengths and failure modes.

## What I believe now

Auto-research is real. For a solo researcher with evenings and seven GPUs, it changes what is possible: most of this month's experiments ran while I was asleep or at work, and the harness they run on was built by agents.

But the loop amplifies what you give it. Give it a blind metric and it produces well-documented noise. Give it an unusual idea without a way to check the build, and it returns a more common idea. Give it a good exam, a frozen spec, a diagram to review and a boring control, and it becomes the best research assistant I have had.

The ideas, the questions and the suspicion are still the researcher's job. I do not think that is a temporary limitation to wait out. It is the division of labour I want.

## What comes next

1. Facts planted in real prose, and a next-token test where the memory has to lower the loss on tokens whose evidence is far away.
2. A two-level memory for the million-token setting.
3. Reasoning loops over the concepts, the part of the vision this memory was built to support.

## References

1. Karpathy, A. (2026). [**autoresearch**](https://github.com/karpathy/autoresearch). GitHub repository.
2. Schnabel, T. et al. (May 2025). [**Lost in Transmission: When and Why LLMs Fail to Reason Globally**](https://arxiv.org/abs/2505.08140). Microsoft Research. NeurIPS 2025. arXiv:2505.08140
3. Tishby, N., Pereira, F. C., Bialek, W. (Apr 2000). [**The information bottleneck method**](https://arxiv.org/abs/physics/0004057). arXiv:physics/0004057
4. Hsieh, C.-P. et al. (Apr 2024). [**RULER: What's the Real Context Size of Your Long-Context Language Models?**](https://arxiv.org/abs/2404.06654). NVIDIA. COLM 2024. arXiv:2404.06654
5. Kuratov, Y. et al. (Jun 2024). [**BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack**](https://arxiv.org/abs/2406.10149). NeurIPS 2024. arXiv:2406.10149
6. Jaegle, A. et al. (Mar 2021). [**Perceiver: General Perception with Iterative Attention**](https://arxiv.org/abs/2103.03206). ICML 2021. arXiv:2103.03206
7. Sopyla, K. (Jul 2026). [**Replacing Gemma-3 Global Attention with Concepts (Toward Longer Context)**](https://ai.ksopyla.com/posts/gemma-with-concepts/). ai.ksopyla.com
8. Sopyla, K. (Mar 2026). [**Quicker Failures lead to better questions: How AI Helped Me Steer my research forward**](https://ai.ksopyla.com/posts/quicker-failures-better-questions/). ai.ksopyla.com
9. MrCogito sources: [project vision](https://github.com/ksopyla/MrCogito/blob/dev/docs/1_Strategy_and_Plans/vision_and_goals.md) · [the exam ladder](https://github.com/ksopyla/MrCogito/blob/dev/docs/engineering_specs/capability_suite.md) · [agent skills](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills) · [memory-cell design and results](https://github.com/ksopyla/MrCogito/blob/e31-latent-memory/docs/experiments_specs/ahead/E31_sliding_window_latent_memory.md) · [experiment log](https://github.com/ksopyla/MrCogito/blob/dev/docs/2_Experiments_Registry/master_experiment_log.md)

*All numbers are from my own runs on two servers with 3 and 4 RTX 3090 GPUs. Models are discarded after each exam. Independent reproduction has not been published.*
