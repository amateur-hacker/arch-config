import decman
from decman.plugins import aur, pacman
from decman.plugins.aur import CustomPackage

from modules.utils import resolve_pkgs, split_pkgs
from shared_types import PackageList

PKGS: PackageList = [
    "grim",
    "satty",
    "slurp",
    (
        CustomPackage(
            "mechsim",
            "https://github.com/amateur-hacker/mechsim",
        ),
        [
            "gcc",
            "make",
            "pkgconf",
            "libevdev",
            "libinput",
            "libsndfile",
        ],
    ),
    # ("wayvibes-git", {"nlohmann-json"}),
    "wf-recorder",
    "wl-clipboard",
    # "wlr-which-key",
    (
        "wshowkeys-mao-git",
        [
            "git",
            "meson",
            "wayland-protocols",
        ],
    ),
    "wtype",
]


class WaylandTools(decman.Module):
    """Wayland tools package profile."""

    def __init__(self):
        super().__init__("wayland_tools")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, self._aur_custom_pkgs = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs

    @aur.custom_packages
    def aur_custom_pkgs(self):
        return self._aur_custom_pkgs
