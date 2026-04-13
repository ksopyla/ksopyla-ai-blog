---
name: linkedin-tracker
description: Track LinkedIn published posts with metrics synced from analytics. Use when the user publishes a LinkedIn post, wants to record it, sync metrics after an analytics import, check publishing history, or asks about what has been posted and how it performed.
---
# LinkedIn Published Content Tracker

Manage `notes/linkedin-published-tracker.md` — what was posted, when, how it performed, and where it came from.

## Responsibility Split

**This skill (linkedin-tracker)** owns:
- The editorial record: what was posted, when, what format, what blog source
- Syncing metrics from analytics into the tracker
- The blog-to-LinkedIn coverage mapping

**The linkedin-analytics skill** owns:
- Raw XLSX imports and storage in `data/linkedin-analytics/`
- Historical time-series data (daily impressions, daily followers)
- Multi-window post records in `posts.jsonl`
- Aggregate reports, trends, demographics

The tracker reads from analytics data (one-way dependency). Analytics does not know about the tracker.

## How Metrics Work

LinkedIn XLSX exports are window-scoped — a post shows different metrics in a 14-day vs 90-day export. The tracker always shows the **best available** metrics by picking the record where the post had the most days to accumulate (widest coverage from post_date to window_end).

The `Window` column shows data freshness:
- `90d` = post had 90 days to accumulate → metrics are reliable
- `14d` = post had only 14 days → metrics are partial, will improve on next wider import
- `—` = no analytics data yet (post not in any import)

Metrics never downgrade — if the tracker has 90d data, a later 14d import won't overwrite it.

## Script

```bash
uv run python .cursor/skills/linkedin-tracker/scripts/linkedin_tracker.py <command> [args]
```

| Command | Purpose |
|---------|---------|
| `add` | Record a new published post |
| `sync-metrics` | Pull best metrics from analytics into tracker |
| `list` | Show all tracked posts with metrics |
| `stats` | Summary statistics |

## Workflow 1: Record a Published Post

When the user says they published or scheduled a LinkedIn post:

```bash
uv run python .cursor/skills/linkedin-tracker/scripts/linkedin_tracker.py add \
  --date "2026-04-14" \
  --hook "Agent Identity & Authorization: The Unsolved Layer" \
  --format "Carousel (7p)" \
  --source "enterprise-agents-new-systems-mindset"
```

Metrics will be `—` until the next analytics import + sync.

## Workflow 2: Sync After Analytics Import

After importing a new XLSX export with the analytics skill, sync the tracker:

```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py import-xlsx <file>
uv run python .cursor/skills/linkedin-tracker/scripts/linkedin_tracker.py sync-metrics
```

The sync command:
1. Reads all records from `data/linkedin-analytics/posts.jsonl`
2. Matches tracker rows to analytics records by cached URL or by date
3. Picks the record with the widest post-lifetime coverage
4. Updates metrics only if the new data is from a wider window (never downgrades)
5. Caches the LinkedIn URL for future syncs

## Workflow 3: Review Performance

```bash
uv run python .cursor/skills/linkedin-tracker/scripts/linkedin_tracker.py list
uv run python .cursor/skills/linkedin-tracker/scripts/linkedin_tracker.py stats
```

For deeper analysis (trends, demographics, weekly breakdowns), use the linkedin-analytics skill directly.

## Data Locations

- **Tracker**: `notes/linkedin-published-tracker.md`
- **Analytics warehouse**: `data/linkedin-analytics/posts.jsonl`
- **LinkedIn drafts**: `content/linkedin/YYYY-MM-slug/`
