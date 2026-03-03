#!/usr/bin/env bash

inactive_monitor=$(hyprctl monitors | grep -B 15 'focused: no' | awk '/Monitor/ {print $2}')

if [[ -n $inactive_monitor ]]; then
	hyprctl dispatch focusmonitor +1 && dunstctl close-all && sleep 0.1 && dunstify -i monitor "Monitor switched to $inactive_monitor" -t 1000
else
	dunstify "No active monitor found"
fi
