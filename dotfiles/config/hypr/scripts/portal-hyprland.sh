#!/bin/bash
# __  ______   ____
# \ \/ /  _ \ / ___|
#  \  /| | | | |  _
#  /  \| |_| | |_| |
# /_/\_\____/ \____|
#
# -----------------------------------------------------
sleep 1

killall xdg-desktop-portal-hyprland
killall xdg-desktop-portal
killall xdg-desktop-portal-gtk
sleep 1

/usr/lib/xdg-desktop-portal-hyprland &
sleep 2

if [ -f /usr/lib/xdg-desktop-portal-gtk ]; then
  /usr/lib/xdg-desktop-portal-gtk &
  sleep 0.5
fi

/usr/lib/xdg-desktop-portal &
sleep 1
