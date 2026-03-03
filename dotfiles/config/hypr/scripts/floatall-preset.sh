#!/usr/bin/env bash

WIDTH=${1:-65%}
HEIGHT=${2:-65%}
OFFSET=${3:-20}

WS_ID=$(hyprctl -j activeworkspace | jq '.id')

MONITOR=$(hyprctl -j monitors | jq '.[] | select(.focused==true)')
MON_X=$(echo "$MONITOR" | jq '.x')
MON_Y=$(echo "$MONITOR" | jq '.y')
MON_W=$(echo "$MONITOR" | jq '.width')
MON_H=$(echo "$MONITOR" | jq '.height')

if [[ "$WIDTH" == *% ]]; then
  WIDTH=$((MON_W * ${WIDTH%%%} / 100))
fi

if [[ "$HEIGHT" == *% ]]; then
  HEIGHT=$((MON_H * ${HEIGHT%%%} / 100))
fi

CENTER_X=$((MON_X + (MON_W - WIDTH) / 2))
CENTER_Y=$((MON_Y + (MON_H - HEIGHT) / 2))

mapfile -t WINDOWS < <(
  hyprctl -j clients | jq -r "
    map(select(.workspace.id == ${WS_ID})) |
    sort_by(.focusHistoryID) |
    .[] |
    @base64
  "
)

INDEX=0
TOPMOST=""

# Toggle all windows floating state
hyprctl dispatch workspaceopt allfloat

for WIN_B64 in "${WINDOWS[@]}"; do
  WIN=$(echo "$WIN_B64" | base64 -d)

  ADDR=$(jq -r '.address' <<<"$WIN")
  FLOATING=$(jq -r '.floating' <<<"$WIN")
  FOCUS_ID=$(jq -r '.focusHistoryID' <<<"$WIN")

  X=$((CENTER_X - OFFSET * INDEX))
  Y=$((CENTER_Y - OFFSET * INDEX))

  # sleep 1
  if [[ "$FLOATING" == "false" ]]; then
    hyprctl --batch "
        dispatch resizewindowpixel exact $WIDTH $HEIGHT,address:$ADDR;
        dispatch movewindowpixel exact $X $Y,address:$ADDR
    "
  fi

  if [[ $FOCUS_ID == 0 ]]; then
    TOPMOST=$ADDR
  fi
  INDEX=$((INDEX + 1))
done

if [[ -n "$TOPMOST" ]]; then
  # hyprctl dispatch focuswindow address:$TOPMOST
  hyprctl dispatch alterzorder top,address:$TOPMOST
fi
