# 📥 Inbox — drop JSON here

This is **where you upload the JSON file.** Put a `.json` file in this folder, then run:

```bash
python3 scripts/generate_notes.py
```

The generator reads every `*.json` here and creates a Markdown note for each learning at
`topics/<subject>/<title>.md`, with frontmatter filled in and the subject's index refreshed
automatically.

> Re-running is safe: notes that already exist are **skipped** (use `--force` to overwrite,
> `--dry-run` to preview).

## JSON format

```json
{
  "source": "AIUB - Data Communication",
  "date": "2026-06-25",
  "learnings": [
    {
      "subject": "networking",
      "title": "TCP Three-Way Handshake",
      "tags": ["tcp", "protocols"],
      "status": "growing",
      "summary": "SYN / SYN-ACK / ACK before any data flows.",
      "content": "## How it works\n1. SYN\n2. SYN-ACK\n3. ACK"
    }
  ]
}
```

### Fields

| Field | Where | Required | Meaning |
|---|---|---|---|
| `source` | top level | no | Default source for all entries (e.g. a course). Defaults to `self-study`. |
| `date` | top level | no | Default ISO date for all entries. Defaults to today. |
| `learnings` | top level | **yes** | The list of notes to generate. (A bare JSON array also works.) |
| `subject` | per entry | **yes** | The topic folder it lands in → `topics/<subject>/`. Free text; slugified. |
| `title` | per entry | **yes** | Note title → filename and `# heading`. |
| `tags` | per entry | no | Array of tags (or a comma-separated string). |
| `status` | per entry | no | `seedling` \| `growing` \| `evergreen`. Defaults to `seedling`. |
| `summary` | per entry | no | One-liner → the **TL;DR** block. |
| `content` | per entry | no | Markdown body (use `\n` for line breaks in JSON). |
| `source` | per entry | no | Overrides the top-level `source` for this entry. |
| `date` | per entry | no | Overrides the top-level `date` for this entry. |

See [`example.json`](example.json) for a complete sample.

> Tip: `subject` is matched to a folder by slug, so `"Computer Science"`, `"computer-science"`,
> and `"COMPUTER SCIENCE"` all land in `topics/computer-science/`. New subjects create a new
> topic folder automatically.
