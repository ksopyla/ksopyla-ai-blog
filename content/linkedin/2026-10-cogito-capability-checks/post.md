---
title: "I started my evaluation too far: back to simple tests for tiny models"
date: 2026-10-11
platform: linkedin
status: draft
related_blog_post: "https://ai.ksopyla.com/projects/cogito-capability-datasets/"
visual: "Optional. A simple sketch of one test: a short story with a planted fact, a long stretch of filler, one question at the end. Or no image."
link_strategy: "Hugging Face links go in the first comment (text below the post). Project page in the same comment."
audience: "Research peers, potential hires, Pearson leaders and colleagues who read silently. Goal: show the ongoing journey honestly, framed as an evening hobby, no bragging."
---

I gave my tiny models the exams the big labs use. They scored zero, night after night.

Some context: I'm over 40, and instead of a sports car I went back to my academic roots. In the evenings I train small memory-based reasoning models, 10M to 200M parameters, from scratch on 3–4 GPUs. Cheaper than the sports car, louder than woodworking 🙂

I've always believed evaluation comes first. So I went straight for real text and well-known long-context benchmarks. But those are made for big pretrained models, and mine learned nothing useful from them. Worse, the loss looked healthy while the model quietly ignored the memory I'd built for it.

My mistake: I was aiming at the finish line before checking that my models could take the first step.

So I went back to basics. Can it hold one fact? Does it read its memory at all? How far back can it reach?

I built a ladder of simple checks:

Step 1: no language. Random symbols, almost like DNA: "key alice val red", thousands of tokens of filler, then "what was alice?"

Step 2: children's stories with planted facts, and questions that slowly get harder: find where someone lives → pick them among look-alike names → track where they live now → follow 2–3 hops → count, deduce.

I know every right answer, so a score finally means something. (Even the tests needed testing: my first version could be passed without reading the facts.)

Still early, and most experiments fail. But now I can see which step on the ladder fails.

That's why I'm sharing these checks. Most long-context benchmarks assume a big pretrained model. If you train small models from scratch, test a new memory or attention design, or do research on a few GPUs, you need tests your model can actually pass.

What you get: open datasets on Hugging Face, lengths from 1K to 128K tokens, a known answer for every question, and a built-in check that a model can't pass by guessing.

Links in the first comment. Shortcuts you find are very welcome.

Four papers that shaped these checks:

1. TinyStories (Eldan & Li, 2023): simple stories that models of a few million parameters can learn to write. https://arxiv.org/abs/2305.07759
2. bAbI (Weston et al., 2015): small templated stories, one reasoning skill per task. https://arxiv.org/abs/1502.05698
3. BABILong (Kuratov et al., 2024): the same skills hidden in very long books. https://arxiv.org/abs/2406.10149
4. Zoology (Arora et al., 2023): recall gets harder with more keys, and many efficient architectures fail exactly there. https://arxiv.org/abs/2312.04927

#AIResearch #MachineLearning #SmallLanguageModels

---

FIRST COMMENT:

The datasets, free to use:

Cogito Text World (facts inside simple stories): https://huggingface.co/datasets/ksopyla/cogito-text-world
CogitoProbe tests without language: Bits https://huggingface.co/datasets/ksopyla/cogito-probe-bits · Bind https://huggingface.co/datasets/ksopyla/cogito-probe-bind · Arith https://huggingface.co/datasets/ksopyla/cogito-probe-arith · Props https://huggingface.co/datasets/ksopyla/cogito-probe-props

The whole collection: https://huggingface.co/collections/ksopyla/cogito-capability-checks-6aca2db88ba9d2714727489f

The whole journey on my blog: https://ai.ksopyla.com/projects/cogito-capability-datasets/

---

SECOND COMMENT (optional):

Four papers that shaped these checks:

1. TinyStories (Eldan & Li, 2023): simple stories that models of a few million parameters can learn to write. https://arxiv.org/abs/2305.07759
2. bAbI (Weston et al., 2015): small templated stories, one reasoning skill per task. https://arxiv.org/abs/1502.05698
3. BABILong (Kuratov et al., 2024): the same skills hidden in very long books. https://arxiv.org/abs/2406.10149
4. Zoology (Arora et al., 2023): recall gets harder with more keys, and many efficient architectures fail exactly there. https://arxiv.org/abs/2312.04927
