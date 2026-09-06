# CLAUDE.md — Digital_Dairy

## Commands (from README.md)
- Scaffold a note: `python3 scripts/new.py <daily|topic|weekly|habit|resource> ...`
- Generate notes from inbox JSON: `python3 scripts/generate_notes.py` (add `--dry-run` to preview, `--force` to overwrite)
- Install docs deps: `python3 -m pip install -r requirements-docs.txt`
- Preview site: `bash scripts/build_site.sh serve` → http://127.0.0.1:8000

## Rules observed
- Filenames: lowercase `kebab-case`, no spaces (README.md:104)
- Dates: ISO `YYYY-MM-DD` everywhere (README.md:105)
- Every folder must have a `README.md` landing page (README.md:106)
- Every note starts with YAML frontmatter: title, date, tags, source, status (README.md:107)
- Links are relative Markdown links, not absolute (README.md:108)
- Site build stages notes into a temporary `docs/` dir; source note folders are never modified by the build (README.md:85-86, 97-98)
- generate_notes.py is safe to re-run — existing notes are skipped unless `--force` (README.md:53)

## Read first
- README.md
- _templates/topic-note.md
- scripts/new.py

Architecture: see ARCHITECTURE.md — read before structural changes
