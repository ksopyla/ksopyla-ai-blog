---
name: linkedin-analytics
description: Parse LinkedIn XLSX analytics exports, store historical metrics, and generate performance reports. Use when the user asks to import LinkedIn data, check post performance, view engagement trends, analyze audience demographics, compare exports, or evaluate LinkedIn content strategy.
---
# LinkedIn Analytics

Parse LinkedIn Creator Analytics XLSX exports into local JSONL storage and generate performance reports, post rankings, trend analysis, and audience demographics.

## How LinkedIn Exports Work

LinkedIn exports contain metrics **scoped to the selected date window**, not lifetime totals. The same post will show different impression counts in a 14-day vs 90-day export. The daily ENGAGEMENT sheet is the authoritative source — its daily rows are consistent across overlapping windows.

The XLSX has 5 sheets: DISCOVERY (summary), ENGAGEMENT (daily impressions/engagements), TOP POSTS (up to 50 posts), FOLLOWERS (daily new followers), DEMOGRAPHICS (audience breakdown).

## Data Locations

- **XLSX imports**: `data/linkedin-analytics/imports/`
- **Stored data**: `data/linkedin-analytics/` (posts.jsonl, engagement.jsonl, followers.jsonl, demographics.json)
- **Snapshots**: `data/linkedin-analytics/snapshots/` (raw parsed exports)

## Utility Script

All commands use the bundled script. Invocation pattern:

```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py <command> [args]
```

Available commands:

| Command | Purpose |
|---------|---------|
| `import-xlsx <file>` | Parse XLSX export and store data |
| `report [--days N]` | Generate markdown performance report |
| `top-posts [--limit N] [--sort impressions\|engagements\|engagement_rate]` | List top posts by metric |
| `trend [--metric impressions\|engagements\|followers] [--days N]` | Daily metric trend with sparklines |
| `demographics` | Audience breakdown |
| `compare <file1> <file2>` | Side-by-side export comparison |

## Workflow 1: Import New Data

When the user provides an XLSX file or mentions importing LinkedIn data:

1. Copy the file to `data/linkedin-analytics/imports/` if it is not already there
2. Run:
```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py import-xlsx <path-to-xlsx>
```
3. Report the summary output to the user (window dates, impressions, posts found, followers)
4. If this is the first import, suggest running `report` next

## Workflow 2: Performance Report

When the user asks about overall LinkedIn performance, engagement, or strategy:

1. Run:
```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py report
```
2. Present the markdown report
3. Interpret the results — highlight:
   - Best/worst performing posts and why (topic, format, timing)
   - Engagement rate relative to benchmarks (1-3% is typical for personal profiles)
   - Posting frequency (aim for 3-5 posts/week for growth)
   - Follower growth trajectory
4. Connect recommendations to the `linkedin-post` skill's content strategy

## Workflow 3: Post Evaluation

When the user asks how a specific post performed or wants general post rankings:

1. Run:
```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py top-posts --limit 10
```
2. For a specific post URL, search posts.jsonl for matching records
3. Compare the post's metrics against the stored averages:
   - Impressions vs average impressions per post
   - Engagement rate vs average rate
4. Score as: significantly above average / above average / average / below average

## Workflow 4: Trend Analysis

When the user asks about trends, growth, or time-based patterns:

1. Run the appropriate trend command:
```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py trend --metric impressions --days 30
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py trend --metric followers --days 30
```
2. Identify patterns: weekday vs weekend, post-publication spikes, growth/decline periods

## Workflow 5: Export Comparison

When the user provides two XLSX files or asks to compare periods:

1. Run:
```bash
uv run python .cursor/skills/linkedin-analytics/scripts/linkedin_analytics.py compare <file1> <file2>
```
2. Highlight the most significant changes in impressions, followers, and which posts gained or lost traction

## Weekly Tracking Recommendation

For ongoing optimization, recommend the user exports a **14-day window every Sunday** from `linkedin.com/analytics/creator/content/`. The 14-day window captures the full decay curve of most posts while providing one week of overlap with the prior export for validation.
