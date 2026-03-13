import decman
from decman.plugins import pacman

from specs import PackageList

from .utils import resolve_pkgs

PKGS: PackageList = [
    "base",
    "base-devel",
    "bluez",
    "bluez-utils",
    "btrfs-progs",
    "efibootmgr",
    "git",
    "grub",
    (
        "linux-zen",
        [
            "linux-firmware",
            "linux-zen-headers",
        ],
    ),
    "man-db",
    "man-pages",
    "networkmanager",
    "ntfs-3g",
    "openssh",
    "pacman-contrib",
    (
        "pipewire",
        [
            "gst-plugin-pipewire",
            "libpulse",
            "pipewire-alsa",
            "pipewire-jack",
            "pipewire-pulse",
        ],
    ),
    "sddm",
    "snapper",
    "sudo",
    "zram-generator",
]


class Base(decman.Module):
    """Base system package profile."""

    def __init__(self):
        super().__init__("base")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
