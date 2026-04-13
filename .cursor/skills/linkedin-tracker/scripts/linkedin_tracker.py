#!/usr/bin/env python3
"""
LinkedIn Published Content Tracker — CLI

Tracks what was published on LinkedIn, syncs metrics from the analytics
data warehouse (data/linkedin-analytics/posts.jsonl).

Commands:
  add            Record a new published post
  sync-metrics   Pull best-available metrics from analytics into the tracker
  list           Show all tracked posts
  stats          Summary statistics
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

TRACKER_PATH = Path("notes/linkedin-published-tracker.md")
POSTS_JSONL = Path("data/linkedin-analytics/posts.jsonl")

HEADER = "| Date | Post | Format | Source | Impressions | Engagements | Rate | Window |"
SEPARATOR = "|------|------|--------|--------|-------------|-------------|------|--------|"

URL_MAP_START = "<!-- URL_MAP (auto-populated by sync-metrics, do not edit manually)"
URL_MAP_END = "-->"


# ─── Parsing ────────────────────────────────────────────────────────────

def parse_tracker(text):
    """Parse the published posts table and URL map from tracker markdown."""
    posts = []
    in_table = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith(HEADER.strip()):
            in_table = True
            continue
        if in_table and s.startswith("|---"):
            continue
        if in_table and s.startswith("|"):
            cols = [c.strip() for c in s.split("|")[1:-1]]
            if len(cols) >= 8:
                posts.append({
                    "date": cols[0],
                    "post": cols[1],
                    "format": cols[2],
                    "source": cols[3],
                    "impressions": cols[4],
                    "engagements": cols[5],
                    "rate": cols[6],
                    "window": cols[7],
                })
            continue
        if in_table and not s.startswith("|"):
            break

    url_map = parse_url_map(text)
    return posts, url_map


def parse_url_map(text):
    """Extract the URL_MAP comment block into a dict keyed by date."""
    match = re.search(
        re.escape(URL_MAP_START) + r"\n(.*?)\n" + re.escape(URL_MAP_END),
        text, re.DOTALL
    )
    if not match:
        return {}
    mapping = {}
    for line in match.group(1).strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 1)
        if len(parts) == 2:
            mapping[parts[0].strip()] = parts[1].strip()
    return mapping


def format_row(p):
    """Format a post dict as a markdown table row."""
    return (
        f"| {p['date']} "
        f"| {p['post']} "
        f"| {p['format']} "
        f"| {p['source']} "
        f"| {p['impressions']} "
        f"| {p['engagements']} "
        f"| {p['rate']} "
        f"| {p['window']} |"
    )


def rebuild_table(posts):
    """Rebuild the full table from post dicts."""
    lines = [HEADER, SEPARATOR]
    for p in posts:
        lines.append(format_row(p))
    return "\n".join(lines)


def rebuild_url_map(url_map):
    """Rebuild the URL_MAP comment block."""
    lines = [URL_MAP_START]
    for dt in sorted(url_map.keys(), reverse=True):
        lines.append(f"{dt}|{url_map[dt]}")
    lines.append(URL_MAP_END)
    return "\n".join(lines)


def write_tracker(text, posts, url_map):
    """Replace the posts table and URL map in the tracker text and write."""
    table_pattern = re.escape(HEADER) + r"\n\|[-\s|]+\n(?:\|[^\n]+\n)*"
    match = re.search(table_pattern, text)
    if not match:
        print("ERROR: Could not find posts table in tracker", file=sys.stderr)
        sys.exit(1)

    new_table = rebuild_table(posts)
    text = text[:match.start()] + new_table + "\n" + text[match.end():]

    url_block_pattern = (
        re.escape(URL_MAP_START) + r"\n.*?" + re.escape(URL_MAP_END)
    )
    new_url_block = rebuild_url_map(url_map)
    text = re.sub(url_block_pattern, new_url_block, text, flags=re.DOTALL)

    today = date.today().strftime("%Y-%m-%d")
    text = re.sub(r"Last synced: .*", f"Last synced: {today}", text)

    TRACKER_PATH.write_text(text, encoding="utf-8")


# ─── Analytics data ─────────────────────────────────────────────────────

def load_analytics_posts():
    """Load all post records from analytics JSONL."""
    if not POSTS_JSONL.exists():
        return []
    records = []
    for line in POSTS_JSONL.read_text().splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def best_record_for_post(records):
    """Given multiple records for the same post URL, pick the one with the
    widest coverage (most days between post_date and window_end).
    This gives the most complete view of the post's lifetime metrics."""
    best = None
    best_coverage = -1
    for r in records:
        try:
            post_dt = datetime.strptime(r["post_date"], "%Y-%m-%d")
            end_dt = datetime.strptime(r["window_end"], "%Y-%m-%d")
            coverage = (end_dt - post_dt).days
        except (ValueError, KeyError):
            coverage = 0
        if coverage > best_coverage:
            best = r
            best_coverage = coverage
    return best, best_coverage


def build_analytics_index(analytics_posts):
    """Build lookup indexes: by URL and by date."""
    by_url = {}
    by_date = {}
    for p in analytics_posts:
        url = p.get("post_url", "")
        dt = p.get("post_date", "")
        by_url.setdefault(url, []).append(p)
        by_date.setdefault(dt, []).append(p)
    return by_url, by_date


def match_tracker_to_analytics(tracker_post, url_map, by_url, by_date):
    """Find the best analytics record for a tracker post.
    Priority: URL match > date match."""
    dt = tracker_post["date"]

    cached_url = url_map.get(dt)
    if cached_url and cached_url in by_url:
        return best_record_for_post(by_url[cached_url])

    if dt in by_date:
        candidates = by_date[dt]
        if len(candidates) == 1:
            return best_record_for_post(
                by_url.get(candidates[0]["post_url"], candidates)
            )
        # Multiple posts on same date — try title substring matching
        hook_lower = tracker_post["post"].lower()[:30]
        for c in candidates:
            url_slug = c.get("post_url", "").lower()
            words = [w for w in hook_lower.split() if len(w) > 3]
            if any(w in url_slug for w in words):
                return best_record_for_post(
                    by_url.get(c["post_url"], [c])
                )
        # Fall back to highest-impression candidate on that date
        best_candidates = sorted(candidates, key=lambda x: x.get("impressions", 0), reverse=True)
        return best_record_for_post(
            by_url.get(best_candidates[0]["post_url"], best_candidates)
        )

    return None, 0


# ─── Commands ───────────────────────────────────────────────────────────

def cmd_add(args):
    text = TRACKER_PATH.read_text(encoding="utf-8")
    posts, url_map = parse_tracker(text)

    new_post = {
        "date": args.date,
        "post": args.hook,
        "format": args.format,
        "source": args.source or "Standalone",
        "impressions": "—",
        "engagements": "—",
        "rate": "—",
        "window": "—",
    }
    posts.insert(0, new_post)
    write_tracker(text, posts, url_map)

    print(f"  Added: {args.date} — {args.hook} [{args.format}]")
    print(f"  Total posts: {len(posts)}")
    print(f"  Run sync-metrics after next analytics import to populate metrics.")


def cmd_sync_metrics(args):
    text = TRACKER_PATH.read_text(encoding="utf-8")
    posts, url_map = parse_tracker(text)

    analytics = load_analytics_posts()
    if not analytics:
        print("No analytics data. Run linkedin-analytics import-xlsx first.")
        sys.exit(1)

    by_url, by_date = build_analytics_index(analytics)

    updated = 0
    matched = 0

    for p in posts:
        record, coverage_days = match_tracker_to_analytics(p, url_map, by_url, by_date)
        if not record:
            continue

        matched += 1

        # Cache the URL for future syncs
        if record.get("post_url") and p["date"] not in url_map:
            url_map[p["date"]] = record["post_url"]

        # Check if this is a better window than what we already have
        current_window = p.get("window", "—")
        current_days = 0
        if current_window not in ("—", ""):
            m = re.match(r"(\d+)d", current_window)
            if m:
                current_days = int(m.group(1))

        has_existing_data = p.get("window", "—") not in ("—", "")
        if has_existing_data and coverage_days <= current_days:
            continue  # don't downgrade or re-apply same window data

        imp = record.get("impressions", 0)
        eng = record.get("engagements", 0)
        rate = eng / imp if imp > 0 else 0

        p["impressions"] = f"{imp:,}"
        p["engagements"] = f"{eng:,}"
        p["rate"] = f"{rate:.1%}"
        p["window"] = f"{coverage_days}d"
        updated += 1

    write_tracker(text, posts, url_map)

    print(f"  Matched: {matched}/{len(posts)} posts")
    print(f"  Updated: {updated} posts with better metrics")
    print(f"  URL mappings cached: {len(url_map)}")


def cmd_list(args):
    text = TRACKER_PATH.read_text(encoding="utf-8")
    posts, _ = parse_tracker(text)
    limit = args.limit or len(posts)

    print(f"{'Date':<12} {'Imp':>7} {'Eng':>5} {'Rate':>6} {'Win':>5}  {'Format':<16} Post")
    print(f"{'—'*12} {'—'*7} {'—'*5} {'—'*6} {'—'*5}  {'—'*16} {'—'*40}")

    for p in posts[:limit]:
        post_text = p["post"][:42] + "…" if len(p["post"]) > 42 else p["post"]
        print(
            f"{p['date']:<12} "
            f"{p['impressions']:>7} "
            f"{p['engagements']:>5} "
            f"{p['rate']:>6} "
            f"{p['window']:>5}  "
            f"{p['format']:<16} "
            f"{post_text}"
        )


def cmd_stats(args):
    text = TRACKER_PATH.read_text(encoding="utf-8")
    posts, _ = parse_tracker(text)

    content = [p for p in posts if p["source"] not in ("Recruitment", "Social")]
    from_blog = [p for p in content if p["source"] != "Standalone"]
    carousels = [p for p in posts if "carousel" in p["format"].lower()]
    text_posts = [p for p in posts if p["format"].lower().startswith("text")]

    with_metrics = [p for p in posts if p["impressions"] not in ("—", "")]
    total_imp = 0
    for p in with_metrics:
        try:
            total_imp += int(p["impressions"].replace(",", ""))
        except ValueError:
            pass

    print("LinkedIn Tracker Stats\n")
    print(f"  Total posts:       {len(posts)}")
    print(f"  Content posts:     {len(content)}")
    print(f"  From blog:         {len(from_blog)}")
    print(f"  Standalone:        {len(content) - len(from_blog)}")
    print(f"  Carousels:         {len(carousels)}")
    print(f"  Text posts:        {len(text_posts)}")
    print(f"  With metrics:      {len(with_metrics)}")
    if with_metrics:
        print(f"  Total impressions: {total_imp:,}")
        print(f"  Avg imp/post:      {total_imp // len(with_metrics):,}")


# ─── Main ───────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="LinkedIn Published Content Tracker")
    sub = p.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Record a new published post")
    add_p.add_argument("--date", required=True, help="ISO date e.g. 2026-04-14")
    add_p.add_argument("--hook", required=True, help="Post hook/title")
    add_p.add_argument("--format", required=True, help="e.g. Text, Carousel (7p)")
    add_p.add_argument("--source", default="Standalone",
                       help="Blog slug, Standalone, Recruitment, or Social")

    sub.add_parser("sync-metrics",
                   help="Pull best metrics from analytics into tracker")

    list_p = sub.add_parser("list", help="List tracked posts")
    list_p.add_argument("--limit", type=int)

    sub.add_parser("stats", help="Summary statistics")

    args = p.parse_args()
    if not args.command:
        p.print_help()
        sys.exit(1)

    cmds = {
        "add": cmd_add,
        "sync-metrics": cmd_sync_metrics,
        "list": cmd_list,
        "stats": cmd_stats,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
