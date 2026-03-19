#!/usr/bin/env bash

set -euo pipefail

# ── Colors ───────────────────────────────────────────────
GREEN=$(tput setaf 2)  # Green (Success)
YELLOW=$(tput setaf 3) # Yellow (Warning)
RED=$(tput setaf 1)    # Red (Error)
BLUE=$(tput setaf 4)   # Blue (Info)
RESET=$(tput sgr0)     # Reset to default color

PACMAN_CONF="/etc/pacman.conf"
CHAOTIC_REPO="chaotic-aur"
AUR_HELPER="paru"

# ── Prevent from executed as root ─────────────────────────────────────────
if [[ $EUID -eq 0 ]]; then
  echo -e "${RED}This script should NOT be executed as root!! Exiting..${RESET}"
  exit 1
fi

# Ask for sudo password upfront
echo -e "${YELLOW}This script will modify system configuration and install packages.${RESET}"
read -rp "Do you want to continue? [y/N]: " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

if sudo -n true 2>/dev/null; then
  echo -e "${GREEN}Sudo already authenticated.${RESET}"
else
  echo -e "${BLUE}Sudo authentication required.${RESET}"
  if ! sudo -v; then
    echo -e "${RED}Sudo authentication failed. Exiting.${RESET}"
    exit 1
  fi
fi

# ── Logging Setup ────────────────────────────────────────
LOG_FILE="/tmp/ac-initial-setup.log"
touch "$LOG_FILE"

exec 3>&1 4>&2
exec >"$LOG_FILE" 2>&1

# ── UI Helpers ───────────────────────────────────────────
log_and_print() {
  local msg="$1"
  echo "$msg"
  echo -e "$msg" >&3
}

info() { log_and_print "${BLUE}→ $1${RESET}"; }
ok() { log_and_print "${GREEN}✓ $1${RESET}"; }
fail() { log_and_print "${RED}✗ $1${RESET}"; }
warning() { log_and_print "${YELLOW}✗ $1${RESET}"; }

trap 'fail "Script failed. See $LOG_FILE" >&3' ERR

echo "===== Arch Config Initial Setup ====="
echo ""

info "Setting up Chaotic AUR..."
if ! grep -q "^\[${CHAOTIC_REPO}\]" "$PACMAN_CONF"; then
  sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
  sudo pacman-key --lsign-key 3056513887B78AEB

  sudo pacman -U --noconfirm \
    https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst \
    https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst

  cat >>"$PACMAN_CONF" <<EOF

# Chaotic AUR
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
EOF
fi
sudo pacman -Syu --noconfirm
ok "Chaotic AUR ready"

info "Installing ${AUR_HELPER}..."
if ! pacman -Qi "$AUR_HELPER" &>/dev/null; then
  sudo pacman -S --noconfirm --needed "$AUR_HELPER"
fi
ok "${AUR_HELPER} installed"

info "Installing decman (AUR)..."
"$AUR_HELPER" -S --noconfirm --needed --skipreview --batchinstall decman
ok "decman installed"

info "Installing python-rich..."
sudo pacman -S --noconfirm --needed python-rich
ok "python-rich installed"

info "Initial setup complete"
