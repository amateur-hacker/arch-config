from os.path import abspath

import decman
from decman.plugins import pacman

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
    ("paru", {"bat", "devtools"}),
    "chaotic-keyring",
    "chaotic-mirrorlist",
]


class AUR(decman.Module):
    """Development tools package profile."""

    def __init__(self):
        super().__init__("aur")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)

    def on_enable(self, store):
        _ = store
        script_path = abspath("scripts/setup-chaotic-aur.sh")
        decman.prg(["bash", script_path], pty=False)
