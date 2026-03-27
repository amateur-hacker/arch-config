import decman
from decman.plugins import pacman

from modules.utils import resolve_pkgs
from shared_types import PackageList

PKGS: PackageList = [
    # (
    #     "package_name",
    #     [
    #         "deps1",
    #         "deps2",
    #     ]
    # ),
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
