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
link_strategy: "No link in the post. After the first hour, add the blog link as a comment (https://ai.ksopyla.com/posts/cogi-memory-evals/), and the repo link for anyone who asks to try it (https://github.com/meridian21lab/cogito-mem)."
engagement: "Stay online for the first hour and answer every comment with substance (a number, a limit of the test, how to install)."
---

By the end of my long Claude Code sessions, only 1 in 10 of the facts I gave Claude at the start was still fully there.

I measured it. My evenings go to a solo research project, and a session runs for hours: an idea, code, an experiment, a changed idea, repeat. When a session gets too long, Claude Code replaces it with a summary. One of mine went from 782,000 tokens to 13,000 in one step. Then the summary gets summarised again.

A Claude session picked 72 early facts from five of my long sessions: requirements, rejected ideas, experiment results. After the first summary, 69% were fully there. By the end, 10%.

So I built Cogi, and kept it deliberately simple. It is plain search, not a new kind of memory. Every message is kept word for word with its date, on my laptop, and saving costs no AI call. When Claude needs something, it searches and gets back about one page of my own words.

What the tests showed:

On my own sessions, that one page fully answered 79% of direct questions about early facts.

On a public test with 1.2 million tokens of history per question, it put the right past chat in its top five 93% of the time. Four other free memory plugins scored 86.6% to 89.8% when I ran them.

Answering from one page reached 95% of the quality of rereading the whole conversation, from about 9 times less text.

The limits matter as much. My own test is small, the public tests are chats rather than coding sessions, and Cogi works best when Claude searches on purpose.

How do you stop Claude from losing your early decisions in a long session?

#AIEngineering #AIAgents #ClaudeCode
