import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

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

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
