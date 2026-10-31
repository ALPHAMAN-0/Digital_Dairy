#!/usr/bin/env python3
"""
Enrich the staged MkDocs site (build-time only — never touches source notes).

Run by scripts/build_site.sh after content is staged into ./docs. It operates purely
on the staged copies, so the repo's source folders stay pristine. It:

  1. Adds a "Linked from" (backlinks) section to each note, derived from [[wiki links]].
  2. Reports dangling [[links]] (referenced notes that don't exist yet).
  3. Appends a "Last updated · N min read" footer to each note. The date comes from the
     source file's git history (the staged copy is gitignored, so the git-revision plugin
     can't be used here); reading time is word-count / 200 wpm.
  4. Generates docs/tags.md (the Material tags index page).
  5. Generates docs/index.md (homepage) with an "At a glance" dashboard + recent notes.

Usage:
    python3 scripts/enrich_site.py [docs_dir]      # default: docs
"""

from __future__ import annotations

import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date as _date
from pathlib import Path

from diary_lib import (
    CONTENT_SECTIONS,
    REPO_ROOT,
    VALID_STATUSES,
    parse_frontmatter,
    prettify,
    slugify,
    today_iso,
)

WORDS_PER_MINUTE = 200
RECENT_LIMIT = 8
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
GENERATED_PAGES = {"index.md", "tags.md"}

# Section -> the source folder it was staged from (templates is the only rename).
SECTION_SOURCE = {"templates": "_templates"}

STATUS_LABEL = {"seedling": "🌱 seedling", "growing": "🌿 growing", "evergreen": "🌳 evergreen"}


class Page:
    def __init__(self, path: Path, docs_dir: Path):
        self.path = path
        self.rel = path.relative_to(docs_dir)
        self.parts = self.rel.parts
        self.name = path.name
        self.text = path.read_text(encoding="utf-8")
        self.meta, self.body = parse_frontmatter(self.text)
        self.is_template = self.parts[0] == "templates"
        self.is_generated = self.rel.as_posix() in GENERATED_PAGES
        self.is_readme = self.name.lower() == "readme.md"
        self.source_rel = self._source_rel()
        self.last_date: str | None = None

    def _source_rel(self) -> Path | None:
        if self.is_generated:
            return None
        head = self.parts[0]
        if head in SECTION_SOURCE:
            return Path(SECTION_SOURCE[head], *self.parts[1:])
        if head in CONTENT_SECTIONS:
            return self.rel
        return self.rel

    @property
    def has_frontmatter(self) -> bool:
        return bool(self.meta)

    @property
    def is_note(self) -> bool:
        """Real content with frontmatter (incl. the databases roadmap README)."""
        return self.has_frontmatter and not self.is_template and not self.is_generated

    @property
    def is_stats_note(self) -> bool:
        """Counts toward dashboard stats / recent list (hub READMEs excluded)."""
        return self.is_note and not self.is_readme

    @property
    def section(self) -> str:
        return self.parts[0]

    @property
    def title(self) -> str:
        t = str(self.meta.get("title", "")).strip()
        if t:
            return t
        m = re.search(r"^#\s+(.*)$", self.body, re.MULTILINE)
        return m.group(1).strip() if m else prettify(self.path.stem)


def git_last_date(source_rel: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%cs", "--", source_rel.as_posix()],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    date = out.stdout.strip()
    return date or None


def resolve_date(page: Page) -> str:
    """git last-commit date → source mtime → today."""
    if page.source_rel:
        date = git_last_date(page.source_rel)
        if date:
            return date
        src = REPO_ROOT / page.source_rel
        if src.exists():
            return _date.fromtimestamp(src.stat().st_mtime).isoformat()
    # Fall back to the staged copy's own mtime, then today.
    try:
        return _date.fromtimestamp(page.path.stat().st_mtime).isoformat()
    except OSError:
        return today_iso()


def reading_minutes(body: str) -> int:
    words = len(re.findall(r"\b\w+\b", body))
    return max(1, math.ceil(words / WORDS_PER_MINUTE))


def link_key(raw: str) -> str:
    """'[[Foo Bar|alias]]' / '[[foo#heading]]' -> normalized target slug."""
    target = raw.split("|", 1)[0].split("#", 1)[0]
    return slugify(target)


def rel_link(from_page: Page, to_page: Page) -> str:
    return os.path.relpath(to_page.path, start=from_page.path.parent).replace(os.sep, "/")


def fmt_counter(counter: Counter, label=prettify) -> str:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return ", ".join(f"{label(k)} ({v})" for k, v in items)


def build_homepage(stats: dict, recent: list[Page]) -> str:
    lines = [
        "# 📓 Digital Diary",
        "",
        "Welcome to my personal learning journal — notes on **computer science, programming,**",
        "**networking, and software development**.",
        "",
        "## Explore",
        "",
        "- 📚 **[Topics](topics/)** — evergreen knowledge by subject",
        "- 🎓 **[Courses](courses/)** — notes from my classes (AIUB)",
        "- 🗓️ **[Journal](journal/)** — my daily learning log",
        "- 🚀 **[Planner](planner/)** — goals, habits, and weekly reviews",
        "- 🔗 **[Resources](resources/)** — books, courses, and links",
        "- 🏷️ **[Tags](tags/)** — browse notes by tag",
        "",
        "## 📊 At a glance",
        "",
        f"- **{stats['total']} notes** across topics, journal, planner, and resources",
    ]
    if stats["by_subject"]:
        lines.append(f"- **Topics by subject:** {fmt_counter(stats['by_subject'])}")
    if stats["by_status"]:
        status_str = " · ".join(
            f"{STATUS_LABEL.get(k, k)} ({v})"
            for k, v in sorted(stats["by_status"].items(),
                               key=lambda kv: VALID_STATUSES.index(kv[0])
                               if kv[0] in VALID_STATUSES else 99)
        )
        lines.append(f"- **By maturity:** {status_str}")
    entries = "entry" if stats["journal"] == 1 else "entries"
    lines.append(f"- **{stats['tags']} unique tags** · {stats['journal']} journal {entries}")
    if stats["dangling"]:
        lines.append(f"- ⚠️ **{stats['dangling']} dangling links** "
                     "(referenced but not written yet)")
    lines += ["", "## 🕘 Recently updated", ""]
    if recent:
        for p in recent:
            lines.append(f"- [{p.title}]({p.rel.as_posix()}) — {p.last_date}")
    else:
        lines.append("_No notes yet._")
    lines += [
        "",
        "!!! tip",
        "    Use the search bar at the top to find anything across the whole diary.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    docs_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "docs").resolve()
    if not docs_dir.is_dir():
        print(f"! enrich: docs dir not found: {docs_dir}")
        return 1

    pages = [Page(p, docs_dir) for p in sorted(docs_dir.rglob("*.md"))]

    # --- Build the link-target map (notes only; hub READMEs are not link targets) ---
    stem_map: dict[str, Page] = {}
    for p in pages:
        if p.is_template or p.is_generated or p.is_readme:
            continue
        stem_map.setdefault(link_key(p.path.stem), p)

    # --- Scan [[wiki links]] for backlinks + dangling links --------------------------
    backlinks: dict[Page, set] = defaultdict(set)
    dangling: list[tuple[str, str]] = []
    for src in pages:
        if src.is_template or src.is_generated:
            continue
        for raw in WIKILINK_RE.findall(src.text):
            key = link_key(raw)
            target = stem_map.get(key)
            if target is None:
                dangling.append((src.rel.as_posix(), raw.strip()))
            elif target is not src and target.is_note:
                backlinks[target].add(src)

    # --- Per-note enrichment: backlinks section + last-updated/reading footer ---------
    for p in pages:
        if not p.is_note:
            continue
        p.last_date = resolve_date(p)
        sections = [p.text.rstrip()]
        sources = sorted(backlinks.get(p, ()), key=lambda s: s.title.lower())
        if sources:
            items = "\n".join(f"- [{s.title}]({rel_link(p, s)})" for s in sources)
            sections.append(f"\n\n## Linked from\n\n{items}")
        sections.append(f"\n\n---\n\n*Last updated: {p.last_date} · "
                        f"{reading_minutes(p.body)} min read*\n")
        p.path.write_text("".join(sections), encoding="utf-8")

    # --- Stats for the homepage dashboard -------------------------------------------
    notes = [p for p in pages if p.is_stats_note]
    by_section = Counter(p.section for p in notes)
    by_subject = Counter(p.parts[1] for p in notes if p.section == "topics" and len(p.parts) > 2)
    by_status = Counter(
        str(p.meta.get("status", "")).strip()
        for p in notes if str(p.meta.get("status", "")).strip()
    )
    tags = {t for p in notes for t in (p.meta.get("tags") or [])}
    unique_dangling = sorted({raw for _, raw in dangling})
    stats = {
        "total": len(notes),
        "by_subject": by_subject,
        "by_status": by_status,
        "tags": len(tags),
        "journal": by_section.get("journal", 0),
        "dangling": len(unique_dangling),
    }
    recent = sorted(notes, key=lambda p: (p.last_date or "", p.title), reverse=True)[:RECENT_LIMIT]

    # --- Generate tags index + homepage ---------------------------------------------
    (docs_dir / "tags.md").write_text("# 🏷️ Tags\n\n<!-- material/tags -->\n", encoding="utf-8")
    (docs_dir / "index.md").write_text(build_homepage(stats, recent), encoding="utf-8")

    # --- Report ----------------------------------------------------------------------
    print(f"→ Enriched {len(notes)} notes · {len(tags)} tags · "
          f"{sum(len(s) for s in backlinks.values())} backlinks")
    if unique_dangling:
        print(f"⚠ {len(unique_dangling)} dangling link(s) (referenced but not written):")
        for raw in unique_dangling[:20]:
            print(f"    [[{raw}]]")
        if len(unique_dangling) > 20:
            print(f"    … and {len(unique_dangling) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
