---
name: mrcogito-project
description: Reference guide for the MrCogito concept encoder research project. Use when writing about MrCogito, referencing experiments, understanding the ConceptEncoder architecture, checking research progress, or connecting blog content to MrCogito results.
---
# MrCogito — Concept Encoder Research Project

## Key Fact

MrCogito is a **separate repository** from this blog. It lives at a different path and has its own git history, branches, and dependencies. Never confuse blog content files with MrCogito source code.

## Locations

| What | Where |
|---|---|
| Local repo | `C:/Users/krzys/Dev Projects/MrCogito` |
| GitHub | `https://github.com/ksopyla/MrCogito` (public, repo owner: ksopyla) |
| Remote | `git@github.com:ksopyla/MrCogito.git` |
| Blog project page | `https://ai.ksopyla.com/projects/concept-encoder` |
| WandB project | `MrCogito` at `https://wandb.ai/ksopyla/MrCogito` |

## Branches

| Branch | Purpose |
|---|---|
| `main` | Stable, merged results |
| `dev` | Active development (usually checked out locally) |
| Feature branches | Named like `feat-wandb-init-*`, `2025-MM-DD-*`, or `cursor/*` for specific experiments |

## What MrCogito Is

A solo open-research project by Krzysztof Sopyla exploring a **concept bottleneck transformer**: instead of self-attention over every token (O(N^2)), the model compresses long input sequences into a small set of dense "concept tokens" via cross-attention (O(C*N)), then reasons in concept space and decodes output.

**End vision:** An audio conversational and reasoning model grounded in a concept bottleneck — encode speech into concepts, reason iteratively, decode back to speech.

**Current focus (Mar 2026):** Phase 1 — proving the text concept bottleneck produces semantically rich, non-collapsed representations. The primary blocker is **concept collapse** (effective rank 5/128 = only 4% of concept space utilized).

## Architecture At a Glance

```
Input text (N tokens)
  → Encoder: cross-attention compresses N tokens into C concept tokens
  → Reasoning: recursive concept refinement (K iterations, weight-tied)
  → Decoder: generates text output from refined concepts
```

Efficiency advantage:

| N tokens | C concepts | Concept O(C*N) | Self-attn O(N^2) | Speedup |
|---|---|---|---|---|
| 512 | 128 | 65K | 262K | 4x |
| 4,096 | 512 | 2.1M | 16.7M | 8x |
| 32,768 | 2,048 | 67M | 1.07B | 16x |
| 1M | 8,192 | 8.6B | 1.1T | 128x |

## Research Phases

| Phase | What | Gate |
|---|---|---|
| 0-1 | Self-reconstruction / MLM / TSDAE | STS-B > 0.70, concept rank > 64/128 |
| 2 | Prefix generation, data scaling, architecture variants | STS-B > 0.75, prefix loss < 3.0 |
| 3 | Full text generation from concepts | Coherent multi-sentence output |
| 4 | Instruction fine-tuning (SFT) | AlpacaEval, MT-Bench |
| 5 | Recursive reasoning, test-time compute scaling | K=12 beats K=6 on reasoning benchmarks |
| 6 | Audio modality (Concept-Talker) | Speech-to-concept-to-speech working |

**Current state:** Phase 1, fighting concept collapse. All downstream phases depend on solving this.

## Research Tracks (Parallel Workstreams)

| Track | Focus | Status |
|---|---|---|
| A | Fix concept quality (critical path) | Active — perceiver denoise + prefix generation |
| B | Data scaling (Minipile → OpenWebText+Wiki) | Blocked on Track A winner |
| C | Architecture variants (recursive encoder, dimension inversion, slot attention) | Code done for recursive, not trained |
| D | Text generation from concepts | Not started (needs SG1) |
| E | Long-context (SCROLLS, LongBench) | Not started (needs Track B) |
| F | Instruction following (SFT) | Not started (needs SG2) |
| G | Reasoning (variable-depth, test-time compute) | Not started (needs SG2) |
| H | Audio modality | Not started (needs SG1 + SG2) |

## Best Results So Far

| Metric | Score | Notes |
|---|---|---|
| MRPC F1 | 82.73% | ViaDecoder evaluation |
| STS-B Pearson | 0.650 | ViaDecoder evaluation |
| QQP F1 | 73.35% | ViaDecoder evaluation |
| MNLI-m Acc | 59.75% | ViaDecoder evaluation |
| Concept effective rank | **5/128 (4%)** | Severe collapse — the main problem |

Source checkpoint: `perceiver_mlm_H512L6C128_20260208_211633` (40 epochs, Minipile).

## Key Failed Experiments

| Approach | What happened |
|---|---|
| `combined` loss + Kendall-Gal | Rank 95% but GLUE collapsed — concepts diverse but semantically empty |
| `combined` loss + fixed weight | Rank 12%, GLUE regressed |
| CLS-query classification head | 128:1 information collapse |
| Diffusion L2 self-reconstruction | Rank 2x better but STS-B near-random |
| L6 Diffusion + ELBO | Rank 5.74/128, STS-B 0.174 — self-recon insufficient |
| L6 Diffusion + VICReg | Rank 5.09/128, no improvement |
| Prefix generation v1 (no BiXT) | Rank 6.19/128, STS-B 0.337 — prefix alone doesn't fix collapse |

**Root insight:** Self-reconstruction teaches a positional hash function, not semantics. The decoder must generate *different* content than the encoder saw (SODA principle).

## Maintained Training Paths

| Family | Entrypoint | Objective |
|---|---|---|
| `perceiver_denoise` | `training/train_perceiver_denoise.py` | TSDAE-style denoising (canonical perceiver path) |
| `weighted_mlm` | `training/train_mlm.py --model_type weighted_mlm` | Sparse MLM baseline |
| `diffusion_mlm` | `training/train_diffusion.py` | Masked diffusion self-reconstruction |
| `prefix_diffusion` | `training/train_prefix_diffusion.py` | Prefix-to-suffix generation |
| `recursive_mlm` | `training/train_recursive_mlm.py` | Isolated recursive experiment |

Retired interfaces: `perceiver_mlm`, `perceiver_posonly_mlm`, `perceiver_decoder_cls`, `train_tsdae.py`.

## Repository Structure

```
MrCogito/
├── nn/                    # Model implementations (encoder, diffusion, loss)
├── training/              # Training scripts (perceiver, MLM, diffusion, prefix)
├── evaluation/            # GLUE, STS-B, concept analysis
├── scripts/               # Launch scripts (Windows .ps1, Linux .sh)
├── analysis/              # Concept space analysis tools
├── tests/                 # Unit tests
├── data/                  # Data collators, datasets
├── docs/
│   ├── 1_Strategy_and_Plans/   # roadmap.md, vision_and_goals.md, active_todos.md
│   ├── 2_Experiments_Registry/ # master_experiment_log.md + run_reports/
│   ├── 3_Evaluations_and_Baselines/ # canonical_baselines.md
│   ├── 4_Research_Notes/       # Root cause analyses, failure diagnoses
│   └── 5_Archive/              # Superseded plans
├── CHANGELOG.md           # Engineering log (what changed + why)
├── README.md              # Project overview
└── pyproject.toml         # Poetry dependencies (Python 3.12)
```

## Content Discovery in MrCogito

When scanning MrCogito for blog content, check these sources in descending order of signal:

1. **`CHANGELOG.md`** — last 2-4 weeks for architecture changes, training results, failures, performance improvements.
2. **Git history** — `git log --oneline -20` in the MrCogito directory. Commit clusters around one theme usually mean a story worth telling.
3. **`docs/2_Experiments_Registry/run_reports/`** — often one step from a publishable experiment post.
4. **`docs/2_Experiments_Registry/master_experiment_log.md`** — unpublished experiments with enough context to explain.
5. **`docs/1_Strategy_and_Plans/roadmap.md`** — "what I'm exploring next" or strategy posts.
6. **`docs/1_Strategy_and_Plans/active_todos.md`** — preview-style content, upcoming experiment narratives.
7. **`docs/4_Research_Notes/`** — high-signal failures, diagnoses, lessons learned.
8. **`analysis/`** — rank plots, similarity matrices, ablation summaries for visual-first content.

## Compute Infrastructure

| Name | Hardware | Role |
|---|---|---|
| Local | RTX 3080 laptop (10GB VRAM) | Tests and quick experiments |
| Polonez | 4x RTX 3090 | Primary training cluster |
| Odra | 3x RTX 3090 | Secondary cluster |

## Key Paper Influences

| Paper | Key contribution to MrCogito |
|---|---|
| TSDAE (Wang 2021) | Denoising autoencoder — 83x stronger gradient per concept |
| SODA (Hudson, CVPR 2024) | Self-reconstruction permits hashing; cross-content generation forces semantics |
| TRM (Jolicoeur-Martineau 2025) | 7M-param recursive model beats LLMs 1000x its size |
| Recurrent Depth (Geiping 2025) | Test-time recurrence = 103B-param equivalent |
| Coconut (Meta 2024) | Latent reasoning outperforms CoT |
| BiXT (Hiller 2024) | Bidirectional cross-attention fixes static token embeddings |
| LLaDA (Nie 2025) | Masked diffusion at 8B scale with ELBO weighting |
| Large Concept Models (Meta 2024) | Sentence-level concept prediction works at scale |

## For Deeper Context

When you need details beyond this overview, read files directly from the MrCogito repo:

- **Current state and next steps:** `docs/1_Strategy_and_Plans/active_todos.md`
- **Full roadmap with decision gates:** `docs/1_Strategy_and_Plans/roadmap.md`
- **Vision document:** `docs/1_Strategy_and_Plans/vision_and_goals.md`
- **Experiment results:** `docs/2_Experiments_Registry/master_experiment_log.md`
- **Failure analyses:** `docs/4_Research_Notes/` (multiple diagnosis files)
- **Engineering changes:** `CHANGELOG.md`
- **Training path status:** `docs/1_Strategy_and_Plans/training_eval_matrix.md`

All paths are relative to `C:/Users/krzys/Dev Projects/MrCogito`.
