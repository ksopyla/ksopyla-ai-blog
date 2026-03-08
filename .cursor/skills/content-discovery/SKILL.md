---
name: content-discovery
description: Discover and triage raw content opportunities by scanning MrCogito activity, existing drafts, Hugging Face, and the web. Use when asked to find new topics, refresh the backlog, or suggest what to write about next.
---
# Content Discovery

## Purpose

Discovery is the sourcing stage of the workflow.

Use it to find promising ideas, explain why they matter now, and identify what material already exists. Do not use this skill to write a full draft, run the formal weighted scoring rubric, or publish content.

## Stage Boundary

- Discovery ends with a shortlist of candidate ideas and a recommendation for what should move into drafting.
- Drafting begins only after one idea is selected for a lean draft.
- Publishing begins only after a draft is approved and ready to go live.

## Source 1: MrCogito Project Activity

MrCogito is a separate repository. For project context (location, architecture, research phases, results, repo structure), read the `mrcogito-project` skill first.

Follow the "Content Discovery in MrCogito" section of that skill for the ordered list of high-signal sources to scan (CHANGELOG, git history, run reports, experiment log, roadmap, research notes, analysis outputs).

## Source 2: Blog Drafts And Notes

Scan `content/drafts/` and each draft's `notes/` material for:

- drafts with good frontmatter but weak body text
- stalled drafts that became timely again because of new MrCogito results
- reading lists, saved links, and paper notes that could become a review or digest
- duplicate ideas that should be merged instead of drafted twice

Keep this stage grounded in what actually exists on disk. If a draft folder was deleted, treat any stale backlog reference as invalid.

## Source 3: Hugging Face

Use the Hugging Face MCP tools for external discovery that connects back to current work.

Good `paper_search` queries:

- `concept encoder cross attention`
- `masked diffusion language model`
- `efficient transformer encoder`
- `representation collapse regularization`
- `latent reasoning`
- `concept learning transformer`

Good `hub_repo_search` targets:

- encoder models comparable to ConceptEncoder
- training recipes relevant to efficient text understanding
- tools, datasets, or demos aligned with current research tracks

The discovery question is not "is this trending?" but "does this create a worthwhile angle for Krzysztof's audience?"

## Source 4: Web Research

Use `WebSearch` for:

- recent commentary on topics already active in MrCogito work
- conference announcements and freshly released papers
- industry or tooling updates related to efficient AI, open science, and reproducible research
- blog posts or threads you can respond to with a sharper, more experience-backed angle

Also check links already collected in draft `notes/` folders before broadening the search.

## Discovery Workflow

1. Start with high-signal internal sources before external research.
2. Cross-reference recent findings against `content/drafts/`, published posts, and saved notes to avoid duplicate topics.
3. Cluster related signals into 3-8 candidate ideas instead of returning a flat list of unrelated links.
4. Prefer ideas backed by first-hand experiments, specific failures, or concrete implementation lessons.
5. Mark what is already available and what evidence is still missing.

## Discovery Output

For each candidate idea, provide:

```markdown
### [Idea Title]
- **Source**: specific file, folder, commit theme, paper, or link
- **Why now**: why this is timely or newly useful
- **Unique angle**: what perspective only Krzysztof can add
- **Best first format**: blog post / LinkedIn post / X thread / research log
- **Key material**: files, links, numbers, screenshots, notes
- **Missing material**: evidence or context still needed
- **Suggested next step**: draft now / wait for more data / park
```

## Backlog Rules

- During discovery, add items to the backlog only as raw ideas, pipeline notes, or candidate topics.
- Do not assign the formal weighted score here unless a lean draft already exists.
- If the user asks for prioritization at discovery time, give a light qualitative ranking such as high / medium / low signal rather than forcing a numeric score too early.
- Remove stale references to draft folders that no longer exist.

## Handoff To Drafting

Once the user picks an idea, pass the following into `content-drafting`:

- working title
- likely slug
- one-sentence thesis
- source files and links
- what makes the angle distinctive
- what evidence is still missing

## Discovery Cadence

- Weekly: quick scan of `CHANGELOG.md` and recent git history
- Biweekly: full scan including Hugging Face and web research
- On-demand: whenever the user asks what to write next or wants backlog refresh
