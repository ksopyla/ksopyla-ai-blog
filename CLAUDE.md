# Krzysztof Sopyła AI Blog — Claude Code guide

The author works in both Cursor and Claude Code. `.cursor/` is the single source of truth:

- **Rules** live in `.cursor/rules/*.mdc`. Claude Code cannot load `.mdc` files, so `scripts/sync_claude_rules.sh` mirrors them into `.claude/rules/*.md`, which Claude loads automatically. Edit the `.mdc` file, then run the script (or let the SessionStart hook do it).
- **Skills** live in `.cursor/skills/<name>/`. `.claude/skills/<name>` are symlinks to them; edit the files under `.cursor/skills/`, never replace a symlink with a copy.
- **Agents** live in `.cursor/agents/`. `.claude/agents/` holds thin wrappers with Claude frontmatter that point to the Cursor file.

When adding a skill, create it under `.cursor/skills/<name>/` and add the link:
`ln -s ../../.cursor/skills/<name> .claude/skills/<name>`

## Claude Code specifics

- **Cloud sessions** (claude.ai/code) run on Linux, not the author's Mac. There may be no `gh` CLI and no Hugo: use the GitHub MCP tools, and download Hugo Extended at the CI version (`HUGO_VERSION` in `.github/workflows/hugo-deployment.yml`) into the scratchpad. Run `git submodule update --init --depth 1` before building, because `themes/congo` is a submodule.
- **Browser checks:** Claude Code has no Cursor browser. The `blog-preview` skill describes the headless Playwright route.
- **Publishing:** a merge to `main` deploys the site. Merge only when the author asks.
