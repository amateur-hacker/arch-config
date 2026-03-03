import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    (
        "hyprland",
        {
            "hyprland-protocols",
            "hyprpicker",
            "hyprpolkitagent",
            "hyprshot",
            "socat",
            "uwsm",
            "xdg-desktop-portal",
            "xdg-desktop-portal-gtk",
            "xdg-desktop-portal-hyprland",
        },
    ),
]


class Hyprland(decman.Module):
    """Hyprland tools package profile."""

    def __init__(self):
        super().__init__("hyprland")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
