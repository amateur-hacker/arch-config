import decman
from decman.plugins import pacman

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
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


class GUI(decman.Module):
    """GUI tools package profile."""

    def __init__(self):
        super().__init__("gui")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)
