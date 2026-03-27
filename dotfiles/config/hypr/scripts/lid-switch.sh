#!/usr/bin/env bash

LID_STATE=$(grep -r "state" /proc/acpi/button/lid/ 2>/dev/null | grep -i open)

EXTERNAL_MONITORS=$(hyprctl monitors | grep -v "eDP-1" | grep -c "Monitor")

if [[ -n "$LID_STATE" ]]; then
  hyprctl keyword monitor "eDP-1, 1920x1080, 1920x0, 1"
else
  if [[ "$EXTERNAL_MONITORS" -gt 0 ]]; then
    hyprctl keyword monitor "eDP-1, disable"
  fi
fi
