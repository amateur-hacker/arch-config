#!/usr/bin/env bash

DIR=${1:-next}

ACTIVE=$(hyprctl -j activewindow)

IS_FLOATING=$(jq -r '.floating' <<<"$ACTIVE")

if [[ "$IS_FLOATING" == "true" ]]; then
  case "$DIR" in
  next)
    hyprctl dispatch cyclenext floating
    hyprctl dispatch bringactivetotop
    ;;
  prev)
    hyprctl dispatch cyclenext prev floating
    hyprctl dispatch bringactivetotop
    ;;
  *)
    exit 1
    ;;
  esac

else
  # ----- TILED STACK LOGIC -----

  case "$DIR" in
  next)
    hyprctl dispatch layoutmsg cyclenext
    ;;
  prev)
    hyprctl dispatch layoutmsg cycleprev
    ;;
  *)
    exit 1
    ;;
  esac
fi
