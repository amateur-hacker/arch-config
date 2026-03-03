#!/usr/bin/env bash

if grep open /proc/acpi/button/lid/LID/state; then
  hyprctl keyword monitor "eDP-1, 1920x1080, 1920x0, 1"
else
  if [[ $(hyprctl monitors | grep -c "Monitor") != 1 ]]; then
    hyprctl keyword monitor "eDP-1, disable"
  fi
fi
