---
name: research-digest
description: Researching, reviewing, and writing about AI papers and tools with HuggingFace MCP integration. Use when reviewing papers, writing paper spotlights, doing tool reviews, or creating "What I'm Reading" posts.
---
# Research Digest — Paper & Tool Review Guide

## Purpose

This skill defines how to discover, research, and write about AI papers and tools. It covers the full flow from discovery to published review, using HuggingFace MCP tools for automated paper/model discovery.

## Paper Reviews

### Discovery Process

1. **From MrCogito context**: Check what topics are active in MrCogito research tracks. Use these as search seeds:
   - Track A (Concept Quality): "concept encoder", "representation collapse", "VICReg regularization", "TSDAE denoising"
   - Track B (Data Scaling): "pretraining data scaling", "OpenWebText", "efficient pretraining"
   - Track C (Architecture): "recursive transformer", "test-time compute", "perceiver architecture"
   - Track D (Long Context): "long context encoder", "efficient attention"
   - Track E (Audio): "speech encoder", "audio tokenization", "concept-based speech"

2. **HuggingFace paper_search**: Use the MCP tool with queries like:
   ```
   paper_search(query="masked diffusion language model", results_limit=5)
   paper_search(query="concept learning cross attention encoder", results_limit=5)
   paper_search(query="representation collapse regularization", results_limit=5)
   ```

3. **From reading notes**: Check `content/drafts/*/notes/` folders for papers already bookmarked but not yet reviewed.

4. **From web research**: Search for recent arXiv papers, blog posts, and conference proceedings on relevant topics.

### Paper Review Structure (Blog Post)

For a full blog post paper review, use this structure:

```markdown
## The Problem
[What problem does this paper address? Why does it matter?
Frame it in terms the target persona cares about.]

## Their Approach
[High-level explanation of the methodology.
Include a key diagram if the paper has one.
Explain the core innovation in plain language.]

## Key Results
[Specific metrics and comparisons to prior work.
Use a table if comparing multiple baselines.
Highlight what's genuinely impressive and what's incremental.]

## My Take
[Your honest opinion. This is the most valuable section.
Where do you agree? Where do you push back?
What questions remain unanswered?
Connect to your own experience — "In my ConceptEncoder experiments, I've seen similar/different behavior because..."]

## How This Relates to my github projects or experties
[Specific connections to your research.
Could you apply their technique?
Does it validate or challenge your approach?
What experiment would you run next based on this paper?]

## References
[Link to the paper, any associated code/models on HuggingFace]
```

### Paper Spotlight Structure (LinkedIn)

For a LinkedIn Paper Spotlight post, distill to the essentials:
- One paper, one key insight, your opinion
- Follow the Paper Spotlight template in the linkedin-post skill
- Always link to the full blog review if one exists

## Tool & Model Reviews

### Discovery Process

1. **HuggingFace hub_repo_search**: Find trending and new models:
   ```
   hub_repo_search(repo_types=["model"], sort="trendingScore", limit=10)
   hub_repo_search(query="concept encoder", repo_types=["model"], limit=10)
   hub_repo_search(query="efficient text encoder", repo_types=["model", "dataset"], limit=10)
   ```

2. **HuggingFace space_search**: Find interactive demos:
   ```
   space_search(query="text encoder comparison", limit=5)
   space_search(query="model evaluation benchmark", limit=5)
   ```

3. **Web research**: Search for tools mentioned in AI communities (OpenClaw, new training frameworks, evaluation tools).

### Tool Review Structure (Blog Post)

```markdown
## What It Is
[Brief description of the tool/model. Who made it? What problem does it solve?]

## Why I Tested It
[Connection to your work. What motivated the evaluation?]

## Setup & Experiment
[How you set it up. Any gotchas or setup issues.
Include key code snippets that show actual usage.
Note: for reproducible experiments, use the ksopyla-ai-lab repo.]

## Results
[What you found. Specific metrics, performance numbers, quality assessment.
Compare to alternatives if relevant.
Include screenshots, outputs, charts.]

## Verdict
[Honest assessment. When would you use this? When wouldn't you?
Who would benefit most?
Star rating is optional but can be useful: ★★★★☆]

## Links
[Tool/model link, your experiment notebook link, related resources]
```




