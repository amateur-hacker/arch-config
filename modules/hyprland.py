import decman
from decman.plugins import aur, pacman

from specs import PkgList

from .utils import resolve_pkgs, split_pkgs

PKGS: PkgList = [
    (
        "hyprland",
        [
            "hyprland-protocols",
            "hyprpicker",
            "hyprpolkitagent",
            "hyprshot",
            "xdg-desktop-portal-hyprland",
        ],
    ),
    "socat",
    "uwsm",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",
]


class Hyprland(decman.Module):
    """Hyprland tools package profile."""

    def __init__(self):
        super().__init__("hyprland")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs
