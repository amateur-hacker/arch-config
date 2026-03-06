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


class WaylandUtils(decman.Module):
    """Wayland utilities package profile."""

    def __init__(self):
        super().__init__("wayland_utils")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
