---
name: linkedin-post
description: Write and repurpose LinkedIn content from blog posts, research notes, drafts, or experiments. Use when creating a LinkedIn text post, carousel outline, post series, publishing sequence, or adapting a long-form article into native LinkedIn content.
---
# LinkedIn Content Packaging Guide

## Core Idea

Do not treat LinkedIn as a place to announce that a blog post exists.

Treat LinkedIn as a native publishing surface with its own job:
- stop the scroll
- create professional recognition
- deliver value without requiring the click
- earn comments, saves, reposts, and profile visits

The blog post is the source material. The LinkedIn asset is a separate product.

## What Performs Best For This Project

Default to these post types because they fit Krzysztof's voice and audience:
- contrarian technical takes backed by real work
- lab notes with failures, trade-offs, and surprising results
- frameworks people can reuse in meetings or architecture discussions
- behind-the-scenes thinking that reveals how a conclusion was reached
- paper or tool commentary tied back to real engineering experience

Avoid:
- generic inspiration
- corporate-speak
- article-announcement posts with little native value
- growth-hack bait such as "comment YES"

## Format Priorities

Use this order unless the user asks otherwise:

1. **Native document / carousel**
   - Best when the article contains a framework, comparison, checklist, or system diagram
   - Optimize for saves and reposts
2. **Text post**
   - Best when the article has one strong thesis, surprise, or contrarian claim
   - Optimize for comments and profile visits
3. **Series**
   - Best when one article contains 3-5 distinct sub-ideas that can stand alone
   - Optimize for repeated exposure and authority building
4. **Image post**
   - Best when there is a single useful architecture sketch, chart, or result visual

Use link posts sparingly. If reach is the goal, keep the value in the post itself.

## Post Format Rules

- **Length**: 800-1800 characters for text posts unless the format clearly benefits from shorter copy
- **Line breaks**: single blank lines between paragraphs
- **No markdown**: LinkedIn does not render markdown
- **Voice**: first person, specific, modest, technical, human
- **Hashtags**: usually 3 total, occasionally 4, placed at the bottom
- **Emojis**: optional, 0-2 max, only if natural
- **Visuals**: prefer a useful chart, diagram, architecture sketch, or carousel over decorative art

## Text Post Structure

Every text post should follow this structure:

```
HOOK

CONTEXT

INSIGHT / EVIDENCE

TAKEAWAY

QUESTION OR LIGHT CTA

#Hashtag1 #Hashtag2 #Hashtag3
```

### Hook Rules

The first 1-2 lines must create tension fast. Preferred hook patterns:
- contrarian claim
- surprising number
- uncomfortable realization
- sharp question
- specific before/after shift

Avoid openings such as:
- "I'm excited to share..."
- "Thrilled to announce..."
- "New blog post is live..."
- anything that sounds like brand copy

## Article-To-LinkedIn Workflow

When adapting an article, follow this sequence.

### 1. Identify the spine

Extract:
- one central thesis
- one strongest quote or sentence
- three to five sub-ideas that can stand alone
- one diagram, comparison, or framework candidate
- one discussion question for practitioners

### 2. Decide the packaging

Use this mapping:
- **one sharp thesis** -> text post
- **framework or model** -> carousel
- **article with multiple useful angles** -> 2-week series
- **strong evidence or visual** -> image post

Most strong articles should become all three: one hero text post, one carousel, one short series.

### 3. Rewrite for native value

Do not summarize the article section by section.

Instead:
- compress to one idea per post
- move the strongest insight into the first screen
- cut caveats unless they increase credibility
- keep one practical takeaway people can reuse
- make the post useful even if the reader never clicks the article

### 4. Add the click only after value

If including the blog link, add it late and lightly.

The post should still work without the link.

## Turning One Article Into A Series

For a strong article, build a content package with:
- `post.md` -> hero text post
- `carousel_1.md` -> native document outline
- `carousel_2.md` -> native document outline [optional]
- `carousel_3.md` -> native document outline [optional]
- `sequence.md` -> 2-week sequence

### Series Design Rules

- The first post should carry the strongest contrarian thesis
- The second post should convert a framework into a saveable asset
- Later posts should isolate one sub-idea each
- Do not repeat the same hook in every post
- Each post must stand alone, but together they should deepen the same worldview

Good sequence building blocks:
- realization story
- framework
- failure / mistake
- implementation implication
- open problem

## Carousel Workflow

Use carousels when the article contains a model people can explain to coworkers.

Preferred length: 5-7 slides.
Generate only the content for the slides that I will add to the carousel template in canva or powerpoint.

### Slide Pattern

```
Slide 1: Big claim / hook
Slide 2: The problem: The old wrong model or the old wrong practice
Slide 3: The solution (part 1) or new way of thinking: The better model or the better practice
Slide 4: The solution (part 2 optional) continue the solution or add the new angle
Slide 5: Start small, piece of advice to start with
Slide 6: The destination, where this will lead you to
Slide 7: Closing question or takeaway or CTA
```

Rules:
- one idea per slide
- short titles
- each slide should be understandable in under 5 seconds


## Two-Week Posting Sequence

Use a 2-week sequence when the article contains enough depth for repeated exposure.

Recommended rhythm:
- Week 1: hero thesis + carousel
- Week 2: two or three supporting angles

For each entry include:
- day
- format
- core angle
- hook
- purpose
- CTA / question

Default sequence shape:

```
Day 1  -> Contrarian hero post
Day 3  -> Carousel / framework
Day 6  -> Failure or misconception
Day 9  -> Practical engineering implication
Day 12 -> Open question / debate starter
```

## Post Templates

### Template 1: Contrarian Insight

```
[Contrarian statement]

I used to think [old mental model].
Then [specific trigger or realization].

What changed my mind:
→ [evidence or example]
→ [engineering consequence]
→ [what teams are still missing]

The takeaway: [portable lesson].

If you're building [system/topic], what breaks first in your stack?

#AIResearch #AIEngineering #[TopicTag]
```

### Template 2: Framework Post

```
[Claim or framing]

Most people treat [topic] like [old model].
I think the better model is [new model].

The shift changes three things:
1. [shift 1]
2. [shift 2]
3. [shift 3]

That is why [practical implication].

Which part of this framework feels least solved today?

#AIEngineering #MachineLearning #[TopicTag]
```

### Template 3: Lessons From The Experience

```
[Strong learning or insight]

While working on [project], I realized [unexpected insight].

Three things I wish I had understood earlier:
1. [lesson 1]
2. [lesson 2]
3. [lesson 3]

The common thread: [unifying idea].

Have you seen the same pattern in your work?

#AIResearch #OpenScience #[TopicTag]
```

### Template 4: Paper / Tool Commentary

```
[Key claim in plain language]

I read/tested [paper/tool] because it touches [your area].

What I find most useful:
→ [insight]
→ [why it matters]
→ [what I still question]

What changed in my thinking: [one line].

What's the most important thing you think people are missing here?

#AIResearch #PaperReview #[TopicTag]
```

## Tone Rules

- Write as Krzysztof, not as a company account
- Use first-hand experience whenever possible
- Prefer honest tension over polished certainty
- Use specific systems terms: model names, protocols, metrics, constraints
- Show what changed your mind, not only your conclusion
- Mention failure when it improves trust
- Do not try to sound viral; try to sound worth forwarding

## Hashtag Strategy

Core hashtags for this repo:
- #AIResearch
- #AIEngineering
- #AIAgents
- #MachineLearning
- #OpenScience

Topic hashtags:
- #AIAgents
- #MultiAgentSystems
- #MCP
- #LLMEngineering
- #VoiceAI
- #ConceptEncoder
- #PaperReview

Default rule: use 2 core hashtags + 1 topic hashtag.

## Engagement Guidelines

- Reply to early comments with substance, not just thanks
- Favor questions that create practitioner discussion
- Tag people only when directly relevant
- Before posting, warm the network by leaving a few thoughtful comments in adjacent conversations
- After posting, note comments, reposts, and saves as the primary quality signals

## Output Format

Save LinkedIn assets under:

```
content/linkedin/YYYY-MM-topic-slug/
```

### `post.md`

```markdown
---
title: "Internal reference title"
date: YYYY-MM-DD
platform: linkedin
status: draft | ready | published
content_score: X.X
related_blog_post: ""
---

[The post text exactly as it should appear on LinkedIn]
```

### `carousel_X.md`

```markdown
---
title: "Internal reference title"
date: YYYY-MM-DD
platform: linkedin
asset_type: carousel
status: draft | ready | published
related_blog_post: ""
---

## Slide 1 - cover
Short headline, main idea of the slide

## Slide 2-6
Keep it short and to the point, one sentence or two sentences max. It needs to fit the slide template.

```


