#!/usr/bin/env bash

set -euo pipefail

VOLUME=5

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

STATE="disabled"

# Toggle mechsim
if pgrep -x mechsim >/dev/null; then
  pkill -x mechsim
else
  mechsim -V 100 >/dev/null 2>&1 &
  STATE="enabled"
fi

# Send notification
notify "Mechsim" "Mechsim sound $STATE" "keyboard"
