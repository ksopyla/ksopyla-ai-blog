---
name: content-drafting
description: Turn a selected idea, paper, experiment, or rough sketch into a scoreable, refined draft ready for publication. Use when creating a new draft, building a lean draft, scoring it, polishing article copy, or preparing a draft handoff to publishing.
---
# Content Drafting Workflow

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

Use this as the tone gate before handing off to publishing:

- Write in first person when sharing experience or judgment.
- Stay modest. Prefer "I found something interesting" over breakthrough language.
- Be precise and technical. Use correct terms and real numbers.
- Be honest about failure modes, uncertainty, and negative results.
- Stay curious rather than dismissive when critiquing papers or trends.
- Avoid hype words such as `game-changing`, `revolutionary`, or `mind-blowing`.
- Keep it educational and readable, not academic for its own sake.
- Avoid corporate-marketing phrasing.

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

### Writing Quality Rules (learned from MCP best practices drafting session)

These rules were extracted from a multi-round drafting session and capture recurring patterns in how Krzysztof writes and what he rejects.

#### 1. Never write shallow summaries — extract specific details from sources

Do not paraphrase a blog post as "Phil Schmid says design for outcomes." Instead, extract the concrete example: "A bad MCP server exposes `get_user_by_email()`, `list_orders(user_id)`, `get_order_status(order_id)` — three tools, three round-trips. A good one exposes `track_latest_order(email)` — one call, one answer."

Before writing any claim backed by a source, re-read the actual source article (not just notes about it). Pull: specific numbers, named examples, before/after comparisons, version histories (e.g. Block's Linear MCP v1→v2→v3 evolution), and real tool/function names.

#### 2. Every factual claim needs a linked reference

If you write "accuracy degrades as tool count increases," the next sentence must have a link with specific numbers: "Grok 4.1 Fast dropped from 86.7% to 76.7% across 25→150 tools." Unlinked claims get flagged with `??` and waste a revision round.

#### 3. Write from the builder's point of view, not the user's

If the article is advice for people building MCP servers, do not open with "You install some MCP servers in Claude Code..." That is the user's perspective. Open with: "If you're building an MCP server for enterprise use, your design choices shape every agent that integrates with you." Match the POV to the audience being advised.

#### 4. Merge sections that say the same thing

If two sections make the same argument from slightly different angles, merge them. Krzysztof flagged a "Design for Others" section as duplicating "Tool Pollution" — they were the same claim (too many tools hurt quality) from designer vs consumer POV. One section with both perspectives is stronger.

#### 5. Kill AI-sounding filler phrases

Krzysztof flags phrases like "Here's the part most MCP tutorials skip" as AI slop. Other phrases to avoid:

- "Let's dive in"
- "In this article, we'll explore"
- "It's worth noting that"
- "Here's the thing"
- "Without further ado"
- "At the end of the day"
- Any sentence that could open any article on any topic

Replace with a specific, concrete statement that only works for this article.

#### 6. Preserve Krzysztof's rewrites exactly

When Krzysztof edits code examples, variable names, function signatures, or inline prose, those edits are final. Do not reformat, rename, or "improve" them. If he changed `query` to `crypto_project_research_query`, keep it exactly. His phrasing in edited sections is the target voice.

#### 7. Add a TL;DR section for AI discoverability

For opinionated or best-practices articles, add a structured TL;DR near the top with do/don't lists. This helps both human scanners and AI systems that summarize web pages. Keep each bullet to one actionable sentence.

#### 8. Use analogies from the sources, not invented ones

If Docker calls MCP tools "macros" or Phil Schmid calls MCP "a User Interface for AI agents," use those framings with attribution. Do not invent new metaphors when the sources already have good ones. Attributed analogies are more credible and more interesting than generic ones.

#### 9. Opinionated claims need to be labeled as opinions

"A great MCP server has 2-4 tools, max" is an opinion. Label it: "My controversial take:" or "My opinion:". This keeps the article honest and signals to the reader that this is a judgment call, not a protocol rule.

#### 10. Research notes are a starting point, not a sufficient source

Notes files (`notes.md`) contain summaries and pointers. They are not deep enough to write strong prose from. Before writing any section, go back to the actual source URL and re-read it. The difference between a weak draft and a strong one is whether the writer read the summary or the original.

## Backlog Sync During Drafting

When drafting changes the status of an idea:

- create or update the backlog entry when a draft folder exists
- store the weighted score after scoring
- keep file paths in sync with the real draft folder
- remove stale entries if a draft folder is intentionally deleted

Do not mark the piece as published here. Publishing status changes belong to `content-publishing`.

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
