# Hugo Runtime Reference

## Runtime Facts For This Repo

- Theme: `themes/congo` as a git submodule
- Hugo minimum from `config/_default/module.toml`: `0.87.0`
- CI/runtime reference from `.github/workflows/hugo-deployment.yml`: Hugo `0.148.0`
- Local browser target for smoke checks: `http://localhost:1313/`
- Do not use `127.0.0.1` for browser validation in this repo because asset URLs can resolve against `localhost` and trigger SRI or CORS issues
- If the page looks badly broken or unstyled in Cursor browser, suspect blocked core assets before suspecting the article content or theme templates

## Do You Need Go?

Usually, no.

For this repo's current setup, the theme is already installed as a git submodule, so running the site only needs:

- Hugo Extended
- git with recursive submodule checkout

Go is only needed if you switch to a Hugo Module installation flow. Congo's `go.mod` declares:

```text
go 1.16
```

So use Go `1.16+` as the minimum for the module-based path.

## Congo Installation Modes

### Existing Repo Mode: Git Submodule

This repo already uses this mode. For a fresh clone:

```bash
git clone --recurse-submodules <repo-url>
git submodule update --init --recursive
```

Core config:

- `config/_default/hugo.toml` contains `theme = "congo"`
- `.gitmodules` points `themes/congo` at the upstream theme repository

### Alternative Mode: Hugo Module

Use only if intentionally changing the repo structure:

```bash
hugo mod init github.com/<username>/<repo-name>
```

Then add this to `config/_default/module.toml`:

```toml
[[imports]]
path = "github.com/jpanther/congo/v2"
```

Module mode requires Go and Hugo. Congo's README explicitly notes both.

## Build Commands

Published content only:

```bash
hugo --gc --minify
```

Include drafts and future posts:

```bash
hugo --gc --minify --buildDrafts --buildFuture
```

## Preview Server Command

Use this exact form for predictable browser checks:

```bash
hugo server --bind 127.0.0.1 --baseURL http://localhost:1313/ -p 1313 --disableFastRender --buildDrafts --buildFuture
```

Why:

- `--baseURL http://localhost:1313/` keeps generated asset URLs aligned with the browser target
- `--buildDrafts --buildFuture` allows draft review workflows
- `--disableFastRender` reduces confusing partial refresh behavior during validation

If you omit the `--baseURL` override and the site falls back to `https://ai.ksopyla.com/`, the local page may request CSS/JS from the production domain. In Cursor browser that can trigger Subresource Integrity or CORS enforcement and block the main stylesheet or appearance script, producing a page that looks half-rendered, unstyled, or full of large black placeholder shapes.

## Mapping Content Paths To Preview URLs

Translate edited content bundle paths directly:

```text
content/posts/<slug>/index.md  ->  http://localhost:1313/posts/<slug>/
content/drafts/<slug>/index.md ->  http://localhost:1313/drafts/<slug>/
```

If the task did not edit a content bundle directly:

- use the article explicitly referenced by the user, or
- pick the most relevant recent post or draft from the conversation context

## Browser Tool Guidance

### Homepage

Check:

- page opens successfully
- site title renders correctly
- main navigation is visible and usable
- `Recent` section is present
- recent article cards or links are visible and not overlapping
- search trigger is discoverable

Search affordances usually appear as:

- button named `Search (/)`
- searchbox named `Search` after opening the search UI

### Article Page

Check:

- `main` content renders
- `article` container renders
- `h1` is visible and matches the article title
- title length does not dominate the viewport
- at least one body paragraph is visible without broken spacing
- metadata and taxonomies do not collide with the main column
- if a feature image exists, it is visible in the article header area and does not collapse the layout
- inline paper links, references, and TOC links look like normal styled links rather than raw fallback browser styling

Before judging page aesthetics, inspect:

- browser console messages
- browser network requests
- whether `main.bundle.min.css` and `appearance.min.js` load from `http://localhost:1313/...`

Treat these as blockers:

- core stylesheet blocked
- core JS blocked
- core assets loaded from `https://ai.ksopyla.com/...` during local preview

### Desktop Layout

Use a wide viewport and check:

- no horizontal overflow
- feature image feels consistent with the site's visual style
- feature image does not overpower the title block
- feature image has natural aspect ratio and is not visibly stretched, cropped badly, or blurry
- TOC is clearly visible for long articles
- TOC does not overlap or cover article text
- inline article images stay inside the content column
- wide images, tables, or code blocks do not break the layout

Suggested desktop blockers:

- title wraps so aggressively that it harms scanning
- TOC hides text or consumes too much of the reading column
- feature image is visibly stretched, blurry, or stylistically jarring
- feature image is missing when expected, or replaced by a broken placeholder / empty gap
- inline images overflow or force horizontal scrolling

### Mobile Layout

Resize to a narrow viewport such as `390x844` and check:

- header remains usable
- top navigation and search remain discoverable
- no horizontal scrolling
- title remains readable
- feature image scales cleanly
- feature image does not push the start of the article too far below the fold
- body text width is comfortable
- TOC stacks cleanly and does not sit on top of article text
- inline images do not push content outside the viewport

Suggested mobile blockers:

- title takes too many lines and buries the start of the article
- sticky or floating elements cover text
- images extend beyond viewport width
- feature image dominates the first screen or becomes awkwardly cropped
- the search UI cannot be opened or used

## Extra Usability Checks

- The first screen should communicate page purpose immediately.
- Click targets in header, recent post cards, and share links should not be cramped.
- Visual hierarchy should be clear: title, metadata, lead, body.
- A feature image may be subjective, but flag it if it feels off-brand, low-quality, or inconsistent with neighboring posts.
- If an article contains multiple images, verify they have enough spacing and do not create abrupt layout jumps.
- Prefer concrete browser evidence: console messages, failed requests, screenshots, and snapshots.
- When possible, take a full-page screenshot after confirming local CSS is loaded correctly. A screenshot taken before core assets load is evidence of a runtime problem, not of the final article appearance.

## Known Non-Blocking Behavior

- Giscus may log `Discussion not found` and return `404` discussion lookups for new or draft posts.
- Treat that as expected unless the task explicitly concerns comments or comment configuration.
