---
name: content-discovery
description: Discover publishable content ideas by scanning MrCogito project, blog drafts, HuggingFace, and web sources. Use when asked to find content ideas, suggest what to write about, or scan for new topics.
---
# Content Discovery — Source Scanning

## Purpose

This skill defines how to autonomously discover content ideas by scanning multiple sources. When asked to find content to publish or to suggest what to write about, follow this systematic process.

## Source 1: MrCogito Project Activity

The MrCogito project lives at local windows machine `C:\Users\krzys\Dev Projects\MrCogito`.
The github repository is available at https://github.com/ksopyla/MrCogito you can review the code and the documentation there if local path is not available.

Scan these local machine locations:

### Recent Changes (highest signal)
1. **CHANGELOG.md** — Read the last 2-4 weeks of entries. Each significant entry is a potential LinkedIn post or blog topic. Look for:
   - New architecture implementations
   - Training run results (both successes and failures)
   - Bug fixes that reveal interesting insights
   - Performance improvements with numbers

2. **Git log** — Run `git log --oneline -20` in the MrCogito directory to see recent commit messages. Clusters of commits around a theme = a story worth telling.

### Experiment Reports (richest material)
3. **docs/2_Experiments_Registry/run_reports/** — Each file is a detailed experiment writeup. These are nearly ready-made blog posts. Check for reports not yet published as content.

4. **docs/2_Experiments_Registry/master_experiment_log.md** — The master log of all experiments with results. Cross-reference with published content to find unpublished experiments.

### Research Context
5. **docs/1_Strategy_and_Plans/roadmap.md** — Current research roadmap with tracks A-E. Upcoming work can be previewed as "here's what I'm exploring next" content.

6. **docs/1_Strategy_and_Plans/active_todos.md** — Prioritized experiment queue. Items about to be worked on = future content opportunities.

7. **docs/4_Research_Notes/** — Deep analyses and diagnoses. Files like `diffusion_diagnosis_20260226.md` contain publishable insights about why things failed.

### Analysis Results
8. **analysis/** — Concept analysis tools and their outputs. Quantitative results (effective rank, similarity matrices) make compelling visual content.

## Source 2: Blog Drafts

Scan `content/drafts/` in the blog project for:
- Drafts with only frontmatter (need content — can they be written now?)
- Drafts with notes but no post body (notes can bootstrap writing)
- Stalled drafts that could be revived given recent MrCogito progress
- Cross-reference draft topics with recent MrCogito work — has new data made an old draft timely?

> **Note**: Keep this list in sync with actual `content/drafts/` folders. Remove entries when draft folders are deleted.

## Source 3: HuggingFace (via MCP Tools)

Use the HuggingFace MCP tools to discover external content opportunities:

### Paper Discovery
Use `paper_search` MCP tool with queries derived from current MrCogito research:
- "concept encoder cross attention"
- "masked diffusion language model"
- "efficient transformer encoder"
- "representation collapse regularization"
- "latent reasoning"
- "concept learning transformer"

For each interesting paper found, assess if it warrants a Paper Spotlight (LinkedIn) or Paper Review (blog).

### Trending Models
Use `hub_repo_search` MCP tool with `sort: trendingScore` to find:
- New encoder models that could be compared to ConceptEncoder
- Novel training approaches relevant to MrCogito
- Models in areas you're working on (text understanding, efficient attention)

## Source 4: Web Research

Use `WebSearch` for:
- Recent blog posts or Twitter threads on topics you're working on
- Conference announcements (NeurIPS, ICML, ACL) with papers in your area
- Industry news about efficient AI, open science initiatives
- New tools worth reviewing
- arxiv papers on topics you're working on
- Check the links that are already in the notes/ folders within blog drafts for accumulated reading materials

## Source 5: Reading List

Check the notes/ folders within blog drafts for accumulated reading materials:
- Papers listed but not yet reviewed
- Links collected but not yet analyzed
- These are low-effort "What I'm Reading" post candidates

## Discovery Output

After scanning, produce a list of 3-8 content ideas. For each idea provide:

```markdown
### [Idea Title]
- **Source**: Which source it came from and specific file/link
- **Content type**: Blog post / LinkedIn post / X thread / Research Log entry
- **Why now**: What makes this timely
- **Unique angle**: What perspective only you can offer
- **Key material**: Files, links, data that would go into the content
- **Estimated effort**: Quick (< 1 hour) / Moderate (1-3 hours) / Deep (3+ hours)
```

Then score each idea using the content-drafting skill's scoring framework and update `notes/content-backlog.md`.

## Discovery Cadence

- **Weekly**: Quick scan of MrCogito CHANGELOG + git log. Takes 5 minutes.
- **Biweekly**: Full scan of all sources including HuggingFace MCP and web research.
- **On-demand**: Whenever the user asks "what should I write about" or "find content ideas."
