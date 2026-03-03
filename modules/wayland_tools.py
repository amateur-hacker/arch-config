import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    "grim",
    "satty",
    "slurp",
    "wl-clipboard",
]


class WaylandTools(decman.Module):
    """Wayland tools package profile."""

    def __init__(self):
        super().__init__("wayland_tools")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
