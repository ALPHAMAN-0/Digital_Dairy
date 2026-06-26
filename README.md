# 📓 Digital Diary

A personal digital diary of my learning journey — notes, topics, concepts, and resources
from **computer science, programming, networking, and software development**.

Everything here is plain Markdown in git, so it's durable, searchable, works on any device,
opens in any editor (and as an [Obsidian](https://obsidian.md) vault), and is backed up the
moment I push to GitHub. That's how I *secure* what I learn: nothing rots, nothing is lost.

---

## How this is organized — the one rule

There's a single rule for deciding where a note goes, so I never stall on "where does this belong?":

| If the note is... | It goes in... | Why |
|---|---|---|
| **Raw / tied to a source** (a class, a course) | [`courses/`](courses/) | Captured as it arrives, organized by where it came from (e.g. AIUB) |
| **Distilled / reusable knowledge** | [`topics/`](topics/) | The library I actually search months later, organized by subject |
| **A dated reflection** ("what I learned today") | [`journal/`](journal/) | The literal *diary* |
| **A pointer to something external** (book, link, video) | [`resources/`](resources/) | Things to read/watch and where to find them |

**The flow:** capture fast in `courses/` or `journal/` → once I truly understand something,
*promote* a clean version into `topics/`.

---

## Sections

- 📚 [**topics/**](topics/) — evergreen knowledge by subject
- 🎓 [**courses/**](courses/) — source-based capture (the AIUB folder lives here)
- 🗓️ [**journal/**](journal/) — dated learning log (with daily to-dos)
- 🚀 [**planner/**](planner/) — productivity hub: goals, habits, weekly reviews
- 🔗 [**resources/**](resources/) — books, courses, links, cheatsheets
- 🧩 [**_templates/**](_templates/) — copy these when starting a new note
- 📥 [**_inbox/**](_inbox/) — drop a JSON file here to auto-generate topic notes (see below)

---

## Generate notes from a JSON file

Instead of writing notes by hand, you can describe what you learned in a JSON file and let a
script create the topic notes for you:

1. Put a `.json` file in [`_inbox/`](_inbox/) (format and a full example are in
   [`_inbox/README.md`](_inbox/README.md))
2. Run:
   ```bash
   python3 scripts/generate_notes.py
   ```
3. Each entry becomes `topics/<subject>/<title>.md` and the subject's index updates itself.

Safe to re-run — existing notes are skipped. Use `--dry-run` to preview, `--force` to overwrite.

---

## Start a note from a template ✍️

For a single note, skip the copy-paste — `scripts/new.py` scaffolds the right file from
[`_templates/`](_templates/) with the date and path already filled in:

```bash
python3 scripts/new.py daily                         # journal/<year>/<today>.md
python3 scripts/new.py topic networking "TCP teardown"   # topics/networking/tcp-teardown.md
python3 scripts/new.py weekly                         # planner/weekly/<year>/<Monday>.md
python3 scripts/new.py habit                          # planner/habits/<YYYY-MM>.md
python3 scripts/new.py resource "Designing Data-Intensive Applications"
```

A `topic` note also refreshes its subject's README index automatically. Add `--date
YYYY-MM-DD` to backfill, `--dry-run` to preview, `--force` to overwrite.

---

## Read it as a website 🌐

This diary can be published as a searchable website with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/),
deployed to **GitHub Pages** by a GitHub Actions workflow. The build also adds, automatically:

- 🏷️ a **[tags](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/) index** so notes are browsable by tag
- 🔗 a **"Linked from"** (backlinks) section on each note, from your `[[wiki links]]`
- 🕘 a homepage **dashboard** (note counts, maturity breakdown, recently updated)
- 🗓️ a **"Last updated · N min read"** footer on each note (date from git history)

These are generated at build time into the temporary `docs/` folder — your source notes are
never modified.

**Preview locally:**
```bash
python3 -m pip install -r requirements-docs.txt
bash scripts/build_site.sh serve     # → http://127.0.0.1:8000
```

**Publish:** push to `main`, then enable it once at
**Repo → Settings → Pages → Build and deployment → Source: _GitHub Actions_**.
After that, [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml) rebuilds and
redeploys the site on every push. The build stages your note folders into a temporary `docs/`
dir (via [`scripts/build_site.sh`](scripts/build_site.sh)) so your repo layout stays untouched.

---

## Conventions

- **Filenames:** lowercase `kebab-case`, no spaces — e.g. `tcp-three-way-handshake.md`
- **Dates:** ISO format `YYYY-MM-DD` everywhere
- **Every folder has a `README.md`** so GitHub renders a nice landing page for it
- **Every note starts with YAML frontmatter** (title, date, tags, source, status) — see the templates
- **Links** are relative Markdown links so they work on GitHub
- **Tags** make a note findable even when it's filed in one folder

> New here (or future me)? Start in [`_templates/`](_templates/), copy a template, and drop the
> filled note into the right folder using the rule above.
