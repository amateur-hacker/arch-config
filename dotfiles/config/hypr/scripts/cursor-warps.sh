#!/usr/bin/env bash

move_to_focused() {
  hyprctl dispatch movecursor "$(
    hyprctl -j activewindow 2>/dev/null |
      jq -r '
        select(.address != null) |
        "\(.at[0] + (.size[0]/2 | rint)) \(.at[1] + (.size[1]/2 | rint))"
      '
  )" >/dev/null
}

move_to_window_id() {
  local ID=$1
  hyprctl dispatch movecursor "$(
    hyprctl -j clients |
      jq -r '
        map(select(.address=="0x'"$ID"'"))[0] |
        "\(.at[0] + (.size[0]/2 | rint)) \(.at[1] + (.size[1]/2 | rint))"
      '
  )" >/dev/null
}

socat -u "unix-connect:${XDG_RUNTIME_DIR}/hypr/${HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock" stdout |
  while read -r line; do
    case $line in
    "openwindow>>"*)
      ID=${line#openwindow>>}
      ID=${ID%%,*}
      move_to_window_id "$ID"
      ;;
    "closewindow>>"*)
      # slight delay so focus updates correctly
      sleep 0.05
      move_to_focused
      ;;
    esac
  done
