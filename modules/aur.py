import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

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

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
