---
title: "Replacing Gemma-3 Global Attention with Concepts (Toward Longer Context)"
date: 2026-07-26
draft: false
description: "I replace Gemma-3's global-attention layers with a recurrent concept workspace. Short context let local windows cheat; at 4K the concepts became load-bearing — a step toward longer context without full N×N attention."
tags: ["AI", "MrCogito", "Gemma", "Concept Reasoning", "Representation Learning", "Muon"]
categories: ["AI Research"]
featureImage: "feature_gemma_concepts_global_attention.png"
featureAlt: "Abstract digital art of dense attention lines compressing into a compact constellation of concept nodes that continue as a long stream of light"
showReadingTime: true
---

{{< lead >}}
Gemma-3 already splits attention into local windows and a few global layers. My bet is to replace those global layers with a small recurrent concept bank — keep local fluency, move long-range state into concepts, and open a path toward longer context without paying full global attention.
{{< /lead >}}

## TL;DR

**What you will learn:**

- How I replace Gemma-3's global-attention layers with a recurrent bank of 128 concepts on frozen Gemma-3 1B + LoRA
- Why short-context CE left that replacement unused — local windows still did the job
- What changed at 4K / 1B tokens under Muon: beyond-local ΔCE rose from ~0.003 to ~2.35 nats
- Why this is a step *toward* longer context, not a claim that 10M context is solved

This is a progress report from [MrCogito — Concept Reasoning Model](/projects/concept-reasoning/). After Phase 1 hit [concept collapse](/posts/quicker-failures-better-questions/), I stopped paying the from-scratch language-acquisition tax on every memory test. The Gemma track asks a narrower architectural question:

**If I remove Gemma's global attention and put concepts in its place, can that concept state actually carry long-range information?**

The honest answer so far: not under short-context CE — local windows are too strong. Under a 4K long-document Muon run, yes: beyond-local next-token prediction started to depend on the concepts. That is not a 10M-token demo. It is evidence that the replacement can work, which is why I am still training in this direction.

## Why replace global attention at all?

Agents need state that survives tools, turns, and long documents. Today that usually means stuffing more tokens into a window, retrieving chunks, or bolting on external memory. Those help. They still inherit expensive attention and a narrow token interface.

Gemma-3 already took one smart step toward efficiency: most layers are local sliding-window attention; only every sixth layer is global ([Gemma 3 Technical Report](https://arxiv.org/abs/2503.19786)). That cuts KV-cache cost for long context. But the global layers still do full attention over N tokens. At million-token scale, that remains the expensive part.

My working bet in MrCogito is to go one step further:

1. Keep **local** attention for fluent token↔token work
2. Replace **global** attention with reads/writes over **C concept vectors** (C ≪ N)
3. Carry those concepts recurrently across blocks, so sequence length grows by looping, not by growing a full global KV cache

If that works, three things become more tractable:

- **Longer context as an architectural consequence.** Attention becomes O(N·(K+C)) with fixed block size K, not O(N²) global attention. Multi-million-token windows become a compute and state-quality problem. The ~10M ambition on the [project page](/projects/concept-reasoning/) is still ambition — this post trains at 4K — but replacing global attention is the mechanism that makes the ambition coherent.
- **Higher reasoning bandwidth.** Discrete CoT writes roughly O(log |V|) bits per step ([Chen et al.](https://openreview.net/forum?id=cCIdxLoLJ5)). Continuous latent work such as [COCONUT](https://arxiv.org/abs/2412.06769) and Soft Thinking ([Zhang et al., 2025](https://arxiv.org/abs/2505.15778)) points at wider internal channels. [Kuratov et al.](https://arxiv.org/abs/2502.13063) show a vector can hold far more than one token's worth of information when used well. Concepts are my trainable version of that wider channel.
- **Reusable state for agents.** A concept workspace is a candidate bus for memory and tools — but only if the model actually depends on it.

Phase 1 trained encoders from scratch and watched concepts collapse. Useful. Expensive. For this track I refuse to re-learn English every time I test the long-range channel. Start from a pretrained decoder. Replace its global path. Measure whether concepts take over that job.

## Why Gemma-3 1B is the right place to do the surgery

I chose [`google/gemma-3-1b-pt`](https://huggingface.co/google/gemma-3-1b-pt) because the hybrid pattern is explicit and the model still fits evening GPUs:

- iterable on **3× RTX 3090**
- strong enough that LoRA fine-tunes are informative
- **5 local + 1 global** already marks where long-range routing lives

On the 1B text model (`num_hidden_layers=26`, `hidden_size=1152`) there are four global layers at **0-indexed indices 5, 11, 17, 23**. Local window is **512** tokens.

Those four layers are the surgical site. Gemma was pretrained to send long-range information through them. Design C keeps that inductive bias and changes the substrate:

| Before (stock Gemma-3) | After (concept graft) |
|---|---|
| Global layers attend all tokens | Global layers attend **concepts + local window** |
| Long-range state lives in full KV over N | Long-range state lives in **C=128 recurrent concepts** |
| Cost grows with global N×N terms | Cost grows as **O(N·(K+C))** with K=512 |

I am not adding concepts on top of global attention. I am **replacing the global-attention channel with concepts**, then asking whether the model learns to use that channel.

## What I built

`BackboneConceptLM` in [MrCogito](https://github.com/ksopyla/MrCogito): frozen Gemma-3 1B + LoRA, plus concept I/O. Related to Perceiver-style latent bottlenecks ([Jaegle et al., 2021](https://arxiv.org/abs/2103.03206)), but grafted into the pretrained hybrid stack rather than trained as a separate encoder.

**Working configuration:**

| Piece | Choice |
|---|---|
| Backbone | frozen `gemma-3-1b-pt` + LoRA r=16 on q/k/v/o |
| Concept bank | **C = 128** slots × **1152** dims |
| Block / write cadence | **K = 512** tokens |
| Objective | plain next-token CE |
| Concept I/O | `shared_depth_recurrent` |

### Read — concepts stand in for global attention

Only the former global layers may attend concepts. Everywhere else, tokens see a local window. If information from far earlier still matters, it cannot come from full global attention anymore. It has to live in `z`.

### Write — concepts are recurrent, not a static prompt

After each concept-reading depth, a tied BiXT write updates the same bank:

```text
z ← z + tanh(α) · RMSNorm(BiXT_lat←tok(z, block_hiddens))
```

α is a scalar gate. Gate init **0.01** keeps the path live without immediately dominating the pretrained backbone.

### Depth-wise updates — refine the long-range state inside the block

The first graft wrote once after all 26 layers, so every concept-reading layer saw the same stale `z`. The better schedule writes after each global layer:

```text
layer 6  reads z     → tied write → z^(6)
layer 12 reads z^(6) → tied write → z^(12)
layer 18 reads z^(12)→ tied write → z^(18)
layer 24 reads z^(18)→ tied write → z^(24)
next block starts from z^(24)
```

That is not full recursive reasoning yet. It is the minimum recursive property the long-context bet needs: one workspace refined as depth progresses, then carried to the next token block.

{{< mermaid >}}
flowchart TB
  subgraph tokens [Token stream]
    B1[Block 1<br/>512 tokens]
    B2[Block 2<br/>512 tokens]
    Bn[Block n ...]
  end

  Z0[(Concept bank z<br/>replaces global attn state)]

  subgraph depth [Former global layers now read/write concepts]
    L6[Layer 6<br/>read z]
    W6[Tied BiXT write + gate]
    L12[Layer 12<br/>read refined z]
    W12[Tied BiXT write + gate]
    L18[Layer 18<br/>read refined z]
    W18[Tied BiXT write + gate]
    L24[Layer 24<br/>read refined z]
    W24[Tied BiXT write + gate]
  end

  B1 --> L6
  Z0 --> L6
  L6 --> W6 --> L12 --> W12 --> L18 --> W18 --> L24 --> W24
  W24 --> Z1[(z carried to next block)]
  Z1 --> B2
{{< /mermaid >}}

## How I measure whether the replacement worked

If concepts replace global attention, the decisive question is not "do concepts look diverse?" It is: **at positions that used to need global reach, does damaging concepts hurt next-token CE?**

Those are **concept ablation ΔCE** metrics on beyond-local positions:

| Metric | Intervention | What a large positive Δ means |
|---|---|---|
| **Δzero** | replace concepts with zeros | some concept pathway was needed |
| **Δstatic** | freeze to init / disable writes | accumulated writes matter, not a static soft prompt |
| **Δshuffle** | permute concept state across the batch | *this document's* concepts matter |
| **Δone-block** | keep only previous-block state | multi-block accumulation beats one-block carry |

"Beyond-local" means past what local windows + one-block carry can explain — roughly ≥1024 on 2K runs, with longer buckets on 4K runs. That is exactly the region where stock Gemma would have used global attention.

Pre-registered gate for the long-context run:

```text
min(Δstatic_beyond, Δshuffle_beyond) ≥ 0.01 nats
```

RankMe tracks geometry. Gates track whether the path is open. Neither substitutes for causal use.

**Healthy concept geometry ≠ a working global-attention replacement.**

## Short context: local windows still win

### Concepts present, long-range channel unused

First 100M-token pilot:

- RankMe **77.1** — not collapsed
- beyond-local recurrent ablations **&lt; 0.001** nats
- WandB: [first Gemma concept pilot](https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260711_152847)

I had replaced global attention in the graph. The model still solved short-context CE mostly from local windows. The replacement existed; the job had not transferred.

### Calibration opened the path, not the transfer

I tried the usability knobs:

- RMSNorm on concept reads
- nonzero gate init (0.01)
- higher LR on concept-memory params
- then the combination at 100M tokens

CE could improve. Beyond-local Δ stayed near zero. Under 2K plain CE, calibration was not enough.

### Forced-memory diagnostics

Delayed-recall tasks, where only earlier-block state identifies a later answer, died early or stayed at chance on the hard block. Useful negative: the issue was not only "missing a synthetic task." At short length, local Gemma context still carried too much of the prediction.

### Depth-wise writes at 2K

Better update schedule, same regime limit at 50M / 2K:

- RankMe **62.2**
- Δstatic / Δshuffle beyond ≈ **0.0005 / 0.0010**
- WandB: [shared-depth run](https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260714_075403)

### Adam vs Muon

Matched 100M / 2K optimizer A/B on the shared-depth architecture:

| Arm | RankMe | min beyond-local Δ | WandB |
|---|---:|---:|---|
| AdamW (LoRA 1e-4, concept LR 3e-4, wd 0) | 59 | ~0.0009 | [Adam](https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260714_211016) |
| Muon (matrix LR 0.01, adamw_lr 2e-4, wd 0.1) | **97** | **0.0028** | [Muon](https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260715_034606) |

[Muon](https://kellerjordan.github.io/posts/muon/) orthogonalizes matrix updates; [Liu et al., 2025](https://arxiv.org/abs/2502.16982) show weight decay and update-scale care matter at LLM scale. Muon won CE and RankMe. Both arms still missed the 0.01 causal-use gate.

Conclusion: the optimizer was not the main blocker. The short-context regime still let local attention finish too much of the work that global attention / concepts were supposed to own. Keep Muon. Make long-range dependence harder to avoid.

## Promising result: when local context is not enough

I kept the replacement architecture fixed and changed the operating regime:

| Factor | Short-context Muon best | Longer-context scale-up |
|---|---|---|
| Sequence length | 2048 | **4096** |
| Data | short 2K fluency-heavy mix | **long-document mix** (FinePDFs, PG19, Wikipedia long tier + fluency corpora) |
| Tokens | 100M | **1B** |
| Optimizer | Muon | Muon (same recipe) |

At 2K / K=512 there are ~4 concept blocks. At 4K there are **8**, and longer documents reward cross-block state — the job global attention used to do.

Training finished stably after ~38 wall hours on Odra (3× 3090). Beyond-local dependence grew with scale:

| approx tokens | eval CE | Δshuffle_beyond | RankMe |
|---:|---:|---:|---:|
| 0.1B | 2.269 | 0.001 | 104 |
| 0.5B | 2.216 | 0.061 | 89 |
| 0.7B | 2.089 | 0.320 | 101 |
| **1.0B** | **1.621** | **1.536** | **101** |

Offline Tier-1 on the best checkpoint:

- within-sample RankMe **101.0 / 128**
- Δshuffle ≥1024 **2.47**
- Δstatic ≥1024 **2.35**
- Δone-block ≥1024 **0.58**
- ≥3/4 read and write gates above 0.005 magnitude

WandB: [long-context Muon run](https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260718_150850)

| Stage | Budget / seq | RankMe | min beyond-local ΔCE |
|---|---|---:|---:|
| First Gemma pilot + calibrations | 100M / 2K | 77–100 | ~0.001 |
| Best short-context Muon | 100M / 2K | 97 | **0.0028** |
| **Longer-context scale-up** | **1B / 4K** | **101** | **~2.35** |

This is the promising signal for the title claim:

**concepts started doing the long-range job that global attention used to do.**

Not STS-B success. Not recursive reasoning. Causal use of the replacement channel for beyond-local CE. Δone-block at 0.58 further suggests multi-block accumulation, not only a one-block carry.

### Why this may have worked

1. **Pressure on the replaced channel.** Longer docs make local windows insufficient; the model has to use whatever long-range path remains — here, concepts.
2. **Scale curve.** Short-context Muon at 0.0028 looks like an early point on a curve 2K runs never climbed.
3. **Compound regime change.** Architecture fixed; length + data + budget + Muon moved together. Factor isolation remains open.
4. **The graft was viable earlier than it looked.** Short-context near-nulls were mostly regime evidence.

## What this does not prove yet

- **Not 10M context.** Toward longer context means the mechanism is pointed that way. This run trained at 4K.
- **Not parity with stock Gemma global attention** on every long-range behavior. I measured causal concept use, not a full quality bake-off against unmodified Gemma at matched length.
- **Not semantic / reasoning success.** Probes are next.
- **Not a single-variable proof** that Muon, 4K, or the long-doc mix alone is enough.
- **Not a bake-off against other read designs** (memory tokens, per-layer KV prefixes).
- **Causal use ≠ desired abstractions.** The channel is used. Whether concepts are the right latent factors remains open.

## Why I continue from here

I keep training because this is one of the few bets where architecture, long context, and agent state point the same way. Gemma already showed hybrid local/global attention is useful. The next question is whether **concepts can own the global role** more scalably than full attention over N.

Phase 1 showed concepts can collapse. The early Gemma runs showed the opposite failure: concepts present while local windows still carry the load. The 4K result is the first time this replacement cleared a pre-registered beyond-local causal-use gate by a large margin.

Next experiments, in order:

1. semantic probes on this checkpoint
2. longer sequences and C-scaling once semantics look real
3. recursive refinement in concept space — the actual reasoning bet on top of the long-range channel

Practical lessons if you are attempting a similar graft:

1. Measure beyond-local causal use. That is where the replaced global path must prove itself.
2. Pretrained hybrid models are excellent surgical targets: the global layers are already labeled.
3. If local context can solve the objective, your global replacement will stay ornamental.
4. Optimizers matter; making the long-range job unavoidable matters more.

I am not claiming a finished long-context concept model. I am claiming a clearer architectural step: **replace Gemma-3 global attention with concepts, and show the model can learn to use that channel.** That is enough reason to keep going — carefully, and toward longer context rather than announcing it early.

## References

1. Chen, L. et al. (2025). [**The Information Bottleneck of Chain-of-Thought and How Latent CoT Overcomes It**](https://openreview.net/forum?id=cCIdxLoLJ5). ICLR 2026 submission.
2. Kuratov, Y. et al. (Feb 2025). [**Cramming 1568 Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space Capacity**](https://arxiv.org/abs/2502.13063). ACL 2025. arXiv:2502.13063
3. Hao, S. et al. (Dec 2024). [**Training Large Language Models to Reason in a Continuous Latent Space**](https://arxiv.org/abs/2412.06769). arXiv:2412.06769
4. Zhang, Z. et al. (May 2025). [**Soft Thinking: Unlocking the Reasoning Potential of LLMs in Continuous Concept Space**](https://arxiv.org/abs/2505.15778). NeurIPS 2025. arXiv:2505.15778
5. Gemma Team et al. (Mar 2025). [**Gemma 3 Technical Report**](https://arxiv.org/abs/2503.19786). Google DeepMind. arXiv:2503.19786
6. Jaegle, A. et al. (2021). [**Perceiver: General Perception with Iterative Attention**](https://arxiv.org/abs/2103.03206). ICML 2021. arXiv:2103.03206
7. Jordan, K. et al. (2024). [**Muon: An optimizer for hidden layers in neural networks**](https://kellerjordan.github.io/posts/muon/)
8. Liu, J. et al. (Feb 2025). [**Muon is Scalable for LLM Training**](https://arxiv.org/abs/2502.16982). arXiv:2502.16982
9. Sopyla, K. (Mar 2026). [**Quicker Failures Lead to Better Questions**](https://ai.ksopyla.com/posts/quicker-failures-better-questions/). ai.ksopyla.com
10. Sopyla, K. [**MrCogito — Concept Reasoning Model**](https://ai.ksopyla.com/projects/concept-reasoning/). Project page.
11. Experiment sources: [long-context run report](https://github.com/ksopyla/MrCogito/blob/main/docs/2_Experiments_Registry/run_reports/e16b_longctx_muon_1b_20260725.md) · [Gemma graft spec](https://github.com/ksopyla/MrCogito/blob/main/docs/experiments_specs/done_failed/E10_gemma_backbone_concept_memory.md) · [shared-depth spec](https://github.com/ksopyla/MrCogito/blob/main/docs/experiments_specs/done_failed/E16_shared_depth_recurrent_concepts.md) · [master experiment log](https://github.com/ksopyla/MrCogito/blob/main/docs/2_Experiments_Registry/master_experiment_log.md)

*Metrics are from my own training and offline Tier-1 evaluation on Odra (3× RTX 3090). Independent reproduction has not been published.*
