#!/usr/bin/env bash

set -euo pipefail

# Screenshot directory
DIR="${XDG_PICTURES_DIR:-$HOME/Pictures}/screenshots"
mkdir -p "$DIR"

# Generate timestamped filename
timestamp=$(date +"%d-%m-%y_%H-%M-%S")
file="$DIR/${timestamp}.png"

# Default mode and action
mode="output"
action="save"

# Counters to prevent multiple modes/actions
mode_count=0
action_count=0

# Get currently focused monitor name
monitor=$(hyprctl monitors -j | jq -r '.[] | select(.focused) | .name')

# Send notification (custom shell IPC)
notify() {
  qs -c noctalia-shell ipc call toast send "{
    \"title\": \"Screenshot\",
    \"body\": \"$1\",
    \"icon\": \"camera\"
  }"
}

# Help message
show_help() {
  cat <<EOF
Usage: $(basename "$0") [options]

Modes:
  -s, --select        Select region
  -a, --active        Active window
  -f, --fullscreen    Active monitor (default)

Actions:
  -c, --copy          Copy to clipboard
  -C, --save          Save
  -e, --edit          Edit in satty
EOF
}

# Convert long options to short options for getopts
args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
  --select) args+=(-s) ;;
  --active) args+=(-a) ;;
  --fullscreen) args+=(-f) ;;
  --copy) args+=(-c) ;;
  --save) args+=(-S) ;;
  --edit) args+=(-e) ;;
  --help)
    show_help
    exit 0
    ;;
  *)
    args+=("$1")
    ;;
  esac
  shift
done

set -- "${args[@]}"

# Parse options
while getopts "safcSe" opt; do
  case $opt in

  # Select region mode
  s)
    ((++mode_count))
    ((mode_count > 1)) && {
      echo "Error: multiple modes specified"
      exit 1
    }
    mode="area"
    ;;

  # Active window mode
  a)
    ((++mode_count))
    ((mode_count > 1)) && {
      echo "Error: multiple modes specified"
      exit 1
    }
    mode="active"
    ;;

  # Fullscreen (focused monitor)
  f)
    ((++mode_count))
    ((mode_count > 1)) && {
      echo "Error: multiple modes specified"
      exit 1
    }
    mode="output"
    ;;

  # Copy to clipboard
  c)
    ((++action_count))
    ((action_count > 1)) && {
      echo "Error: multiple actions specified"
      exit 1
    }
    action="copy"
    ;;

  # Save to file
  S)
    ((++action_count))
    ((action_count > 1)) && {
      echo "Error: multiple actions specified"
      exit 1
    }
    action="save"
    ;;

  # Edit screenshot in satty
  e)
    ((++action_count))
    ((action_count > 1)) && {
      echo "Error: multiple actions specified"
      exit 1
    }
    action="edit"
    ;;

  esac
done

# Build grim command based on mode
case "$mode" in
area)
  geom=$(slurp)
  [[ -z "$geom" ]] && exit 1 # exit if selection cancelled
  cmd=(grim -g "$geom")
  ;;
active)
  geom=$(hyprctl activewindow -j | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"')
  [[ -z "$geom" ]] && exit 1
  cmd=(grim -g "$geom")
  ;;
output)
  cmd=(grim -o "$monitor")
  ;;
esac

# Perform selected action
case "$action" in
edit)
  "${cmd[@]}" -t ppm - | satty --filename - --fullscreen --output-filename "$file"
  ;;
copy)
  "${cmd[@]}" - | wl-copy && notify "Copied to clipboard"
  ;;
save)
  "${cmd[@]}" "$file" && notify "Saved → $file"
  ;;
esac
