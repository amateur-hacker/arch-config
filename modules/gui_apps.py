import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    "google-chrome",
    "imv",
    "kitty",
    "libreoffice-fresh",
    ("mpv", {"mpv-mpris"}),
    "qalculate-gtk",
    ("nautilus", {"nautilus-open-any-terminal", "xdg-user-dirs-gtk"}),
    (
        "spotify",
        {
            "ffmpeg4.4",
            "libnotify",
            "zenity",
        },
    ),
    (
        "telegram-desktop",
        {
            "geoclue",
            "geocode-glib-2",
            "webkitgtk-6.0",
        },
    ),
    ("zathura", {"zathura-pdf-poppler"}),
]


class GUIApps(decman.Module):
    """GUI Apps package profile."""

    def __init__(self):
        super().__init__("gui_tools")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
