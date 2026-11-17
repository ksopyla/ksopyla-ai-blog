# Writing Preferences & Style Guide

Single source of truth for how Krzysztof writes and what he expects from AI-generated drafts. The content-drafting skill reads this file before producing any long-form content.

Last updated: 2026-11-17

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

### Kill List — Machine-Like Patterns

Krzysztof spots these as "written by AI" and rejects them:

- **Twist reveals and slogan endings:** "Wrong question.", "It was never about X. It was about Y.", a one-line motto as the last sentence.
- **Schematic, repeated openings:** sections or paragraphs that all start the same way ("Before AI, …", "In my experience, …"). Start each one from a different side: a scene, a question, a feeling, a number.
- **Obvious, banal lines:** "They rarely had a special title. They were the people other teams called first." If the sentence states what every reader already assumes, cut it.
- **Generic section intros:** "None of these signals is a title, and I have seen them in junior engineers too." Open with what the section actually gives the reader.
- **Data dumps:** several studies or numbers piled into one paragraph ("too much data, and feels not human"). One finding per point, spread across the argument.
- **Arrow bullets and decorative lists** where a sentence would do.

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

When he asks to "proof read" his edits, fix grammar, spelling and tense only, and keep his wording ("Before, I mostly managed and lead, now I took part…" → "Before, I mostly managed and led. Now I take part…"). When he gives a line to add ("often beauty is in simple idea that just work, I like those"), use it nearly verbatim with corrected grammar.

### 6. Use analogies from the sources, not invented ones

If a source uses a good framing or metaphor, use it with attribution. Attributed analogies are more credible and more interesting than generic invented ones.

### 7. Keep opinions in first person, without "My opinion:" labels

It is Krzysztof's blog, so everything in it is his opinion. Do not prefix claims with "My opinion:" or "My controversial take:" (rejected in the systems-thinkers draft, Nov 2026). Keep judgment calls honest through the voice instead: state them in first person ("I see", "in my teams", "my test"), and keep them visibly separate from claims attributed to a source. "A great MCP server has 2-4 tools, max" can stand as Krzysztof's claim, as long as it is not dressed up as a cited fact.

### 8. Research notes are a starting point, not a sufficient source

Notes files contain summaries and pointers. They are not deep enough to write strong prose from. Before writing any section, go back to the actual source URL and re-read it. The difference between a weak draft and a strong one is whether the writer read the summary or the original.

### 9. Public-facing surfaces stay humble, topic-first, and reader-friendly

Homepage, about page, projects index, post-list descriptions, RSS/SEO descriptions, and any first-touch surface follow stricter rules than a long-form article:

- **Lead with topics, not project brand names.** Readers landing on the homepage do not know what `MrCogito`, `Concept Reasoning Model`, or `Agent Patterns Lab` are. Say `agentic systems`, `concept-reasoning architectures`, `multi-agent patterns`, `AI team leadership`. Brand names belong on project pages and inside posts where context exists, not in the first sentence a stranger reads.
- **Be humble in framing, not promotional.** Prefer `Notes on…` to `This blog is where I write up…`. Prefer `I share what I try, what breaks, and what I think it means` to `the definitive guide to…` or `everything you need to know about…`. The motto and content carry the authority — the framing should not also try to.
- **One sentence is usually enough.** Public surfaces are not the place for three-clause architectural arguments. If a sentence has three "and" connectors and an em-dash, it is too long for a homepage alert.
- **Soft verbs over assertive ones.** `browse`, `read`, `share` over `jump into`, `dive into`, `master`. The motto `Build agents by day, train models by night, publish the mess` already does the assertive work — the rest of the surface should not compete with it.
- **Reader's goal first, author's identity second.** A homepage sentence should answer "what will I find here?" not "who is the author?". The bio and headline already handle identity.

This rule applies to: `content/_index.md`, `content/about.md`, `content/posts/_index.md`, `content/projects/_index.md`, frontmatter `description` fields, `config/_default/languages.en.toml` `bio` and `description`, and any RSS / OpenGraph / Twitter card copy.

It does *not* apply to: long-form blog posts, project pages, LinkedIn posts, X threads, or anywhere the reader has already opted into reading more from Krzysztof.

### 10. The post is Krzysztof's story; sources support it, never frame it

A post built around someone else's talk, paper or podcast reads "as not mine". Do not title sections "What the two talks agree on", do not put other people's quotes in the lead, and do not open with "X told Y that…". Open with Krzysztof's own question or observation, state his view, then bring in sources as proof: "I am not the only one saying it. In July, Netflix's CPTO told…". Sources can be cited heavily, but each one sits inside a paragraph that makes his point.

### 11. Show the path from observation to evidence

When a paragraph moves from Krzysztof's experience to research, show him investigating: he noticed something in his team, wondered whether it was only his team, went looking, and found work that confirms or explains it. An observation paragraph followed by an unconnected evidence paragraph "looks distinct, like written by AI". Smooth transitions between paragraphs matter; "too sharp transition" is a common `??`. Weave each finding into the sentence it supports (see also the memory note on blending evidence into prose).

### 12. Personal evidence must be recent, exact and his

- **Recent:** use experience from the AI era (roughly the last two years) when the argument is about AI. Do not pad with career history ("in my software house, in startups, and now at Pearson") unless it is the point.
- **Exact:** do not overstate personal facts. "My role changed from EM to staff engineer" was wrong; the truth was "my title did not change, but my role drifted toward staff engineer: I build more things myself with AI, where before I mostly managed and took part in RFCs". When a comment is ambiguous or cut off, write the best reading and flag it in the reply.
- **His:** do not invent anecdotes or scenes. Use the personal takes he writes into `??` comments. Leave at most one or two `TODO (Krzysztof)` story prompts; he deletes the ones he cannot fill, and too many make the draft feel like a form.
- **Pearson examples are real but anonymized:** conversational capability refactors, applied AI science with product owners, daily Snyk scans that can block a deployment. One Pearson example per point, not the whole lens.

### 13. Refer to organizations, not to people the reader does not know

"Stone says…" stops readers: "who is Stone?". Introduce a person once with name and role ("Elizabeth Stone, Chief Product and Technology Officer at Netflix"), then refer to the organization or the source: "Netflix found…", "the Netflix talk", "Google Research expects…". Hosts and interviewers rarely need a name at all.

### 14. Links in the text and in the References

Link sources inline where they are first used (on the verb phrase, e.g. "[told Lenny Rachitsky](url)"), and keep the numbered `[n]` markers and the `## References` list as well. Do not choose one or the other.

### 15. Simple language, precise terms

"Could you simplify the language" is the most frequent request. Use short sentences, everyday words and one idea per sentence. Replace phrases like "a generalist who dabbles" or "a deep craft who uses AI's wider range to build across it" with "someone who knows a little about everything" and "they know one area deeply and use AI to build beyond it".

Simplifying never means dropping the precise identifiers technical readers need. On the Cogi LinkedIn post he asked to bring back the benchmark names (`LongMemEval_M`, `LoCoMo`) and the token budgets after they were simplified away. Keep the term and add the plain explanation next to it: "a 1,000-token budget, about one page"; "LongMemEval_M: 500 questions, each answer hidden in about 1.2 million tokens of old chats".

### 16. Examples: technical, simple, close to the point

- Prefer small, concrete technical examples readers have lived: a Python import error, a failing cloud deployment, a container out of memory, a backend engineer editing a React component, a frontend developer writing Terraform.
- An example must illustrate the exact claim. "Join a cross-team review, meet the SRE team" was rejected for a point about relationships; what he meant was product and business people, people who understand user needs, and the people who build templates and processes and protect them. When an example is marked "weak", find one closer to the claim rather than polishing the old one.

### 17. Don't oversell Krzysztof's work

For his own projects (Cogi, MrCogito, Agent Patterns Lab) the bet is usually a simple idea done carefully, not an invention. Say plainly what it is before a critic does ("this is plain search over chat logs, built with care"), compare fairly against what was actually tested, and let the evals carry the claim. "Often, the beauty is in a simple idea that just works" is his framing.

---

## Content-Specific Preferences

### Accuracy First
- **Never overstate or exaggerate claims.** If a number or timeline isn't verified, don't use it. "Seconds of delay" is wrong if streaming pipelines achieve sub-1s. Hedge with "can range from X to Y depending on..." rather than picking the worst case to make a point.
- **Seek truth, be blunt and honest.** Don't believe marketing materials. Find supporting evidence, compare, verify numbers against benchmarks and papers, not blog announcements.
- **If unsure about a date or fact, say so and try to find the evidence.** Don't fabricate timelines like "until late 2025" without evidence.
- **Evidence must match the current state of AI.** Early AI-coding studies that assume humans write or review every diff (Faros PR review times, the METR slowdown RCT, CodeRabbit defect counts) are outdated for his arguments: agents write and review code now, and people guide. Prefer sources from the last year or two, or timeless ones (Brooks, DORA).

### Balanced Analysis
- **Never push a single winner.** Present pros and cons of each approach honestly. Open source vs closed source is not a clear fight — both have strengths. Present the trade-offs and let the reader decide.
- **Consider what the reader might already know.** Don't write as though everyone is unaware of streaming ASR pipelines — the audience is technical.
- **Include counter-arguments proactively.** If an approach has a clear weakness, mention it. If the competing approach has a clear strength, acknowledge it.
- **Size the limits to the post type.** In research, benchmark and tool posts, a fairness or limits section earns its place (the Cogi post kept "Is this a fair test?"). In leadership and column posts, Krzysztof removed standalone "Limits and counterpoints" sections twice: put the caveat in one or two sentences inside the argument or in the takeaway ("Going too far in the other direction isn't good; what matters most is that these people deliver results"), and leave the rest for the comments.

### Tone & Framing
- **Don't center the article around one narrow use case.** Krzysztof's experience (e.g., conversational tutoring at Pearson) adds credibility but should be mentioned as one example among several, not as the sole lens. Show breadth.
- **Show, don't sell.** Building tutoring systems is mentioned to establish authority, not to make the whole article about tutoring.
- **Use concrete, diverse examples.** When discussing use cases (e.g., script adherence), go beyond one benchmark. Show customer service, tutoring, personal assistants, medical intake, coaching — demonstrate the pattern across domains.

### Technical Depth
- **Go deeper on architectures.** Krzysztof wants to understand *why* something works, not just *that* it works. Explain the architectural choices (Thinker-Talker, Inner Monologue, Mimi codec, hybrid prompting) and their technical implications.
- **Compare architectures head-to-head.** What specifically did PersonaPlex add on top of Moshi? What makes Qwen's approach different? These are the interesting questions.
- **Include product-specific implications.** What does an architectural choice mean for someone deploying this in production? Not just latency numbers — context window limits, knowledge injection feasibility, infrastructure costs, fine-tuning requirements.

### Structure
- **Length.** Every blog post stays under 2,500 words. Ideal is under 10 minutes of reading (Hugo shows it next to the date); 11 minutes is fine. One post tells one story; if there are two, split them.
- **Conclusions matter.** Don't end with a summary. End with implications, predictions, and actionable insights. What should the reader do differently after reading this?
- **Technical deep-dives earn trust.** The audience values understanding the mechanism, not just the result.
- **Trust the reader with "how-to" sections.** If the body already shows what to do, a long advice section repeats it. Keep the three most important items, not five or seven.
- **Merge and dedupe across rounds.** After adding his notes, check that no idea now appears twice; "this is similar to the previous paragraph, maybe concat" is a frequent `??`. Merging is better than a fourth point.
- **Grow what he marks as valuable.** "This is valuable, elaborate" means add a concrete example and a source, not more abstract sentences.
- **Make the core claim stand out.** One key idea per post can go in a Congo callout (`{{< alert "lightbulb" >}}…{{< /alert >}}`). Emojis on section headings, subheadings that split long sections, and one pull quote per main section work well (the "What AI quietly broke" post layout). When a LinkedIn post accompanies the blog, reuse the same emojis so the two correlate.

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

## Review Rounds With `??` Comments

Krzysztof reviews drafts in the file. Each round:

1. **Snapshot first.** Commit the draft with his comments before changing anything, so every round can be compared.
2. **Read the comment's position.** A `??` line usually refers to the text right below it; `^^` or "above" points up; a `??` inside a sentence refers to that sentence. A bare `??` means "this point needs work": rewrite it or merge it, do not leave it as is.
3. **Classify each comment:**
   - *Content he supplies* (his experience, a new angle, a line to add): build the paragraph around his words.
   - *Keep signals* ("good one, I like it", "really good summary", "keep"): do not touch that text.
   - *Rejections* ("I don't like this", "sounds not mine", "too obvious"): replace the idea, not just the wording.
   - *Structure* ("too long", "concat", "shrink to three", "move to takeaway"): restructure, then check for duplicates.
4. **Remove every `??` marker** and every `TODO` he has answered or made obsolete.
5. **Report per comment** in the reply: what changed, quoted where useful, and flag any comment that was cut off or ambiguous along with the reading you chose.
6. **Check length** against the 2,500-word limit and name what to cut when his additions push it over.
7. **When his feedback contradicts this guide, his feedback wins.** Update this file in the same session (rule 7 changed this way).

---

## Article-Specific Feedback Log

### Systems Thinkers Draft (2026-11-15 to 2026-11-17)

Three `??` rounds on `content/drafts/systems-thinkers/`, a column built on a Netflix podcast and a Google Research talk.

- **Round 1:** the draft was framed around the two talks ("What the two talks agree on", talk quotes in the lead). Rejected as "not mine". Rebuilt to open with his question (the most important skill for a software engineer when AI widens what one person can build) and to use the talks as proof. Readers did not know who "Stone" was, so the text now refers to Netflix and Google Research. The seven signals became six, the how-to section shrank to three habits, and the Limits section moved into two sentences of the takeaway.
- **Round 2:** only recent evidence (the last two years, AI era), and people with context are not only developers. Inline links plus References. His role "drifted", it did not "change". The example of relationships with SRE and security was replaced by product, business and systems people. New claims he added: AI cannot replace systems thinkers because it lacks their context and taste for what to build; depth earns trust and technology understanding while AI widens the range.
- **Round 3:** no "My opinion:" labels (it is his blog). The core claim went into a callout. Why depth matters: time spent on hard problems in one area (technology, finance, methodology of learning) lets people decompose problems and connect components at a deeper level. Two context paragraphs merged. Context for agents means business, user needs, strategy and roadmaps, not only what sits between teams; documentation is written for agents, not humans. "Simplify the language" again.

### What AI Quietly Broke In My Engineering Team (2026-10-12 to 2026-10-14)

- Research presented as a list of studies "reads hard": blend each into the paragraph it supports.
- Early AI-coding productivity studies cut as outdated.
- "Find a good transition from my observation to the evidence… I would like readers to see that I tried to understand this phenomenon": show him investigating (rule 11).
- "The same opening, too schematic and repetition, start differently, start with psychology": vary section openings.
- He added personal passages (Stack Overflow badges, solving algorithm puzzles at university as a group, local meetups) and asked to extend the collective-creativity point: the human details became the emotional peak of the post and the LinkedIn version.
- Limits section and unfillable `??STORY` prompts removed.
- LinkedIn version: technical but simple examples ("something related to the cloud or Python code"), emojis matching the blog, no twist reveal, no arrow bullets, no slogan ending.

### Cogi Memory Evals Post (2026-11-01 to 2026-11-11)

- First draft centered on a benchmark finding. Rejected: "this is not what I wanted to write". The post he wanted told why he built Cogi, what it is and where it is strong, then the evals, with an honest note that benchmarks do not match real usage.
- Then simplified for a general audience: about 1,100 words, token budgets explained in pages.
- "I don't want to sound like I invented something big": the idea section became "plain search, built with care", with a fair comparison of what was actually tested (rule 17).
- LinkedIn: "simplify the language", then "keep the benchmark names, those are important" and "and token budget also" (rule 15). His closing line was kept nearly verbatim.

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

### Homepage Tagline And Public Surfaces (2026-04-26)

Round of edits on `content/_index.md`, `content/about.md`, `content/projects/_index.md`, `content/posts/_index.md`, the Hugo `bio`, and the blog manifesto. The persona was correct, but the public-facing copy leaned too positional and used internal brand names readers do not recognize. See Writing Quality Rule 9 for the full rule.

#### What got rewritten

**Homepage alert (`content/_index.md`)**

- Before: *"This blog is where I write up enterprise agent architecture, MrCogito research notes, and the occasional honest leadership lesson — what I tried, what broke, and what I think it means. Start with the blog manifesto or jump straight into the projects."*
- After: *"Notes on agentic systems, concept-reasoning architectures, and leading AI teams. I share what I try, what breaks, and what I think it means. Start with the blog manifesto or browse the projects."*

#### What changed and why

1. **Drop unknown brand names from first-touch surfaces.** `MrCogito` is meaningless to a stranger landing on the homepage. Replace with the topic the brand sits inside — `concept-reasoning architectures`. The brand name only helps once the reader has clicked through.
2. **Lead with topics, not the act of writing.** `Notes on X, Y, Z` is humble and reader-first. `This blog is where I write up X, Y, Z` puts the author and the act in the foreground.
3. **Compress to one sentence per idea.** The before-version had three clauses joined by an em-dash and a parenthetical aside. One topic sentence + one process sentence + one navigation sentence is enough on a homepage.
4. **Soften verbs.** `browse the projects` over `jump straight into the projects`. The motto already does the loud, confident work — the explanatory line should not compete with it.
5. **Apply the same rule consistently across surfaces.** Once the homepage was simplified, the about page, projects index, and posts index were checked for the same anti-patterns (insider brand names, three-clause sentences, promotional verbs).
