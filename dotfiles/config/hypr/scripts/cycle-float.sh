#!/usr/bin/env bash

DIR=${1:-next}

WS_ID=$(hyprctl -j activeworkspace | jq '.id')

mapfile -t WINDOWS < <(
  hyprctl -j clients | jq -r "
    map(select(.workspace.id == ${WS_ID} and .floating == true)) |
    sort_by(.focusHistoryID) |
    .[].address
  "
)

COUNT=${#WINDOWS[@]}
((COUNT < 2)) && exit 0

case "$DIR" in
next)
  # Move top to bottom
  TOP="${WINDOWS[0]}"
  hyprctl dispatch alterzorder bottom,address:$TOP

  NEW_TOP="${WINDOWS[1]}"
  ;;

prev)
  # Move bottom to top
  BOTTOM="${WINDOWS[$((COUNT - 1))]}"
  hyprctl dispatch alterzorder top,address:$BOTTOM

  NEW_TOP="$BOTTOM"
  ;;

*)
  echo "Usage: $0 [next|prev]"
  exit 1
  ;;
esac

# hyprctl dispatch focuswindow address:$NEW_TOP
hyprctl dispatch alterzorder top,address:$NEW_TOP
