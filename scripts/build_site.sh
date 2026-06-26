#!/usr/bin/env bash
#
# Build (or preview) the Digital Diary as a static website using MkDocs Material.
#
# Your notes live at the repo root. MkDocs builds from a `docs/` folder and won't
# let its output folder sit inside the content folder — so this script *stages*
# the note folders into a temporary ./docs directory and builds from there. The
# repo's clean root layout is never touched, and CI uses this exact same script.
#
#   bash scripts/build_site.sh          # build the site into ./site
#   bash scripts/build_site.sh serve    # live preview at http://127.0.0.1:8000
#
# Note: `serve` stages once and watches ./docs. After editing source notes,
# stop it and re-run to pick up the changes.
#
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v mkdocs >/dev/null 2>&1; then
  echo "✗ mkdocs not found. Install the docs dependencies first:" >&2
  echo "    python3 -m pip install -r requirements-docs.txt" >&2
  exit 1
fi

# Folders that make up the published site.
CONTENT=(topics courses journal planner resources)

echo "→ Staging content into ./docs"
rm -rf docs
mkdir -p docs
for item in "${CONTENT[@]}"; do
  if [[ -d "$item" ]]; then
    cp -R "$item" docs/
  else
    echo "  · skipping missing folder: $item"
  fi
done

# Publish the note templates too, under a web-friendly name
# (MkDocs ignores folders that start with "_").
cp -R _templates docs/templates

# Rewrite links that point at the "_templates" source folder so they resolve on the site.
find docs -name '*.md' -print0 | xargs -0 perl -pi -e 's{_templates/}{templates/}g'

# Enrich the staged site: backlinks, last-updated/reading-time footers, the tags index,
# and the homepage dashboard. Operates only on ./docs — source notes are never touched.
echo "→ Enriching staged site"
python3 scripts/enrich_site.py docs

if [[ "${1:-build}" == "serve" ]]; then
  echo "→ Serving at http://127.0.0.1:8000 (Ctrl+C to stop)"
  exec mkdocs serve
else
  echo "→ Building site/"
  mkdocs build
  echo "✓ Done — open site/index.html or deploy the site/ folder."
fi
