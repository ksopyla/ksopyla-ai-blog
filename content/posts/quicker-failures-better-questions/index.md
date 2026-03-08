---
title: "Quicker Failures lead to better questions: How AI Helped Me Steer my research forward"
date: 2026-03-08
draft: false
description: "How AI, Cursor skills, and agents helped me ask better questions in MrCogito research, understand model failures more deeply, and steer the concept-encoder work toward better solutions."
tags: ["AI", "Concept Encoder", "Representation Learning", "Diffusion", "BiXT", "MrCogito"]
categories: ["AI Research"]
featureImage: "feature_concept_encoder_research_update.png"
featureAlt: "Abstract colorful streams compressing through a narrow concept bottleneck and expanding into richer geometric structure"
showReadingTime: true
aliases:
  - /posts/concept-encoder-research-update/
---

{{< lead >}}
Sometimes the most useful research update is not a better metric. It is the moment when better questions finally expose what the model is really doing, and the next experiment stops being random motion.
{{< /lead >}}

For the last few weeks I have been deep in the concept-encoding part of the [`MrCogito`](/projects/concept-encoder/) project.

This is the part I care about most right now. Before I spend serious time on generation, latent reasoning, or speech-to-speech systems, I want a compact representation that actually carries meaning. If I cannot reliably compress text into a small bank of useful concepts, the rest of the stack will be built on sand.

But this update is not really about one architecture tweak.

It is about a change in how I worked.

Recently, the biggest value I got from AI tools was not "write code faster" or "summarize a paper for me." It was something more useful: they helped me ask better questions while the research was still hot, while the logs, code, half-formed hypotheses, and annoying contradictions were all still in front of me.

That shift mattered because this part of the project had become messy. Some results looked decent. Some plots looked encouraging. Some variants failed in ways that were hard to interpret. I could easily have spent another few weeks doing what researchers often do under pressure: trying another tweak, chasing another metric, and hoping the next run would make the story cleaner.

Instead, AI helped me compress the clerical part of the loop, so I could spend more time on the part that actually matters: interpretation.

## The Real Update: Better Questions Changed The Work

The core idea behind `MrCogito` is still the same:

encode a sequence into a relatively small set of concept vectors, then use those concepts as the compact semantic state of the model.

I care about this because if the model can preserve meaning in a compact concept space, that gives me a much better foundation for latent reasoning, reusable internal state, and systems that generalize in a less brute-force way.

In practice, I want the model to capture something closer to semantic factors:

- what the sentence is about
- which entities matter
- what relation is being expressed
- which information should survive compression and still be useful downstream

That ambition did not change.

What changed was the way I navigated failure.

For a while, I was still framing the work in the usual local way:

- which decoder should I try next
- which regularizer might rescue collapse
- whether one more architecture tweak might improve the score

Those are not useless questions. But they are often second-order questions. When you ask them too early, you can spend a lot of time optimizing the wrong thing.

The much more useful questions turned out to be:

- what is the model actually learning through this bottleneck
- which shortcut is the objective quietly allowing
- why do some results look better on paper without getting semantically better
- what part of the system is the evaluation really measuring

Once those questions became explicit, the project started moving again.

## What AI Actually Changed In My Research Loop

I genuinely love working with `Cursor`, but the useful version of that sentence comes with fine print.

AI did not give me the answer. It did not replace judgment. And it definitely did not save me from believing a bad explanation for longer than I should have.

What it did do was let me move much faster between:

- code
- experiment logs
- analysis scripts
- notes
- papers
- implementation ideas

That sounds simple, but it changes the texture of research.

Instead of spending energy on "where is that script again?" or "which run report had that metric?" or "did I already compare these two variants?", I could keep pressure on the actual reasoning loop. I could inspect the training code, compare the run reports, revisit the papers, and test the explanation much faster.

That made it easier to keep asking "why?" long enough to get past the first comfortable story.

This is where the custom setup mattered too. The combination of `Cursor`, my own rules, and task-specific skills made the repo much easier to navigate under pressure. Once the question became sharp, I could move quickly without losing the thread.

The important distinction is this:

AI improved my speed of evidence gathering.
It did not automate taste.

And in research, taste often means knowing which question deserves another hour and which explanation deserves suspicion.

## The Failure That Looked Good Enough

One reason this mattered is that the project produced several results that were easy to misread.

The first serious line was a Perceiver-style MLM setup. Numerically, it was not a complete disaster. The six-layer baseline reached respectable downstream numbers, including `MRPC = 81.3%` and `STS-B = 0.627`.

If I had been in a hurry, I could have treated that as provisional validation and moved on.

But the internal geometry told a different story.

The same model had an effective concept rank of only `5 / 128`. I allocated 128 concept slots and the model behaved as if only a handful were really active. That is compact, but not in an interesting way.

So I built a small analysis pipeline around `analysis/run_concept_analysis.py` and `analysis/concept_analysis.py`, because I wanted something better than vague intuition.

Then another misleading result appeared. With stronger regularization, one run pushed the effective rank to `122 / 128`. That sounds great until you look at the semantic side: `STS-B` dropped to `0.341`.

That was one of the first moments where the better question mattered more than the prettier metric.

The lesson was not "collapse solved" or "regularization works."

It was this:

**geometric diversity without semantic content is not a win.**

## The Better Questions That Changed The Diagnosis

Once I slowed down and kept asking "why?", the diagnosis became much more precise.

The problem was not "concept bottlenecks are a bad idea."

The problem was a bad match between architecture, objective, and evaluation.

The first issue was my own architectural oversight. In the original encoder path, token embeddings were computed once and then reused across all layers. I had effectively built a multi-layer concept refiner on top of a weak token representation and hoped semantic structure would appear by force of optimism.

It did not.

That made one question unavoidable:

**If the token side is too static, what exactly are the concepts supposed to summarize?**

That question is what led me to `BiXT` ([Hiller et al., 2024](https://arxiv.org/abs/2402.12138)).

I did not find it in a dramatic whiteboard moment. I found it during one of those long `Cursor` sessions where I kept drilling into the same bottleneck from different angles until the question finally got sharp enough.

`BiXT` mattered because it updates token-side and latent-side representations together instead of treating tokens as mostly static memory. In other words, it looked less like a random architectural curiosity and more like an answer to a concrete weakness I could already see in my own code.

That also reshaped how I thought about complexity. If I want to keep the `O(C * N)` story and still make this direction attractive, the token side has to stay thin relative to the concept side. Otherwise I keep the elegant asymptotic story on paper while quietly paying too much for token-side richness in practice.

## Why Diffusion Clarified The Wrong Part

The switch from MLM toward diffusion came from frustration with the training signal. MLM gives weak and uneven pressure to the concept bottleneck. Only a subset of positions are supervised, and the decoder can often solve too much through local shortcuts.

Diffusion looked attractive because it should, in principle, force the decoder to rely more on the concept bank.

There was real progress on the engineering side. After redesigning the diffusion decoder to remove token self-attention, switching to cross-attention-only decoding, and stabilizing timestep conditioning with `AdaLN-Zero`, I got a stable training path. The original diffusion run had blown up. The new one trained cleanly.

But again, better engineering did not automatically mean better understanding.

The L2 diffusion run improved effective rank from `5 / 128` to `10.1 / 128`, and the singular value distribution looked healthier. But `STS-B` was only `0.138`.

Then I pushed further:

- deeper encoder: `L6`
- proper `ELBO`-style weighting
- higher `t_min`
- `VICReg + t_regs_mst` regularization

The deeper self-reconstruction diffusion run still failed semantically: `STS-B = 0.174`, effective rank `5.74 / 128`. Adding regularization barely changed the story.

That was the moment where the local question, "Which regularizer should I try next?", stopped being useful.

The better question was:

**What if self-reconstruction through this bottleneck is optimizing the wrong solution?**

That question did more for the project than any individual tweak.

## The Shortcut Became Visible

The best current explanation is not that diffusion is bad. It is that **self-reconstruction diffusion lets the model learn a low-dimensional retrieval code instead of semantic abstraction**.

In the self-reconstruction setup, the encoder sees the clean sequence before noise is applied. The decoder then reconstructs masked tokens by querying the concept bank. Under that setup, the cheapest path is not "understand the sentence." It is "store enough token identity and positional information in compressed form to recover the missing pieces."

Once I phrased the problem that way, several confusing results became less confusing:

- why geometry sometimes improved without semantics improving
- why deeper models did not rescue the setup
- why regularization changed spread but not meaning
- why low-rank solutions kept coming back

This is exactly the kind of moment I mean when I say better questions move the work forward.

The model was not failing randomly.

It was succeeding at the wrong game.

## A Better Question Opened A Better Direction

Another useful outcome from those deep review sessions was that they pushed me toward a cleaner analogy from vision: `SODA` ([Hudson et al., 2023](https://arxiv.org/abs/2311.17901)).

The useful idea was not "copy this paper into text and profit." The useful idea was narrower: if the decoder has to generate content the encoder never saw, the bottleneck has a much better chance of carrying semantics instead of a compressed cheat sheet.

That idea had been floating around in my notes for a while. What changed was that the question became sharp enough to implement:

if self-reconstruction rewards the wrong shortcut, what happens if the encoder only sees a prefix and the decoder has to generate a suffix?

So I implemented a prefix-to-suffix diffusion path.

The first baseline did not solve the problem. It reached `STS-B = 0.337`, which is clearly better than the self-reconstruction diffusion runs, but still far from where I want it. Effective rank was `6.19 / 128`, so collapse remained.

But I do not read that result as failure in the simple sense.

I read it as evidence that the direction is more plausible than self-reconstruction, while still being underpowered as a first implementation.

That baseline still lacked several things that now look important:

- `BiXT`
- thinner token embeddings
- sentence-boundary-aware prefix/suffix splits
- stronger evaluation routing
- probably a stronger initialization story

So the project did not move forward because AI magically found the right model.

It moved forward because AI helped me get to a better research question sooner, and that better question pointed to a more promising family of solutions.

## Cursor Helps, But Judgment Still Matters

This is the part I care about most philosophically.

AI agents are good at helping me gather evidence. They are good at comparing files, surfacing papers, tracing code paths, summarizing logs, and making the repo feel smaller.

They are much less good at deciding which comforting explanation I should stop believing.

The real bottleneck is rarely "I cannot inspect eight files."

The real bottleneck is more often one of these:

- I am asking the wrong question
- I am trusting the wrong metric
- I am comparing experiments that are not really comparable
- I am telling myself a story that feels elegant but is not supported by the code

That part still seems to require human suspicion, decent taste, and occasional mild embarrassment.

So my current rule is simple:

ask "why?" five times before touching the next training script.

That habit already changed several conclusions for me:

- diffusion did not fail because diffusion is bad
- MLM did not fail because concept bottlenecks are useless
- prefix generation did not fail enough to reject the idea
- some of my historical evaluation paths were weaker than I thought

That may not sound dramatic, but in research these are expensive distinctions.

## Open Source

The entire [`MrCogito`](https://github.com/ksopyla/MrCogito) project is open source. The [`dev` branch](https://github.com/ksopyla/MrCogito/tree/dev) contains training scripts, model code, experiment reports, and the custom `Cursor` skills that power the research workflow I described above:

- [**experiment-tracking**](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills/experiment-tracking) — structured logging of runs, metrics, and comparisons
- [**research-methodology**](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills/research-methodology) — hypothesis formulation, ablation design, failure analysis
- [**pytorch-architecture**](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills/pytorch-architecture) — model building conventions and architecture templates
- [**engineering-change-tracking**](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills/engineering-change-tracking) — tracking code and config changes across experiment iterations
- [**huggingface-project**](https://github.com/ksopyla/MrCogito/tree/dev/.cursor/skills/huggingface-project) — dataset and model management on HuggingFace Hub

Feel free to check them out, try them in your own `Cursor` setup, and adapt them to your workflow.

## What I Believe Now

My current view is roughly this:

The original MLM line found a real signal, but it mixed semantic learning with shortcuts and weak evaluation choices.

Self-reconstruction diffusion was worth trying, but in this architecture it strongly appears to optimize the wrong information path.

Prefix-conditioned diffusion is the most interesting recent pivot, not because it already works, but because it removes the biggest shortcut and asks the bottleneck to carry a more useful kind of information.

And `BiXT` is no longer a side experiment. It is becoming part of the core fix list.

More broadly, I now believe the most useful role of AI in my research workflow is not to produce answers.

It is to help me reach the sharper question sooner.

And sharper questions often steer the model forward more than one more clever trick.

## What Comes Next

The next experiments I care about most are:

1. Prefix diffusion v2 with `BiXT`, reduced token width, and sentence-boundary splits.
2. `TSDAE` ([Wang et al., 2021](https://arxiv.org/abs/2104.06979)) + `BiXT`, because dense denoising is still one of the strongest candidates for forcing semantic compression.
3. Better reevaluation of the MLM line, especially the routes that do not silently discard what pretraining actually taught.
4. Possibly a stronger warm-start from a pretrained language backbone, because asking a small concept model to learn language understanding, compression, and semantic organization from scratch may simply be too much at once.

In other words, the project is not at the "we found the answer" stage.

It is at the better stage than that:

the bad explanations are starting to die.

And in research, that is usually when the work finally gets interesting.

## References

1. Hudson, D. A. et al. (Nov 2023). [**SODA: Bottleneck Diffusion Models for Representation Learning**](https://arxiv.org/abs/2311.17901). arXiv:2311.17901.
2. Hiller, M. et al. (Feb 2024). [**Perceiving Longer Sequences With Bi-Directional Cross-Attention Transformers**](https://arxiv.org/abs/2402.12138). arXiv:2402.12138.
3. Wang, K. et al. (Apr 2021). [**TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupervised Sentence Embedding Learning**](https://arxiv.org/abs/2104.06979). arXiv:2104.06979.
4. Gao, T. et al. (Apr 2021). [**SimCSE: Simple Contrastive Learning of Sentence Embeddings**](https://arxiv.org/abs/2104.08821). arXiv:2104.08821.
5. Sahoo, S. S. et al. (Jun 2024). [**Simple and Effective Masked Diffusion Language Models**](https://arxiv.org/abs/2406.07524). arXiv:2406.07524.
6. Meng, Y. et al. (Feb 2023). [**MAE-LM: Investigating Representation Deficiency in Masked Language Modeling**](https://arxiv.org/abs/2302.02060). arXiv:2302.02060.
