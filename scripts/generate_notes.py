#!/usr/bin/env python3
"""
Generate topic-organized Markdown notes from JSON.

Drop a JSON file in _inbox/ (see _inbox/README.md for the format), then run:

    python3 scripts/generate_notes.py

Each "learning" entry becomes a note at topics/<subject>/<title>.md with YAML
frontmatter, and the subject's README index is refreshed automatically.

Standard library only — no third-party dependencies, no pip install.

Usage:
    python3 scripts/generate_notes.py                 # process every *.json in _inbox/
    python3 scripts/generate_notes.py path/to/file.json
    python3 scripts/generate_notes.py --dry-run       # show what would happen, write nothing
    python3 scripts/generate_notes.py --force         # overwrite notes that already exist
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from diary_lib import (
    INBOX_DIR,
    REPO_ROOT,
    TOPICS_DIR,
    VALID_STATUSES,
    refresh_index,
    slugify,
    today_iso,
    yaml_quote,
)


def build_note(entry: dict, title: str, default_source: str, default_date: str) -> str:
    tags = entry.get("tags", []) or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    status = str(entry.get("status", "seedling")).strip() or "seedling"
    if status not in VALID_STATUSES:
        print(f"  ! note '{title}': unknown status {status!r} "
              f"(expected one of {', '.join(VALID_STATUSES)}) — keeping it anyway")
    source = str(entry.get("source", default_source)).strip() or "self-study"
    date = str(entry.get("date", default_date)).strip() or default_date
    summary = str(entry.get("summary", "")).strip()
    content = str(entry.get("content", "")).strip()

    tag_list = ", ".join(yaml_quote(str(t)) for t in tags)
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date}",
        f"tags: [{tag_list}]",
        f"source: {yaml_quote(source)}",
        f"status: {status}",
        "---",
        "",
        f"# {title}",
        "",
    ]
    if summary:
        lines += ["## TL;DR", f"> {summary}", ""]
    if content:
        lines += [content, ""]
    if not summary and not content:
        lines += ["_No details captured yet._", ""]
    return "\n".join(lines)


def load_doc(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"learnings": data}
    if isinstance(data, dict):
        return data
    raise ValueError("JSON root must be an object or a list of learnings")


def process_file(path: Path, force: bool, dry_run: bool):
    doc = load_doc(path)
    default_source = str(doc.get("source", "self-study")).strip() or "self-study"
    default_date = str(doc.get("date", today_iso())).strip() or today_iso()
    learnings = doc.get("learnings", [])
    if not isinstance(learnings, list):
        raise ValueError("'learnings' must be a list")

    created, skipped, seen_subjects = [], [], set()

    for i, entry in enumerate(learnings):
        if not isinstance(entry, dict):
            print(f"  ! entry #{i + 1} skipped: not an object")
            continue
        subject = str(entry.get("subject", "")).strip()
        title = str(entry.get("title", "")).strip()
        if not subject or not title:
            print(f"  ! entry #{i + 1} skipped: needs both 'subject' and 'title'")
            continue

        subject_slug = slugify(subject)
        subject_dir = TOPICS_DIR / subject_slug
        seen_subjects.add((subject_dir, subject_slug))
        target = subject_dir / f"{slugify(title)}.md"
        rel = target.relative_to(REPO_ROOT)

        if target.exists() and not force:
            skipped.append(rel)
            print(f"  - skip (exists): {rel}")
            continue

        if dry_run:
            print(f"  + would write: {rel}")
            created.append(rel)
            continue

        subject_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(build_note(entry, title, default_source, default_date), encoding="utf-8")
        created.append(rel)
        print(f"  + wrote: {rel}")

    if not dry_run:
        for subject_dir, subject_slug in seen_subjects:
            if subject_dir.exists():
                refresh_index(subject_dir, subject_slug)

    return created, skipped


def gather_json_paths(arg_paths):
    paths = []
    for target in (arg_paths or [str(INBOX_DIR)]):
        p = Path(target)
        if not p.is_absolute():
            p = Path.cwd() / p
        p = p.resolve()
        if p.is_dir():
            paths.extend(sorted(p.glob("*.json")))
        elif p.is_file():
            paths.append(p)
        else:
            print(f"! not found: {target}")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate topic notes from JSON.")
    parser.add_argument("paths", nargs="*", help="JSON files or directories (default: _inbox/)")
    parser.add_argument("--force", action="store_true", help="overwrite notes that already exist")
    parser.add_argument("--dry-run", action="store_true", help="show actions without writing")
    args = parser.parse_args()

    json_paths = gather_json_paths(args.paths)
    if not json_paths:
        print(f"No JSON files found. Drop one in {INBOX_DIR.name}/ and rerun.")
        return 0

    total_created = total_skipped = 0
    for jp in json_paths:
        print(f"\n{jp.name}:")
        try:
            created, skipped = process_file(jp, args.force, args.dry_run)
        except (ValueError, json.JSONDecodeError) as e:
            print(f"  ! could not process: {e}")
            continue
        total_created += len(created)
        total_skipped += len(skipped)

    verb = "would create" if args.dry_run else "created"
    print(f"\nDone: {verb} {total_created} note(s), skipped {total_skipped} existing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
