#!/usr/bin/env bash

set -euo pipefail

# Default window size (can be absolute pixels or percentage of monitor size).
# Example: "960" (px) or "50%" (percentage).
WIDTH=${1:-65%}
HEIGHT=${2:-65%}

# Extract active window's floating state
FLOATING=$(hyprctl -j activewindow | jq -r '.floating')

# Toggle active window floating state
hyprctl dispatch togglefloating

# If the active window is not floating yet, resize and center it
if [[ "$FLOATING" == "false" ]]; then
  hyprctl dispatch resizeactive exact "$WIDTH" "$HEIGHT"
  hyprctl dispatch centerwindow
  hyprctl dispatch alterzorder top
fi
