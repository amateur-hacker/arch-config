#!/usr/bin/env bash

set -euo pipefail

TMP_FILE="/tmp/lens_search.png"

# Select region
GEOM=$(slurp)
[ -z "$GEOM" ] && exit 1

# Capture screenshot
grim -g "$GEOM" "$TMP_FILE"

# Upload image
URL=$(curl -sF "files[]=@$TMP_FILE" https://uguu.se/upload | jq -r '.files[0].url')

# Cleanup
rm -f "$TMP_FILE"

notify() {
  local TITLE="$1"
  local BODY="$2"
  local ICON="$3"

  JSON=$(jq -n \
    --arg title "$TITLE" \
    --arg body "$BODY" \
    --arg icon "$ICON" \
    '{
      title: $title,
      body: $body,
      icon: $icon
    }')

  qs -c noctalia-shell ipc call toast send "$JSON"
}

# Handle result
if [ -n "$URL" ] && [ "$URL" != "null" ]; then
  notify "Lens Search" "Opening Google Lens..." "camera-search"
  xdg-open "https://lens.google.com/uploadbyurl?url=$URL" >/dev/null 2>&1
else
  notify "Lens Search Failed" "Image upload failed" "alert-circle"
  exit 1
fi
