#!/usr/bin/env bash

set -euo pipefail

notify() {
  local TITLE="$1"
  local BODY="$2"
  local ICON="$3"
  local DURATION=3000

  LENGTH=$(echo "$BODY" | wc -c)

  if [ "$LENGTH" -gt 80 ]; then
    DURATION=5000
  fi

  JSON=$(jq -n \
    --arg title "$TITLE" \
    --arg body "$BODY" \
    --arg icon "$ICON" \
    --arg duration "$DURATION" \
    '{
      title: $title,
      body: $body,
      icon: $icon,
      duration: $duration
    }')

  qs -c noctalia-shell ipc call toast send "$JSON"
}

# Get and sanitize selected text
TEXT=$(wl-paste --primary 2>/dev/null |
  sed 's/^[ \t]*//;s/[ \t]*$//' |
  tr '[:upper:]' '[:lower:]' |
  sed 's/[^a-z-]//g')

[ -z "$TEXT" ] && {
  notify "Search Meaning" "No text selected" "alert-circle"
  exit 1
}

# Fetch dictionary data
RESPONSE=$(curl -s "https://api.dictionaryapi.dev/api/v2/entries/en/$TEXT")

if echo "$RESPONSE" | jq -e '.[0].word' >/dev/null 2>&1; then

  WORD=$(echo "$RESPONSE" | jq -r '.[0].word')

  DATA=$(echo "$RESPONSE" | jq -r '
    .[0].meanings[0] as $m |
    $m.definitions[0] as $d |
    {
      pos: $m.partOfSpeech,
      def: $d.definition,
      ex: ($d.example // "")
    }
  ')

  PART_OF_SPEECH=$(echo "$DATA" | jq -r '.pos')
  DEFINITION=$(echo "$DATA" | jq -r '.def')
  EXAMPLE=$(echo "$DATA" | jq -r '.ex')

  BODY=$(printf "%s — %s" "$PART_OF_SPEECH" "$DEFINITION")

  [ -n "$EXAMPLE" ] &&
    BODY=$(printf "%s\n\nExample: \"%s\"" "$BODY" "$EXAMPLE")

  notify "$WORD" "$BODY" "book"

else
  notify "Search Meaning" "No definition found" "alert-circle"
fi
