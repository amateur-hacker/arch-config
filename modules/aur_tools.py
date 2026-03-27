import decman
from decman.plugins import pacman

from modules.utils import resolve_pkgs, split_pkgs
from shared_types import PackageList

PKGS: PackageList = [
    (
        "paru",
        [
            "bat",
            "devtools",
        ],
    ),
    "chaotic-keyring",
    "chaotic-mirrorlist",
]


class AURTools(decman.Module):
    """Install tools needed to use AUR"""

    def __init__(self):
        super().__init__("aur")
        resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, _, _ = split_pkgs(resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs
