---
title: "Speech-to-Speech Models in 2026: Three Architectural Bets and What Each Actually Gives You"
date: 2026-02-27
draft: true
description: "An honest technical comparison of Moshi, NVIDIA PersonaPlex, Qwen2.5-Omni, and OpenAI gpt-realtime. Which architecture wins on naturalness, script adherence, and knowledge grounding — and what no one tells you about deploying them."
icon: "microphone"
tags: ["Speech AI", "Voice Models", "Full Duplex", "Architecture", "Production AI"]
categories: ["AI Research"]
featureImage: "feature_speech_to_speech_architectures.png"
featureAlt: "Abstract digital painting of two intertwining audio streams — warm orange and electric teal — representing competing speech-to-speech AI architectures."
showReadingTime: true
---

{{< lead >}}
Moshi showed that a voice model can listen and speak simultaneously. PersonaPlex showed you can tell it who to be. But when you need the agent to actually remember what happened yesterday, follow a structured script, or pull in domain knowledge — the architecture you chose at the start determines whether any of that is even possible.
{{< /lead >}}

## The Real Story Is Not Latency

The narrative around speech-to-speech AI tends to center on latency. Moshi achieves 160ms. PersonaPlex maintains 205ms while handling interruptions. The cascade pipeline takes "seconds." These numbers get quoted in every benchmark tweet and paper abstract.

But latency is a solved problem at this point — at least at the first-response level. The more interesting question is what happens after the first response: Can the model stay on task? Can it know who it's talking to? Can it remember what you said three turns ago? And if you try to give it that memory, does the whole latency advantage evaporate?

I've been watching this field closely while building conversational systems in production, and the honest picture is more nuanced than the benchmarks suggest. Three fundamentally different architectures are competing right now, each with a coherent technical thesis and a specific set of trade-offs. None of them wins on everything.

---

## Three Competing Architectures

### Moshi and PersonaPlex: Audio-Native Full-Duplex

[Moshi](https://arxiv.org/abs/2410.00037) ([GitHub](https://github.com/kyutai-labs/moshi)) (Kyutai, September 2024) is the reference model that changed how this field thinks about voice AI. Its core idea is straightforward but technically demanding: model both the user's audio and the system's audio simultaneously, on parallel streams, using the same underlying model. This is what "full-duplex" actually means — not just fast response, but genuinely concurrent listening and speaking.

The architecture uses a Temporal Transformer processing the conversation over time, a Depth Transformer operating on audio codec layers, and the Mimi neural audio codec running at 12.5Hz and 1.1 kbps. Mimi was designed specifically to produce tokens at a rate LLMs can process in real time — this design decision is what makes the end-to-end approach feasible. The underlying language model is Helium (7B parameters), pretrained on 2.1 trillion tokens.

The most architecturally interesting technique is the **Inner Monologue** method. Rather than generating only audio tokens, Moshi also predicts time-aligned text tokens as a prefix to each audio token. This text stream is never spoken — it's an internal reasoning layer that improves linguistic coherence without abandoning the audio-native pipeline. A practical side effect: Inner Monologue gives you streaming ASR and TTS transcriptions for free, since the text predictions correspond to what's being said.

What Moshi couldn't do was be anyone in particular. It had one voice, one personality, and no way to change either. This severely limited its usefulness for any application requiring role-specific behavior.

**[NVIDIA PersonaPlex](https://research.nvidia.com/labs/adlr/personaplex/)** ([paper](https://research.nvidia.com/labs/adlr/files/personaplex/personaplex_preprint.pdf) | [GitHub](https://github.com/NVIDIA/personaplex) | [HuggingFace](https://huggingface.co/nvidia/personaplex-7b-v1)) (January 2026) builds directly on the Moshi architecture and addresses this limitation. The core addition is a **hybrid prompting system**: a text prompt that defines the role, background, and personality of the agent ("you work for First Neuron Bank, your name is Sanni Virtanen, a transaction of $1,200 was flagged for an unusual location"), and a voice prompt — an audio embedding that captures the vocal characteristics, accent, and prosody of a desired speaker. Both conditioning signals are injected into the Moshi backbone.

The training approach behind PersonaPlex is worth examining carefully, because it explains why it works where you might expect it to fail. NVIDIA blended two very different data sources:

- **1,217 hours of real human conversations** from the [Fisher English corpus](https://catalog.ldc.upenn.edu/LDC2004S13), which contains genuine backchanneling, overlapping speech, hesitations, and the natural messiness of human interaction. These were back-annotated with personality and role descriptions using GPT-OSS-120B.
- **2,250 hours of synthetic dialogues** covering customer service and assistant scenarios, generated by Qwen3-32B and synthesized into audio with [ChatterBox TTS](https://github.com/resemble-ai/chatterbox). These conversations are artificial but cover a wide range of roles, topics, and instruction types.

The result is a model that inherits naturalness from the real conversations and task-following ability from the synthetic ones. The hybrid prompt format serves as the bridge — the same prompt structure is used across both data sources, so the model learns to separate "how to sound human" from "what role to play." NVIDIA's finding: approximately 5,000 hours of directed fine-tuning on pretrained Moshi weights is sufficient for this specialization.

On [FullDuplexBench](https://arxiv.org/abs/2503.04721), PersonaPlex achieves 100% user interruption success rate (compared to 43.9% for Gemini Live and 60.6% for Moshi), average latency of 205ms, and a task adherence score of 4.34/5 for assistant scenarios and 4.40/5 on NVIDIA's own ServiceDuplexBench for customer service roles. For comparison: Moshi scores 1.26/5 on task adherence, Qwen2.5-Omni scores 3.82, and Gemini Live scores 3.68.

These are self-reported NVIDIA numbers. Independent reproduction would be welcome.

### Qwen2.5-Omni: Thinker-Talker Separation

Alibaba's [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215) ([blog](https://qwenlm.github.io/blog/qwen2.5-omni/) | [GitHub](https://github.com/QwenLM/Qwen2.5-Omni)) (March 2025) takes a fundamentally different architectural approach. Rather than processing audio natively throughout the model, it separates reasoning from speaking into two distinct components:

The **Thinker** is a multimodal large language model that processes all input modalities — text, audio, images, video — and produces reasoning in the text and hidden state domain. The **Talker** is a separate dual-track autoregressive model that converts the Thinker's hidden representations into streaming audio tokens in real time. A custom position embedding called TMRoPE synchronizes audio and video timestamps to keep the modalities temporally coherent.

The architectural consequence of this separation is significant. Because the Thinker operates entirely in text/hidden state space — not raw audio tokens — everything that the LLM ecosystem has built becomes available: long context windows, tool calls, function calling, retrieval injection. The Talker only needs to handle the audio generation, which it does with streaming output that begins immediately as the Thinker produces hidden states.

The trade-off is that true simultaneous listening-and-speaking — the way Moshi's dual audio streams work — is harder to achieve. The Thinker processes inputs and produces states; the Talker converts them. This is near-duplex rather than strictly full-duplex, which shows in the benchmark numbers: 257ms average latency vs Moshi/PersonaPlex's 200–240ms range.

Qwen2.5-Omni is also the only architecture here with full multimodal capability out of the box — it handles image, video, audio, and text in a single model. Available in 7B and 3B variants, with the 3B designed for edge deployment.

### Streaming ASR → LLM → TTS: Still Deployed, Still Relevant

The cascade pipeline gets dismissed in speech-to-speech literature as the thing we're moving away from. This is somewhat misleading in production contexts.

With streaming ASR (real-time transcription as the user speaks), a capable LLM, and a low-latency TTS engine, the cascade achieves sub-1-second end-to-end latency. The latency is not seconds by default — that's the naive implementation. With streaming and sentence-level output, it's a competitive pipeline for many real applications.

Its genuine strengths are hard to replicate in audio-native architectures:
- The LLM component handles 128K+ token context windows natively, without audio token budget constraints
- RAG integration is architecturally trivial — the LLM is already processing text
- Tool calls, function calling, structured outputs all work natively
- The pipeline components are independently upgradeable and debuggable
- Proven at production scale

The actual weakness of the cascade is not latency. It's the complete absence of duplex conversational behavior. The system must detect the end of the user's turn, process it, and respond. There is no overlapping speech, no natural backchanneling ("mm-hmm", "I see"), no mid-sentence interruption capability. Even at sub-1-second response time, the conversational rhythm feels turn-based and robotic compared to a true duplex system — because it is.

---

## Companions vs. Goal-Oriented Agents

There is a more important distinction than "full-duplex vs. cascade," and the field's benchmarks haven't caught up to it yet.

Speech-to-speech models are predominantly trained on conversational data — people chatting, telling stories, asking and answering questions. This training distribution makes them very good at one kind of task: being an engaging companion. But it makes them unreliable at a different kind of task: being a goal-oriented agent that must follow structured procedures across multiple turns.

The difference matters because most commercially valuable voice applications are goal-oriented:

- **Customer service**: Verify customer identity, retrieve account details, resolve the specific issue, escalate if needed — in that order, with appropriate handling for each branch.
- **Medical intake**: Collect name, date of birth, allergies, medications, prior conditions — never skip a field, never improvise advice, handle sensitive answers with care.
- **Technical support**: Walk through a troubleshooting tree, adapt based on user responses, know when to suggest escalation.
- **Language tutoring**: Elicit specific grammatical structures, wait for the student to produce them, provide targeted correction at the right moment — not just have a pleasant conversation about the weekend.
- **Interview practice or coaching**: Ask structured questions in sequence, evaluate responses, give calibrated feedback.

PersonaPlex's task adherence scores (4.34–4.40/5 on assistant and customer service benchmarks) show meaningful progress in this direction. The synthetic customer service training data — covering identity verification, pricing explanation, appointment scheduling — gives it procedural instruction-following ability that Moshi completely lacks (1.26/5).

But those benchmarks test relatively contained, single-turn instruction following: follow this role description, answer this question, handle this scenario. Multi-turn structured goal pursuit — following a lesson plan across fifteen turns, maintaining a troubleshooting tree state, ensuring a medical intake form is fully completed — is not yet benchmarked in the published literature.

OpenAI's [gpt-realtime](https://platform.openai.com/docs/guides/realtime) model (released August 2025) specifically optimized for complex instruction following, tool calls, and word-for-word script reading. For applications requiring rigid procedural adherence, the closed API still has an advantage. PersonaPlex's training approach — blending synthetic task-specific data with real conversational data — is the right direction for closing this gap in open-source models, but it hasn't closed it yet.

---

## The Knowledge Problem: Context, RAG, and What Actually Works in Production

Every useful voice agent eventually needs to know things that aren't baked into its weights. Who is this user? What happened in the last session? What products does the company sell this week? This is where the architectural choices become consequential in ways the latency benchmarks don't reveal.

**Stuffing context into the prompt** is the first and simplest approach. Include the user's profile, session history, preferences, and relevant facts in the system prompt. No retrieval latency, no additional infrastructure. The problem for audio-native models is an audio token budget constraint: Moshi and PersonaPlex process audio at 12.5Hz, consuming context rapidly. The more background knowledge you load into the context, the less space remains for the conversational audio history the model needs for coherent, non-repetitive responses. The cascade pipeline sidesteps this entirely — the LLM sees text, can hold 128K+ tokens of context natively, and audio history doesn't compete with background knowledge for the same token budget.

**Adding RAG** is the second impulse. Build a vector index of relevant documents, user history, session summaries, and retrieve dynamically based on what the user is saying. In a text-based LLM pipeline, this is well-understood engineering. In a full-duplex voice system, it creates a specific timing problem: a full-duplex model targets 160–200ms response time, and a standard vector database lookup takes 50–300ms depending on index size and infrastructure. If you run retrieval after the user finishes speaking, you add that latency directly to the response window and break the duplex illusion you built the system to provide.

Mitigations exist. You can run streaming ASR in the background while the user is still speaking and fire retrieval queries before they finish — "speculative retrieval" that mirrors how humans prepare contextual memories during listening rather than after. You can pre-load likely contexts at session start. Semi-cascaded architectures like FireRedChat run retrieval in parallel with audio processing. But each of these adds substantial engineering complexity, and none of them fully eliminates the latency cost.

The Thinker-Talker architecture has a structural advantage here. Because the Thinker operates on text and hidden states rather than raw audio tokens, retrieved context can be injected into the Thinker's input without competing with audio token budgets. The Talker converts the resulting hidden states into audio. The latency of retrieval still exists, but the integration is architecturally cleaner.

The honest summary: for knowledge-grounded voice conversations in production today, the cascade pipeline remains the most practical architecture. It wasn't built for natural conversation. But it was built for everything else a voice agent needs to actually be useful.

---

## Open Source vs. Closed Source: A Genuine Trade-Off

The instinct to frame open-source deployment as "faster because no network hop" is too simple, and it deserves a more careful look.

### Where open source has real advantages

- Fine-tuning on domain-specific data. PersonaPlex demonstrated that 5,000 hours of directed fine-tuning on top of Moshi pretrained weights is enough to specialize a model for a new domain. That's a feasible training run for well-resourced teams.
- Full control over Voice Activity Detection thresholds, backchanneling behavior, and the Mimi codec parameters — important when the model's turn-taking behavior doesn't match your product's conversational style.
- No per-token API cost for audio streaming, which becomes significant at scale.
- Architecture transparency for debugging unexpected behavior in production.

### Where closed source has real advantages

- OpenAI's infrastructure includes regional deployments, especially through Azure. The network latency argument against cloud APIs weakens considerably when the endpoint is deployed in the same region as your users.
- Script-following and tool-calling capabilities remain stronger in [gpt-realtime](https://platform.openai.com/docs/guides/realtime) as of early 2026.
- No GPU infrastructure to manage. For teams without ML ops capability, self-hosting a 7B model with real-time audio inference is a substantial operational commitment.
- Semantic VAD — using a classifier to determine whether the user has actually finished their thought vs. pausing mid-sentence — is available in OpenAI's Realtime API and is harder to replicate from scratch.

The honest frame: even open-source models deployed on "edge" still have network latency between the user and your server. It might be 20ms instead of 80ms, but it's not zero. A well-deployed cloud API with regional endpoints might offer 60ms network latency with superior instruction-following out of the box. The right choice depends on your scale (API costs vs. GPU infrastructure costs), your team's capabilities, how much domain fine-tuning you actually need, and whether natural conversation or strict procedural adherence matters more.

There is no universal winner here.

---

## What This Means in Practice

The most useful framing isn't "which model is best" but "which architecture matches the constraint that actually binds your application."

| What you need most | Best current option |
|---|---|
| Maximum conversational naturalness, real interruptions, backchanneling | Moshi / PersonaPlex (audio-native) |
| Custom persona, open weights, fine-tunable | PersonaPlex |
| Knowledge grounding, long context, RAG, tool calls | Streaming ASR→LLM→TTS cascade |
| Full multimodal (voice + vision + text) | Qwen2.5-Omni |
| Strict script adherence, minimal ops overhead | OpenAI gpt-realtime API |

Most non-trivial production applications will end up combining elements: a full-duplex model for conversational feel with an external orchestration layer managing session state, user history, and goal tracking. The speech-to-speech model handles the "feels human" part; the orchestration layer handles the "actually useful" part.

The open technical question that will determine which architecture eventually wins: can the Thinker-Talker separation achieve Moshi-level duplex naturalism while retaining its knowledge injection advantage? If yes, it becomes the dominant approach. If not, the field will converge on hybrid systems where an audio-native front-end (PersonaPlex or its successors) hands off to a text-domain reasoning layer for structured tasks.

I don't think we're at the point where any of these models replaces a well-built streaming ASR pipeline for production structured applications. But the gap between "natural companion" and "useful agent" is narrowing, and the pace of progress between Moshi (September 2024) and PersonaPlex (January 2026) suggests it will narrow faster than most people expect.

---

## References

1. Défossez, A. et al. (Sep 2024). [**Moshi: a speech-text foundation model for real-time dialogue**](https://arxiv.org/abs/2410.00037). Kyutai. arXiv:2410.00037
2. Roy, R. et al. (Jan 2026). [**PersonaPlex: Voice and Role Control for Full Duplex Conversational Speech Models**](https://research.nvidia.com/labs/adlr/files/personaplex/personaplex_preprint.pdf). NVIDIA ADLR.
3. Xu, J. et al. (Mar 2025). [**Qwen2.5-Omni Technical Report**](https://arxiv.org/abs/2503.20215). Alibaba Qwen Team. arXiv:2503.20215
4. Lin, G-T. et al. (Mar 2025). [**Full-Duplex-Bench: A Benchmark to Evaluate Full-duplex Spoken Dialogue Models on Turn-taking Capabilities**](https://arxiv.org/abs/2503.04721). arXiv:2503.04721
5. Cui, W. et al. (Oct 2024). [**Recent Advances in Speech Language Models: A Survey**](https://arxiv.org/abs/2410.03751). arXiv:2410.03751

*PersonaPlex benchmark numbers are NVIDIA-reported. Independent reproduction has not been published at time of writing.*
