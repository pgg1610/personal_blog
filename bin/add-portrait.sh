#!/usr/bin/env bash
# Add images to the home-page portrait rotation.
#
#   bin/add-portrait.sh ~/Downloads/photo1.jpg ~/Downloads/photo2.png
#
# Each image is resized and compressed to AVIF into assets/img/portraits/,
# where the landing page discovers it automatically. Commit and deploy to
# publish. Tune with PORTRAIT_WIDTH / PORTRAIT_QUALITY if you want.
set -euo pipefail

cd "$(dirname "$0")/.."
dest="assets/img/portraits"
width="${PORTRAIT_WIDTH:-256}"
quality="${PORTRAIT_QUALITY:-60}"

if [ "$#" -eq 0 ]; then
  echo "usage: bin/add-portrait.sh <image> [image ...]" >&2
  exit 1
fi

command -v sips >/dev/null 2>&1 || { echo "sips is required (macOS)" >&2; exit 1; }
mkdir -p "$dest"

for src in "$@"; do
  if [ ! -f "$src" ]; then
    echo "skip (not found): $src" >&2
    continue
  fi
  base=$(basename "$src")
  base=${base%.*}
  slug=$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/^-//; s/-$//')
  out="$dest/$slug.avif"
  sips -s format avif -s formatOptions "$quality" --resampleWidth "$width" "$src" --out "$out" >/dev/null
  echo "added $out ($(wc -c < "$out" | tr -d ' ') bytes)"
done

echo "Done. Commit and deploy; the rotation picks up new files automatically."
