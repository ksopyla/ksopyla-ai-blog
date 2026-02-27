# Writing Preferences & Feedback Log

This file tracks what Krzysztof likes and dislikes in AI-generated drafts, so future writing respects his style and avoids repeated mistakes.

---

## General Preferences & Style

### Accuracy First
- **Never overstate or exaggerate claims.** If a number or timeline isn't verified, don't use it. "Seconds of delay" is wrong if streaming pipelines achieve sub-1s. Hedge with "can range from X to Y depending on..." rather than picking the worst case to make a point.
- **Seek truth, be blunt and honest.** Don't believe marketing materials. Find supporting evidence, compare, verify numbers against benchmarks and papers, not blog announcements.
- **If unsure about a date or fact, say so and try to find the evidence.** Don't fabricate timelines like "until late 2025" without evidence.

### Balanced Analysis
- **Never push a single winner.** Present pros and cons of each approach honestly. Open source vs closed source is not a clear fight — both have strengths. Present the trade-offs and let the reader decide.
- **Consider what the reader might already know.** Don't write as though everyone is unaware of streaming ASR pipelines — the audience is technical.
- **Include counter-arguments proactively.** If an approach has a clear weakness, mention it. If the competing approach has a clear strength, acknowledge it.

### Tone & Framing
- **Don't center the article around one narrow use case.** Krzysztof's experience (e.g., conversational tutoring at Pearson) adds credibility but should be mentioned as one example among several, not as the sole lens. Show breadth.
- **Show, don't sell.** Building tutoring systems is mentioned to establish authority, not to make the whole article about tutoring.
- **Use concrete, diverse examples.** When discussing use cases (e.g., script adherence), go beyond one benchmark. Show customer service, tutoring, personal assistants, medical intake, coaching — demonstrate the pattern across domains.

### Technical Depth
- **Go deeper on architectures.** Krzysztof wants to understand *why* something works, not just *that* it works. Explain the architectural choices (Thinker-Talker, Inner Monologue, Mimi codec, hybrid prompting) and their technical implications.
- **Compare architectures head-to-head.** What specifically did PersonaPlex add on top of Moshi? What makes Qwen's approach different? These are the interesting questions.
- **Include product-specific implications.** What does an architectural choice mean for someone deploying this in production? Not just latency numbers — context window limits, knowledge injection feasibility, infrastructure costs, fine-tuning requirements.

### Structure
- **Conclusions matter.** Don't end with a summary. End with implications, predictions, and actionable insights. What should the reader do differently after reading this?
- **Technical deep-dives earn trust.** The audience values understanding the mechanism, not just the result.

---

## Article-Specific Feedback Log

### Voice-to-Voice Models 2026 Review (2026-02-27)

#### What was OK
- Paragraph 2 (Companions vs Tutors): Good framing, the distinction between "companion" and "goal-oriented agent" is strong. Keep this concept.
- PersonaPlex technical breakdown: The hybrid prompting (text + voice) analysis was appreciated.
- RAG latency tension: The core insight (RAG kills duplex latency) is valid and interesting.
- Cross-disciplinary connection (cognitive priming): Good.

#### What was NOT OK
1. **False claim: "ASR → LLM → TTS had seconds of delay"** — This is not true. Streaming pipelines achieve sub-1 second. The cascade approach has proven its usefulness in many production scenarios. Don't dismiss it to make full-duplex look better.
2. **Unverified timeline: "Until late 2025"** — Speech-to-speech models existed before that. Don't fabricate timelines.
3. **Tutoring over-emphasis** — The entire article was framed through a tutoring lens. Tutoring should be ONE example mentioned for credibility. Not the central angle. Show broader applicability.
4. **Companions vs Tutors: Too narrow examples** — Only used "customer service benchmark." Should include more diverse use cases: personal AI assistants, medical intake, coaching, technical support — show the pattern.
5. **RAG paragraph: Wrong starting point** — Should start from the *need* for personalization (the agent needs to know you, remember your history). Then introduce context window as the first approach (stuff everything into the prompt). Then explain why current speech-to-speech models struggle with large context windows — and why the ASR-LLM-TTS pipeline actually wins here because the LLM component can handle long contexts natively.
6. **Open Source vs Closed: Biased toward open source** — Was too pushy for open source without acknowledging: (a) even open source on "edge" still has network latency, (b) OpenAI has many regional deployments especially via Azure, (c) there is no clear winner. Present both sides fairly.
7. **Too shallow on architectures** — Needed more depth on Moshi's Inner Monologue, Qwen's Thinker-Talker, what exactly PersonaPlex adds on top of Moshi (hybrid prompting, Fisher data disentanglement, voice conditioning). The reader wants to understand the mechanism.
8. **Weak conclusions** — Ended with a one-line takeaway. Needs deeper analysis: product implications, architectural trade-off matrix, what to choose when.
