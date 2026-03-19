import decman
from decman.plugins import aur, pacman

from specs import PackageList

from .utils import resolve_pkgs, split_pkgs

PKGS: PackageList = [
    "blanket",
    # "gimp",
    "google-chrome",
    "gnome-clocks",
    "imv",
    "keypunch-git",
    "kitty",
    "libreoffice-fresh",
    "localsend",
    "mpv",
    "pinta",
    (
        "pitivi",
        [
            "gst-libav",
            "gst-plugins-good",
            "gst-plugins-bad",
            "gst-plugins-ugly",
            "gst-plugin-gtk",
            "gst-plugin-opencv",
            "libpeas",
            "python-librosa",
        ],
    ),
    "qalculate-gtk",
    ("nautilus", ["nautilus-open-any-terminal", "xdg-user-dirs-gtk", "file-roller"]),
    (
        "spotify",
        [
            "spotx-git",
            # Optional deps
            "ffmpeg4.4",
            "libnotify",
            "zenity",
        ],
    ),
    (
        "telegram-desktop",
        [
            "geoclue",
            "geocode-glib-2",
            "webkitgtk-6.0",
        ],
    ),
    (
        "timeshift",
        [
            ("btrfs-progs", ["inotify-tools"]),
            "grub-btrfs",
            "xorg-xhost",
        ],
    ),
    ("zathura", ["zathura-pdf-poppler"]),
]


class GUIApps(decman.Module):
    """GUI Apps package profile."""

    def __init__(self):
        super().__init__("gui_tools")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs
