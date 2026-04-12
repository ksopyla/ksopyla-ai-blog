---
name: content-publishing
description: Finalize and publish an approved blog draft by moving it from content/drafts to content/posts, checking the tone and story generating missing feature art, running Hugo and browser smoke checks, and asking whether to generate a LinkedIn post.
---
# Content Publishing

## Purpose

Publishing is the final stage of the workflow. It starts only after a blog draft is approved and ready to go live.

This skill owns:

- final editorial pass
- title assessment
- tone and clarity check
- feature image fallback
- moving the bundle from `content/drafts/` to `content/posts/`
- Hugo and browser validation
- check the story teling narrative by running the `story-review` skill
- post-publish prompt for LinkedIn

## Stage Boundary

- `content-discovery` finds ideas.
- `content-drafting` creates and refines the draft.
- `content-publishing` makes the article publish-ready and validates the live result.

Do not use this skill to discover topics or build a draft from scratch.

## Preconditions

Before using this skill, confirm:

- the article exists as `content/drafts/<slug>/index.md`
- the core facts and references are already in place
- the user wants to publish now, or explicitly wants a publish-readiness pass

If the article still needs major structural rewriting, return to `content-drafting`.

## Publish Workflow

### 1. Read The Whole Article

Read the full draft before changing anything.

Check:

- does the article deliver what the title promises
- is the opening strong enough for the target reader
- are the H2 and H3 sections easy to scan
- does the argument build cleanly from setup to takeaway
- are limitations and uncertainty stated honestly

### 2. Do The Final Editorial Pass

Polish the article for clarity and flow:

- tighten the opening paragraph
- cut repetition
- smooth transitions between sections
- make headings more informative
- check grammar, phrasing, and readability
- ensure the `## References` section is complete when claims depend on outside sources

### 3. Assess The Title

Review the title before publishing. A strong title should:

- describe the real topic clearly
- create curiosity without sounding like clickbait
- contain enough technical signal for the target audience
- match the article's actual claim
- avoid hype and vague corporate phrasing

If the title is weak, generate 3-5 stronger options and either:

- pick the best one if the intent is obvious, or
- ask the user to choose if the options imply meaningfully different positioning

### 4. Run The Tone Gate

Check the article against the writing voice:

- first person when sharing experience or judgment
- modest, not boastful
- precise and technical
- honest about failures and uncertainty
- curious rather than dismissive
- anti-hype
- educational and readable

If the article drifts into summary-without-insight, add more first-hand judgment or clearer lessons.

### 5. Validate Frontmatter And Bundle Assets

Before moving the post, verify:

- `title` is final
- `date` is set for publication
- `draft: false` will be applied at publish time
- `description` is accurate and useful for SEO/share cards
- `tags` and `categories` are appropriate
- `featureImage` and `featureAlt` are present, or clearly marked as missing

Keep images and related assets inside the same content bundle.

### 6. Generate The Feature Image If Missing

If the article lacks a credible feature image:

1. Prefer real visuals first: charts, screenshots, diagrams, architecture art.
2. If none exist, use the `image-generation` skill to create concept art aligned with the blog's visual style.
3. Save the asset in the article bundle and update `featureImage` and `featureAlt`.

If an image already exists, keep it unless it is obviously off-theme, low quality, or visually harmful during browser review.

### 7. Move Draft To Published

When the article is ready:

1. Move the content bundle from `content/drafts/<slug>/` to `content/posts/<slug>/`.
2. Update frontmatter:
   - set `draft: false`
   - set the final publish `date`
   - keep the rest of the metadata consistent
3. Preserve the bundle structure, including images and notes that should stay with the post.

### 8. Update Backlog And Pipeline State

After moving the post:

- remove or update the draft entry in `notes/content-backlog.md`
- make sure there are no stale references to the old draft path
- record derivative opportunities only if they are still relevant

### 9. Run Hugo And Browser Smoke Checks

Use `hugo-runtime-smoke-check` after the post move.

Minimum checks:

- build the site successfully
- run the local preview on `http://localhost:1313/`
- open the homepage
- open the published article URL under `/posts/<slug>/`
- confirm CSS and JS load from localhost
- confirm the feature image renders well
- confirm the article layout, TOC, and typography look correct
- check both desktop and mobile layouts

If the browser smoke check fails, fix the issue before considering the article published successfully.

### 10. Ask About LinkedIn

After the blog post is published and smoke-checked, ask the user whether they want a LinkedIn post generated from the article.

- If yes, use the `linkedin-post` skill.
- Do not auto-generate the LinkedIn post unless the user confirms.

## Default Publish Checklist

Use this checklist during execution:

```text
[ ] Read the full draft
[ ] Final editorial polish done
[ ] Title assessed and improved if needed
[ ] Tone and voice checked
[ ] Frontmatter validated
[ ] Feature image present or generated
[ ] Bundle moved from drafts to posts
[ ] Backlog updated
[ ] Hugo/browser smoke check passed
[ ] Asked about LinkedIn follow-up
```

## Output To The User

When the workflow completes, report:

- final post path
- final title
- whether the feature image was generated or reused
- whether Hugo and browser checks passed
- any remaining low-risk follow-ups
- the LinkedIn prompt
