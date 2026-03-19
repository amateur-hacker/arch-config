#!/usr/bin/env bash

set -euo pipefail

wifi="$(nmcli r wifi | awk 'FNR = 2 {print $1}')"
if [ "$wifi" == "enabled" ]; then
  rfkill block all &
else
  rfkill unblock all &
fi
