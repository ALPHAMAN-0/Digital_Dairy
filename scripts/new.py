#!/usr/bin/env python3
"""
Scaffold a new diary entry from a template, with the date and path filled in.

The templates in _templates/ are the source of truth for each note's structure; this
script just copies one, substitutes the date/title placeholders, and writes it to the
right folder. Standard library only — no pip install.

Usage:
    python3 scripts/new.py daily                       # journal/<year>/<today>.md
    python3 scripts/new.py topic networking "TCP teardown"
    python3 scripts/new.py weekly                      # planner/weekly/<year>/<Monday>.md
    python3 scripts/new.py habit                       # planner/habits/<YYYY-MM>.md
    python3 scripts/new.py resource "Computer Networking (Kurose)"

Options (all subcommands):
    --date YYYY-MM-DD   use this date instead of today
    --force             overwrite the file if it already exists
    --dry-run           print the path and content, write nothing
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date as _date
from datetime import timedelta
from pathlib import Path

from diary_lib import (
    REPO_ROOT,
    TEMPLATES_DIR,
    TOPICS_DIR,
    month_label,
    refresh_index,
    slugify,
    yaml_quote,
)


def read_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def set_title(content: str, title: str) -> str:
    """Replace the frontmatter `title:` line with a safely-quoted value."""
    return re.sub(r"(?m)^title:.*$", f"title: {yaml_quote(title)}", content, count=1)


# --- per-type renderers: return (target_path, content[, subject_slug]) ----------------

def render_daily(d: _date):
    iso = d.isoformat()
    content = read_template("daily-log.md").replace("2026-06-25", iso)
    target = REPO_ROOT / "journal" / str(d.year) / f"{iso}.md"
    return target, content


def render_weekly(d: _date):
    monday = d - timedelta(days=d.weekday())
    iso = monday.isoformat()
    content = read_template("weekly-review.md").replace("2026-06-22", iso)
    target = REPO_ROOT / "planner" / "weekly" / str(monday.year) / f"{iso}.md"
    return target, content


def render_habit(d: _date):
    content = read_template("habit-month.md")
    content = content.replace("Month YYYY", month_label(d))
    content = content.replace("2026-06-25", d.isoformat())          # frontmatter date
    content = content.replace("2026-06-01", d.replace(day=1).isoformat())  # sample row
    target = REPO_ROOT / "planner" / "habits" / f"{d.year}-{d.month:02d}.md"
    return target, content


def render_topic(d: _date, subject: str, title: str):
    content = set_title(read_template("topic-note.md"), title)
    content = content.replace("<Concept name>", title)
    content = content.replace("2026-06-25", d.isoformat())
    subject_slug = slugify(subject)
    target = TOPICS_DIR / subject_slug / f"{slugify(title)}.md"
    return target, content, subject_slug


def render_resource(d: _date, title: str):
    content = set_title(read_template("resource.md"), title)
    content = content.replace("<Resource title>", title)
    content = content.replace("2026-06-25", d.isoformat())
    target = REPO_ROOT / "resources" / f"{slugify(title)}.md"
    return target, content


def write_note(target: Path, content: str, force: bool, dry_run: bool) -> bool:
    rel = target.relative_to(REPO_ROOT)
    if target.exists() and not force:
        print(f"! exists (use --force to overwrite): {rel}")
        return False
    if dry_run:
        print(f"+ would write: {rel}\n")
        print("\n".join("    " + line for line in content.splitlines()))
        return True
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"+ wrote: {rel}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new diary entry from a template.")
    sub = parser.add_subparsers(dest="kind", required=True)

    def add_common(p):
        p.add_argument("--date", help="date to use (YYYY-MM-DD); defaults to today")
        p.add_argument("--force", action="store_true", help="overwrite if the file exists")
        p.add_argument("--dry-run", action="store_true", help="show the result, write nothing")

    for name in ("daily", "weekly", "habit"):
        add_common(sub.add_parser(name))
    p_topic = sub.add_parser("topic")
    p_topic.add_argument("subject", help="subject folder, e.g. networking")
    p_topic.add_argument("title", help="note title, e.g. \"TCP teardown\"")
    add_common(p_topic)
    p_resource = sub.add_parser("resource")
    p_resource.add_argument("title", help="resource title")
    add_common(p_resource)

    args = parser.parse_args()

    if args.date:
        try:
            d = _date.fromisoformat(args.date)
        except ValueError:
            print(f"! invalid --date {args.date!r}: expected YYYY-MM-DD")
            return 2
    else:
        d = _date.today()

    subject_slug = None
    if args.kind == "daily":
        target, content = render_daily(d)
    elif args.kind == "weekly":
        target, content = render_weekly(d)
    elif args.kind == "habit":
        target, content = render_habit(d)
    elif args.kind == "topic":
        target, content, subject_slug = render_topic(d, args.subject, args.title)
    elif args.kind == "resource":
        target, content = render_resource(d, args.title)
    else:  # pragma: no cover - argparse enforces a valid subcommand
        parser.error(f"unknown command {args.kind!r}")

    wrote = write_note(target, content, args.force, args.dry_run)

    # Keep the subject index in sync, exactly like generate_notes.py does.
    if wrote and not args.dry_run and args.kind == "topic" and subject_slug:
        refresh_index(TOPICS_DIR / subject_slug, subject_slug)

    return 0 if wrote else 1


if __name__ == "__main__":
    sys.exit(main())
