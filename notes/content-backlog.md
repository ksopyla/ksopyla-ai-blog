# Content Backlog

Scored content ideas for blog, LinkedIn, and X. Updated: 2026-02-27.
See `.cursor/rules/content-scoring.mdc` for the scoring framework.
See `.cursor/rules/content-drafting-workflow.mdc` for how ideas move through the pipeline.

---

## Queued (Score 4.0+)

### Concept Collapse: Why My 128 Concepts Collapsed to 5 Effective Dimensions
- **Source**: MrCogito diffusion experiments (Feb 2026), `docs/4_Research_Notes/diffusion_diagnosis_20260226.md`
- **Scores**: Relevance=5, Timeliness=4, Uniqueness=5, Value=5, Effort=4 → **Weighted: 4.70**
- **Platforms**: Blog post + LinkedIn (Research Insight) + X thread
- **Status**: Ready to write
- **Key material**: diffusion_diagnosis_20260226.md, concept_analysis_diffusion_L6_step20k.json, WandB training curves
- **Notes**: Original data nobody else has. Concept collapse (effective rank 5.45/128) is a general problem in representation learning. The root cause analysis identifies 5 structural causes. Strong "Failed Experiments" angle — what went wrong and what it teaches about training objectives. Include VICReg + t_regs_mst warmup fix attempted on 2026-02-27.

### The SODA Principle: Why Your Decoder Must See Different Content Than Your Encoder
- **Source**: MrCogito diagnosis across MLM, diffusion, and TSDAE approaches, `docs/4_Research_Notes/mlm_perceiver_diagnosis_20260221.md`
- **Scores**: Relevance=5, Timeliness=4, Uniqueness=5, Value=5, Effort=3 → **Weighted: 4.55**
- **Platforms**: Blog post + LinkedIn (Contrarian Take) + X thread
- **Status**: Ready to write
- **Key material**: mlm_perceiver_diagnosis_20260221.md, diffusion_diagnosis_20260226.md
- **Notes**: Key insight across all experiments: self-reconstruction permits surface-level hashing. The decoder must generate different content than the encoder saw (prefix generation, TSDAE denoising). This is a deep architectural lesson applicable to anyone building encoders. High uniqueness — this synthesizes findings across multiple failed approaches.

### Diffusion vs MLM for Concept Encoders: A Head-to-Head Comparison
- **Source**: MrCogito experiment results, `docs/2_Experiments_Registry/run_reports/diffusion_L2_eval_20260225.md`
- **Scores**: Relevance=5, Timeliness=5, Uniqueness=5, Value=4, Effort=3 → **Weighted: 4.50**
- **Platforms**: Blog post + LinkedIn (Research Insight) + X thread
- **Status**: Ready to write
- **Key material**: diffusion_L2_eval_20260225.md, master_experiment_log.md
- **Notes**: Direct comparison: diffusion gave 2x better concept rank (10.1 vs 5/128) but near-random STS-B (0.138). Shows geometry improved but semantics didn't follow. Interesting tension between structural metrics and downstream performance.

---

## Pipeline (Score 3.0-3.9)

### ViaDecoder: A Better Way to Evaluate Concept Encoders
- **Source**: MrCogito ViaDecoder evaluation, `docs/2_Experiments_Registry/run_reports/via_decoder_eval_20260222.md`
- **Scores**: Relevance=5, Timeliness=3, Uniqueness=4, Value=3, Effort=4 → **Weighted: 3.75**
- **Platforms**: LinkedIn (Research Insight) + X thread
- **Status**: Ready to write
- **Key material**: via_decoder_eval_20260222.md
- **Notes**: Consistent +0.65-2.3% improvement over CLS-query baseline. Shows the classification head was a secondary bottleneck. Good technical content but narrower audience than the collapse story.

### MrCogito Research Log #1: February 2026
- **Source**: MrCogito CHANGELOG.md (Feb 2026 entries)
- **Scores**: Relevance=5, Timeliness=5, Uniqueness=4, Value=3, Effort=5 → **Weighted: 4.20**
- **Platforms**: LinkedIn (Research Log template)
- **Status**: Draft exists at `content/linkedin/2026-02-research-log-1/post.md`
- **Key material**: CHANGELOG.md entries from Feb 2026
- **Notes**: Low-effort, high-authenticity. Summarize Feb 2026 work: diffusion decoder redesign (4x speedup), ViaDecoder evaluation, ELBO weighting, VICReg regularization, concept collapse diagnosis. Launch the "MrCogito Research Log" series.

### Why I'm Building a 21M Parameter Encoder in the Age of 405B Parameter LLMs
- **Source**: MrCogito project philosophy, README.md, about.md
- **Scores**: Relevance=5, Timeliness=3, Uniqueness=5, Value=4, Effort=3 → **Weighted: 4.10**
- **Platforms**: Blog post + LinkedIn (Contrarian Take)
- **Status**: Draft exists at `content/linkedin/2026-02-why-21m-params/post.md`
- **Key material**: MrCogito README, ConceptEncoder architecture description, model size configs (Micro-2 = 21M params)
- **Notes**: Strong positioning piece. "Everyone is scaling up. I'm scaling differently." Connects to values about efficiency and sustainability. Could be a flagship LinkedIn post. Tie to 1000x memory reduction claim from cross-attention approach.

### GLUE Benchmark: What the History Tells Us About Encoder Progress
- **Source**: Blog draft `content/drafts/glue-results-history/`, MrCogito evaluation results
- **Scores**: Relevance=4, Timeliness=2, Uniqueness=3, Value=4, Effort=3 → **Weighted: 3.25**
- **Platforms**: Blog post
- **Status**: Draft exists (frontmatter + lead section)
- **Key material**: Existing draft, MrCogito GLUE evaluation scripts and results
- **Notes**: Evergreen content. Could be enhanced with MrCogito ConceptEncoder results as a "where does my model stand" comparison. Revive this stalled draft.

### What I'm Reading: February 2026
- **Source**: Blog draft notes (latent reasoning, MoE, voice-to-voice papers)
- **Scores**: Relevance=4, Timeliness=3, Uniqueness=2, Value=3, Effort=5 → **Weighted: 3.20**
- **Platforms**: LinkedIn ("What I'm Reading" format)
- **Status**: Ready to write
- **Key material**: `content/drafts/latent-reasoning-2025-sota/notes/`, `content/drafts/mixture-of-experts-explanation/notes/`, `content/drafts/voice-to-voice-models-2025-review/notes/`
- **Notes**: Low-effort first edition. Curate 3-5 papers from existing notes with 2-sentence commentary. Launches the series.

---

## Parked (Score < 3.0)

### Voice-to-Voice Models 2025 Review
- **Source**: Blog draft `content/drafts/voice-to-voice-models-2025-review/`
- **Scores**: Relevance=3, Timeliness=2, Uniqueness=2, Value=3, Effort=2 → **Weighted: 2.45**
- **Platforms**: Blog post
- **Status**: Notes collected, needs significant writing
- **Key material**: voice2voice-2025-notes.md
- **Notes**: Good research but lower relevance to current MrCogito focus. Park until Track E (Audio) becomes active. Would score higher once audio experiments begin.

### Mixture of Experts: An Intuitive Explanation
- **Source**: Blog draft `content/drafts/mixture-of-experts-explanation/`
- **Scores**: Relevance=3, Timeliness=2, Uniqueness=1, Value=3, Effort=2 → **Weighted: 2.25**
- **Platforms**: Blog post
- **Status**: Frontmatter only
- **Key material**: mixture-experts-notes.md
- **Notes**: Well-covered topic by others (low uniqueness). Unless you implement MoE in MrCogito and can share first-hand experience, skip for now.

---

## Raw Ideas (Not Yet Scored)

These ideas need a lean draft before scoring. See `content-drafting-workflow.mdc` Phase 2.

### Illusion of Intelligence — How Should We Measure AI Intelligence?
- **Source**: Apple paper "Illusion of Intelligence", FutureBench by Stanford/Together AI
- **Angle**: Critical take on current evaluation methods. Non-monotonic reasoning as a better test. AGI should help us solve problems we can't solve now.
- **Key links**: https://www.together.ai/blog/futurebench, https://huggingface.co/spaces/togethercomputer/FutureBench
- **Connection to MrCogito**: ConceptEncoder evaluation challenges — GLUE may not capture what matters
- **Needs**: Read the Apple paper, gather X community reactions, develop the non-monotonic reasoning angle

### AI Leadership — Creating AI-Powered Products
- **Source**: Personal experience leading R&D teams
- **Angle**: Practical lessons on culture, UX-first design, avoiding ROI tunnel vision
- **Key points**: 
  - Engage UI designers from the start (AI is a tool, not the product)
  - Strict deadlines kill creativity and risk-taking
  - Leader ego and micromanagement destroy team growth
  - ROI impatience leads to short-term thinking and idea-hopping
- **Needs**: Frame as personal reflection, not prescriptive advice. Connect to MrCogito journey.
- **Draft exists**: `content/drafts/creating-ai-products/notes/post-prompts.md`

---

## Content Series Tracker

| Series Name | Format | Cadence | Episodes Published | Next Due |
|-------------|--------|---------|-------------------|----------|
| MrCogito Research Log | LinkedIn | Biweekly | 0 | March 2026 |
| What I'm Reading | LinkedIn | Monthly | 0 | March 2026 |
| Failed Experiments | Blog + LinkedIn | As available | 0 | TBD |
| Paper Bites | LinkedIn | Weekly | 0 | TBD |
| Behind the Architecture | Blog | Monthly | 0 | TBD |

---

## AI Blogs to Watch (Inspiration & Benchmarks)

- https://www.philschmid.de/
- https://mdda.net/about
- https://thomwolf.io/
- https://www.ruder.io/about/
- https://intuitmachine.medium.com/
- https://trelis.com/about/ — YouTube: https://www.youtube.com/@TrelisResearch/videos
- https://www.inference.vc/
