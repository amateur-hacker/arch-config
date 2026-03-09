#!/usr/bin/env bash

# NOTE: In noctalia shell tabler icons are used by default.
SOUNDPACK="$HOME/.config/wayvibes/soundpacks/akko_lavender_purples"
VOLUME=5

notify() {
  qs -c noctalia-shell ipc call toast send "$1"
}

STATE="disabled"

if pgrep -x mechsim >/dev/null; then
  pkill -x mechsim
else
  mechsim -V 100 >/dev/null 2>&1 &
  STATE="enabled"
fi

payload=$(
  cat <<EOF
{
  "title": "Mechsim",
  "body": "Mechanical sound $STATE",
  "icon": "keyboard"
}
EOF
)

notify "$payload"
