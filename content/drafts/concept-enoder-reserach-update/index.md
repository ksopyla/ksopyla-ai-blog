---
title: "Concept Encoder Research Update: Better Failures, Better Questions"
date: 2026-03-08
draft: true
description: "A research update from MrCogito: why the MLM path stalled, what diffusion clarified, why prefix conditioning is still promising, and how much of research is really about asking better questions."
tags: ["AI", "Concept Encoder", "Representation Learning", "Diffusion", "BiXT", "MrCogito"]
categories: ["AI Research"]
showReadingTime: true
---

{{< lead >}}
Sometimes the most useful research update is not a new best model. It is a sharper explanation of why the last few ideas failed, what they actually taught me, and which questions are now worth asking next.
{{< /lead >}}

For the last few weeks I have been deep in the concept-encoding part of the [`MrCogito`](/projects/concept-encoder/) project.

This is the part I care about most right now. Before I think seriously about generation, reasoning, or speech-to-speech systems, I want a compact representation that actually carries meaning. If I cannot reliably compress text into a small bank of useful concepts, the rest of the stack will be built on sand.

So this post is not a victory lap. It is a lab note in public: what I tried, what broke, what got better for the wrong reasons, and why I recently shifted attention from MLM-style training toward diffusion and prefix-conditioned objectives.

## The Goal

The working idea behind `MrCogito` is simple to state and annoyingly hard to make work:

encode a sequence into a relatively small set of concept vectors, then use those concepts as the compact semantic state of the model.

This is the part of the field that keeps pulling me back. People who disagree on almost everything, like Yann LeCun and Gary Marcus, still converge on one useful point: next-token prediction alone is probably not the whole story. My own version of that argument is more practical. If I can learn a compact concept space that preserves meaning, I get a much better foundation for latent reasoning, reusable internal state, and models that generalize in a less brute-force way.

In practice, that means I want the model to do more than compress tokens. I want it to capture something closer to semantic factors:

- what the sentence is about
- which entities matter
- what relation is being expressed
- which information should survive compression and still be useful downstream

If this works, it could become a good foundation for long-context systems, controllable generation, and later multimodal work. If it fails, I want to understand *why* it fails, not just move to the next fashionable architecture.

## Where The MLM Line Started To Stall

The first serious line was a Perceiver-style MLM setup: text goes into a concept encoder, then a lightweight decoder reconstructs masked tokens.

Numerically, that line was not a complete disaster. The canonical only 6 layers MLM baseline reached decent downstream numbers, including `MRPC = 81.3%` and `STS-B = 0.627`.

But the internal geometry told a different story.

The same model had an effective concept rank of only `5 / 128`. In other words, I allocated 128 concept slots and the model behaved as if only a handful really mattered. That is not the kind of bottleneck I want. It is compact, but not in an interesting way. I asked for a concept parliament and got five active members plus 123 people silently forwarding emails.

To make this visible, I built a small analysis pipeline around `analysis/run_concept_analysis.py` and `analysis/concept_analysis.py`, because I wanted something better than "the model vibes feel collapsed."

I then tried regularization to spread the concepts out. One run pushed rank to `122 / 128`, which sounds great until you look at the semantic metrics: `STS-B` fell to `0.341`. That was an important lesson:

**geometric diversity without semantic content is not a win.**

The fresh diagnosis from the MLM branch now looks more precise than my earlier intuition. The problem was not "concept bottlenecks are a bad idea." The problem was a bad match between architecture, objective, and evaluation:

1. The standard encoder was too static before compression.
2. The normal MLM decoder was shortcut-friendly.
3. The cleaner PosOnly variant was probably under-supervised rather than definitively bad.
4. The evaluation path often measured the wrong part of the pretrained system.

That first point was especially important, and it was my own architectural oversight.

In the default encoder path, token embeddings were computed once and then reused across all layers. I had effectively built a six-layer concept refiner on top of a one-layer token representation and hoped the model would somehow invent the missing contextualization by force of character. It did not.

So instead of six rounds of increasingly contextual token representations, the concepts kept reading from something closer to a fixed lexical-position memory bank.

That is a bad setup if you want semantic concepts. The model can compress surface statistics surprisingly well without learning richer structure.

## How I Found BiXT

One of the most useful architectural clues came from `BiXT` ([Hiller et al., 2024](https://arxiv.org/abs/2402.12138)), which updates token-side and latent-side representations together instead of treating tokens as mostly static memory.

What is mildly funny is that I did not discover this in a cinematic research epiphany while staring at a whiteboard. I found it during one of those long Cursor sessions where I kept asking "why?" often enough that the agent probably deserved hazard pay. I had already set up a small research workflow in Cursor, including custom rules and my `research-digest` skill, so once the question became precise, I could move quickly between code, notes, experiment logs, and papers without losing the thread.

The key question was simple: why does the encoder keep collapsing even when the downstream numbers look respectable? Following that trail kept pointing back to the same weakness: the token side of the model was too static, so the concepts were compressing weak source representations.

That matters here because semantic structure does not appear from token embeddings alone. Things like role assignment, clause structure, and interaction between phrases usually emerge through contextualization. If concepts keep reading from nearly frozen token states, then collapse is not surprising. The encoder is trying to summarize a weak source representation.

So `BiXT` became important to me for two reasons:

First, it is a plausible fix for a concrete bottleneck I can already see in my own codebase.

Second, it matches the long-term direction of the project: preserve the `O(C * N)` story, but make the interaction between tokens and concepts more meaningful.

Another important lesson here is that if I want to keep the `O(C * N)` complexity story and still make `BiXT` attractive, the token side should stay thin relative to the concept side, something like `32` or `64` versus `512`. Otherwise I keep the nice asymptotic story on paper while quietly paying too much for token-side richness in practice.

At this point I do not think of `BiXT` as a random architectural add-on. I think of it as one of the first genuinely necessary corrections.

## Why I Moved To Diffusion

The switch from MLM toward diffusion was not driven by novelty. It was driven by frustration with the training signal.

MLM gives weak and uneven pressure to the concept bottleneck. Only a small fraction of positions are supervised, and the decoder can often solve too much of the task through local shortcuts. So I wanted an objective that would force the model to rely more heavily on the concept bank.

Masked diffusion looked attractive for that reason. At higher noise levels, the decoder should need more global information, which in principle makes the concepts more useful.

The first win was engineering, not semantics.


After redesigning the diffusion decoder to remove token self-attention, switching to cross-attention-only decoding, and stabilizing timestep conditioning with `AdaLN-Zero`, I got a stable training path. That alone was progress. The original diffusion run had blown up badly. The new one trained cleanly.

But the semantic result was still disappointing.

The L2 diffusion run improved effective rank from the MLM baseline's `5 / 128` to `10.1 / 128`, which was directionally interesting. The singular value distribution also looked healthier. But `STS-B` was only `0.138`, essentially telling me that better geometry did not translate into better meaning.

Then I pushed further:

- deeper encoder: `L6`
- proper `ELBO`-style weighting
- higher `t_min`
- `VICReg + t_regs_mst` regularization

The result was clarifying in a painful but useful way.

The deeper self-reconstruction diffusion run still failed semantically: `STS-B = 0.174`, effective rank `5.74 / 128`. Adding regularization barely changed the story. One run even dropped to `5.09 / 128`.

That was the point where I stopped asking, "Which regularizer should I try next?" and started asking the better question:

**What if self-reconstruction through this bottleneck is optimizing the wrong solution?**

## The Main Diffusion Lesson

The best current explanation is not that diffusion is bad. It is that **self-reconstruction diffusion lets the model learn a low-dimensional retrieval code instead of semantic abstraction**.

In the self-reconstruction path, the encoder sees the clean sequence before noise is applied. The decoder then reconstructs masked tokens by querying the concept bank. Under that setup, the cheapest solution is not "understand the sentence." The cheapest solution is "store enough token identity and positional information in a compressed form to recover the missing pieces."

That is a very different objective.

Once I phrased it that way, several confusing results became less confusing:

- why geometry sometimes improved without semantics improving
- why deeper models did not rescue the setup
- why regularization changed spread but not meaning
- why the model kept finding low-rank solutions

This was one of those annoying research moments where the model is not failing randomly. It is succeeding at the wrong game.

## The Next Step: A SODA-Inspired Pivot

Another good outcome from those deep review sessions was that they pushed me toward a much cleaner analogy from vision: `SODA` ([Hudson et al., 2023](https://arxiv.org/abs/2311.17901)).

The useful idea was not "copy this paper into text and profit." Research is rarely that polite. The useful idea was narrower: if the decoder has to generate content the encoder never saw, the bottleneck has a much better chance of carrying semantics instead of a compressed cheat sheet.

I had been circling around prefix conditioning for a while, but the design still felt vague: how should the split work, how weak would the task be, and how should I evaluate it fairly? Cursor helped a lot here. Once the question was sharp, going from "this might be the right direction" to "the code is implemented and the job is on the cluster" was very fast. The implementation took minutes. Convincing myself it was worth implementing took considerably longer, which is a more honest summary of research anyway.



`SODA` showed in vision that bottleneck diffusion learns better representations when the decoder has to generate *different* content than the encoder saw. I wanted the text analogue of that: encode a prefix, generate a suffix.

The intuition is simple:

if the encoder only sees the first part of a document, then the concepts cannot just memorize the exact target tokens. They need to store something more like the semantic gist, discourse state, or likely continuation.

So I implemented a prefix-to-suffix diffusion path.

The first baseline did not solve the problem, but it was still informative. It reached `STS-B = 0.337`, which is clearly better than the self-reconstruction diffusion runs, but still far from where I want it. Effective rank was `6.19 / 128`, so collapse remained.

That means I do **not** read the result as "prefix conditioning failed."

I read it as:

1. The direction is more plausible than self-reconstruction.
2. Text continuation through a concept bottleneck is harder than the vision version of the idea might suggest.
3. My first text baseline was too weak to count as a decisive test.

That baseline still lacked several things that now look important:

- `BiXT`
- thinner token embeddings
- sentence-boundary aware prefix/suffix splits
- stronger evaluation routing
- probably a stronger initialization story as well

So the prefix line is still alive, but now under a much narrower claim: promising idea, underpowered first implementation.

## Cursor Helps, But Taste Still Matters

I genuinely love working with `Cursor`. It has made me much faster. But the useful version of that sentence comes with fine print.

It helps a lot more once you invest in the boring setup work: skills, rules and a research repo that is structured well enough for an agent to navigate without inventing archaeology. I will probably write a separate post about that setup, because it has become a real part of how I work now.

One side theme in this period has been how much `Cursor` and agents changed the pace of my research loop.

I can audit training scripts faster, compare experiment logs faster, trace code paths faster, summarize run reports faster, and keep a much more explicit paper trail than I used to. In practical terms, that means I spend less energy on clerical work and more on interpretation.

But this is the part I find interesting: better tooling does **not** remove the messy part of research.

If anything, it makes the messy part more visible. A good agent can help me inspect eight files in a minute. It cannot stop me from believing a bad explanation for three days if I am emotionally attached to it.

The real bottleneck is rarely "I cannot read eight files." The real bottleneck is usually one of these:

- I am asking the wrong question
- I am trusting the wrong metric
- I am comparing two experiments that are not actually comparable
- I am explaining a failure with a story that feels elegant but is not supported by the code

Agents are good at helping me gather evidence. They are much less good at deciding which comforting explanation I should stop believing. That part still seems to require human suspicion, decent taste, and occasional mild embarrassment.

So lately I keep coming back to a simple rule: ask "why?" five times before touching the next training script.

That habit already changed a few conclusions for me:

- diffusion did not fail because diffusion is bad
- MLM did not simply fail because concept bottlenecks are useless
- prefix generation did not fail enough to reject the idea
- some of my historical evaluation paths were weaker than I thought

That may not sound dramatic, but in research these are expensive distinctions.

## What I Think Now

My current view is roughly this:

The original MLM line found a real signal, but it mixed semantic learning with shortcuts and weak evaluation choices.

Self-reconstruction diffusion was worth trying, but the latest analysis strongly suggests that in this architecture it optimizes the wrong information path.

Prefix-conditioned diffusion is the most interesting recent pivot, not because it already works, but because it removes the biggest shortcut and asks the bottleneck to carry a more useful kind of information.

And `BiXT` is no longer a side experiment. It is becoming part of the core fix list.

## What Comes Next

The next experiments I care about most are:

1. Prefix diffusion v2 with `BiXT`, reduced token width, and sentence-boundary splits.
2. `TSDAE` ([Wang et al., 2021](https://arxiv.org/abs/2104.06979)) + `BiXT`, because dense denoising is still one of the strongest candidates for forcing semantic compression.
3. Better reevaluation of the MLM line, especially the routes that do not silently discard what pretraining actually taught.
4. Possibly a stronger warm-start from a pretrained language backbone, because asking a small concept model to learn language understanding, compression, and semantic organization from scratch may simply be too much at once.

In other words, the project is not at the "we found the answer" stage.

It is at the better stage than that: the bad explanations are starting to die.

And in research, that is usually when the work finally gets interesting.

## References

1. Hudson, D. A. et al. (Nov 2023). [**SODA: Bottleneck Diffusion Models for Representation Learning**](https://arxiv.org/abs/2311.17901). arXiv:2311.17901.
2. Hiller, M. et al. (Feb 2024). [**Perceiving Longer Sequences With Bi-Directional Cross-Attention Transformers**](https://arxiv.org/abs/2402.12138). arXiv:2402.12138.
3. Wang, K. et al. (Apr 2021). [**TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupervised Sentence Embedding Learning**](https://arxiv.org/abs/2104.06979). arXiv:2104.06979.
4. Gao, T. et al. (Apr 2021). [**SimCSE: Simple Contrastive Learning of Sentence Embeddings**](https://arxiv.org/abs/2104.08821). arXiv:2104.08821.
5. Sahoo, S. S. et al. (Jun 2024). [**Simple and Effective Masked Diffusion Language Models**](https://arxiv.org/abs/2406.07524). arXiv:2406.07524.
6. Meng, Y. et al. (Feb 2023). [**MAE-LM: Investigating Representation Deficiency in Masked Language Modeling**](https://arxiv.org/abs/2302.02060). arXiv:2302.02060.