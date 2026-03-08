---
title: "Speech-to-Speech Architectures — Latency Is the Wrong Metric"
date: 2026-03-04
platform: linkedin
status: draft
content_score: 0
related_blog_post: "posts/voice-to-voice-models-2026-review"
---


Speech-to-Speech Architectures — Latency Is the Wrong Metric

160ms response time means nothing if the model can't remember what you said three turns ago.

I've been comparing three competing speech-to-speech architectures — Moshi/PersonaPlex, Qwen2.5-Omni, and the classic ASR→LLM→TTS cascade — while building conversational systems in production. The benchmarks focus on latency. The real differences are elsewhere.

Here's what I found 👇

🎙️ Audio-native models (Moshi, PersonaPlex) win on conversational naturalness — real interruptions, backchanneling, overlapping speech. But their audio token budgets limit how much context you can inject. More knowledge in the prompt = less room for conversation history.

🧠 Qwen2.5-Omni's Thinker-Talker separation keeps reasoning in latent text/audio aligned space. This is a good design decision because it allows more reasoning power to be injected into the system. But true full-duplex is harder to achieve with this split.

⚙️ The cascade pipeline everyone dismisses? It still wins for knowledge-grounded, goal-oriented agents. 128K+ token context, native RAG, independently upgradeable components. The weakness isn't latency — it's the complete absence of natural turn-taking.

🎯 PersonaPlex showed that ~5,000 hours of directed fine-tuning on Moshi weights is enough to add persona control and task adherence. That's a feasible training run.

The key question nobody's answering yet: can the Thinker-Talker approach achieve Moshi-level duplex naturalism while keeping its knowledge injection advantage? If yes, it becomes the dominant architecture. If not, we'll see hybrid systems — audio-native front-end for conversational feel, text-domain reasoning layer for structured tasks.

No universal winner. Architecture choice depends on whether you need natural conversation or strict procedural adherence.

📝 Full comparison with architecture deep-dives: https://ai.ksopyla.com/posts/voice-to-voice-models-2026-review/

What architecture are you using (or evaluating) for voice agents in production?

#AIResearch #SpeechAI #VoiceModels #DeepLearning #ProductionAI
