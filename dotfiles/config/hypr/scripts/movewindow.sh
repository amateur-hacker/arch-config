#!/usr/bin/env bash

# Get the active window monitor
inactive_monitor=$(hyprctl monitors | grep -B 15 "focused: no" | awk '/Monitor/ {print $2}')

# Dispatch movewindow command
if [[ -n $inactive_monitor ]]; then
	hyprctl dispatch movewindow mon:"$inactive_monitor" && dunstctl close-all && sleep 0.1 && dunstify -i monitor "Monitor switched to $inactive_monitor" -t 1000
else
	dunstify "No inactive monitor found"
fi
