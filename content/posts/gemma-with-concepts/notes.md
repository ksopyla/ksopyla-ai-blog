# Notes — Gemma with Concepts

Working draft: `content/drafts/gemma-with-concepts/index.md`

## Original sketch

My recent progress and observation from working on MrCogito: experiments equipping Gemma models with concepts.

### Why concepts matter (beliefs)

* concepts are key to understanding the world
* concepts + wide enough space → reasoning bandwidth for models/agents
* concepts enable long context (~10M ambition) via O(C·N) and lower compute vs O(N²)

### Why Gemma-3 1B

* small but useful starting point
* global attentions at layers 5,11,17,23 (0-indexed) / 6,12,18,24 (1-indexed) are concept candidates

### Experiment path to cover

* E10 → E10b–e → E14/E15 → E16 → E16a → **E16b**
* E11/E12 are design-only (not run) — do not narrate as completed steps
* Adam vs Muon summary (E16a + earlier E05 context)
* Architecture, writes/reads, gates, delta metrics, WandB links

---

## Discovery findings (2026-07-26)

### High-signal sources used

* MrCogito `CHANGELOG.md` (2026-07-08 → 2026-07-15 Gemma track)
* `docs/2_Experiments_Registry/master_experiment_log.md` focus note 2026-07-25
* Run report: `docs/2_Experiments_Registry/run_reports/e16b_longctx_muon_1b_20260725.md`
* Specs: E10, E16, E16a, E16b
* Vision: `docs/1_Strategy_and_Plans/vision_and_goals.md` (10M ambition, reasoning bandwidth)
* Research notes: `docs/4_Research_Notes/embedding_space_capabilites.md` (Cramming 1568 tokens)
* Blog: prior post `quicker-failures-better-questions` (Phase 1 collapse) — complementary, not duplicate
* Gemma 3 report: arXiv:2503.19786 (5:1 local/global)

### Corrected lineage (important)

User sketch said "E10 through E11, E12 and E15". Actual executed path:

```
E10 → E10b → E10c → E10d → E10e → E14 → E15 → E16 → E16a → E16b(success)
E11, E12 = design-only alternatives
```

### Headline numbers for draft

| Run | Result |
|---|---|
| E10 | RankMe 77; Δbeyond <0.001 @ 100M/2K |
| E16 | RankMe 62; Δbeyond ~0.001 @ 50M/2K |
| E16a Adam | RankMe 59; minΔ ~0.0009 |
| E16a Muon | RankMe 97; minΔ 0.0028 (best short-ctx, still fail 0.01) |
| **E16b** | RankMe **101**; Δshuffle/static≥1024 **2.47/2.35**; Δone-block **0.58** |

WandB E16b: https://wandb.ai/ksopyla/MrCogito/runs/backbone_concept_gemma_3_1b_pt_K512_concept_20260718_150850

### Literature pulled in

* Chen et al. — Information Bottleneck of CoT (OpenReview; ICLR 2026 sub) — strongest bandwidth formalization
* Kuratov et al. 2025 — Cramming 1568 tokens (arXiv:2502.13063, ACL 2025)
* Hao et al. — COCONUT continuous latent reasoning (arXiv:2412.06769)
* Zhang et al. — Soft Thinking continuous concept space (arXiv:2505.15778)
* Gemma 3 Technical Report — hybrid attention; 1B: 26 layers, SW=512, global @ 5/11/17/23
* Jaegle et al. — Perceiver latent bottleneck precedent
* Muon (Jordan) + Muon is Scalable (Liu et al. 2025)
* Scout notes: [Scout concept literature](3c294f26-6399-443a-b8d3-ae761ccd2eac)

### Still missing / strengthen later

* [x] Kuratov title confirmed (Embedding Space Capacity)
* [x] Gemma-3-1B layer indices / SW=512 confirmed via scout
* [x] COCONUT / Soft Thinking / Chen CoT bottleneck added to draft
* [ ] Optional figure: training curve of Δbeyond vs tokens for E16b
* [ ] Optional screenshot of gate magnitudes over training
* [ ] Semantic probe results on E16b ckpt (STS-B etc.) — agenda next step; do not invent
* [ ] Feature image at publishing time
* [ ] Optional later: Titans / LM2 memory-bank comparisons if expanding related-work

### Draft status (2026-07-26 rewrite)

Full story rewrite applied after user feedback + story-review:
- Hook leads with human tension, not RankMe jargon
- Problem/motivation before experiment IDs (E-codes demoted)
- Phase 1 collapse → pretrained graft rationale
- MrCogito project page linked early
- Closing framed as transferable advice for researchers/engineers
- Technical numbers, WandB, architecture, metrics retained
