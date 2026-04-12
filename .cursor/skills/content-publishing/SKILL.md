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

### 2. Assess The Title

A strong title should describe the topic clearly, create curiosity without clickbait, carry technical signal for the target audience, and match the article's actual claim.

If weak, generate 3-5 alternatives. Pick the best if intent is obvious, or ask the user to choose.

### 3. Tone Gate

Quick sanity check against the voice defined in the persona-and-audience rule: first person, modest, precise, honest about failure, anti-hype, educational. If the article drifts into summary-without-insight, flag it.

### 4. Story Review

Run the `story-review` skill if the article would benefit from narrative quality feedback — especially for experience-driven or failure-report pieces.

### 5. Validate Frontmatter And Bundle

Verify before moving:

- `title` is final
- `date` is set for publication
- `description` is accurate (SEO/share cards)
- `tags` and `categories` are appropriate
- `featureImage` and `featureAlt` are present or clearly marked as missing

Keep all assets inside the content bundle.

### 6. Generate Feature Image If Missing

1. Prefer real visuals: charts, screenshots, diagrams, architecture art.
2. If none exist, use the `image-generation` skill.
3. Save in the bundle and update `featureImage` and `featureAlt`.

### 7. Move Draft To Published

1. Move bundle from `content/drafts/<slug>/` to `content/posts/<slug>/`.
2. Set `draft: false` and the final publish `date`.
3. Preserve the bundle structure.

### 8. Update Backlog

- Remove or update the entry in `notes/content-backlog.md`
- Clear stale references to the old draft path

### 9. Hugo And Browser Smoke Check

Use `hugo-runtime-smoke-check`. Minimum:

- Successful build
- Homepage renders
- Article page at `/posts/<slug>/` renders correctly
- Feature image, layout, TOC, typography look correct
- Desktop and mobile layouts checked

Fix any issue before considering the article published.

### 10. Ask About LinkedIn

After smoke check passes, ask if the user wants a LinkedIn post via the `linkedin-post` skill. Do not auto-generate.

## Publish Checklist

```text
[ ] Editorial review done
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
