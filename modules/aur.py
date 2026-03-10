import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs, split_pkgs

PKGS: PkgList = [
    (
        "paru",
        {
            "bat",
            "devtools",
        },
    ),
    "chaotic-keyring",
    "chaotic-mirrorlist",
]


class AUR(decman.Module):
    """Development tools package profile."""

    def __init__(self):
        super().__init__("aur")
        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, _, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs
