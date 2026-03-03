import decman
from decman.plugins import pacman

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
    "grim",
    "hyprland",
    "hyprland-protocols",
    "hyprpicker",
    "hyprpolkitagent",
    "hyprshot",
    "satty",
    "slurp",
    "socat",
    "uwsm",
    "wl-clipboard",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",
    "xdg-desktop-portal-hyprland",
]


class Hyprland(decman.Module):
    """Hyprland tools package profile."""

    def __init__(self):
        super().__init__("hyprland")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)
