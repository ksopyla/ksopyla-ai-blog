---
name: hugo-runtime-smoke-check
description: Run and review Hugo plus Congo sites in local or Cursor Cloud Agent environments. Use when setting up Hugo or the Congo theme, building published or draft content, starting a preview server, or smoke-checking homepage and article rendering with Cursor browser tools on desktop and mobile.
---
# Hugo Runtime Smoke Check

## When To Use

Use this skill when the task involves any of:

- installing or updating Hugo runtime prerequisites
- setting up the Congo theme
- building the site for published-only or draft-inclusive output
- starting a predictable local preview server
- using Cursor browser tools to review homepage or article rendering

## Current Repo Defaults

- This repo uses the Congo theme as a git submodule in `themes/congo`.
- Hugo Extended is required.
- `config/_default/module.toml` requires Hugo `>= 0.87.0`.
- CI currently installs Hugo `0.148.0`.
- Use `http://localhost:1313/` for browser checks, not `127.0.0.1`.

## Runtime Setup

For this repo's current submodule-based setup:

- Go is not required just to run the existing site.
- You need Hugo Extended and recursive git submodules.
- Clone or update with submodules before building.

For Congo installed as a Hugo Module instead of a submodule:

- Go is required.
- Congo's `go.mod` declares `go 1.16`, so treat Go `1.16+` as the minimum.
- Use Hugo Modules only if the repo is intentionally switching away from the current submodule setup.

## Preferred Commands

Use direct `hugo` CLI commands:

```bash
hugo --gc --minify
hugo --gc --minify --buildDrafts --buildFuture
hugo server --bind 127.0.0.1 --baseURL http://localhost:1313/ -p 1313 --disableFastRender --buildDrafts --buildFuture
```

## Browser Workflow

1. Build the site with or without drafts, depending on the task.
2. Start the preview server on `http://localhost:1313/`.
3. Open the homepage first.
4. Open the changed article or draft next. Derive its URL from the edited content path:
   - `content/posts/<slug>/index.md` -> `/posts/<slug>/`
   - `content/drafts/<slug>/index.md` -> `/drafts/<slug>/`
5. If no content bundle was edited directly, choose the main article the task focused on or the most recently relevant post/draft from the conversation context.
6. Inspect console and network traffic after each page load.
7. Run both desktop and mobile layout checks before finishing.

## High-Value Browser Targets

- Homepage search trigger is typically exposed as a button named `Search (/)`.
- After opening search, the input is typically exposed as a searchbox named `Search`.
- Homepage article discovery usually happens under the `Recent` heading.
- Article pages should expose a clear `h1`, a readable main column, visible taxonomies, and a visible table of contents for long posts.

## Review Priorities

- Verify layout and usability before cosmetic polish.
- Treat critical console errors, failed core assets, horizontal overflow, unreadable text, hidden TOC, or broken image sizing as real issues.
- Treat subjective visual mismatch in feature art as a suggestion unless it clearly harms consistency or credibility.
- Giscus `Discussion not found` on new or draft posts is non-blocking unless the task is about comments.

## Additional Resources

- For exact setup commands, Congo installation modes, and browser/layout heuristics, read [reference.md](reference.md).
