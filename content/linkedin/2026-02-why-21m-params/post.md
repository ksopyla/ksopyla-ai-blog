---
title: "Why I'm building a 21M parameter model in the age of 405B"
date: 2026-02-27
platform: linkedin
status: draft
content_score: 4.10
related_blog_post: ""
---

Everyone is scaling up. I'm scaling differently.

While the industry races toward 405B parameter models, I'm training a 21M parameter ConceptEncoder. Not because I can't access bigger compute — but because I think there's a better path.

My ConceptEncoder uses 128 learnable concept tokens with cross-attention to the input sequence. Instead of every token attending to every other token (128K × 128K operations), concepts attend to the sequence (128 × 128K operations). That's a 1000x theoretical memory reduction.

The bet: a small set of concepts, forced to compress meaning, might learn more efficiently than billions of parameters trained to predict the next token.

Is it working? Honestly — not yet, not fully. My concepts keep collapsing (effective rank 5/128). But each failed experiment teaches me something about how representations form and why brute-force scaling avoids these fundamental questions rather than solving them.

Three things I've learned so far:
→ Efficiency constraints force architectural innovation. You can't just throw more parameters at a collapsed representation.
→ Small models reveal failure modes that large models hide behind sheer capacity.
→ The training objective matters more than model size. A bad objective wastes parameters at any scale.

I don't claim this will work. But I believe exploring alternatives to "just scale it up" is research worth doing — especially when a single large training run costs more energy than I'll use in a year.

What's your take — is there value in exploring small, efficient architectures, or is scaling the only game in town?

github.com/ksopyla/MrCogito

#AIResearch #EfficientAI #MachineLearning #OpenScience #ConceptEncoder
