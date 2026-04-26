---
name: blog-preview
description: REQUIRED workflow for any local Hugo page check. MUST be read before calling any browser tool against localhost, before starting `hugo server`, and before giving visual judgment about a rendered blog page. Use when the user says any of - check the website, check the page, check in the browser, preview the site, see how it looks, review the layout, assess the visual aspect, inspect the homepage, verify rendering, check mobile/desktop, or asks for design feedback on a Hugo page (homepage, post, project, draft).
---

# Blog Preview

Local Hugo preview + Cursor browser verification for the `ksopyla-ai-blog`. This is how you look at a rendered page before claiming anything about how it appears.

## First Action

Before doing **any** of the following, write one short line in your response: *"Using `blog-preview` skill."*

- Calling any `browser_*` tool against `localhost` or the blog
- Running `hugo server`
- Giving visual or design judgment about a rendered page

If you skipped this announcement, stop, re-read this skill, then proceed.

## When To Use

- Starting Hugo preview server for local development
- Checking how a homepage, post, project page, or draft renders (layout, hierarchy, spacing, callouts, typography)
- Verifying a feature image, diagram, code block, or shortcode looks correct
- Comparing desktop and mobile layout after publishing or editing
- Giving design feedback (e.g. "is the alert box too heavy?", "does the intro feel cluttered?")
- Investigating a styling regression after a config or theme change

If the task is "see how this looks on the actual blog," this skill applies — even if the user does not say "Hugo" or "smoke check."

## Hard Rules

1. **NEVER fall back to production** (`ai.ksopyla.com`). If local preview is broken, diagnose and fix the local issue. Production checks prove nothing about local changes.
2. **Always override baseURL** — the config has the production URL. Every `hugo server` invocation must include `--baseURL http://localhost:1313/`.
3. **Check console and network BEFORE any visual judgment** — if CSS/JS is blocked, every screenshot is evidence of a runtime problem, not of the article.
4. **Use `http://localhost:1313/`** for all browser URLs, never `127.0.0.1`.
5. **Resize the browser to desktop (1280x800) BEFORE the first navigation** — Cursor browser may default to a tiny viewport that makes the page unreadable.

## Starting the Server

### The SRI/CORS Problem

Congo generates SRI integrity hashes on all assets (`fingerprintAlgorithm = "sha256"` in `params.toml`). Hugo's dev server uses an internal livereload port (e.g. 54707) separate from the main port (1313). Cursor browser blocks cross-port SRI resources because CORS headers are missing.

**Symptoms**: page shows unstyled text, large black bars (dark-styled elements with no CSS), Mermaid diagrams don't render, code blocks have no highlighting.

**Console evidence**: `Subresource Integrity: The resource 'http://localhost:54707/...' has an integrity attribute, but the resource requires the request to be CORS enabled...`

### Server Command (use this exact form)

Disable livereload to prevent the port split:

```bash
hugo server --bind 127.0.0.1 --baseURL http://localhost:1313/ -p 1313 --disableFastRender --disableLiveReload --buildDrafts --buildFuture
```

Drop `--buildDrafts --buildFuture` when checking only published content.

### Verify the Fix Before Proceeding

After navigating to the page, **immediately** check console messages:

- SRI / `Subresource Integrity` errors → assets still blocked, try the next server command variant
- Assets loaded from `https://ai.ksopyla.com/...` → baseURL override not working, check the command
- No SRI errors and `main.bundle.min.css` loads from `http://localhost:1313/...` → preview is working, proceed to visual checks

If a previous preview is already running on port 1313 with stale assets, kill it (or use a different port like 1314) before starting a new one. Do not silently keep two servers alive.

## Browser Workflow

Check both light and dark mode, check fonts/colors/contrast, check diagrams, images, tables, code blocks. Use the recommended usability checks below.

1. **Resize to desktop** (1280x800).
2. **Navigate to homepage** (`http://localhost:1313/`). Confirm it loads styled (site title, nav links, article cards visible).
3. **Check console and network.** This is a BLOCKER — do not proceed if core CSS or JS is missing.
4. **Navigate to the target page:**
   - `content/posts/<slug>/index.md` → `http://localhost:1313/posts/<slug>/`
   - `content/drafts/<slug>/index.md` → `http://localhost:1313/drafts/<slug>/`
   - `content/projects/<slug>/index.md` → `http://localhost:1313/projects/<slug>/`
5. **Take a desktop screenshot** and verify:
   - H1 title renders
   - Feature image loads, not stretched/clipped/blurry
   - TOC visible in sidebar for long posts
   - Tags and categories display
   - Code blocks have syntax highlighting
   - Mermaid diagrams render with readable labels (scroll to them)
   - Inline images stay inside the content column
   - No horizontal overflow
6. **Resize to mobile** (390x844), reload page, take screenshot:
   - No horizontal scrolling
   - Title readable
   - Feature image scales, doesn't dominate the viewport
   - Body text is comfortable width
   - TOC collapses cleanly

## Design-Review Mode

When the user asks subjective questions like *"is the homepage cluttered?"*, *"should we keep the alert box?"*, *"does the hierarchy work?"* — the workflow is the same as above plus:

- Confirm the page actually rendered correctly (Hard Rule 3) before giving any opinion
- Use the snapshot to identify shortcodes / components in play (`alert`, `lead`, `mermaid`, etc.)
- Comment on hierarchy in concrete terms: *what competes with what*, *what is the first thing the eye lands on*, *what could be merged or removed*
- Reference the visual at desktop AND mobile — issues often only appear on one

## Non-Blocking Issues

- Giscus `Discussion not found` — expected for new or draft posts, ignore
- `[CursorBrowser] Native dialog overrides` warnings — internal to Cursor, ignore

## Repo Facts

- Theme: Congo via git submodule in `themes/congo`
- Hugo Extended required (minimum `0.87.0`, CI uses `0.160.1`)
- `fingerprintAlgorithm = "sha256"` in `config/_default/params.toml` — generates SRI hashes
- `baseURL = 'https://ai.ksopyla.com/'` in `config/_default/hugo.toml` — must be overridden for local preview
