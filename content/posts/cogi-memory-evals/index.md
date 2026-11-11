---
title: "Claude forgets. I measured how much, and built a simple memory to bring it back"
date: 2026-11-11
draft: false
description: "Notes on Claude Code forgetting what was said early in long sessions, how much survived in my own transcripts, and how Cogi, a local word-for-word memory, was tested on chat histories of up to 1.2 million tokens."
tags: ["AI", "AI Engineering", "Agent Memory", "Evals", "Claude Code", "MCP"]
categories: ["AI Engineering"]
showReadingTime: true
---

{{< lead >}}
If you work in long Claude Code sessions, you have seen it: Claude no longer knows what you asked for at the start. I measured this on my own sessions, and by the end only 1 in 10 early facts was still fully there. So I built Cogi, a memory that keeps every message word for word and lets Claude look things up again. This post shows how I tested it, and where the tests are weaker than I would like.
{{< /lead >}}

## TL;DR

- In my long sessions, only 10% of early facts were still fully visible to Claude at the end.
- Cogi keeps every message and hands Claude one page of the most relevant text when it searches.
- Its search put the right past chat in the top five 93% of the time in 1.2 million tokens of history, and one page answered questions almost as well as rereading the whole conversation.

## Claude forgets, and I measured it

My evenings go to [MrCogito](/projects/concept-reasoning/), a solo research project. A session goes like this: I explain an idea, Claude writes code, we run an experiment, I change the idea, and we repeat. After a few hours the session is huge.

When a session gets too long, Claude Code replaces it with a summary. One of my sessions went from 782,000 tokens to 13,000 in one step. Then the summary gets summarised again, and again.

I wanted to know how much survives. A Claude session picked 72 early facts from five of my long sessions: requirements, rejected ideas, experiment results. Then it checked which ones Claude could still see.

After the first summary, 69% of the facts were fully there. By the end of the sessions, only 10% were fully there, and 28% at least partly. Some of the lost facts were later replaced by better decisions, so losing those was fine. I did not count how many.

This is five sessions from one person, so it is not a rate for every user. But it matched what I felt every evening.

## The idea: plain search, built with care

Cogi is not a new kind of memory. It is search: keep the text, index it well, and find the right part when asked.

Many memory tools do more. An AI model reads each message, writes down "facts", and sometimes links them into a graph. That is hard to get right, and it costs an AI call for every message. It also decides, at the moment of saving, what will matter later. Nobody knows that yet.

Cogi skips that step. It keeps every message word for word, with its date, in one file on my laptop. It indexes each message twice: by its exact words and by its meaning. Saving needs no AI call, no account and no money.

When Claude needs something, it searches and gets back a fixed amount of text: 1,000 tokens in the tests below. A token is about three quarters of a word, so that is roughly 750 words, about one page.

Why one page is enough: the answer to "what did we decide about X?" usually sits in one or two messages. If search finds those, Claude does not need the other two million tokens. It reads my own words, with their dates, not a summary written by a model.

So my bet is small: careful search over your own words is enough for most of what Claude forgets. A bet is only worth something if you test it, and the rest of this post is that test.

## How I tested it

I used three tests. Each one asks a different question.

### Can it answer questions about my own sessions?

From the same 72 facts, an AI agent wrote 24 direct questions, like "what did I say about the parameter count at the start?". Cogi searched a memory of over 2 million tokens of my sessions and handed Claude one page. Another agent judged the answers.

That one page answered 79% of the questions fully, and 88% at least partly. The rest of my history never had to be read.

### Can it find the needle in a very large history?

[LongMemEval](https://arxiv.org/abs/2410.10813) is a public test with 500 questions. In its long version, each question hides its answer in about 480 past chats, around 1.2 million tokens. That is more than Claude can read in one request: when we tried to send a whole history, it refused.

Cogi put the right chat among its first five results for 93% of the questions, 465 of 500, with no AI model involved. We ran four other free memory plugins on the same questions, each at the best setting its authors publish or at its default. They scored between 86.6% and 89.8%.

### Is one page as good as rereading everything?

[LoCoMo](https://arxiv.org/abs/2402.17753) has 10 long conversations and 1,540 questions. An AI model answers each question twice: once from Cogi's page, once from the whole conversation.

With GPT-5 mini answering, the whole conversation scored 94.1% and Cogi's page scored 89.4%. That is 95% of the quality while reading about 9 times less text. With five pages instead of one, the scores were level: 93.5% against 94.1%. Three other answering models showed the same pattern.

All numbers, settings and commands are on the [results page](https://meridian21lab.github.io/cogito-mem/results.html) and in the [benchmarks document](https://github.com/meridian21lab/cogito-mem/blob/main/docs/benchmarks.md).

## Is this a fair test?

Mostly, with limits you should know:

- **My own test is small.** 72 facts from one researcher, with questions written and judged by AI agents. Treat 79% as "about three out of four", not a precise number.
- **The public tests are chats, not coding sessions.** People talking about their lives look different from a week of debugging the same model.
- **We ran the other plugins ourselves.** We used their best published settings, but their authors have not reviewed our runs.
- **I did not test fact or graph memories.** The four plugins I compared also search plain text. The fair yardstick is rereading everything: one page gets 95% of the way there (91% with the strict grader), so a more complex method has only that gap left to close.
- **The grader matters.** LoCoMo's usual rules are generous. With stricter rules, Cogi's page scores 83.1% against 90.8% for the whole conversation, a bigger gap.
- **LoCoMo conversations are short.** At about 19,000 tokens, Claude could reread them in full. The test shows how little a page loses, not that you need memory there.
- **Cogi works best when Claude searches on purpose.** It also adds a few lines to each prompt automatically, and that part often misses. If something matters, ask Claude to check its memory.

## Next: one memory for many agents

Today Cogi serves one person on one laptop. The part I find most exciting is what comes next: many agents sharing one memory.

Picture a group of agents running experiments overnight. Before each step, an agent asks the memory "has this been tried?". After it, the agent writes down what happened. Every agent sees what the others learned, in their exact words.

The engine already handles this load. In a stress test, 16 agents wrote 820 messages at the same time with no errors, and a new message could be found about 60 ms after it was saved. Whether shared memory makes agents finish their work better, I have not measured yet. That is the next test.

## Try it

Cogi is open source under MIT and runs on your own machine. If you have noticed Claude forgetting, I would like to hear what Cogi found for you, and what it missed.

```sh
claude plugin install cogito-mem --marketplace meridian21lab/cogito-mem
```

## References

1. Wu, D. et al. (Oct 2024). [**LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory**](https://arxiv.org/abs/2410.10813). arXiv:2410.10813
2. Maharana, A. et al. (Feb 2024). [**Evaluating Very Long-Term Conversational Memory of LLM Agents**](https://arxiv.org/abs/2402.17753). arXiv:2402.17753

*All Cogi numbers are my own runs on a MacBook Pro (M5 Max), 19 October to 3 November 2026, and have not been independently reproduced. The tests on my own sessions used private transcripts, so they cannot be published as they are.*
