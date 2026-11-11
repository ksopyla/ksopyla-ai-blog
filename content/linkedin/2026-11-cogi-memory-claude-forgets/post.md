---
title: "Claude forgets. I measured how much, and built a simple memory to bring it back"
date: 2026-11-11
platform: linkedin
status: draft
content_score: 4.4
related_blog_post: "https://ai.ksopyla.com/posts/cogi-memory-evals/"
video: "video/cogi-memory-claude-forgets.mp4 (4:5 explainer with voiceover; upload video/cover.jpg as the thumbnail)."
visual: "Fallback if no video: the blog feature image (Cogi the squirrel)."
hook_alternatives: "1) Claude Code forgets what you asked for at the start of a long session. I measured how much. 2) 69% of my early facts survived the first summary. 10% survived the session. 3) I stopped trusting Claude's summaries of my own sessions, so I counted what they keep."
link_strategy: "No link in the post. After the first hour, paste comment.md as the first comment: the blog post and the full benchmark results on GitHub."
fairness: "The rival numbers are our own runs, not reviewed by the maintainers; the post says so. If a maintainer comments, point them to docs/notes/longmemeval_m_rivals_20261101.md in the repo for every setting and script."
engagement: "Stay online for the first hour and answer every comment with substance (a number, a limit of the test, how to install)."
---

By the end of my long Claude Code sessions, only 1 in 10 of the facts I gave Claude at the start was still fully there.

I measured it. My evenings go to a solo research project, and a session runs for hours: an idea, code, an experiment, a changed idea, repeat. When a session gets too long, Claude Code replaces it with a summary. One of mine went from 782,000 tokens to 13,000 in one step. Then the summary gets summarised again.

A Claude session picked 72 early facts from five of my long sessions. After the first summary, 69% were fully there. By the end, 10%.

So I built Cogi, and kept it deliberately simple: plain search, not a new kind of memory. Every message is kept word for word with its date, on my laptop, and saving costs no AI call. When Claude needs something, it gets back about one page of my own words.

On my own sessions, that one page fully answered 79% of direct questions about early facts.

Then I ran it next to four other free, local memory plugins on LongMemEval_M: 500 questions, each hiding its answer in about 1.2 million tokens of past chats. Each plugin ran at the best setting its authors publish.

Right past chat in the top five:
Cogi 93.0%
hippo-memory 89.8%
deja-vu 89.0%
MemPalace 87.8%
agentmemory 86.6%

Ranking is only half of it. What counts is what reaches Claude. With each plugin's own search at its default and the same 2,500-token reply, every message the answer needed was there for 70.6% of questions with Cogi and 61.2% with MemPalace. hippo-memory, agentmemory and deja-vu stayed under 25%, mostly because they return one whole session or a few short snippets, not because they rank worse.

On LoCoMo, answering from one page reached 95% of the quality of rereading the whole conversation, from about 9 times less text.

The limits matter as much. These are my runs, not reviewed by the plugins' maintainers. The tests are chats, not coding sessions. And Cogi works best when Claude searches on purpose.

How do you stop Claude from losing your early decisions in a long session?

#AIEngineering #AIAgents #ClaudeCode
