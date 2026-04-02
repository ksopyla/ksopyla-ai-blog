# Hugo Setup Reference

Setup and installation facts. For the smoke-check workflow, see [SKILL.md](SKILL.md).

## Runtime Requirements

For this repo's git-submodule setup:

- Hugo Extended (minimum `0.87.0`, CI uses `0.148.0`)
- git with recursive submodule checkout
- Go is **not** needed

## Fresh Clone

```bash
git clone --recurse-submodules <repo-url>
git submodule update --init --recursive
```

## Congo Installation Mode

This repo uses the **git submodule** mode:

- `config/_default/hugo.toml` has `theme = "congo"`
- `.gitmodules` points `themes/congo` at the upstream theme repo

Hugo Module mode is an alternative but requires Go. Only switch if intentionally changing the repo structure.

## Build Commands

Published content only:

```bash
hugo --gc --minify
```

Include drafts and future posts:

```bash
hugo --gc --minify --buildDrafts --buildFuture
```

## Content Path to URL Mapping

```text
content/posts/<slug>/index.md  →  /posts/<slug>/
content/drafts/<slug>/index.md →  /drafts/<slug>/
```

## Key Config Files

| File | Relevant setting |
|------|-----------------|
| `config/_default/hugo.toml` | `baseURL`, `theme` |
| `config/_default/params.toml` | `fingerprintAlgorithm = "sha256"` (SRI hashes), `colorScheme`, feature toggles |
| `config/_default/markup.toml` | Markdown rendering options |
| `config/_default/module.toml` | Hugo version constraint |
