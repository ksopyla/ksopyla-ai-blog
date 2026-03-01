---
name: content-drafting
description: End-to-end content drafting workflow (intake, lean draft, scoring, refinement, platform adaptation) and content scoring framework. Use when creating new blog posts, drafting content from ideas/papers/experiments, scoring content ideas, or refining existing drafts.
---
# Content Drafting Workflow

## Overview

This skill governs the entire lifecycle of a piece of content, from the moment an idea enters the system to a polished, scored draft ready for publishing.

The core principle: **build a lean draft first, score it, then refine.** Don't write a full polished piece before knowing if it's worth publishing.

## Phase 1: Intake — Recognizing What the User Gave You

Content ideas arrive in one of four modes. Identify which mode applies and follow its specific protocol.

### Mode A: Paper Link
**Trigger**: User pastes a link to a paper (arXiv, HuggingFace, conference) or mentions a paper by name.

What to do:
1. **Read the paper** — Fetch the paper via WebFetch or paper_search MCP. Extract: title, authors, abstract, key contribution, methodology, results.
2. **Find related work** — Use `paper_search` MCP with 2-3 queries derived from the paper's topic to find related/competing papers (3-5 results).
3. **Connect to MrCogito** — Check if the paper's techniques relate to any MrCogito research tracks (A-E). Read the relevant experiment reports or research notes if they exist.
4. **Connect to broader ideas** — Think beyond ML: does this connect to ideas from information theory, neuroscience, cognitive science, philosophy of mind, or other fields? Krzysztof values cross-disciplinary thinking.
5. **Draft the lean draft** — See Phase 2 below.

### Mode B: MrCogito Experiment Results
**Trigger**: User says they've run an experiment, got results, wants to share them. May mention a specific training run, metric, or finding.

What to do:
1. **Gather experiment data** — Read the relevant files from MrCogito:
   - Check `CHANGELOG.md` for the entry
   - Check `docs/2_Experiments_Registry/run_reports/` for a detailed report
   - Check `docs/4_Research_Notes/` for analyses
   - Ask the user for specific numbers if not available in files
2. **Identify the story** — What's the surprising/interesting finding? What failed? What was the hypothesis vs. reality? Look for tension and contrast.
3. **Find external context** — Use `paper_search` to find papers that attempted similar things. How do the user's results compare? Is this a known problem or something novel?
4. **Draft the lean draft** — See Phase 2 below.

### Mode C: Tool / Framework / Model Discovery
**Trigger**: User pastes a link to a tool, names a model, or mentions something they want to review (e.g., "OpenClaw", "Qwen2.5-Omni", a new HuggingFace model).

What to do:
1. **Research the tool** — WebSearch and/or WebFetch to understand: what it does, who made it, when it was released, what problem it solves.
2. **Find on HuggingFace** — Use `hub_repo_search` or `space_search` MCP to find the model/tool and related resources (datasets, demo spaces).
3. **Assess relevance** — How does this relate to the user's work? Is it a potential tool for MrCogito experiments? A competitor to something he uses? A new capability worth exploring?
4. **Check what others say** — WebSearch for reviews, blog posts, Twitter threads about this tool. What's the consensus? What's missing from existing coverage?
5. **Draft the lean draft** — See Phase 2 below.

### Mode D: User's Bullet Point Sketch
**Trigger**: User writes rough bullet points, a thesis statement, a question, or a partial outline of an idea.

What to do:
1. **Understand the core claim** — Identify the single main point the user is making. If unclear, ask: "What's the one thing you want the reader to walk away with?"
2. **Verify assumptions** — Fact-check any claims. Search for supporting or contradicting evidence. If the user cites a number or result, verify it against MrCogito data or published sources.
3. **Check originality** — WebSearch for existing content on this exact angle. Has someone made this argument before? If yes, what can the user add that's new?
4. **Deepen with cross-disciplinary connections** — This is where the user specifically wants you to add value. Connect the idea to:
   - Related concepts in other sciences (neuroscience, cognitive science, physics, biology)
   - Philosophical frameworks (epistemology, philosophy of mind, philosophy of science)
   - Historical precedents in CS/AI (what did researchers try before?)
   - Analogies and metaphors that make the idea more memorable
5. **Expand the skeleton** — Add supporting points, evidence, counter-arguments. Fill gaps in reasoning.
6. **Draft the lean draft** — See Phase 2 below.

## Phase 2: Lean Draft — The Minimum Scoreable Unit

A lean draft has exactly enough substance to score but no more. It's not polished prose — it's a structured sketch that demonstrates the idea has legs.

### Lean Draft Structure

```markdown
---
title: "[Working title — can be rough]"
date: YYYY-MM-DD
draft: true
intake_mode: paper | experiment | tool | sketch
status: lean-draft
---

## Main Point
[1-2 sentences: What is the single key insight or argument?]

## Hook Angle
[1-2 sentences: How would you open this to stop someone scrolling?]

## Core Argument (3-5 paragraphs)
[The meat of the piece. Not polished, but complete enough to evaluate.
Each paragraph should have a clear point.
Include specific data, names, numbers where available.
Mark gaps with [TODO: need X] rather than leaving them invisible.]

## Evidence / Data
[Bullet list of supporting evidence:
- Experiment results with numbers
- Paper citations
- Tool benchmarks
- Personal experience anecdotes]

## Cross-Disciplinary Connections
[Optional but valuable. Connections to other fields, philosophical angles,
historical precedents. This is what makes the content distinctive.]

## Counter-Arguments / Limitations
[What would a critic say? What are you NOT claiming?
This section builds credibility and prevents overreach.]

## Takeaway
[1 sentence: What should the reader do or think differently after reading this?]

## Platform Fit
[Which platforms suit this content and why:
- Blog: if deep enough for 1000+ words
- LinkedIn: if a single insight can stand alone
- X thread: if the argument can be broken into tweet-sized chunks
- Multiple: if the content can be repurposed across platforms]
```

### Lean Draft Quality Bar

A lean draft is READY FOR SCORING when:
- The main point is clear and specific (not "AI is interesting" but "concept collapse happens because the decoder can cheat")
- There's at least one piece of concrete evidence (a number, a citation, a personal experiment)
- The hook angle is defined (you know how to open it)
- You can identify which platform(s) it suits
- The [TODO] markers are in non-critical sections only

A lean draft is NOT READY when:
- The main point is vague or covers too many ideas
- There's no evidence beyond opinion
- You can't articulate why someone would read this over existing content
- The critical sections are all [TODO]

## Phase 3: Score the Draft

Apply the scoring framework below to the lean draft.

Important: you need the lean draft to score properly. A one-line idea can't be reliably scored on Audience Value or Uniqueness — you need to see the angle and evidence.

After scoring:
- **4.0+**: Proceed directly to Phase 4 (refinement)
- **3.0-3.9**: Proceed, but flag which dimension is weakest and suggest how to boost it
- **2.0-2.9**: Pause. Present the score to the user with specific suggestions: "This scored 2.7 — the uniqueness is low (2). If you could add your MrCogito experiment results comparing X, it would jump to ~3.5."
- **Below 2.0**: Recommend dropping or radically rethinking the angle. Explain why.

Present the score to the user with the breakdown so they can decide whether to proceed, pivot, or park it.

## Phase 4: Refinement — From Lean Draft to Polished Content

Once the user approves proceeding (explicitly or by giving feedback), refine the draft:

### Refinement Checklist

1. **Tighten the hook** — Rewrite the opening using patterns from the platform-specific skills (linkedin-post, x-thread). Test: would YOU stop scrolling for this?
2. **Sharpen the main point** — Cut anything that doesn't serve the central argument. If a paragraph could be removed without losing the thread, remove it.
3. **Add specificity** — Replace vague statements with numbers, names, metric values. "The model performed poorly" → "STS-B correlation was 0.138, essentially random."
4. **Apply voice principles** — Check against persona-and-audience rule. Is the tone modest? Honest? Technical but accessible? Remove any hype language.
5. **Strengthen cross-disciplinary connections** — If a connection to another field was noted in the lean draft, develop it into a proper paragraph with a source or reference.
6. **Add counter-arguments** — Ensure the piece acknowledges limitations. This is non-negotiable for credibility.
7. **Write the takeaway** — One clear, actionable insight. Not "AI is complicated" but "If your concepts collapse, change the training objective before adding regularization."
8. **Add a References section** — For any post that cites papers, models, or benchmarks, close with a `## References` numbered list. Format: `Author, F. et al. (Mon YYYY). [**Full paper title**](url). Institution. arXiv:XXXX`. Always fetch the exact title from arxiv or the project page — do not abbreviate. See `notes/writing-preferences.md` for the full format spec and an example.
9. **Suggest visuals** — Identify where an image would help: WandB chart, architecture diagram, concept art. Use the image-generation skill if needed.

### Refinement Loop

The user may provide feedback at any point. Common feedback types:
- "Too long" → Cut aggressively, prioritize the strongest points
- "Not technical enough" → Add formulas, code, architecture details
- "Too technical" → Add more context, analogies, plain-language explanations
- "Missing X" → Add the requested angle or data
- "Wrong tone" → Re-read persona-and-audience rule and adjust
- "I don't agree with Y" → Rewrite to reflect the user's actual view, not what you inferred

Continue refining until the user says it's ready or explicitly approves.

## Phase 5: Platform Adaptation

Once the refined draft is approved, produce platform-specific versions:

### Decision Logic

| Draft Length | Main Content Is | Produce |
|-------------|-----------------|---------|
| 1000+ words with depth | Technical analysis, experiment report, paper review | Blog post + 2-3 LinkedIn posts + 1 X thread |
| 500-1000 words | Single insight with evidence | LinkedIn post + X thread (skip blog) |
| < 500 words | Quick observation or data point | LinkedIn post only |

### Adaptation Process

1. **Blog post** — Expand the refined draft into full blog format following the blog-setup rule. Add frontmatter, structure with H2/H3, include code blocks and images. Save to `content/drafts/topic-slug/index.md`.
2. **LinkedIn post** — Extract the single strongest insight from the draft. Apply the appropriate template from the linkedin-post skill. Strip markdown, add line breaks, add hashtags. Save to `content/linkedin/YYYY-MM-topic-slug/post.md`.
3. **X thread** — Break the argument into tweet-sized chunks following the x-thread skill. Ensure tweet 1 is a strong hook. Save to `content/x-threads/YYYY-MM-topic-slug/thread.md`.
4. **Note derivatives in backlog** — If a blog post was created, add entries for the derivative LinkedIn/X content in `notes/content-backlog.md` with cross-references.

### Derivative Angles

When creating multiple LinkedIn posts from one blog post, use different angles:
- **Angle 1**: The main finding (Research Insight template)
- **Angle 2**: A lesson learned or failure (Lessons from the Lab template)
- **Angle 3**: Connection to a broader trend or contrarian take (Contrarian Take template)

## Backlog Maintenance — Keeping `notes/content-backlog.md` Clean

The backlog is the single source of truth for what's in the pipeline. It must stay in sync with reality. Apply these rules whenever the content state changes.

### When to Update the Backlog

| Event | Action |
|-------|--------|
| New idea scored | Add entry to the correct section (Queued / Pipeline / Parked / Raw Ideas) |
| Draft folder created | Update Status field in backlog entry to reflect draft path |
| Draft published | Remove entry from backlog (or move to an "Archive" note if needed) |
| Draft abandoned / folder deleted | **Remove entry from backlog immediately** |
| Idea deprioritized | Move entry to Parked section, update score rationale |
| Score changes (new data, new angle) | Update Scores and Weighted fields in-place |
| Platform adaptation created | Add derivative entries (LinkedIn, X) with cross-reference to parent |

### Backlog Sync Rules

1. **Draft folder exists ↔ Backlog entry exists**: If you delete a draft folder, delete its backlog entry. If you add an entry referencing a draft path, that path must exist.
2. **No orphan entries**: Do not leave entries pointing to non-existent files or folders. Check the referenced paths when updating entries.
3. **Raw Ideas → Lean Draft**: When a Raw Idea gets a lean draft written, move it to the scored sections (Queued / Pipeline / Parked) with a proper score. Remove it from Raw Ideas.
4. **After every cleanup session**: Verify that all `content/drafts/` folders have a matching backlog entry, and all backlog entries referencing draft folders point to folders that actually exist.

### Backlog Sync Check (run when in doubt)

```
1. List content/drafts/ folders
2. List all backlog entries referencing content/drafts/
3. Flag any entry whose referenced path no longer exists → remove it
4. Flag any draft folder with no backlog entry → add it or confirm intentional omission
```

---

## Quick Reference: Workflow by Intake Mode

| Mode | Phase 1 (Research) | Phase 2 (Lean Draft) | Phase 3 (Score) | Phase 4 (Refine) | Phase 5 (Adapt) |
|------|-------------------|---------------------|-----------------|------------------|-----------------|
| A: Paper link | Read paper, find related work, connect to MrCogito | Draft using Paper Review structure | Score lean draft | Refine with user feedback | Blog review + LinkedIn spotlight + X thread |
| B: Experiment results | Gather data from MrCogito, find external context | Draft using Experiment Report angle | Score lean draft | Refine with user feedback | Blog post + LinkedIn insight + X thread |
| C: Tool discovery | Research tool, check HF, find reviews | Draft using Tool Review structure | Score lean draft | Refine with user feedback | Blog review + LinkedIn verdict + X thread |
| D: Bullet sketch | Verify, check originality, add depth | Expand skeleton into lean draft | Score lean draft | Refine with user feedback | Depends on depth |

---

# Content Scoring Framework

## Purpose

Every content idea MUST be scored using this framework before committing to a polished draft. The score determines priority and whether the content is worth producing. Scores are recorded in `notes/content-backlog.md`.

**When to score**: After a lean draft exists (see Phase 2 above). A lean draft has a clear main point, a hook angle, core argument paragraphs, and at least one piece of evidence. You cannot reliably score a one-line idea — you need to see the angle and evidence to assess Uniqueness and Audience Value.

**If you don't have enough material**: Call it out as "Not enough material to score" and specify what's missing (e.g., "need experiment numbers" or "need to check if this angle has been covered elsewhere").

## Scoring Rubric (1-5 Scale)

Rate each dimension from 1 (lowest) to 5 (highest):

### 1. Relevance (Weight: 25%)
How closely does this tie to Krzysztof's MrCogito work, expertise, or stated values?

| Score | Criteria |
|-------|----------|
| 5 | Directly from MrCogito experiments, your own training runs, your own architecture decisions |
| 4 | Closely related to your research area (concept learning, efficient encoders, attention alternatives) |
| 3 | Adjacent to your expertise (general ML training, NLP, transformer architectures) |
| 2 | Broadly AI-related but outside your active research |
| 1 | Tangentially related or purely trending topic with no personal connection |

### 2. Timeliness (Weight: 20%)
Is this relevant right now? Will it be stale soon?

| Score | Criteria |
|-------|----------|
| 5 | Paper/tool released this week, you have immediate commentary or results |
| 4 | Recent development (last 2-4 weeks) with ongoing community discussion |
| 3 | Evergreen topic but with a timely hook (new paper references your area) |
| 2 | Evergreen with no particular urgency |
| 1 | Already well-covered by others, discussion has moved on |

### 3. Uniqueness (Weight: 25%)
Do you have a perspective others don't?

| Score | Criteria |
|-------|----------|
| 5 | You have original experiment data nobody else has (MrCogito results, failure analyses) |
| 4 | You've tested/implemented the thing you're writing about and can share first-hand experience |
| 3 | You have a distinctive opinion backed by your research background |
| 2 | You're synthesizing others' work with modest personal commentary |
| 1 | Pure summary of existing content without novel perspective |

### 4. Audience Value (Weight: 20%)
Will the target persona learn something actionable?

| Score | Criteria |
|-------|----------|
| 5 | Reader can apply this insight to their own models/research immediately |
| 4 | Reader gains a mental model or framework they'll reference repeatedly |
| 3 | Reader learns something interesting that deepens understanding |
| 2 | Reader finds it mildly interesting but won't change their behavior |
| 1 | Only relevant to a very narrow audience or purely navel-gazing |

### 5. Effort-to-Impact (Weight: 10%)
Can this be produced quickly relative to its potential reach?

| Score | Criteria |
|-------|----------|
| 5 | Content nearly writes itself (CHANGELOG entry → LinkedIn post, notes already exist) |
| 4 | 1-2 hours of work, material is mostly ready |
| 3 | Half-day of work, needs some research or writing |
| 2 | Full day+ of work, significant research or experimentation needed |
| 1 | Multi-day effort with uncertain payoff |

## Weighted Score Calculation

```
Score = (Relevance × 0.25) + (Timeliness × 0.20) + (Uniqueness × 0.25) + (Audience Value × 0.20) + (Effort-to-Impact × 0.10)
```

## Decision Thresholds

| Score Range | Action |
|-------------|--------|
| **4.0 - 5.0** | Write immediately. High priority. Schedule for next publishing slot. |
| **3.0 - 3.9** | Queue for next available slot. Good content worth producing when time allows. |
| **2.0 - 2.9** | Park for later. Revisit when circumstances change or combine with other ideas. |
| **Below 2.0** | Skip. Not worth the effort given current positioning and audience. |

## Platform Minimum Thresholds

- **Blog post**: Minimum score 3.5 (high effort, needs strong justification)
- **LinkedIn post**: Minimum score 3.0 (moderate effort, broader reach)
- **X thread**: Minimum score 2.5 (low effort, can test ideas)

## Score Block Format

When recording in `notes/content-backlog.md`, use this format:

```markdown
### [Content Title]
- **Source**: Where the idea came from (MrCogito experiment, paper, trending topic)
- **Scores**: Relevance=X, Timeliness=X, Uniqueness=X, Value=X, Effort=X → **Weighted: X.X**
- **Platforms**: Blog / LinkedIn / X thread (which platforms this suits)
- **Status**: Idea / Ready to write / In progress / Published
- **Key material**: Links to source files, experiment logs, papers
- **Notes**: Any additional context or angle to take
```

## Example Scores

### High-scoring example (4.5):
**"Concept Collapse: Why My 128 Concepts Collapsed to 5"**
- Relevance=5 (direct MrCogito experiment), Timeliness=4 (active research), Uniqueness=5 (original data nobody else has), Value=4 (generalizable insight about representation learning), Effort=4 (experiment log already written)
- → (5×0.25)+(4×0.20)+(5×0.25)+(4×0.20)+(4×0.10) = 1.25+0.80+1.25+0.80+0.40 = **4.50**

### Medium-scoring example (3.2):
**"What I'm Reading: 5 Papers on Latent Reasoning"**
- Relevance=4 (related to research interests), Timeliness=3 (papers are a few weeks old), Uniqueness=2 (curated list, modest commentary), Value=3 (useful for discovery), Effort=5 (notes already exist)
- → (4×0.25)+(3×0.20)+(2×0.25)+(3×0.20)+(5×0.10) = 1.00+0.60+0.50+0.60+0.50 = **3.20**

### Low-scoring example (2.25):
**"Overview of Recent LLM Releases"**
- Relevance=2 (not your research area), Timeliness=4 (current topic), Uniqueness=1 (everyone covers this), Value=2 (no unique angle), Effort=3 (needs research)
- → (2×0.25)+(4×0.20)+(1×0.25)+(2×0.20)+(3×0.10) = 0.50+0.80+0.25+0.40+0.30 = **2.25**
