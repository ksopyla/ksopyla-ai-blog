# Writing Preferences & Style Guide

Single source of truth for how Krzysztof writes and what he expects from AI-generated drafts. The content-drafting skill reads this file before producing any long-form content.

Last updated: 2026-04-12

---

## Voice And Editorial Standards

### Baseline Voice

- Write in first person when sharing experience or judgment.
- Stay modest. Prefer "I found something interesting" over breakthrough language.
- Be precise and technical. Use correct terms and real numbers.
- Be honest about failure modes, uncertainty, and negative results.
- Stay curious rather than dismissive when critiquing papers or trends.
- Avoid hype words: `game-changing`, `revolutionary`, `mind-blowing`, `groundbreaking`.
- Keep it educational and readable, not academic for its own sake.
- Avoid corporate-marketing phrasing.

### Kill List — AI-Sounding Filler Phrases

Never use these (or equivalents):

- "Let's dive in"
- "In this article, we'll explore"
- "It's worth noting that"
- "Here's the thing"
- "Without further ado"
- "At the end of the day"
- "Here's the part most tutorials skip"
- Any sentence that could open any article on any topic

Replace with a specific, concrete statement that only works for this article.

---

## Writing Quality Rules

These rules were extracted from real multi-round drafting sessions. They capture recurring patterns in how Krzysztof writes and what he rejects.

### 1. Never write shallow summaries — extract specific details from sources

Do not paraphrase a blog post as "Phil Schmid says design for outcomes." Instead, extract the concrete example: "A bad MCP server exposes `get_user_by_email()`, `list_orders(user_id)`, `get_order_status(order_id)` — three tools, three round-trips. A good one exposes `track_latest_order(email)` — one call, one answer."

Before writing any claim backed by a source, re-read the actual source article (not just notes about it). Pull: specific numbers, named examples, before/after comparisons, version histories, and real tool/function names.

### 2. Every factual claim needs a linked reference

If you write "accuracy degrades as tool count increases," the next sentence must have a link with specific numbers: "Grok 4.1 Fast dropped from 86.7% to 76.7% across 25→150 tools." Unlinked claims get flagged with `??` and waste a revision round.

### 3. Write from the builder's point of view, not the user's

If the article is advice for people building MCP servers, do not open with "You install some MCP servers in Claude Code..." That is the user's perspective. Open with: "If you're building an MCP server for enterprise use, your design choices shape every agent that integrates with you." Match the POV to the audience being advised.

### 4. Merge sections that say the same thing

If two sections make the same argument from slightly different angles, merge them. One section with both perspectives is stronger than two sections that feel repetitive.

### 5. Preserve Krzysztof's rewrites exactly

When Krzysztof edits code examples, variable names, function signatures, or inline prose, those edits are final. Do not reformat, rename, or "improve" them. His phrasing in edited sections is the target voice.

### 6. Use analogies from the sources, not invented ones

If a source uses a good framing or metaphor, use it with attribution. Attributed analogies are more credible and more interesting than generic invented ones.

### 7. Opinionated claims need to be labeled as opinions

"A great MCP server has 2-4 tools, max" is an opinion. Label it: "My controversial take:" or "My opinion:". This keeps the article honest and signals that it's a judgment call, not a rule.

### 8. Research notes are a starting point, not a sufficient source

Notes files contain summaries and pointers. They are not deep enough to write strong prose from. Before writing any section, go back to the actual source URL and re-read it. The difference between a weak draft and a strong one is whether the writer read the summary or the original.

---

## Content-Specific Preferences

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

## References & Citations

### Format

Every blog post that cites papers, models, or benchmarks must end with a proper `## References` section — a numbered list, one entry per line, in this format:

```
Author, F. et al. (Mon YYYY). [**Full paper title as on arxiv/venue**](url). Institution/venue. arXiv:XXXX
```

Example:
```markdown
## References

1. Défossez, A. et al. (Sep 2024). [**Moshi: a speech-text foundation model for real-time dialogue**](https://arxiv.org/abs/2410.00037). Kyutai. arXiv:2410.00037
2. Roy, R. et al. (Jan 2026). [**PersonaPlex: Voice and Role Control for Full Duplex Conversational Speech Models**](https://research.nvidia.com/.../personaplex_preprint.pdf). NVIDIA ADLR.
```

### Rules

- **Link text = full paper title, in bold** — never just the model name or a shortened label
- **Always fetch the real title** from arxiv.org or the project page — do not guess or abbreviate
- **Include**: first author + "et al.", date (month + year), linked bold title, institution, arXiv ID (if applicable)
- **Add a separate italic caveat line** below the list when numbers are self-reported or unverified (e.g. `*PersonaPlex benchmark numbers are NVIDIA-reported. Independent reproduction has not been published at time of writing.*`)
- **Do NOT use inline dot-separated links** like `Papers: Moshi · PersonaPlex · ...` — these wrap badly on mobile and look unprofessional
- The `## References` heading automatically appears in the Congo ToC sidebar, which is a useful navigation anchor for longer posts
- arXiv IDs are worth keeping even when the title is linked — technical readers copy-paste them into tools like Semantic Scholar and Zotero

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
