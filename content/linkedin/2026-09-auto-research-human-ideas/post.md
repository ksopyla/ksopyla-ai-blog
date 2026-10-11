---
title: "Agents built the ordinary version of my idea"
date: 2026-09-27
platform: linkedin
status: draft
content_score: 4.7
related_blog_post: "https://ai.ksopyla.com/posts/auto-research-and-human-ideas/"
visual: "interactive_wiring_page.png (the diagram the post is about). Alternative: the Canva feature image."
link_strategy: "No link in the post or in an immediate first comment. After the first hour, reply to a comment that asks for details with the blog link, or add it then as a comment: https://ai.ksopyla.com/posts/auto-research-and-human-ideas/"
engagement: "Stay online for the first hour and answer every comment with substance (a detail, a number, a follow-up question)."
sequence: "Post 1 of 2. Post 2 (memory result) 3-4 days later."
---

I gave my AI agents an unusual research idea. They built me a common one.

Nothing crashed. The curves looked healthy. The model trained and scored reasonably.

But every run hit the same number: 26 bits out of 64.
Bigger model: 26. Longer inputs: 25. Harder exam: 26.

A number that refuses to move is not a result. It's a fingerprint.

So I asked the agents for an interactive diagram of what the code actually does, step by step. The first clue was right there on the screen.

My design note said: don't average the tokens, pick the signal from the noise.
The code averaged the tokens. And each note-taker could see only 16 tokens back, which explained the 26 exactly.

This is the risk of agent-run research nobody warned me about:
not wrong code. Ordinary code.

An unusual idea sits far from the patterns an agent has seen thousands of times. It gets pulled back, one reasonable decision at a time. Tests don't catch it, because tests check the code the agent wrote, not the idea you had.

A good spec doesn't save you either. Mine was pinned down and approved before any code was written. Then the agents kept changing things: while implementing, while fixing bugs, while tuning mid-run.

So my rule now: before every launch, I click through a diagram of the code that will actually run. Fifteen minutes of that beats reading a thousand lines of diff at 11 pm.

Agents do most of my research engineering now, and they do it well. The idea, and the suspicion, still have to be mine.

How do you check that what an agent built is still what you designed?

#AIAgents #AIResearch #MachineLearning
