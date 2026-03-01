---
name: linkedin-post
description: Writing and publishing LinkedIn posts from blog/research content. Use when creating, drafting, editing, or adapting content for LinkedIn.
---
# LinkedIn Post Writing Guide

## General Format

- **Length**: 800-1800 characters (the engagement sweet spot). LinkedIn truncates at ~210 characters with "...see more" — make those first lines count.
- **Line breaks**: Use single blank lines between paragraphs. LinkedIn renders these as visual breaks. Short paragraphs (1-3 sentences) read best on mobile.
- **No markdown**: LinkedIn doesn't render markdown. Use plain text, Unicode symbols (→, •, ↓) for structure.
- **Hashtags**: 3-5 relevant hashtags at the bottom, separated by spaces. Core set: #AIResearch #MachineLearning. Add topic-specific ones per post.
- **Visuals**: Always include an image when possible — chart from WandB, architecture sketch, concept art, or screenshot. Posts with images get 2x engagement.

## Post Structure

Every LinkedIn post follows this skeleton:

```
HOOK (1-2 lines)
← blank line →
CONTEXT (2-3 lines)
← blank line →
INSIGHT / DATA (3-6 lines)
← blank line →
TAKEAWAY (1-2 lines)
← blank line →
QUESTION or CTA
← blank line →
#Hashtag1 #Hashtag2 #Hashtag3
```

### Hook
The first 1-2 lines must stop the scroll. Patterns that work:
- **Surprising result**: "My 128 concept tokens collapsed to just 5 effective dimensions."
- **Contrarian statement**: "Bigger models aren't the answer. Here's what my small encoder taught me."
- **Specific number**: "After 40 epochs of training, I found the real bottleneck — and it wasn't the model."
- **Direct question**: "What happens when your neural network forgets 96% of what it learned?"

What NOT to use as hooks:
- "I'm excited to share..."
- "Thrilled to announce..."
- "Big news!"
- Any hook that could come from a corporate PR account

### Context
Set the scene briefly. What were you working on? What's the background? Keep it tight — 2-3 sentences max.

### Insight / Data
The core value. Share the specific finding, data point, or lesson. Use numbers when available. Be concrete, not abstract.

### Takeaway
One clear lesson the reader can carry away. Frame it as applicable beyond your specific work.

### Question
End with a genuine question to drive comments. Not rhetorical — something you actually want to hear opinions on.

## Post Templates

### Template 1: Research Insight
Best for: Sharing a specific finding from MrCogito experiments.
Frequency: Most common (1-2x per week).

```
[Surprising finding in 1-2 sentences]

I've been working on [brief context of what you're building/training].
[What you tried and why.]

Here's what happened:
→ [Data point 1]
→ [Data point 2]
→ [What this means]

The lesson: [Generalizable takeaway].

Have you seen something similar in your models? [Genuine question]

#AIResearch #MachineLearning #[TopicTag]
```

### Template 2: Paper Spotlight
Best for: Sharing a paper you read with your commentary.
Frequency: Weekly or biweekly.

```
[Paper's key claim or finding, in your words]

I just read "[Paper Title]" by [Authors] and one idea stands out:
[The key insight in 2-3 plain-language sentences]

What makes this interesting for [your area]:
→ [Connection to your work or broader field]
→ [What it changes about how you think]
→ [What's still missing or what you'd push back on]

Paper: [link]

What's the most interesting paper you've read recently?

#AIResearch #PaperReview #[TopicTag]
```

### Template 3: Lessons from the Lab
Best for: Aggregating learnings over a period of work.
Frequency: Monthly or after milestones.

```
[Provocative framing of what you've learned]

After [time period/milestone] of [what you've been doing], here's what I wish I knew earlier:

1. [Lesson 1 — specific, with brief context]
2. [Lesson 2]
3. [Lesson 3]

The common thread: [Unifying insight]

Which of these resonates with your experience?

#AIResearch #MachineLearning #LessonsLearned
```

### Template 4: Research Log
Best for: Regular updates on MrCogito progress (series format).
Frequency: Weekly or biweekly.
Series name: "MrCogito Research Log"

```
MrCogito Research Log #[N]

This week I worked on [brief overview]:

What I tried:
→ [Experiment/change 1 + result]
→ [Experiment/change 2 + result]

What surprised me:
→ [Unexpected finding]

Next up: [What you're trying next and why]

Full project: github.com/ksopyla/MrCogito

#AIResearch #OpenScience #ConceptEncoder #ResearchLog
```

### Template 5: Contrarian Take
Best for: Challenging conventional wisdom with evidence.
Frequency: Occasionally (1-2x per month). Use sparingly for impact.

```
[Contrarian statement]

[Brief context for why you hold this view — grounded in experience]

The evidence from my work:
→ [Specific data point or observation]
→ [What this suggests about the mainstream approach]

I'm not saying [acknowledge the other side]. But [restate your position with nuance].

Am I wrong? I'd genuinely like to hear the counterargument.

#AIResearch #[TopicTag]
```

## Tone Rules (applies to ALL LinkedIn content)

- Write as yourself, in first person. This is Krzysztof speaking.
- Modest: "I found something interesting" not "I made a breakthrough"
- Specific: Use numbers, model names, metric values. Vagueness kills credibility.
- Honest: Mention what didn't work. "The STS-B score was near-random (0.138)" builds more trust than only sharing wins.
- Conversational but technical: Imagine explaining to a smart colleague at a conference.
- No corporate-speak: avoid "leverage", "synergize", "ecosystem", "unlock value"
- No emoji overload: 0-2 emojis per post maximum, only if natural

## Hashtag Strategy

Core hashtags (use 2-3 of these on every post):
- #AIResearch
- #MachineLearning
- #DeepLearning
- #OpenScience

Topic-specific hashtags (pick 1-2 per post):
- #ConceptEncoder, #TransformerArchitecture, #AttentionMechanism
- #NLP, #TextUnderstanding, #BERT
- #PaperReview, #ResearchLog
- #PyTorch, #HuggingFace
- #AIEngineering, #MLOps
- #EfficientAI, #GreenAI

## Engagement Guidelines

- Respond to every comment within 24 hours
- When commenting on others' posts in your niche, add substance (not "Great post!")
- Tag relevant people only when genuinely citing their work (not for attention)
- Share your blog post link naturally within the post when relevant, don't force it

## Output Format

Save LinkedIn posts as:
```
content/linkedin/YYYY-MM-topic-slug/post.md
```

File structure:
```markdown
---
title: "Post title for internal reference"
date: YYYY-MM-DD
platform: linkedin
status: draft | ready | published
content_score: X.X
related_blog_post: ""
---

[Post content here, exactly as it should appear on LinkedIn]
```

## Visual Prompts for LinkedIn

When a post needs a visual and no chart/screenshot is available, use the image-generation skill to generate one. Recommended aspect ratio for LinkedIn: 1200:627 (approximately 1.91:1).
