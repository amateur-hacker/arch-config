#!/usr/bin/env bash

set -euo pipefail

# Default window size.
# Accepts pixels (960) or percentage of monitor size (65%).
WIDTH=${1:-65%}
HEIGHT=${2:-65%}

# Get active workspace ID and currently focused window address
WS=$(hyprctl -j activeworkspace | jq '.id')
ACTIVE=$(hyprctl -j activewindow | jq -r '.address')

# Read monitor geometry and reserved areas
# reserved order: [left, top, right, bottom]
read MON_X MON_Y MON_W MON_H LEFT TOP RIGHT BOTTOM <<<"$(
  hyprctl -j monitors |
    jq -r '.[] | select(.focused) |
  "\(.x) \(.y) \(.width) \(.height) \(.reserved[0]) \(.reserved[1]) \(.reserved[2]) \(.reserved[3])"'
)"

# Convert percentage window sizes into pixels
[[ $WIDTH == *% ]] && WIDTH=$((MON_W * ${WIDTH%%%} / 100))
[[ $HEIGHT == *% ]] && HEIGHT=$((MON_H * ${HEIGHT%%%} / 100))

# Calculate visible workspace (excluding bars/panels)
VISIBLE_X=$((MON_X + LEFT))
VISIBLE_Y=$((MON_Y + TOP))

VISIBLE_W=$((MON_W - LEFT - RIGHT))
VISIBLE_H=$((MON_H - TOP - BOTTOM))

# Compute centered position inside visible workspace
CENTER_X=$((VISIBLE_X + (VISIBLE_W - WIDTH) / 2))
CENTER_Y=$((VISIBLE_Y + (VISIBLE_H - HEIGHT) / 2))

# Collect all windows on the active workspace
# Format: "address floating"
mapfile -t windows < <(
  hyprctl -j clients |
    jq -r --argjson ws "$WS" \
      '.[] | select(.workspace.id==$ws) | "\(.address) \(.floating)"'
)

# Detect if every window is already floating
all_float=true
for w in "${windows[@]}"; do
  [[ $w == *" false" ]] && {
    all_float=false
    break
  }
done

# Build a single batch command to reduce IPC calls
batch=""

for w in "${windows[@]}"; do
  read -r addr floating <<<"$w"

  # If all windows are floating → toggle everything back to tiled
  # Otherwise float any tiled windows
  if $all_float || [[ $floating == false ]]; then
    batch+="dispatch togglefloating address:$addr;"
  fi

  # When floating windows are being created, resize + center them
  if ! $all_float && [[ $floating == false ]]; then
    batch+="dispatch resizewindowpixel exact $WIDTH $HEIGHT,address:$addr;"
    batch+="dispatch movewindowpixel exact $CENTER_X $CENTER_Y,address:$addr;"

    # Stack non-active windows first
    [[ "$addr" != "$ACTIVE" ]] && batch+="dispatch alterzorder top,address:$addr;"
  fi
done

# Finally ensure the active window is on top of the floating stack
[[ "$ACTIVE" != "null" ]] && batch+="dispatch alterzorder top,address:$ACTIVE;"

# Execute all window operations in one compositor call
hyprctl --batch "$batch"
