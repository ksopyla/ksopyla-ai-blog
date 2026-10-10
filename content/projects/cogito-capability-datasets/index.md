---
title: "Cogito Capability Datasets: Long-Context Tests for Small Models"
description: "Long-context benchmark datasets for small language models (5M–100M): known facts, filler up to 128k tokens, one question, an exactly scored answer."
summary: "Five open Hugging Face datasets that test whether small (5M–100M) models actually use facts from far back in their context: recall, binding, structure, multi-hop, counting and deduction, on a length ladder from 1k to 128k tokens."
date: 2026-10-10
draft: false
weight: 15
tags: ["datasets", "long context", "evaluation", "small language models", "synthetic data", "needle in a haystack", "Hugging Face", "MrCogito"]
categories: ["AI research"]
icon: "🧪"
showReadingTime: true
keywords: ["long-context benchmark", "small language model evaluation", "needle in a haystack dataset", "associative recall", "synthetic long-context dataset", "capability evaluation", "TinyStories long context", "memory architecture benchmark"]
datasetFamily:
  name: "Cogito Capability Datasets"
  alternateName: ["CogitoProbe", "Cogito Text World"]
  description: "A family of open synthetic datasets for testing whether small language models (5M–100M parameters, trained from scratch) can store and use facts that appear thousands of tokens before the question. Every item plants known facts, pads the document with filler to 1k–128k tokens, and asks a question whose answer is computed by the generator and scored on the answer tokens only."
  license: "https://www.apache.org/licenses/LICENSE-2.0"
  keywords: ["long context", "small language models", "needle in a haystack", "associative recall", "entity binding", "multi-hop reasoning", "synthetic data", "capability evaluation"]
  citation: "Sopyła, K. (2026). Cogito Capability Datasets: Long-Context Tests for Small Models. https://ai.ksopyla.com/projects/cogito-capability-datasets/"
datasets:
  - name: "Cogito Text World"
    url: "https://huggingface.co/datasets/ksopyla/cogito-text-world"
    license: "https://cdla.dev/sharing-1-0/"
    description: "Story-world training and evaluation set for small language models: TinyStories and SimpleStories with an invented cast and woven-in facts; seven question types (quote, lookup, keyed lookup, latest state, multi-hop, count, deduce) at 1k–128k tokens, with evidence-removed twins."
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

## TL;DR

**What you get:**

- **One question:** *can a small model use a fact it read thousands of tokens ago?* Every item has known facts, a known distance to the question, and a generator-computed answer, so a score means one thing.
- **A length ladder:** the CogitoProbe sets run 1k → 32k tokens; Cogito Text World trains at 4k and tests at 1k → 128k.
- **Skills, not one number:** copy, look up, pick among look-alikes, bind, track the latest state, follow 1–3 hops, count, deduce.
- **Shortcut checks built in:** guessing floors, evidence-removed twins, answer information labelled in bits.

## Long-context datasets at a glance

| Dataset | What it asks | Lengths | Size |
|---|---|---|---|
| [**Cogito Text World**](https://huggingface.co/datasets/ksopyla/cogito-text-world) | Facts inside simple stories: quote, lookup, latest state, 1–3 hops, count, deduce | train 4k, test 1k–128k | 29k exam items, ~2.1B train tokens |
| [**CogitoProbe-Bits**](https://huggingface.co/datasets/ksopyla/cogito-probe-bits) | Values for keys listed at the start | 1k–32k | 10,240 rows |
| [**CogitoProbe-Bind**](https://huggingface.co/datasets/ksopyla/cogito-probe-bind) | Who has which colour, who lives where, where a friend lives | 1k–32k | 10,240 rows |
| [**CogitoProbe-Arith**](https://huggingface.co/datasets/ksopyla/cogito-probe-arith) | Internal values and bracket matches of a nested expression | 1k–32k | 10,240 rows |
| [**CogitoProbe-Props**](https://huggingface.co/datasets/ksopyla/cogito-probe-props) | Object colours stated in short sentences, then filler | 1k–32k | 10,240 rows |

Licenses: Text World is CDLA-Sharing-1.0 (inherited from TinyStories); the four CogitoProbe sets are Apache-2.0.

Start with **Text World** to see whether a small *language* model learns to use facts in text, e.g. when comparing memory, recurrence, state-space or sparse attention. Use **CogitoProbe** for a clean, information-labelled test of a memory mechanism without language in the way.

## Why I built them

I work on [MrCogito](/projects/concept-reasoning/), a small research model (~20–30M parameters) that compresses a long context into a few dense "concept" vectors and reasons from those. The question I kept failing to answer was simple: **does the compressed memory actually hold the facts, or does the model only look good on the next word?**

Ordinary evaluation could not tell me. Web text is locally predictable: a model can reach a decent loss by guessing the next word from the last few hundred tokens and never use anything older. In one experiment I trained a memory model on ~0.44B tokens of natural text at 32k context. The memory slots carrying far context were worth **0.05 nats** of loss, flat from 1k to 32k, while a passkey test scored 0% and keyed recall 4.8%. The memory held diverse vectors; the decoder simply did not read them for content. The loss curve gave no warning.

Popular long-context benchmarks did not fit either: in my experience they assume a large pretrained model, and a 30M model trained from scratch fails them for reasons unrelated to memory.

So I needed exams with three properties:

1. **Known facts, known distance.** I know the right answer and how far back it sits.
2. **Nothing to gain from the filler.** Answering without the evidence means a shortcut.
3. **Learnable from scratch.** Simple vocabulary, so a 5M–100M model can learn the task, and failure means a missing capability, not a missing language.

The CogitoProbe sets came first (September 2026). Text World followed (October 2026), because a memory that works on symbols can still be ignored once it competes with learning language.

## One idea, one layout

Every row in every dataset has the same shape:

```text
key alice val red .        <- facts the generator planted
key bob val blue .
glfw bigger signaling ...  <- filler: the gap,
...                           1k to 128k tokens
Q alice bob                <- question
red blue                   <- answer: the only
                              scored tokens
```

Length grows by adding filler, not facts, so a score reads as a function of distance.

## Cogito Text World: facts inside simple stories

Text World is a **training and evaluation set** for small language models (its card targets roughly 2M–150M parameters). The language comes from [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) and [SimpleStories](https://huggingface.co/datasets/SimpleStories/SimpleStories), simple stories that models of a few million parameters learn to write fluently [1, 2]. The generator weaves in an invented cast with homes, siblings, signs and moves, then asks one question.

A real item from the 1k-token exam (shortened):

```text
Once there was a little girl called Millie. ... On the door of Malu there was
a sign that said: bears at happy in. Millie sat down in the front row ...
A sign by Sima's gate said: the frogs little old. ...
The sign on Tadeta's door said: warm hills bears little rain. ...
The sign on Mosi's door said: trees hills sleep warm to jump. ... Malu laughed.
Question: What did the sign of Malu say?
Answer: bears at happy in.
```

Four signs, one asked: guessing gives 25%, and that floor is stored in every row.

### The seven question types

| Level | Task | Example question | Guessing floor |
|---|---|---|---|
| T1 | `quote` | What did the sign of Lumo say? | 1/4 |
| T2 | `lookup` | Where does Lumo live? | ≈0 |
| T3 | `keyed` | Where does Lumo live? (16 homes, a quarter with look-alike names) | 1/16 |
| T4 | `latest` | Where does Lumo live now? (after 4 moves, others move later) | 1/5 |
| T5 | `compose` | Where does the sister of the sister of Lumo live? | 1/8 |
| T6 | `count` | How many times did Lumo visit the market? | 1/7 |
| T7 | `deduce` | Is Pim shiny? (made-up category rules) | 1/2 |

The levels go from copying to reasoning: passing T2 but not T3 means it finds *a* fact but not the right one among look-alikes; passing T3 but not T5 means it stores facts but cannot chain them.

### What keeps it honest

- **Train short, test long.** Train at 4,096 tokens; the `eval_id` exams run at 1k, 2k, 4k, 8k, 16k, 32k, 64k and 128k. Longer documents add filler, never facts.
- **Evidence-removed twins.** Every exam item has a `prompt_removed` version with the answering sentences replaced by filler. A model that still beats the floor there is using a shortcut.
- **Held-out names and phrasings.** One name in five appears only in exams. `eval_paraphrase` uses unseen sentence templates; `eval_harder` uses a 64-person cast, 3 hops and 8 moves.
- **Clean filler.** Filler sentences that mention a cast member with a fact word (lives, moved, sister, sign) are dropped, and place answers are invented words that never occur in filler.

The training configs (~2.1B tokens) and tokenizer ship with the dataset, so architectures can be compared on the same token stream.

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

In Arith, the `eval` task (the final number) is only a calculator-shortcut control; `subexpr` and `match` are the real tests. Splits use disjoint random streams with zero fact overlap.

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
| Main score | exact answer (all answer tokens top-1) | token accuracy on the answer span; recovered bits `max(0, prize_bits + Σ log2 p(gold))` |

Text World training configs contain token ids only, for the bundled 4,096-token tokenizer. Probe `input_ids` are SmolLM3 / Llama-3 ids; use them as they are or rebuild from the text columns with your own tokenizer, but do not re-tokenize the ids.

A protocol I would suggest, based on what I learned the hard way:

1. **Calibrate with a dense Transformer first.** Train a plain decoder of the same size on the same data. If it does not reach ~75% at the shortest length, the task is too hard for that budget and says nothing about your architecture.
2. **Always print the floor next to the score.** A 40% score on `compose` (floor 12.5%) and a 40% score on `deduce` (floor 50%) mean opposite things. On the probes, report recovered bits next to `prize_bits`.
3. **Run the twin.** On Text World, score `prompt_removed` too. On Props, shuffle the filler. A model above the floor without the evidence is not using memory.
4. **Report by length, not one average.** Plot score against `length` (or `gap`). Where the curve breaks is the result.

## What these datasets are not

- **Not language understanding.** Children's-story language, templated facts and symbols test the *mechanisms* of storing and using information, not knowledge.
- **Not a leaderboard.** No official baselines yet. Text World is `text-world-v0`, its calibration runs are in progress, and settings may change in a later version.
- **Not calibrated yet on the probes.** My first dense run on CogitoProbe-Bits (one layer, hidden size 256, 1k tokens, a 2,048-row subset for 12 epochs) reached 6.5% packed-answer accuracy and overfit the subset. I have not diagnosed whether the cause was the recipe, the budget or the data, so treat the probes as uncalibrated until a dense baseline passes them.
- **Facts are easier to spot than in real text.** Same-shaped decoys and the twins limit, but do not remove, that advantage.

## Related work and inspirations

These datasets borrow heavily from earlier work:

- **bAbI** [3] isolated reasoning skills with small templated stories; **BABILong** [4] hid them in PG-19 books up to millions of tokens. Text World follows that plan with simple stories, so a model under 100M can learn the language.
- **Needle in a haystack** [5] made "plant a fact, ask at the end" the standard test; **RULER** [6] added multi-key retrieval and tracking; **Lost in the Middle** [7] showed why evidence position must be reported.
- **Zoology / MQAR** [8] showed that recall gets harder with more keys, not only more length: the `scaled` variant and the keyed task.
- **Physics of Language Models 3.1** [9] showed facts need several phrasings to be extractable: four templates per relation, plus a held-out paraphrase split.
- **Grokked Transformers** [10] and **ProntoQA** [11] shaped the hop and deduction levels; **Long Range Arena** [12] tests efficient Transformers on long-input classification, not fact use.

As far as I could find, there is no single small-vocabulary testbed that combines fluent language, a fact layer, multi-hop questions and 1k → 128k lengths for models trained from scratch. That is the gap this family tries to fill.

## Citation (BibTeX)

If you use any of the datasets, please cite this page as the reference for the whole family:

```bibtex
@misc{sopyla2026cogitocapability,
  title        = {Cogito Capability Datasets: Long-Context Tests for Small Models},
  author       = {Sopyła, Krzysztof},
  year         = {2026},
  howpublished = {\url{https://ai.ksopyla.com/projects/cogito-capability-datasets/}},
  note         = {Datasets: ksopyla/cogito-text-world, ksopyla/cogito-probe-bits,
                  ksopyla/cogito-probe-bind, ksopyla/cogito-probe-arith, ksopyla/cogito-probe-props}
}
```

Results, failures and especially shortcuts you find are welcome in the comments or on [Hugging Face](https://huggingface.co/ksopyla).

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
