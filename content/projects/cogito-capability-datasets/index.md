---
title: "Cogito Capability Checks: Long-Context Datasets for Small Models"
lastmod: 2026-10-10
description: "Long-context benchmark datasets for small language models (5M–100M): known facts, filler up to 128k tokens, one question, an exactly scored answer."
summary: "Five open Hugging Face datasets that test whether small (5M–100M) models actually use facts from far back in their context: recall, binding, structure, multi-hop, counting and deduction, on a length ladder from 1k to 128k tokens."
date: 2026-10-10
draft: false
weight: 15
tags: ["datasets", "Cogito Capability Checks", "long context", "evaluation", "small language models", "synthetic data", "needle in a haystack", "Hugging Face", "MrCogito"]
categories: ["AI research"]
icon: "🧪"
showReadingTime: true
keywords: ["long-context benchmark", "small language model evaluation", "needle in a haystack dataset", "associative recall", "synthetic long-context dataset", "capability evaluation", "TinyStories long context", "memory architecture benchmark"]
datasetFamily:
  name: "Cogito Capability Checks"
  alternateName: ["Cogito Capability Datasets", "CogitoProbe", "Cogito Text World"]
  description: "A family of open synthetic datasets for testing whether small language models (5M–100M parameters, trained from scratch) can store and use facts that appear thousands of tokens before the question. Every item plants known facts, pads the document with filler to 1k–128k tokens, and asks a question whose answer is computed by the generator and scored on the answer tokens only."
  license: "https://www.apache.org/licenses/LICENSE-2.0"
  keywords: ["long context", "small language models", "needle in a haystack", "associative recall", "entity binding", "multi-hop reasoning", "synthetic data", "capability evaluation"]
  citation: "Sopyła, K. (2026). Cogito Capability Checks: synthetic tests of whether models store and use facts from long context. https://ai.ksopyla.com/projects/cogito-capability-datasets/"
datasets:
  - name: "Cogito Text World"
    url: "https://huggingface.co/datasets/ksopyla/cogito-text-world"
    license: "https://cdla.dev/sharing-1-0/"
    description: "Story-world training and evaluation set for small language models: TinyStories and SimpleStories with an invented cast and woven-in facts; seven question types (quote, lookup, keyed lookup, latest state, two-hop chain, count, deduce), each with a guessing rate below 10%, at 1k–128k tokens, with evidence-removed twins. Data version text-world-v2."
  - name: "CogitoProbe-Bits"
    url: "https://huggingface.co/datasets/ksopyla/cogito-probe-bits"
    license: "https://www.apache.org/licenses/LICENSE-2.0"
    description: "Key–value recall in a long haystack, 1k–32k tokens, with the information content of every answer labelled in bits."
  - name: "CogitoProbe-Bind"
    url: "https://huggingface.co/datasets/ksopyla/cogito-probe-bind"
    license: "https://www.apache.org/licenses/LICENSE-2.0"
    description: "Entity–attribute binding and one-hop friend lookups in a long haystack, 1k–32k tokens."
  - name: "CogitoProbe-Arith"
    url: "https://huggingface.co/datasets/ksopyla/cogito-probe-arith"
    license: "https://www.apache.org/licenses/LICENSE-2.0"
    description: "Nested arithmetic with mixed brackets: sub-expression values and bracket matching from an expression written far back in the context, 1k–32k tokens."
  - name: "CogitoProbe-Props"
    url: "https://huggingface.co/datasets/ksopyla/cogito-probe-props"
    license: "https://www.apache.org/licenses/LICENSE-2.0"
    description: "Fact-versus-filler control: object colours stated in short propositions, then long filler, 1k–32k tokens."
---

{{< lead >}}
Can a small model use a fact it read 30,000 tokens ago? Plant facts you know. Bury them under thousands of tokens of filler. Ask at the end. Score exactly what came back. Five open datasets built on that one idea, sized for models of 5M–100M parameters trained from scratch.
{{< /lead >}}

The family is **Cogito Capability Checks**, all in one [Hugging Face collection](https://huggingface.co/collections/ksopyla/cogito-capability-checks-6aca2db88ba9d2714727489f).

## TL;DR

**What you get:**

- **One question:** *can a small model use a fact it read thousands of tokens ago?* Every item has known facts, a known distance to the question, and a generator-computed answer, so a score means one thing.
- **A length ladder:** the CogitoProbe sets run 1k → 32k tokens; Cogito Text World trains at 4k and tests at 1k → 128k.
- **Skills, not one number:** copy, look up, pick among look-alikes, bind, track the latest state, follow 1–3 hops, count, deduce.
- **Shortcut checks built in:** guessing rates (below 10% on every Text World task), evidence-removed twins, answer information labelled in bits.

## Long-context datasets at a glance

| Dataset | What it asks | Lengths | Size |
|---|---|---|---|
| [**Cogito Text World**](https://huggingface.co/datasets/ksopyla/cogito-text-world) | Facts inside simple stories: quote, lookup, latest state, two-hop chain, count, deduce | train 4k, test 1k–128k | 29,400 exam items, ~1.0B train tokens |
| [**CogitoProbe-Bits**](https://huggingface.co/datasets/ksopyla/cogito-probe-bits) | Values for keys listed at the start | 1k–32k | 10,240 rows |
| [**CogitoProbe-Bind**](https://huggingface.co/datasets/ksopyla/cogito-probe-bind) | Who has which colour, who lives where, where a friend lives | 1k–32k | 10,240 rows |
| [**CogitoProbe-Arith**](https://huggingface.co/datasets/ksopyla/cogito-probe-arith) | Internal values and bracket matches of a nested expression | 1k–32k | 10,240 rows |
| [**CogitoProbe-Props**](https://huggingface.co/datasets/ksopyla/cogito-probe-props) | Object colours stated in short sentences, then filler | 1k–32k | 10,240 rows |

Licenses: Text World is CDLA-Sharing-1.0 (inherited from TinyStories); the four CogitoProbe sets are Apache-2.0.

Start with **Text World** to compare architectures (attention, memory, recurrence) trained from scratch on language. Use **CogitoProbe** to test a memory mechanism without language in the way.

## Why I built them

I work on [MrCogito](/projects/concept-reasoning/), a small research model (~20–30M parameters) that compresses a long context into a few dense "concept" vectors and reasons from those. The question I kept failing to answer was simple: **does the compressed memory actually hold the facts, or does the model only look good on the next word?**

Ordinary evaluation could not tell me: on web text a model reaches a decent loss from the last few hundred tokens alone. In one experiment I trained a memory model on ~0.44B tokens of natural text at 32k context. The memory slots carrying far context were worth **0.05 nats** of loss, flat from 1k to 32k, while a passkey test scored 0% and keyed recall 4.8%. The decoder simply did not read the memory, and the loss curve gave no warning.

Popular long-context benchmarks did not fit either: in my experience they assume a large pretrained model.

So I needed exams with three properties:

1. **Known facts, known distance.** I know the right answer and how far back it sits.
2. **Nothing to gain from the filler.** Answering without the evidence means a shortcut.
3. **Learnable from scratch.** Simple vocabulary, so a 5M–100M model can learn the task, and failure means a missing capability, not a missing language.

The CogitoProbe sets came first (September 2026). Text World followed (October 2026), because a memory that works on symbols can still be ignored once it competes with learning language.

## Cogito Text World: facts inside simple stories

Text World is a **training and evaluation set** for small language models. The current data version is `text-world-v2`. The language comes from [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) and [SimpleStories](https://huggingface.co/datasets/SimpleStories/SimpleStories), simple stories that models of a few million parameters learn to write fluently [1, 2]. The generator weaves in an invented cast with homes, teachers, signs and moves, then asks one question. Places and rules are invented words, so no answer can come from prior knowledge.

An abridged `latest` item, from the dataset card:

```text
... Once upon a time Lumo found a red ball ... Lumo lived in Tavimere. ...
... Later that spring, Lumo moved to Kodaford. ... (filler up to 1k–128k tokens) ...
Question: Where does Lumo live now?
Answer: Kodaford.
```

Others move too, so the last place mentioned is not the answer. Each row stores its guessing rate as `floor`.

### The seven question types

| Level | Task | Example question | Guessing rate |
|---|---|---|---|
| T1 | `quote` | What did the sign of Lumo say? (12 signs) | 1/12 |
| T2 | `lookup` | Where does Lumo live? (12 homes stated) | 1/12 |
| T3 | `keyed` | Where does Lumo live? (16 homes, a quarter with look-alike names) | 1/16 |
| T4 | `latest` | Where does Lumo live now? (10 moves each, 5 people) | 1/11 |
| T5 | `compose` | Where does the teacher of the teacher of Lumo live? | 1/12 |
| T6 | `count` | How many times did Lumo visit the market? (zero to ten) | 1/11 |
| T7 | `deduce` | Pim is a wump. Every wump is a tove. Every tove is shiny. What is Pim like? | 1/12 |

Passing T2 but not T3 means the model finds *a* fact but not the right one; passing T3 but not T5 means it stores facts but cannot chain them.

### What keeps it honest

- **Train short, test long.** Train at 4k; `eval_id` runs from 1k to 128k. Longer documents add filler, never facts.
- **Evidence-removed twins.** Each item has a `prompt_removed` copy without the answering sentences; beating the floor there means a shortcut.
- **Held-out names and phrasings.** One name in five appears only in exams. `eval_paraphrase` uses unseen sentence templates; `eval_harder` uses 24 signs, 64 people in `keyed`, 16 moves, 3 hops and depth-3 rules.
- **Clean filler.** Filler sentences that pair a cast member with a fact word (lives, moved, teacher, sign) are dropped, and place answers are invented words that never occur in filler.
- **Audited.** On all 29,400 items a rule-based reader scores 100% and shortcut readers stay at the guessing rate (except 1 in 5 on `latest`).

The training configs (~1.0B tokens) and tokenizer ship with the dataset, so architectures can be compared on the same token stream.

**Use v2.** The first release, `text-world-v0`, had five shortcuts (for example, `lookup` was 98% solvable by copying the only place word). v2 fixes them; v0 stays loadable with `revision="text-world-v0"`, but not for conclusions.

**A first reference point** (2026-10-10, one seed, draft protocol): a 30M dense Transformer trained on 1.5B tokens of the mix passes `quote` (95% at 4k, against 8% guessing) and stays near guessing on `lookup` and `keyed`. Larger models are being run.

## CogitoProbe: four clean probes without language

The CogitoProbe sets drop language. Facts are short symbolic sentences, filler is a repeating cycle, and every symbol is one SmolLM3 / Llama-3 token. Unlike a plain needle-in-a-haystack test, **every row carries `prize_bits`**, the information the answer is worth, so you can report how many bits a model recovered.

| Set | Facts look like | Question → answer | What a failure tells you |
|---|---|---|---|
| **Bits** | `key alice val red . key bob val blue .` | `Q alice bob` → `red blue` | The memory cannot hold that many bits at that distance |
| **Bind** | `alice in paris . alice friend bob . bob in oslo .` | `Q hop place alice` → `oslo` | It stored a list of attributes, not who has what |
| **Arith** | `{ { 2 + 8 } - 2 } .` | `Q sub 1 . 0 .` → `8 . 1 0` (internal node values) | It computed a result but lost the tree |
| **Props** | `the baker dropped the red cup in paris .` | `Q color cup hat` → `red blue` | It learned the statistics of the filler, not the facts |

Real rows use random single-token words (`gonzalez`, `validators`) instead of these readable names.

Each set has 10,240 rows (8,448 train, 896 validation, 896 test), five length rungs (1k, 4k, 8k, 16k, 32k), and two variants:

- **`fixed`**: the same number of facts as at 1k (16 key–value pairs in Bits) at every length. A score that falls with length is a **distance** failure.
- **`scaled`**: more facts as the row grows (up to 256 key–value pairs at 32k in Bits). A score that falls is a **capacity** failure.

Guessing gives 1/32 per value in Bits and Props, and 1/32 per colour or place and 1/64 per name in Bind.

In Arith, `eval` (the final number) is only a shortcut control; `subexpr` and `match` are the real tests.

## How to load and score them

Load any of them with the `datasets` library:

```python
from datasets import load_dataset
from transformers import AutoTokenizer

# Language-based exams at every length (test split only)
exams = load_dataset("ksopyla/cogito-text-world", "eval_id", split="test")
tok = AutoTokenizer.from_pretrained("ksopyla/cogito-text-world", subfolder="tokenizer")

# Symbolic probes: train / validation / test, answer span already marked
bits = load_dataset("ksopyla/cogito-probe-bits")
small = bits["train"].filter(lambda r: r["seq_len"] == 1024 and r["variant"] == "fixed")
```

The columns you need, and the score each family uses:

| | Cogito Text World (eval configs) | CogitoProbe (all four) |
|---|---|---|
| Input | `prompt` (ends in `Answer:`) | `context` + `query`, or ready `input_ids` |
| Gold | `answer` (with the final period) | `answer`; `labels` are `-100` outside it |
| Difficulty dials | `length`, `depth`, `task` | `seq_len`, `variant`, `task`, `gap` |
| Chance | `floor` per item, `candidates` | `prize_bits` |
| Control | `prompt_removed` twin | shuffle filler / shuffle facts |
| Main score | exact answer (all answer tokens top-1); pass = ≥75% with the twin at its guessing rate | token accuracy on the answer span; recovered bits `max(0, prize_bits + Σ log2 p(gold))` |

Text World training data is token ids for the bundled tokenizer. Probe ids are SmolLM3 / Llama-3 ids: use them as they are, or tokenize the text columns yourself.

A protocol I would suggest, based on what I learned the hard way:

1. **Calibrate with a dense Transformer first.** Train a plain decoder of the same size on the same data. If it does not reach ~75% at the shortest length, the task is too hard for that budget and says nothing about your architecture.
2. **Print the guessing rate and run the twin.** A score is evidence only if the evidence-removed twin (or, on Props, shuffled filler) falls back to the guessing rate. On the probes, report recovered bits next to `prize_bits`.
3. **Report by length, not one average.** Plot score against `length` (or `gap`). Where the curve breaks is the result.

## What these datasets are not

- **Not language understanding.** Children's-story language, templated facts and symbols test the *mechanisms* of storing and using information, not knowledge.
- **Not a leaderboard.** There is only one reference point so far (above). Text World is a calibrated draft at `text-world-v2`; future versions get a new tag, and old ones stay loadable.
- **Not calibrated yet on the probes.** My first dense run on Bits (one layer, 1k tokens, a 2,048-row subset) reached 6.5% and overfit; the cause is not diagnosed, so treat the probes as uncalibrated until a dense baseline passes.
- **Facts are easier to spot than in real text.** Same-shaped decoys and the twins limit, but do not remove, that advantage.

## Related work and inspirations

These datasets borrow heavily from earlier work:

- **bAbI** [3] isolated reasoning skills with small templated stories; **BABILong** [4] hid them in PG-19 books up to millions of tokens. Text World follows that plan with simple stories, so a model under 100M can learn the language.
- **Needle in a haystack** [5] and **passkey retrieval** [13] made "plant a fact, ask at the end" the standard test; **RULER** [6] added multi-key retrieval and tracking; **Lost in the Middle** [7] showed why evidence position must be reported.
- **Zoology / MQAR** [8]: recall gets harder with more keys, hence the `scaled` variant.
- **Physics of Language Models 3.1** [9]: facts need several phrasings, hence four templates per relation.
- **Binding IDs** [14] and **ListOps** [15] inspired the Bind and Arith probes. **Grokked Transformers** [10] and **ProntoQA** [11] shaped the hop and deduction levels; **Long Range Arena** [12] is the classic synthetic benchmark for efficient Transformers.

As far as I could find, there is no single small-vocabulary testbed that combines fluent language, a fact layer, multi-hop questions and 1k → 128k lengths for models trained from scratch. That is the gap this family tries to fill.

## Citation (BibTeX)

If you use any of the datasets, please cite the family. The same entry appears in every dataset card, next to a per-dataset entry:

```bibtex
@misc{sopyla2026cogitochecks,
  title        = {Cogito Capability Checks: synthetic tests of whether models store and use facts from long context},
  author       = {Sopyła, Krzysztof},
  year         = {2026},
  howpublished = {\url{https://ai.ksopyla.com/projects/cogito-capability-datasets/}},
  note         = {Datasets: cogito-probe-bits, -bind, -arith, -props; cogito-text-world}
}
```

Results and especially shortcuts you find are welcome in the comments.

**Generator code:** [github.com/ksopyla/MrCogito](https://github.com/ksopyla/MrCogito) (`data/text_world.py`, `data/concept_probes/`; Text World also ships its generator in the dataset repo under `generator/`) · **Background:** [A Memory That Reads by Content](/posts/memory-that-reads-by-content/)

## References

1. Eldan, R. and Li, Y. (May 2023). [**TinyStories: How Small Can Language Models Be and Still Speak Coherent English?**](https://arxiv.org/abs/2305.07759) Microsoft Research. arXiv:2305.07759
2. Finke, L. et al. (Apr 2025). [**Parameterized Synthetic Text Generation with SimpleStories**](https://arxiv.org/abs/2504.09184). arXiv:2504.09184
3. Weston, J. et al. (Feb 2015). [**Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks**](https://arxiv.org/abs/1502.05698). Facebook AI Research. arXiv:1502.05698
4. Kuratov, Y. et al. (Jun 2024). [**BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack**](https://arxiv.org/abs/2406.10149). AIRI. arXiv:2406.10149
5. Kamradt, G. (Nov 2023). [**Needle In A Haystack — Pressure Testing LLMs**](https://github.com/gkamradt/LLMTest_NeedleInAHaystack). GitHub.
6. Hsieh, C.-P. et al. (Apr 2024). [**RULER: What's the Real Context Size of Your Long-Context Language Models?**](https://arxiv.org/abs/2404.06654) NVIDIA. arXiv:2404.06654
7. Liu, N. F. et al. (Jul 2023). [**Lost in the Middle: How Language Models Use Long Contexts**](https://arxiv.org/abs/2307.03172). Stanford University. arXiv:2307.03172
8. Arora, S. et al. (Dec 2023). [**Zoology: Measuring and Improving Recall in Efficient Language Models**](https://arxiv.org/abs/2312.04927). Stanford University. arXiv:2312.04927
9. Allen-Zhu, Z. and Li, Y. (Sep 2023). [**Physics of Language Models: Part 3.1, Knowledge Storage and Extraction**](https://arxiv.org/abs/2309.14316). Meta FAIR. arXiv:2309.14316
10. Wang, B. et al. (May 2024). [**Grokked Transformers are Implicit Reasoners: A Mechanistic Journey to the Edge of Generalization**](https://arxiv.org/abs/2405.15071). The Ohio State University. arXiv:2405.15071
11. Saparov, A. and He, H. (Oct 2022). [**Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought**](https://arxiv.org/abs/2210.01240). New York University. arXiv:2210.01240
12. Tay, Y. et al. (Nov 2020). [**Long Range Arena: A Benchmark for Efficient Transformers**](https://arxiv.org/abs/2011.04006). Google Research. arXiv:2011.04006
13. Mohtashami, A. and Jaggi, M. (May 2023). [**Landmark Attention: Random-Access Infinite Context Length for Transformers**](https://arxiv.org/abs/2305.16300). EPFL. arXiv:2305.16300
14. Feng, J. and Steinhardt, J. (Oct 2023). [**How do Language Models Bind Entities in Context?**](https://arxiv.org/abs/2310.17191) UC Berkeley. arXiv:2310.17191
15. Nangia, N. and Bowman, S. R. (Apr 2018). [**ListOps: A Diagnostic Dataset for Latent Tree Learning**](https://arxiv.org/abs/1804.06028). New York University. arXiv:1804.06028
