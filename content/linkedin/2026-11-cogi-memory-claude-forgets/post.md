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

By the end of my long Claude Code sessions, Claude had lost most of what I told it at the start. Only 1 in 10 early facts was still fully there.

I measured it. My evenings go to a solo research project, and one session can run for hours: an idea, some code, an experiment, a new idea, and again. When a session gets too long, Claude Code swaps it for a short summary. One of mine went from 782,000 tokens to 13,000 in one step. Later, the summary gets summarised again.

With Claude's help, I picked 72 early facts from five long sessions and checked which ones Claude could still see. After the first summary: 69%. At the end: 10%.

So I built Cogi, and kept the idea simple: keep every message word for word on my laptop, and search it when needed. Saving a message needs no AI call and costs nothing. When Claude asks, it gets back a 1,000-token budget of my own words, about one page.

When I asked directly about an early fact, that one page fully answered 79% of the questions.

Then I compared Cogi with four other free memory plugins on LongMemEval_M. It has 500 questions, and each answer is hidden in about 1.2 million tokens of old chats. Every plugin used its best published setting.

How often the right chat was in the top five:
Cogi 93.0%
hippo-memory 89.8%
deja-vu 89.0%
MemPalace 87.8%
agentmemory 86.6%

Finding the right chat is not enough. Claude needs the right text in what it reads. With the same 2,500-token budget for every plugin, about two and a half pages, and each on its default settings, everything the answer needed was there for 70.6% of questions with Cogi and 61.2% with MemPalace. The other three stayed under 25%, mostly because they return a whole old chat or a few short snippets, not because their search is worse.

On a second benchmark, LoCoMo, Cogi's 1,000-token page was 95% as good as rereading the whole conversation, with 9 times less text to read.

Some honest limits: I ran these tests myself, and the plugins' authors have not checked them. The tests use chats, not coding sessions. And Cogi works best when you ask Claude to check its memory.

How do you keep Claude from forgetting your early decisions?

#AIEngineering #AIAgents #ClaudeCode
