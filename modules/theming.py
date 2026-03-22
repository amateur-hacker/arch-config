import decman
from decman.plugins import aur, pacman

from specs import PackageList

from .utils import resolve_pkgs, split_pkgs

PKGS: PackageList = [
    "adw-gtk-theme",
    "bibata-cursor-theme",
    "catppuccin-mocha-grub-theme-git",
    ("kvantum", ["kvantum-qt5"]),  # kvanutm-qt6-git
    "matugen",
    "nwg-look",
    "papirus-folders-catppuccin-git",
    ("plymouth", ["plymouth-theme-cybernetic-git"]),
    "qt5ct",
    "qt6ct",
    "sddm-silent-theme",
    "spicetify-cli",
    "tela-circle-icon-theme-blue",
]


class Theming(decman.Module):
    """Theming package profile."""

    def __init__(self):
        super().__init__("theming")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs
