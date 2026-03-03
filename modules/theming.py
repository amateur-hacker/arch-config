import decman
from decman.plugins import pacman, aur

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
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

AUR_PKGS: list[str | tuple[str, set[str]]] = [
    "sddm-silent-theme",
]


class Theming(decman.Module):
    """Theming tools package profile."""

    def __init__(self):
        super().__init__("cli")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)

    @aur.packages
    def aur_pkgs(self) -> set[str]:
        return resolve_pkgs(AUR_PKGS)
