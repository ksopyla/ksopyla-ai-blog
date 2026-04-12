---
name: hugo-runtime-smoke-check
description: Run Hugo preview server and visually verify pages using Cursor browser tools. Use when starting a preview server, smoke-checking article rendering, or verifying feature images, diagrams, and code blocks locally.
---

# Hugo Local Preview Smoke Check

## When To Use

- Starting Hugo preview server for local development
- Visually checking how a post or draft renders (layout, images, diagrams, code blocks)
- Verifying a feature image loads and looks correct
- Checking desktop and mobile layout after publishing or editing

## Hard Rules

1. **NEVER fall back to production** (`ai.ksopyla.com`). If local preview is broken, diagnose and fix the local issue. Production checks prove nothing about the dev workflow.
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

If assets are still blocked, also add `--renderToDisk`:

```bash
hugo server --bind 127.0.0.1 --baseURL http://localhost:1313/ -p 1313 --disableFastRender --disableLiveReload --renderToDisk --buildDrafts --buildFuture
```

Drop `--buildDrafts --buildFuture` when checking only published content.

### Verify the Fix Before Proceeding

After navigating to the page, **immediately** check console messages:
- SRI / `Subresource Integrity` errors → assets still blocked, try the next server command variant
- Assets loaded from `https://ai.ksopyla.com/...` → baseURL override not working, check the command
- No SRI errors and `main.bundle.min.css` loads from `http://localhost:1313/...` → preview is working, proceed to visual checks

## Browser Workflow

Check in the light and dark mode, check the fonts colors and contrast, check the diagrams, images, tables, code blocks, etc. - use the recommended usability checks

1. **Resize to desktop** (1280x800).
2. **Navigate to homepage** (`http://localhost:1313/`). Confirm it loads styled (site title, nav links, article cards visible).
3. **Check console and network.** This is a BLOCKER — do not proceed if core CSS or JS is missing.
4. **Navigate to the target article:**
   - `content/posts/<slug>/index.md` → `http://localhost:1313/posts/<slug>/`
   - `content/drafts/<slug>/index.md` → `http://localhost:1313/drafts/<slug>/`
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



## Non-Blocking Issues

- Giscus `Discussion not found` — expected for new or draft posts, ignore
- `[CursorBrowser] Native dialog overrides` warnings — internal to Cursor, ignore

## Repo Facts

- Theme: Congo via git submodule in `themes/congo`
- Hugo Extended required (minimum `0.87.0`, CI uses `0.160.1`)
- `fingerprintAlgorithm = "sha256"` in `config/_default/params.toml` — generates SRI hashes
- `baseURL = 'https://ai.ksopyla.com/'` in `config/_default/hugo.toml` — must be overridden for local preview
