import decman
from decman.plugins import aur, pacman

from modules.utils import resolve_pkgs, split_pkgs
from shared_types import PackageList

PKGS: PackageList = [
    (
        "hyprland-git",
        [
            "hyprland-protocols-git",
            "hyprpicker-git",
            "hyprpolkitagent",
            "hyprshot",
            (
                "xdg-desktop-portal-hyprland-git",
                [
                    "grim",
                    "slurp",
                ],
            ),
        ],
    ),
    "socat",
    "uwsm",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",
]


class HyprlandWM(decman.Module):
    """Hyprland window manager package profile."""

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
