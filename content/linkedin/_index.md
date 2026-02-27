---
title: "LinkedIn Posts"
date: 2026-02-27
draft: true
_build:
  render: never
  list: never
---

# LinkedIn Post Drafts

This directory stores LinkedIn post drafts organized by topic and date.

## Structure

Each post lives in its own folder:

```
content/linkedin/
├── YYYY-MM-topic-slug/
│   ├── post.md         # The LinkedIn post content
│   └── images/         # Optional visuals (charts, MidJourney art)
```

## Post Frontmatter

```yaml
---
title: "Internal reference title"
date: YYYY-MM-DD
platform: linkedin
status: draft | ready | published
content_score: X.X
related_blog_post: ""
---
```

## Writing Rules

See `.cursor/rules/linkedin-post-writing.mdc` for format, templates, tone, and hashtag guidelines.
See `.cursor/rules/persona-and-audience.mdc` for voice principles.
See `.cursor/rules/content-scoring.mdc` for how to score ideas before writing.
