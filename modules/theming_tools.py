import decman
from decman.plugins import aur, pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    "adw-gtk-theme",
    "bibata-cursor-theme",
    "catppuccin-mocha-grub-theme-git",
    "matugen",
    "nwg-look",
    ("plymouth", {"plymouth-theme-cybernetic-git"}),
    "qt5ct",
    "qt6ct",
    "spicetify-cli",
    "tela-circle-icon-theme-blue",
]

AUR_PKGS: PkgList = [
    "sddm-silent-theme",
]


class ThemingTools(decman.Module):
    """Theming tools package profile."""

    def __init__(self):
        super().__init__("theming_tools")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)

    @aur.packages
    def aur_pkgs(self):
        return resolve_pkgs(AUR_PKGS)
