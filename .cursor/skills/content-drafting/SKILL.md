---
name: content-drafting
description: Turn a selected idea, paper, experiment, or rough sketch into a scoreable, refined draft ready for publication. Use when creating a new draft, building a lean draft, scoring it, polishing article copy, or preparing a draft handoff to publishing.
---
# Content Drafting Workflow

## Context Loading

Before starting any draft, read these reference files from this skill's folder:

- `.cursor/skills/content-drafting/writing-preferences.md` — voice rules, editorial standards, writing quality rules, citation format, and article-specific feedback log
- `.cursor/skills/content-drafting/author-profile.md` — full author identity, credentials, project context, and biographical depth for positioning

The persona-and-audience rule (always in context) provides the content strategy and audience. These co-located files provide the writing craft and author depth that only the drafting skill needs.

## Purpose

This skill owns the middle stage of the workflow:

- intake and research
- lean draft creation
- formal scoring
- refinement into a strong draft
- handoff preparation for publishing

It does not own idea sourcing or going live.

## Stage Boundary

- `content-discovery` finds and triages candidate topics.
- `content-drafting` turns one chosen topic into an approved draft in `content/drafts/`.
- `content-publishing` handles the final polish, publish move, feature image, Hugo/browser checks, and LinkedIn prompt.

Do not move a draft into `content/posts/`, run the publish smoke-check flow, or create LinkedIn derivatives as part of the default drafting stage. That is the publishing stage unless the user explicitly asks otherwise.

## Draft Target

Draft articles live at:

```text
content/drafts/<topic-slug>/index.md
```

At drafting time:

- keep `draft: true`
- use the Hugo frontmatter conventions from the repo rule
- treat `featureImage` as optional until publishing
- keep supporting notes, links, screenshots, or source material in the same bundle when useful

## Intake Modes

Content ideas usually arrive in one of four modes. Identify the mode first, then gather the minimum material needed for a lean draft.

### Mode A: Paper Link

Trigger: the user shares a paper link, title, or arXiv reference.

What to do:

1. Read the paper and extract the core claim, method, results, and limitations.
2. Find 3-5 related papers, models, or critiques.
3. Connect the paper to MrCogito work, current research questions, or prior experiments.
4. Identify the angle that is genuinely yours rather than a generic summary.
5. Draft the lean article.

### Mode B: MrCogito Experiment Results

Trigger: the user wants to write about a training run, ablation, failure, architecture change, or result.

What to do:

1. Gather the experiment evidence from logs, reports, research notes, and changelog entries.
2. Identify the tension in the story: what was expected, what actually happened, and why it matters.
3. Add external context only after the first-hand evidence is clear.
4. Draft the lean article around the strongest finding or lesson.

### Mode C: Tool, Framework, Or Model

Trigger: the user shares a tool, model, framework, or product they want to review.

What to do:

1. Research what it does, who made it, and why it matters.
2. Check how it connects to current work, active problems, or architecture choices.
3. Look for what existing coverage misses.
4. Draft the lean article around the evaluation angle, not just the announcement.

### Mode D: User Sketch

Trigger: the user provides bullets, a thesis, half an outline, or a rough intuition.

What to do:

1. Identify the single main claim.
2. Verify assumptions and collect supporting evidence.
3. Check whether the angle is already saturated elsewhere.
4. Add useful cross-disciplinary connections only when they make the piece sharper.
5. Expand the sketch into a lean draft.

## Phase 1: Research And Framing

Before writing full prose, make sure you can answer these questions:

1. What is the single thing the reader should walk away with?
2. What concrete evidence supports it?
3. Why is this worth reading now?
4. What is the unique perspective Krzysztof can add?
5. What would a skeptical but fair reader push back on?

If those answers are still fuzzy, do more research before polishing.

## Phase 2: Lean Draft

A lean draft is the minimum article-shaped unit that can be scored honestly. It is not finished prose, but it must already contain the argument, evidence, and limits.

### Lean Draft Structure

```markdown
---
title: "[Working title]"
date: YYYY-MM-DD
draft: true
description: "[1-2 sentence summary]"
tags: ["AI", "Research"]
categories: ["AI Research"]
showReadingTime: true
---

## Main Point
[1-2 sentences with the core thesis]

## Why This Matters
[Why the reader should care now]

## Core Argument
[3-5 paragraphs or section-level bullets with concrete claims and evidence]

## Evidence
- experiment results
- citations
- benchmarks
- code or implementation details
- personal observations from the work

## Limitations And Counterpoints
[What the article is not claiming, where uncertainty remains]

## Takeaway
[1 sentence readers should remember]

## References
[Numbered list or TODO markers for sources still to fetch]
```

### Lean Draft Quality Bar

A lean draft is ready for scoring when:

- the main point is specific
- there is at least one concrete piece of evidence
- the reason-to-read is visible
- the limits are acknowledged
- only non-critical gaps remain as TODOs

If the draft is mostly placeholders, it is still an idea, not a scoreable draft.

## Phase 3: Formal Scoring

Apply the scoring framework only after a lean draft exists.

### Weighted Score

```text
Score = (Relevance x 0.25) + (Timeliness x 0.20) + (Uniqueness x 0.25) + (Audience Value x 0.20) + (Effort-to-Impact x 0.10)
```

### Rubric

#### 1. Relevance (25%)

How directly does this tie to Krzysztof's work, expertise, or recurring themes?

- 5: direct MrCogito experiment, architecture choice, or first-hand training result
- 4: closely tied to active research areas
- 3: adjacent to active areas but not central
- 2: broadly AI-related
- 1: trend-driven with weak personal connection

#### 2. Timeliness (20%)

Why now?

- 5: newly released, newly observed, or newly useful this week
- 4: active conversation in the last 2-4 weeks
- 3: evergreen topic with a timely hook
- 2: evergreen with no urgency
- 1: stale or already heavily covered

#### 3. Uniqueness (25%)

What can Krzysztof say that others usually cannot?

- 5: original data, failure analysis, or implementation experience
- 4: first-hand testing or replication
- 3: distinctive synthesis with real commentary
- 2: modest synthesis
- 1: generic summary

#### 4. Audience Value (20%)

Will a senior ML lead learn something actionable or reusable?

- 5: directly usable insight
- 4: strong mental model or framework
- 3: meaningful understanding boost
- 2: mildly interesting
- 1: narrow or low-value

#### 5. Effort-to-Impact (10%)

How efficiently can this become strong content?

- 5: most material already exists
- 4: 1-2 hours of work
- 3: half-day
- 2: full day or more
- 1: large effort with unclear payoff

### Decision Thresholds

- `4.0-5.0`: high priority, proceed
- `3.0-3.9`: worth writing, but note the weakest dimension
- `2.0-2.9`: park or strengthen before continuing
- `< 2.0`: drop or rethink

### Platform Thresholds

- Blog post: `3.5+`
- LinkedIn post: `3.0+`
- X thread: `2.5+`

### Score Output

Record results like this:

```markdown
### [Content Title]
- **Source**: where the idea came from
- **Scores**: Relevance=X, Timeliness=X, Uniqueness=X, Value=X, Effort=X -> **Weighted: X.X**
- **Platforms**: Blog / LinkedIn / X
- **Status**: Lean draft / Refining / Ready for publishing
- **Key material**: files, logs, papers, links
- **Notes**: missing evidence, title risk, or angle adjustments
```

## Phase 4: Refinement

Once the lean draft passes the threshold or the user still wants to continue, refine it into a publishable-quality draft.

### Draft Refinement Checklist

1. Tighten the hook so the opening earns attention.
2. Cut anything that does not serve the central claim.
3. Replace vague language with names, numbers, metrics, and examples.
4. Make sure section structure is clean and Hugo-friendly with `H2` and `H3`.
5. Add counter-arguments and limitations explicitly.
6. Add a `## References` section for papers, models, or benchmark claims.
7. Mark any unresolved fact checks clearly instead of hiding uncertainty.
8. Suggest where visuals would help, but do not block drafting on missing art.

### Voice And Editorial Checklist

Apply the full voice and editorial standards from `writing-preferences.md` (in this skill's folder) as the tone gate before handing off to publishing. Key reminders:

- First person, specific, modest, technical, human
- Anti-hype: no `game-changing`, `revolutionary`, `mind-blowing`
- Every claim needs evidence; every opinion needs a label
- Preserve Krzysztof's rewrites exactly — his edits are final
- Kill AI-sounding filler phrases (see the kill list in `writing-preferences.md`)

### When The User Gives Feedback

Krzysztof often give feedback inline in the draft by adding some sentences, rewrite paragraphs add comments with tags `improve`, `add links`, `rewrite the paragrph to ... ` or `add a section about ...` and you need to follow it. 
Often uses the `??` to tag the parts that need improvement.

Krzysztof edits have priority over the current draft. If sentence or paragraph was edited, try to change the surrounding main point to match the new context.

Typical refinement responses:

- `Too long`: cut aggressively
- `Not technical enough`: add methods, metrics, implementation detail
- `Too technical`: add context and cleaner explanations
- `Wrong tone`: rerun the voice checklist line by line
- `Missing angle`: strengthen the core claim, not just add more text

### Writing Quality Rules

Follow all 9 writing quality rules documented in `writing-preferences.md` (in this skill's folder). These were extracted from real drafting sessions and are non-negotiable. The most commonly violated:

1. Never write shallow summaries — extract specific details from actual sources
2. Every factual claim needs a linked reference with specific numbers
3. Kill AI-sounding filler phrases (see kill list in writing-preferences)
4. Research notes are a starting point, not a sufficient source — re-read originals

## Handoff To Publishing

This skill is complete when there is an approved draft plus a short publish handoff package.

Before handing off, confirm:

- draft path in `content/drafts/<slug>/index.md`
- current title and any stronger title candidates
- whether `featureImage` is missing
- any unresolved factual checks
- preferred publish date if known
- the most natural LinkedIn angle if the user later wants one

When the user says the draft is ready to publish, switch to `content-publishing`.
