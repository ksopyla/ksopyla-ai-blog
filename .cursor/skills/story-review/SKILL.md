---
name: story-review
description: Review blog posts, articles, and LinkedIn posts for narrative quality, storytelling structure, and human interest. Use when asked to review content as a story, improve the opening hook, add personal depth, check if the article is interesting beyond its technical content, or annotate a draft with storytelling hints.
---
# Story Review

## Purpose

This skill reviews content through the lens of storytelling craft and human interest.

It does not own topic selection, technical accuracy, scoring, or publishing mechanics. Those belong to `content-discovery`, `content-drafting`, and `content-publishing`.

This skill answers one question: **would a smart, busy reader actually want to finish this piece?**

## When To Use

- The user asks to review a post "as a story" or "from a human perspective"
- The user wants to improve the opening or hook
- The user wants the article to feel more personal, more honest, or more engaging
- The user asks for storytelling feedback, narrative structure review, or drama
- The user wants inline annotations that prompt them to add personal detail
- Before publishing, as a narrative quality gate alongside the editorial pass

## Stage Boundary

- This skill reads and annotates. It does not rewrite the whole article.
- It produces a **narrative assessment** and **inline annotations** in the draft.
- The user decides which suggestions to accept. The agent can propose rewrites only when asked.

## The Review Process

### Step 1: Read The Whole Piece First

Read the full article before making any judgment. Do not annotate while reading the first time.

### Step 2: Identify The Story Type

Most technical articles follow one of these narrative shapes. Identify which one the piece is using, or should be using:

**The Realization**
Something happened that changed how you think. The reader follows your shift.
Arc: old belief -> event or evidence -> uncomfortable truth -> new understanding

**The Expedition**
You went deep into a problem. The reader follows your journey.
Arc: question -> exploration -> dead ends -> discovery -> lesson

**The Argument**
You believe something others do not. The reader weighs your case.
Arc: contrarian claim -> why people disagree -> your evidence -> nuance -> conclusion

**The Failure Report**
Something did not work. The reader learns from your honesty.
Arc: what you tried -> what went wrong -> what you learned -> what you would do differently

**The Framework**
You built a mental model. The reader adopts or adapts it.
Arc: messy problem -> your organizing principle -> how it applies -> limits

If the piece does not fit any shape, that is often the core problem.

### Step 3: Assess The Opening

The opening paragraph is the most important part of any article. It must earn the next paragraph.

Check these qualities:

- **Tension**: Does the opening create a question the reader wants answered?
- **Specificity**: Does it name a real situation, not an abstract concept?
- **Personal stake**: Is the author present in the first 3 sentences?
- **Honesty**: Does it feel like a real person talking, not a summary?
- **Speed**: Does it reach the interesting part within 50 words?

Rate the opening:

- `5/5 — Stops the scroll.` The reader is hooked within 2 sentences.
- `4/5 — Strong start.` Clear tension, but could be sharper or more specific.
- `3/5 — Decent but generic.` Reads like an introduction, not a hook.
- `2/5 — Slow warm-up.` The real story starts 2-3 paragraphs later.
- `1/5 — Abstract or corporate.` No human presence, no tension, no reason to keep reading.

### Step 4: Check For Emotional Beats

Technical content becomes memorable when the reader feels something alongside the author. Scan for these:

- **Surprise**: A moment where the author (or reader) did not expect the outcome.
- **Frustration**: A genuine struggle, not a sanitized summary.
- **Vulnerability**: The author admitting they were wrong, confused, or defensive.
- **Relief or satisfaction**: The moment something finally clicked.
- **Curiosity**: A question that pulls the reader forward.

If the article has zero emotional beats, it reads like documentation, not a story.

### Step 5: Check For The Human Thread

Ask these questions:

1. Can the reader picture a real person writing this?
2. Is there at least one moment where the author shares how they felt, not just what they thought?
3. Does the article reveal something the author learned about themselves, not just about the technology?
4. Would a non-technical colleague find at least the opening and closing interesting?
5. Is there a single sentence that only this author could have written?

### Step 6: Check Structure And Pacing

- Does the article have a clear beginning, middle, and end?
- Does each section earn the next one, or does it just list points?
- Is there a moment of highest tension or insight (the peak)?
- Does the peak happen too early, too late, or at the right place (usually 60-70% through)?
- Does the ending land, or does it trail off into a generic summary?

### Step 7: Produce The Narrative Assessment

Output a short assessment using this format:

```markdown
## Narrative Assessment

**Story type**: [which shape the article follows or should follow]
**Opening score**: [1-5] — [one sentence explanation]
**Emotional beats found**: [list the moments, or "none detected"]
**Human thread**: [present / weak / missing] — [one sentence]
**Pacing**: [front-loaded / well-paced / back-loaded / flat]
**Peak moment**: [quote or describe the strongest line or paragraph]
**Biggest narrative gap**: [what is missing that would make this piece memorable]

### Strongest line
> [quote the single best sentence in the article]

### Where the story lives
[1-2 sentences about where the real human story is hiding in this draft, even if the author has not surfaced it yet]
```

### Step 8: Add Inline Annotations

Insert `??STORY` annotations directly into the article at specific locations. These are prompts for the author to add personal depth. They should feel like a thoughtful writing coach leaving margin notes.

Annotation format:

```
??STORY [category]: [specific prompt for the author]
```

Categories and example prompts:

**FEEL**
- `??STORY FEEL: How did this make you feel when you first realized it?`
- `??STORY FEEL: What was your gut reaction before you had time to think?`
- `??STORY FEEL: Was there a moment of frustration, relief, or surprise here?`

**TENSION**
- `??STORY TENSION: This is where the reader needs to feel the stakes. What would go wrong if you ignored this?`
- `??STORY TENSION: Slow down here. The reader does not yet know why this matters.`
- `??STORY TENSION: Add a beat before the resolution. Let the problem breathe.`

**DETAIL**
- `??STORY DETAIL: Name the moment. Where were you? What triggered this thought?`
- `??STORY DETAIL: Replace this abstract claim with a specific example from your work.`
- `??STORY DETAIL: This reads like a summary. Can you show one concrete instance?`

**VOICE**
- `??STORY VOICE: This paragraph sounds like documentation. Rewrite it as if you were explaining to a colleague over coffee.`
- `??STORY VOICE: You are being too careful here. Say what you actually think.`
- `??STORY VOICE: This is the most interesting claim in the article. Give it more weight.`

**DRAMA**
- `??STORY DRAMA: This is the turning point of the article. Make it feel like one.`
- `??STORY DRAMA: The reader needs a before/after contrast here. What changed?`
- `??STORY DRAMA: You resolved the tension too quickly. Let the reader sit with the problem first.`

**CUT**
- `??STORY CUT: This paragraph repeats the previous point. Choose the stronger version.`
- `??STORY CUT: This section breaks the narrative flow. Consider moving it to a footnote or appendix.`

### Annotation Rules

- Place 5-12 annotations per article, not more. Too many dilutes the signal.
- At least 2 annotations should be in the first third of the article (opening matters most).
- At least 1 annotation should be near the ending.
- Never annotate something the author already does well. Only annotate gaps.
- Be specific. "Add more here" is useless. "What was your first reaction when your leader said this?" is useful.

## What This Skill Does Not Do

- It does not rewrite the article unless the user asks.
- It does not check technical accuracy or references.
- It does not score for relevance, timeliness, or audience fit (that is `content-drafting`).
- It does not handle publishing, frontmatter, or Hugo checks (that is `content-publishing`).
- It does not adapt content for LinkedIn or X (those are separate skills).

## Storytelling Principles Reference

These are the principles behind the review. Do not recite them to the user. Use them as your internal compass.

1. **Specificity beats abstraction.** "My leader challenged me" is stronger than "leadership teams are asking."
2. **Vulnerability creates trust.** "I was defensive at first" earns more credibility than being right from the start.
3. **Tension creates momentum.** If the reader already knows the answer, there is no reason to keep reading.
4. **One strong line beats three adequate paragraphs.** Find the line and protect it.
5. **The opening is a promise.** If the opening promises a personal story, the article must deliver one.
6. **The ending is a mirror.** The best endings reflect the opening from a changed perspective.
7. **Show the thinking, not just the conclusion.** The journey matters more than the destination.
8. **Silence and space matter.** Short paragraphs after long ones create emphasis. Use them at peak moments.
9. **The author's presence is not vanity.** In technical writing, the first person is what separates insight from summary.
10. **Not every article needs to be a story. But every article needs a reason to finish reading.**
