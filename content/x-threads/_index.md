---
title: "X Threads"
date: 2026-02-27
draft: true
_build:
  render: never
  list: never
---

# X Thread Drafts

This directory stores X (Twitter) thread drafts organized by topic and date.

## Structure

Each thread lives in its own folder:

```
content/x-threads/
├── YYYY-MM-topic-slug/
│   ├── thread.md       # The thread content (numbered tweets)
│   └── images/         # Visuals to attach to specific tweets
```

## Thread Frontmatter

```yaml
---
title: "Internal reference title"
date: YYYY-MM-DD
platform: x-twitter
status: draft | ready | published
content_score: X.X
related_blog_post: ""
---
```

## Writing Rules

See `.cursor/rules/x-thread-writing.mdc` for format, hook patterns, and visual placement.
See `.cursor/rules/persona-and-audience.mdc` for voice principles.
See `.cursor/rules/content-scoring.mdc` for how to score ideas before writing.
