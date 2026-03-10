import decman
from decman.plugins import aur, pacman

from specs import PkgList

from .utils import resolve_pkgs, split_pkgs

PKGS: PkgList = [
    "noto-fonts",
    "noto-fonts-cjk",
    "noto-fonts-emoji",
    "terminus-font",
    "ttf-cascadia-mono-nerd",
    # "ttf-jetbrains-mono-nerd",
    # "ttf-ms-fonts",
    "ttf-nerd-fonts-symbols",
    "ttf-nerd-fonts-symbols-mono",
]


class Fonts(decman.Module):
    """Fonts package profile."""

    def __init__(self):
        super().__init__("fonts")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs
