---
name: content-publishing
description: Publish an approved blog draft — editorial pass, title check, feature image, move to content/posts, Hugo smoke check, LinkedIn prompt.
---
# Content Publishing

## Purpose

Final stage of the content workflow. Starts only after a draft is approved and ready to go live.

This skill owns: editorial pass, title assessment, tone check, story review, feature image, moving the bundle to `content/posts/`, Hugo/browser validation, and the LinkedIn prompt.

It does not discover topics or build drafts — those belong to `content-discovery` and `content-drafting`.

## Preconditions

- Article exists at `content/drafts/<slug>/index.md`
- Core facts and references are in place
- User wants to publish or wants a publish-readiness pass

If the article needs major rewriting, return to `content-drafting`.

## Publish Workflow

### 1. Editorial Review

Read the full draft, then polish for clarity and flow:

- Does the article deliver what the title promises?
- Tighten the opening paragraph
- Cut repetition, smooth transitions
- Make headings scannable and informative
- Check grammar and readability
- Ensure `## References` is complete when claims cite outside sources

### 2. Generate TL;DR

Every published article gets a TL;DR section. It serves two purposes: it helps readers quickly understand what the article is about and what value they will get from reading it, and it improves AI-generated summaries when search engines or LLMs process the page.

**Structure** (must follow this exact order):

1. **`{{< lead >}}` shortcode** — placed immediately after the frontmatter, before anything else. Contains a 1–2 sentence hook that summarizes what the article is about and what the reader gets. Renders in muted/lighter text as a visual intro.
2. **`## TL;DR` heading** — placed immediately after the lead shortcode, before the first content section.
3. **Bullet list** under the TL;DR heading with the format appropriate for the article type.

Example layout:

```markdown
---
frontmatter here
---

{{< lead >}}
One or two sentences summarizing what this article covers and why it matters.
{{< /lead >}}

## TL;DR

**What you will learn:** (or **Do:** / **Don't:** for prescriptive articles)

- Bullet 1
- Bullet 2
- Bullet 3

## First Content Section
```

**Format depends on the article type**:
- **Best-practices or opinionated articles**: use **Do / Don't** bullets
- **Technical how-to or process articles**: use **Key takeaways** or **What you will learn** bullets
- **Experience or narrative articles**: use **What you will learn** bullets summarizing the key sections

**Rules**:
- Keep each bullet to one actionable sentence
- The TL;DR should be useful on its own — a reader who stops here should still walk away with something
- Do not just repeat the `description` from frontmatter — the TL;DR should be more specific and structured
- Any opening paragraphs that were before the TL;DR should move into the first content section

### 3. Assess The Title

A strong title should describe the topic clearly, create curiosity without clickbait, carry technical signal for the target audience, and match the article's actual claim.

If weak, generate 3-5 alternatives. Pick the best if intent is obvious, or ask the user to choose.

### 4. Tone Gate

Quick sanity check against the voice defined in the persona-and-audience rule: first person, modest, precise, honest about failure, anti-hype, educational. If the article drifts into summary-without-insight, flag it.

### 5. Story Review

Run the `story-review` skill if the article would benefit from narrative quality feedback — especially for experience-driven or failure-report pieces.

### 6. Validate Frontmatter And Bundle

Verify before moving:

- `title` is final
- `date` is set for publication
- `description` is accurate (SEO/share cards)
- `tags` and `categories` are appropriate
- `featureImage` and `featureAlt` are present or clearly marked as missing

Keep all assets inside the content bundle.

### 7. Generate Feature Image If Missing

1. Prefer real visuals: charts, screenshots, diagrams, architecture art.
2. If none exist, use the `image-generation` skill.
3. Save in the bundle and update `featureImage` and `featureAlt`.

### 8. Move Draft To Published

1. Move bundle from `content/drafts/<slug>/` to `content/posts/<slug>/`.
2. Set `draft: false` and the final publish `date`.
3. Preserve the bundle structure.

### 9. Update Backlog

- Remove or update the entry in `notes/content-backlog.md`
- Clear stale references to the old draft path

### 10. Hugo And Browser Smoke Check

Use `hugo-runtime-smoke-check`. Minimum:

- Successful build
- Homepage renders
- Article page at `/posts/<slug>/` renders correctly
- Feature image, layout, TOC, typography look correct
- Desktop and mobile layouts checked

Fix any issue before considering the article published.

### 11. Ask About LinkedIn

After smoke check passes, ask if the user wants a LinkedIn post via the `linkedin-post` skill. Do not auto-generate.

## Publish Checklist

```text
[ ] Editorial review done
[ ] TL;DR generated
[ ] Title assessed
[ ] Tone gate passed
[ ] Frontmatter validated
[ ] Feature image present or generated
[ ] Bundle moved to posts
[ ] Backlog updated
[ ] Hugo/browser smoke check passed
[ ] Asked about LinkedIn
```

## Output

Report: final post path, final title, feature image status, smoke check result, remaining follow-ups, LinkedIn prompt.
