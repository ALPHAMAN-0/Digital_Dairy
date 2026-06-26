#!/usr/bin/env python3
"""
Shared helpers for the Digital Diary scripts.

Standard library only — no third-party dependencies, no pip install. This keeps the
author-invoked tools (generate_notes.py, new.py) runnable on a bare Python install.

Used by:
    - generate_notes.py  (JSON -> topic notes)
    - new.py             (scaffold a note from a template)
    - enrich_site.py     (build-time site enrichment)
"""

from __future__ import annotations

import re
from datetime import date as _date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "topics"
TEMPLATES_DIR = REPO_ROOT / "_templates"
INBOX_DIR = REPO_ROOT / "_inbox"

# Content folders that make up the published site (also staged by build_site.sh).
CONTENT_SECTIONS = ("topics", "courses", "journal", "planner", "resources")

# Allowed values for a note's `status:` frontmatter field.
VALID_STATUSES = ("seedling", "growing", "evergreen")

# The subject README's note list is regenerated between these markers.
NOTES_START = "<!-- notes:start -->"
NOTES_END = "<!-- notes:end -->"

# Month names (avoid locale-dependent strftime so output is deterministic).
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def slugify(text: str) -> str:
    """'TCP Three-Way Handshake' -> 'tcp-three-way-handshake'."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "untitled"


def prettify(slug: str) -> str:
    """'computer-science' -> 'Computer Science'."""
    return slug.replace("-", " ").replace("_", " ").title()


def yaml_quote(value: str) -> str:
    """Safely quote a string for a YAML frontmatter scalar."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def today_iso() -> str:
    return _date.today().isoformat()


def month_label(d: _date) -> str:
    """date(2026, 6, 1) -> 'June 2026'."""
    return f"{MONTHS[d.month - 1]} {d.year}"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Split a Markdown document into (metadata, body).

    Returns ({}, text) when there is no YAML frontmatter. The parser is intentionally
    minimal (stdlib only, no PyYAML): it handles scalar values and inline lists like
    `tags: [a, b, c]`, which is everything this project's frontmatter uses.
    """
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
    if not m:
        return {}, text
    front, body = m.group(1), text[m.end():]
    meta: dict = {}
    for line in front.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        # Strip YAML-style trailing comments (whitespace + '#'); leaves URLs intact.
        val = re.sub(r"\s+#.*$", "", raw).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            meta[key] = [
                part.strip().strip('"').strip("'")
                for part in inner.split(",")
                if part.strip()
            ]
        else:
            meta[key] = val.strip('"').strip("'")
    return meta, body


def read_note_title(path: Path) -> str | None:
    """Pull the title from a note's frontmatter, falling back to its first H1."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    meta, _ = parse_frontmatter(text)
    title = str(meta.get("title", "")).strip()
    if title:
        return title
    m = re.search(r"^#\s+(.*)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def refresh_index(subject_dir: Path, subject_slug: str) -> None:
    """Regenerate the auto-managed note list inside the subject's README.md."""
    notes = sorted(p for p in subject_dir.glob("*.md") if p.name.lower() != "readme.md")
    if notes:
        body = "\n".join(
            f"- [{read_note_title(p) or prettify(p.stem)}]({p.name})" for p in notes
        )
    else:
        body = "_No notes yet._"
    block = f"{NOTES_START}\n{body}\n{NOTES_END}"

    readme = subject_dir / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        if NOTES_START in text and NOTES_END in text:
            pre = text.split(NOTES_START)[0]
            post = text.split(NOTES_END, 1)[1]
            text = pre + block + post
        else:
            text = text.rstrip() + "\n\n## Notes\n" + block + "\n"
    else:
        text = f"# {prettify(subject_slug)}\n\n## Notes\n{block}\n"
    readme.write_text(text, encoding="utf-8")
