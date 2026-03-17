#!/usr/bin/env bash

set -euo pipefail

state=$(hyprctl activewindow -j | jq -r ".floating")

if [ "$state" = "true" ]; then
  hyprctl dispatch focuswindow "tiled"
else
  hyprctl dispatch focuswindow "floating"
  hyprctl dispatch alterzorder top
fi
