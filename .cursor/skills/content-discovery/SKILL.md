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

The MrCogito project lives at `C:\Users\krzys\Dev Projects\MrCogito`.
If the local path is unavailable, review `https://github.com/ksopyla/MrCogito`.

Check these sources in descending order of signal:

1. `CHANGELOG.md`
Look at the last 2-4 weeks for architecture changes, training results, failed experiments, bug fixes with lessons, and concrete performance improvements.

2. Git history
Run `git log --oneline -20` in the MrCogito directory. A cluster of commits around one theme usually means there is a story worth telling.

3. `docs/2_Experiments_Registry/run_reports/`
These reports are often one step away from a publishable experiment post.

4. `docs/2_Experiments_Registry/master_experiment_log.md`
Use this to spot unpublished experiments or results that now have enough context to explain well.

5. `docs/1_Strategy_and_Plans/roadmap.md`
Good source for "what I'm exploring next" or strategy posts.

6. `docs/1_Strategy_and_Plans/active_todos.md`
Useful for preview-style content and upcoming experiment narratives.

7. `docs/4_Research_Notes/`
High-signal failures, diagnoses, and lessons learned often live here.

8. `analysis/`
Quantitative outputs such as rank plots, similarity matrices, or ablation summaries can anchor strong visual-first content.

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
