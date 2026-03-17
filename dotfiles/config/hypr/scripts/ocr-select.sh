#!/usr/bin/env bash

set -euo pipefail

# Select screen region
geom=$(slurp) || exit 1
[[ -z "$geom" ]] && exit 1

# Build OCR language list (eng+deu+...)
langs=$(tesseract --list-langs | sed '1d' | paste -sd+ -)

# Create temporary file for OCR output
tmp="/tmp/ocr-selected-text"
trap 'rm -f "$tmp.txt"' EXIT

# Capture selected region and run OCR
grim -g "$geom" - |
  tesseract stdin "$tmp" -l "$langs" 2>/dev/null

# Exit if OCR produced no text
[[ ! -s "$tmp.txt" ]] && exit 0

# Copy result to clipboard
wl-copy <"$tmp.txt"

# Open result in editor inside terminal
"${TERMINAL:-kitty}" -e "${EDITOR:-nvim}" "$tmp.txt"
