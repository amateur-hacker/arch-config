#!/usr/bin/env bash

set -euo pipefail

notify() {
  qs -c noctalia-shell ipc call toast send "$1"
}

STATE="disabled"

if pgrep -x wshowkeys >/dev/null; then
  pkill -x wshowkeys
else
  setsid -f wshowkeys \
    -a bottom -a right \
    -F "Sans Bold 30" \
    -s "#bebefe" \
    -f "#cdd6f4" \
    -b "#1e1e2e" \
    -l 60 >/dev/null 2>&1
  STATE="enabled"
fi

payload=$(
  cat <<EOF
{
  "title": "Wshowkeys",
  "body": "Show keys $STATE",
  "icon": "keyboard"
}
EOF
)

notify "$payload"
