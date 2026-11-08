---
title: "Why I built Claude Code a long-term memory, and what the benchmarks don't tell you"
date: 2026-11-01
draft: true
description: "Notes on Cogi, a local memory for Claude Code: why I built it, where it helps in my research sessions, how it scores on LongMemEval and LoCoMo, and why those scores say less than I hoped about real use."
tags: ["AI", "AI Engineering", "Agent Memory", "Evals", "Claude Code", "MCP"]
categories: ["AI Engineering"]
showReadingTime: true
---

{{< lead >}}
I do my AI research in long Claude Code sessions, and by the end of one Claude has lost most of what I said at the start. So I built Cogi, a memory that keeps every message word for word on my laptop. It finds the right past session for 99.0% of the questions on a standard benchmark, over histories of about 115k tokens. On 2.3M tokens of my own research sessions, it fully answers 79% of direct questions and 42% of all the questions I tested. Both numbers are true, and this post is about the distance between them.
{{< /lead >}}

## TL;DR

**What you will learn:**

- How much of a long session survives repeated compaction, measured on my own transcripts
- What Cogi is, and where it has helped me so far
- How it scores on LongMemEval-S and LoCoMo, and how much the grader changes that
- Why those benchmarks predict little about a memory behind a coding agent

## Why I built it

My evenings go to [MrCogito](/projects/concept-reasoning/), a solo research project on concept-reasoning models. A typical session goes like this: I discuss an idea, Claude writes the code, we run an experiment, I change the idea, and we repeat. Claude Code compacts the conversation when it gets long, and one of my sessions went from 782k to 13k tokens in a single step. Sooner or later I notice that Claude no longer knows what I asked for at the beginning or what we already tried. The second loss is quieter. I work across several sessions, a paper or an idea gets explained in one of them, and two weeks later it matters and neither of us remembers it. <!-- TODO Krzysztof: this paragraph is built from your own prompts in the Cogi sessions. Please add the specific moment that made you start, if there was one. -->

The case I wrote into the [requirements](https://github.com/meridian21lab/cogito-mem/blob/main/docs/requirements.md) was one sentence: *"Do you remember that idea from a week ago? I'd like to revisit it."* At the time I was also studying neural memory for MrCogito ([memory that reads by content](/posts/memory-that-reads-by-content/)), and I wanted to see how far plain retrieval goes before training anything.

I only measured the forgetting later, while preparing this post. My transcripts hold 89 compaction records, and 15 session files passed 1M tokens, though some of those are forks of each other. A Claude session extracted 72 early facts from 5 long sessions, such as requirements, rejected ideas and experiment results, and checked which ones survived:

| Where I looked | Fact fully or partly present | Fully present |
|---|---|---|
| First compaction summary | 83% | 69% |
| Middle summary | 44% | 15% |
| Last summary | 21% | 4% |
| Everything Claude can see at the end of the session | **28%** | 10% |

Some of those facts were later replaced by better decisions, so forgetting them was correct. Even so, a summary of a summary keeps less each time.

## What Cogi is

Most memory products have an LLM extract facts from each message and search those. Cogi makes the opposite bet: keep every message word for word with its date, make no AI calls to store anything, and put the effort into finding the right text later. Nothing that comes back was generated, so it cannot invent a decision I never made.

Search fuses BM25 keywords with [EmbeddingGemma 2](https://github.com/meridian21lab/cogito-mem/blob/main/docs/benchmarks.md#setup) running in llama.cpp, and each query returns stored text inside a token budget. Everything sits in one SQLite file on my machine, with no account and no API key. In Claude Code it arrives as a plugin with two paths:

- **Automatic:** hooks save each turn and add at most 300 tokens of matching memories to each new prompt.
- **On request:** Claude calls `memory_query`, which returns 1,000 tokens by default, or `memory_append` to save a note.

Cogi is about two weeks old, and Claude Code sessions wrote the eval harnesses and ran the evaluations. I decided what to build, what to test and what to believe.

## Where it helps

These are the uses I would stand behind today. The numbers come from the same 72 facts: blind agents wrote the questions and judged the answers, using a scratch copy of the memory.

**An undo for compaction, when you ask.** Of the 72 facts, 52 were completely gone from what Claude could see at the end of the session. Of the 16 direct questions about those, Cogi's search answered 12 fully and 2 partly. "What did I say about the parameter count at the start?" now gets my own sentence back, with its date, rather than Claude's reconstruction of it.

**That idea from three weeks ago.** Across all 24 direct questions, explicit search answered 79% fully and 88% at least partly, from 1,000 tokens. If I can name the topic, this works, across every project.

**Parallel sessions on shared hardware.** I did not plan for this one, and it is the most useful thing I found. A blind review of 97 real automatic recalls rated 12 as useful, and 7 of those 12 were about another running session: which GPUs a run had taken, a past GPU clash, a checkout that held live run folders and should not change branch.

**Catching a constraint I forgot.** This is the behaviour I hoped would be common. A test prompt proposed adding millions of weights to my E31 model, and the automatic recall brought back my own earlier requirement to keep the parameter count the same. That fact was gone from the session's context. It is also rare, as the next sections show.

**Unpublished work.** Nothing leaves the machine and there is no per-message bill. That is a design fact rather than a measurement.

One pattern is promising but unproven: an experiment ledger for autonomous loops, where the harness queries before each step ("has this been tried?") and appends after it. In a stress test 16 concurrent agents made 820 writes with no errors, but nobody has measured whether agents finish tasks better with it.

## How we tested it

Before any of the above, I ran the benchmarks that memory tools are compared on. All runs are on a MacBook Pro with an M5 Max, on 19 and 20 October 2026, on versions 0.1.0 and 0.2.0, and the [benchmarks page](https://github.com/meridian21lab/cogito-mem/blob/main/docs/benchmarks.md) has the commands and hashes.

**Finding the right session.** [LongMemEval](https://arxiv.org/abs/2410.10813) gives each of 500 questions a history of about 50 chat sessions, roughly 115k tokens, and labels the sessions holding the answer. No LLM is involved. Cogi puts an answer session in the top five for 99.0% of questions (95% CI 97.7 to 99.6), next to self-reported runs from [hippo-memory](https://github.com/kitfunso/hippo-memory/blob/main/docs/evals/2026-09-23-longmemeval-reproduction.md) at 98.0 and [deja-vu](https://github.com/vshulcz/deja-vu) at 97.2. With 500 questions those three are level. The test is also close to saturated: my keyword-only run reaches 95.0. When every answer session must be in the top five, Cogi falls to 90.8, and on that stricter metric [gbrain](https://github.com/garrytan/gbrain-evals/blob/main/docs/benchmarks/2026-05-07-longmemeval-s.md) is ahead. Blocking sessions dated after the question, which the protocol allows, gives 95.0.

**Answering from a small budget.** [LoCoMo](https://arxiv.org/abs/2402.17753) has 10 long conversations and 1,540 questions, and the control I care about is rereading the whole conversation of about 20,600 tokens in the same harness. Under [Mem0's 2026 protocol](https://github.com/mem0ai/memory-benchmarks), with GPT-5 mini grading:

| Answering model | Whole conversation | Cogi, 1,000 tokens | Paired gap (95% CI) | Gap, stricter rules |
|---|---|---|---|---|
| Claude Haiku 5.5 | 94.5 | 89.9 | −4.6 (−6.0 to −3.2) | −9.0 |
| GPT-5 mini | 94.1 | 89.4 | −4.7 (−6.2 to −3.3) | −7.8 |
| Qwen3-235B | 92.5 | 88.1 | −4.4 (−6.0 to −2.8) | −7.3 |
| gpt-oss-120b | 89.0 | 85.6 | −3.4 (−5.1 to −1.6) | −4.0 |

So 1,000 tokens get about 95% of the score from about 9 times less reading. That is a good trade but not a tie, and I first claimed a tie. With gpt-4o-mini and the Mem0 paper's rules, on 762 questions, the gap was −1.8 (−5.5 to +1.8), and my README said "level with rereading the whole conversation". The model, the grader and the sample all changed between those runs. I have since [corrected the public pages](https://meridian21lab.github.io/cogito-mem/results.html).

Most of the gap comes from retrieval. On the 1,114 questions where all the evidence fit in the budget, GPT-5 mini scores 95.7 with Cogi and 95.1 with the whole conversation. On the other 426 it scores 72.8 against 91.5. Multi-hop questions pay most among the charted types, because their evidence fits only 26.6% of the time:

![Line chart of answer accuracy with GPT-5 mini at 300, 1,000 and 2,500 tokens and with the whole conversation. All questions: 79.6, 89.4, 92.1, 94.1. Single-hop: 84.7, 93.6, 95.4, 96.1. Temporal: 80.1, 86.0, 90.7, 90.7. Multi-hop: 68.8, 86.2, 89.4, 94.3.](budget_vs_answer_quality.png "Answer accuracy against reading budget, GPT-5 mini answering, Mem0's 2026 rules. The 96 open-domain questions count in the 'All' line but have no line of their own.")

**The grader moves more than you would like.** Under the 2026 prompt, one correct item from a list is enough, dates within 14 days count, and durations within 50% count. Re-grading the same GPT-5 mini answers under the stricter 2025 rules takes Cogi from 89.4 to 83.1 but the whole conversation only from 94.1 to 90.8, so the lenient rules hide part of the memory's loss. An [independent audit of LoCoMo](https://github.com/dial481/locomo-audit) found 99 of the 1,540 gold answers wrong, which caps a truly correct system at 93.57%, and GPT-5 mini with the whole conversation scores above that.

**Speed and tuning.** The p95 search over 10M tokens is 26 ms on the laptop CPU, though that measures time only, on synthetic text and random vectors, and says nothing about quality at that size. I also tuned how messages are embedded on LoCoMo, so it is no longer a held-out test for Cogi.

## Where the benchmarks and real use part ways

What happens on my own sessions, through the path I actually use? I ran the shipped hook logic over LongMemEval, then both paths over the 72 facts, each asked three ways.

| Test | Automatic hook | Explicit search |
|---|---|---|
| LongMemEval, answer session returned (470 answerable) | 69.4% | 98.5% |
| LongMemEval, preference questions | 13.3% | 96.7% |
| My sessions, direct question: full / at least partial | 42% / 58% | 79% / 88% |
| My sessions, forgotten fact inside a work prompt | 12.5% / 12.5% | 38% / 50% |
| My sessions, heavily reworded question | 0% / 0% | 8% / 25% |

The benchmark row and the "reworded" row use the same search code, and they are 90 points apart. I see four reasons.

**The benchmarks measure a question, and I rarely ask one.** A benchmark question exists because someone wants the fact. The value I imagined was different: a memory that speaks up while I am working on something else, because I have forgotten there is anything to ask. That is the work-prompt row, and the hook managed 3 of 24. Of 97 real injections, 60 were rated noise. My picture of a quiet servant bringing back what I forgot is not true yet.

**The automatic path is not the path that was tested.** The 99.0% assumes a search with five results. The hook returns at most 300 tokens and requires words shared with the prompt, which throws away most of what searching by meaning buys. It also skips the current session and does not fire after compaction, so it cannot undo compaction on its own. Search only rescues a lost fact when someone asks, and since installing Cogi Claude has called `memory_query` just 12 times, in 2 sessions.

**Technical work does not look like these chats.** LongMemEval is personal conversation and LoCoMo is friends talking, where a question's words and its answer overlap and the topics are distinct. My sessions are full of near-identical discussions of the same model, and the numbers often live in tool output. Cogi does not capture tool output, about 8.9M tokens in my history against 0.85M of assistant text, so an experiment result survives only if Claude repeated it in prose.

**The sizes differ.** Every quality number in the previous section comes from a history of 20k tokens (LoCoMo) or 115k (LongMemEval-S), and a LoCoMo conversation fits in any current context window. My memory holds 2.3M tokens, and these 72 probes are the only quality test above 1M so far: explicit search answered 42% fully and 54% at least partly across all three question types. So I cannot say the benchmark quality holds at 1M+. LongMemEval-M, at about 1.5M tokens per question, was the gate in my own requirements, and it has not been run.

My own test has limits too. It is 72 probes from one researcher, roughly ±12 points, written and judged by AI agents. The reworded questions were deliberately hard, and I did not test whether Claude uses recalled text well once it has it.

## What I would do differently

My opinion: benchmarks are worth running, but they should not be the claim you lead with. If you are evaluating a memory for your own agents:

- **Build probes from your own transcripts early.** It took one session to run, and it changed my view of the product more than the benchmarks did.
- **Measure each path users get.** My headline was 99.0%, and my hook's path scored 69.4% on the same test.
- **Test the question nobody asks.** Put the forgotten fact inside a work prompt. That is where "memory" and "search" stop being the same thing.
- **Keep a whole-context baseline in the same harness, and grade twice.** Paired intervals under two rubrics showed me the tie was not a tie.

For Cogi, the near-term work follows from the table: capture on non-typed messages and tool results, recall after compaction, and fewer word gates. Fixing the gates will not be enough, because even explicit search reaches 8% on reworded questions. After that come LongMemEval-M and a test set from my own sessions.

Today Cogi is a memory you ask. For me that is already useful, and it is open source under MIT if you want to try it. I would most like to hear what it failed to bring back:

```sh
claude plugin install cogito-mem --marketplace meridian21lab/cogito-mem
```

## References

1. Wu, D. et al. (Oct 2024). [**LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory**](https://arxiv.org/abs/2410.10813). arXiv:2410.10813
2. Maharana, A. et al. (Feb 2024). [**Evaluating Very Long-Term Conversational Memory of LLM Agents**](https://arxiv.org/abs/2402.17753). arXiv:2402.17753
3. Chhikara, P. et al. (Apr 2025). [**Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory**](https://arxiv.org/abs/2504.19413). Mem0. arXiv:2504.19413
4. dial481. [**locomo-audit**](https://github.com/dial481/locomo-audit). GitHub.
5. Mem0. [**memory-benchmarks**](https://github.com/mem0ai/memory-benchmarks). GitHub.

*All Cogi numbers are my own runs and have not been independently reproduced. Other projects' scores are self-reported, checked against their documents on 19 and 20 October 2026. The tests on my own sessions used private transcripts, so they cannot be published as they are.*
