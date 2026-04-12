---
title: "MrCogito — Concept Encoder" 
description: "An open research project exploring concept bottleneck transformers: compressing sequences into dense concept tokens, reasoning in concept space, and eventually generating speech from concepts." 
date: 2026-02-15
draft: false
tags: ["AI research", "AI R&D", "Concept Encoder", "MrCogito"]
categories: ["AI research"]
featureAlt: "Concept Encoder architecture diagram showing input tokens compressed into concept tokens via cross-attention"
icon: "🧠"
showReadingTime: true
---

{{< lead >}}
What if a transformer did not attend over every token, but instead compressed long sequences into a small number of dense "concept tokens" and reasoned from there?
{{< /lead >}}

MrCogito is my open research project exploring this question. It is a solo effort, hobby project done alongside a full-time job, and I document the process honestly — including the failures.

The name comes from the poem *"Mr. Cogito"* by Zbigniew Herbert, a figure who thinks carefully, doubts patiently, and keeps going. That felt right for this kind of work.

**Repository:** [github.com/ksopyla/MrCogito](https://github.com/ksopyla/MrCogito)
**Experiment tracking:** [wandb.ai/ksopyla/MrCogito](https://wandb.ai/ksopyla/MrCogito)

---

## Why This Project Exists

The standard transformer architecture is remarkable, but it has a structural problem: self-attention is O(N²). At 128K tokens the attention matrix is enormous. At 1M tokens it is computationally intractable. The field's answer so far has been better hardware, clever approximations, and bigger clusters.

I want to explore a different direction.

Instead of making self-attention cheaper, what if the model did not need it at all for most of its reasoning? What if it compressed the input into a compact semantic state and then operated on that?

This is not a new idea in isolation — Perceivers, Flamingo, and Meta's Large Concept Models all use forms of cross-attention bottlenecks. But most of those systems treat the bottleneck as a means to an end (efficiency or multimodal fusion), not as the primary locus of reasoning.

MrCogito asks: **can a small set of concept tokens become the model's working memory?**

If the answer is yes, that opens several doors at once:

- **Efficient long-context processing.** O(C×N) instead of O(N²), where C is the number of concepts and C << N.
- **Test-time compute scaling.** A recursive, weight-tied encoder can run more iterations at inference to "think harder" without retraining.
- **Modality-agnostic reasoning.** If different inputs (text, audio) map into the same concept space, the reasoning module does not need to know the modality.
- **Interpretable internal states.** A small concept bank is easier to inspect than 32K hidden states.

The bet is straightforward: if I can make the concept bottleneck carry real semantic content, the rest of the architecture becomes simpler, cheaper, and more composable.

---

## The Core Architecture

```
Input text (N tokens)
  → Encoder: cross-attention compresses N tokens into C concept tokens
  → Reasoning: recursive concept refinement (K iterations, weight-tied)
  → Decoder: generates text output from refined concepts
```

The encoder uses cross-attention between a small set of learned concept tokens (C) and the full input sequence (N). This produces a compact representation in concept space:

| Sequence length N | Concepts C | Compression | Self-attn O(N²) | Concept O(C×N) | Speedup |
|---|---|---|---|---|---|
| 512 | 128 | 4:1 | 262K | 65K | 4× |
| 4,096 | 512 | 8:1 | 16.7M | 2.1M | **8×** |
| 32,768 | 2,048 | 16:1 | 1.07B | 67M | **16×** |
| 1,048,576 | 8,192 | 128:1 | 1.1T | 8.6B | **128×** |

At 1M tokens, full self-attention is impossible on any current hardware. Concept attention with C=8K remains tractable — while forcing the model to produce increasingly abstract, semantic representations.

The current model is small by design: **~21M parameters** in the Micro-2 configuration. This is deliberate. I want to prove the architecture works before scaling, not prove that enough parameters can brute-force any objective.

---

## The End Vision

The long-term goal is an **audio conversational and reasoning model** grounded in a concept bottleneck:

```
User speech (mel-spectrogram)
  → Audio adapter: maps audio features into concept space
  → Reasoning: recursive concept refinement (shared weights with text)
  → Audio decoder (Talker): generates speech tokens from concepts
```

Text and audio would share the same concept space and the same reasoning module. The only modality-specific parts are the adapter and the decoder.

This vision has six phases, each gated by concrete success criteria:

| Phase | What | Gate |
|---|---|---|
| 1 | Prove concept bottleneck captures semantics | STS-B > 0.70, concept rank > 64/128 |
| 2 | Stronger representations, data scaling, architecture variants | STS-B > 0.75, prefix loss < 3.0 |
| 3 | Full text generation from concepts | Coherent multi-sentence output |
| 4 | Instruction fine-tuning (SFT) | AlpacaEval, MT-Bench |
| 5 | Recursive reasoning, test-time compute scaling | K=12 beats K=6 on reasoning benchmarks |
| 6 | Audio modality (Concept-Talker) | Speech-to-concept-to-speech working |

**Current state (April 2026):** Phase 1 — paused. Every experiment so far has hit concept collapse (128 concepts collapse to ~5-20 effective dimensions). The training objectives I've tried — combined losses, diffusion reconstruction, prefix generation — each taught me something, but none solved the core problem. 

I've shifted my active focus to [Agent Patterns Lab](/projects/agent-patterns-lab/) while I rethink the approach. The plan is to return with agentic auto-research techniques: using AI agents to systematically explore the hyperparameter and architecture space. This project is not abandoned — it's waiting for a better strategy.

---

## What I Have Learned So Far

### The Concept Collapse Problem

The best checkpoint so far reaches decent downstream numbers: MRPC = 82.7%, STS-B = 0.650, QQP = 73.4%. Those look reasonable for a 21M parameter model.

But the internal geometry tells a different story. I allocated 128 concept slots, and the model uses effectively **5 of them**. That is 4% utilization. The concepts have collapsed into a low-dimensional subspace.

This is the core problem. High downstream scores with collapsed concepts means the evaluation head is doing all the work, not the concept space. And a collapsed concept space cannot support generation, reasoning, or modality transfer.

### What Failed

I document failures because I think they are as instructive as successes.

| Approach | What happened |
|---|---|
| Combined loss + Kendall-Gal weighting | Concept rank jumped to 95%, but all semantic metrics collapsed — concepts were diverse but empty |
| Combined loss + fixed weight | Rank stuck at 12%, everything regressed |
| CLS-query classification head | 128:1 information collapse — a single query flattens all concept structure |
| Diffusion L2 self-reconstruction | Rank 2× better but STS-B near-random (0.138) |
| Deep diffusion + ELBO + VICReg | Rank barely moved (5.74/128), STS-B 0.174 |
| Prefix generation v1 (without BiXT) | Rank 6.19/128, STS-B 0.337 — better direction but underpowered |

**The root insight:** Self-reconstruction (feed in X, reconstruct X) teaches the model to build a positional hash function, not to extract semantics. The decoder needs to generate content the encoder never saw. This is the SODA principle (Hudson et al., 2024).

### What I Believe Now

- Self-reconstruction through a bottleneck optimizes the wrong information path
- Prefix-conditioned generation (encode prefix, decode suffix) is the most promising current direction
- BiXT (bidirectional cross-attention) is no longer optional — the token side needs to evolve alongside concepts
- Geometric diversity without semantic content is not a win
- Regularization alone cannot fix collapse if the training objective rewards the wrong shortcut

A fuller account of this diagnostic journey: [Quicker Failures Lead to Better Questions](/posts/quicker-failures-better-questions/).

---

## Research Workflow and Tools

This section is for people curious about the practical side: how a solo researcher runs a multi-track research project with limited compute, AI-assisted development, and remote GPU clusters.

### Cursor as the Research IDE

I run the entire project inside [Cursor](https://www.cursor.com/). Not just for writing code faster — the real value is in research navigation.

When I am in the middle of diagnosing a failed experiment, I need to move quickly between training scripts, experiment logs, analysis plots, papers, and notes. Cursor with Claude Opus 4.6 (and recently GPT 5.4) made that loop significantly faster.

But the raw AI capability is only part of it. What made it actually useful was building **custom Cursor skills** — structured instructions that teach the agent how my specific project works.

### Custom AI Skills

The MrCogito repository has a set of [Cursor skills](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills) that encode the project's conventions, so the AI agent can work within the project context rather than guessing:

- **experiment-tracking** — structured logging of runs, metrics, and comparisons. The agent knows where experiment logs live, how they are formatted, and how to compare runs.
- **research-methodology** — hypothesis formulation, ablation design, failure analysis. When I ask "why did this run fail?", the agent follows a diagnostic protocol instead of making things up.
- **pytorch-architecture** — model building conventions and architecture templates. The agent writes code that fits the existing codebase, not generic PyTorch.
- **engineering-change-tracking** — tracking code and config changes across experiment iterations. Every change is logged with rationale.
- **huggingface-project** — dataset and model management on HuggingFace Hub.

The blog itself has a parallel set of skills for content creation, publishing, and social media — the same principle of encoding project-specific knowledge into reusable agent instructions.

Everything started to click with Claude Opus 4.6. Earlier models could help with code snippets, but Opus 4.6 was the first that could reliably navigate a complex research codebase, compare experiment reports, trace architectural decisions through code, and maintain coherent multi-step reasoning across a long session.

### Remote Training via SSH

All serious training runs happen on remote GPU clusters. The workflow:

1. **SSH with public key authentication** — no passwords, agents can connect directly.
2. **byobu (tmux wrapper) sessions** — training runs persist across SSH disconnections. Each experiment gets a named session.
3. **Shell logs are critical** — the AI agent can SSH into the server, attach to a byobu session, and read training logs directly. This means I can ask "how is the current run doing?" and get a real answer, not a guess.

The ability for the agent to check live training logs, compare them with previous runs, and suggest next steps — all within the same Cursor session — compresses the feedback loop significantly.

A typical sequence:
- Start training via SSH from Cursor terminal
- Agent monitors logs, spots anomalies early
- When training finishes, agent pulls metrics, runs evaluation, updates the experiment log
- Comparison with previous runs happens in the same context window

### Compute Infrastructure

| Name | Hardware | Role |
|---|---|---|
| Local | RTX 3080 laptop (10 GB VRAM) | Smoke tests, quick experiments, debugging |
| **Polonez** | 4× RTX 3090 (24 GB each) | Primary training cluster — multi-GPU runs |
| **Odra** | 3× RTX 3090 (24 GB each) | Secondary cluster, parallel experiments |

Both clusters are accessible via SSH and run Ubuntu. Training scripts support single-GPU and multi-GPU (via PyTorch DDP) with the same entrypoint.

This is modest hardware by industry standards. But it is enough for Phase 1-2 experiments on the Minipile dataset (0.6B tokens). Data scaling to OpenWebText+Wikipedia will require more careful scheduling across both clusters.

### Experiment Tracking

Every training run is logged to [Weights & Biases](https://wandb.ai/ksopyla/MrCogito) with:
- Full hyperparameters and config
- Git commit hash (so every run is reproducible from source)
- Training loss curves, learning rate schedules
- Concept analysis metrics (effective rank, pairwise similarity, singular value distributions)
- GLUE evaluation results

In addition to WandB, I maintain a `master_experiment_log.md` in the repo with human-written summaries of each run: what I tried, what happened, and what I concluded. The machine-readable metrics are in WandB; the reasoning is in the log.

### What the Audience Often Asks

**"Why not just fine-tune an existing model?"**
Because the research question is about the architecture, not the task. I want to know whether concept bottlenecks can work as the primary representation, not whether I can get good STS-B scores (there are easier ways).

**"Why so small? 21M parameters is tiny."**
Deliberately. If the architecture cannot produce good concepts at 21M, scaling will not fix the fundamental problem. If it can, scaling will make it better. Small models also mean faster iteration and lower compute costs — important for a solo researcher.

**"What happens if concept collapse cannot be solved?"**
I have a fallback path (Slot Attention) and a pivot option (decoder-only with concept conditioning). But I believe the current diagnostic work points to solvable problems — wrong training objective, not wrong architecture.

**"How much time do you spend on this?"**
Evenings and weekends, with occasional stretches of deeper focus. This is a side project alongside my full-time work as an AI R&D manager at Pearson. I estimate 10-15 hours per week on average, with significant variance.

**"Can I contribute?"**
The repo is public and MIT-licensed. I am not actively seeking contributors yet (the project is still too exploratory), but I welcome discussions, feedback, and suggestions. Open an issue or reach out on [LinkedIn](https://www.linkedin.com/in/krzysztof-sopyla/).

---

## Key Papers and Influences

| Paper | Key contribution to MrCogito |
|---|---|
| [TSDAE](https://aclanthology.org/2021.findings-emnlp.59/) (Wang 2021) | Denoising autoencoder — 83× stronger gradient signal per concept vs sparse MLM |
| [SODA](https://openaccess.thecvf.com/content/CVPR2024/html/Hudson_SODA_Bottleneck_Diffusion_Models_for_Representation_Learning_CVPR_2024_paper.html) (Hudson, CVPR 2024) | Bottleneck model learns semantics only when decoder generates different content than encoder saw |
| [TRM](https://hf.co/papers/2510.04871) (Jolicoeur-Martineau 2025) | 7M-param recursive model beats LLMs 1000× its size on ARC-AGI |
| [Recurrent Depth](https://hf.co/papers/2502.05171) (Geiping 2025) | Test-time recurrence — 3.5B model matches 103B equivalent |
| [Coconut](https://github.com/facebookresearch/coconut) (Meta 2024) | Latent chain-of-thought outperforms token-space CoT |
| [BiXT](https://arxiv.org/abs/2402.12138) (Hiller 2024) | Bidirectional cross-attention fixes static token embeddings in Perceivers |
| [Large Concept Models](https://hf.co/papers/2412.08821) (Meta 2024) | Sentence-level concept prediction works for generation at scale |
| [LLaDA](https://arxiv.org/abs/2502.09992) (Nie 2025) | Masked diffusion language model at 8B scale — validates diffusion for text |

---

## Updates

- **2026-04-12** — Project paused. Shifting active focus to [Agent Patterns Lab](/projects/agent-patterns-lab/). All Phase 1 experiments hit concept collapse. Planning to return with agentic auto-research approach.
- **2026-03-08** — Published [Quicker Failures Lead to Better Questions](/posts/quicker-failures-better-questions/): how AI helped me navigate the concept collapse diagnosis and find better research directions.
- **2026-02-21** — Architecture overhaul: BiXT, TSDAE, PosOnly decoder, ViaDecoder evaluation, VICReg + t_regs_mst regularization.
- **2026-02-08** — Best baseline checkpoint: Perceiver MLM L6, 40 epochs on Minipile. MRPC 82.7%, STS-B 0.650, concept rank 5/128.

---

## Open Source

The entire project is open source under the MIT license.

- **Code:** [github.com/ksopyla/MrCogito](https://github.com/ksopyla/MrCogito)
- **Experiments:** [wandb.ai/ksopyla/MrCogito](https://wandb.ai/ksopyla/MrCogito)
- **Blog:** [ai.ksopyla.com](https://ai.ksopyla.com)

If you find this work interesting, the most useful things you can do are: read the code, open an issue, or tell me what I am getting wrong.
