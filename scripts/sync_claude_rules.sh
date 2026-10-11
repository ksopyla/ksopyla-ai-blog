#!/usr/bin/env bash
# Mirror Cursor rules (.cursor/rules/*.mdc, the source of truth) into Claude Code
# rules (.claude/rules/*.md). Claude Code does not load .mdc files, so it needs
# real .md copies. Runs automatically at the start of every Claude Code session
# (SessionStart hook in .claude/settings.json); safe to run by hand.
set -euo pipefail
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
src="$root/.cursor/rules"
dst="$root/.claude/rules"
mkdir -p "$dst"

for f in "$src"/*.mdc; do
  name="$(basename "$f" .mdc)"
  {
    echo "<!-- Generated from .cursor/rules/$name.mdc by scripts/sync_claude_rules.sh. Edit the .mdc file, not this one. -->"
    echo
    # Drop the Cursor frontmatter (first --- ... --- block); keep the body.
    awk 'NR==1 && $0=="---" {fm=1; next} fm && $0=="---" {fm=0; next} !fm' "$f"
  } > "$dst/$name.md.tmp"
  mv "$dst/$name.md.tmp" "$dst/$name.md"
done

# Remove copies whose source rule was deleted.
for f in "$dst"/*.md; do
  [ -e "$f" ] || continue
  name="$(basename "$f" .md)"
  if [ ! -e "$src/$name.mdc" ] && head -1 "$f" | grep -q "Generated from .cursor/rules"; then
    rm "$f"
  fi
done
