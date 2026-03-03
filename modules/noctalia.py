import decman
from decman.plugins import pacman

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
    (
        "noctalia-shell",
        {
            "cava",
            "cliphist",
            "ddcutil",
            "fastfetch",
            "gpu-screen-recorder",
            "libnotify",
            "wlsunset",
        },
    ),
]


class Noctalia(decman.Module):
    """Noctalia shell package profile."""

    def __init__(self):
        super().__init__("noctalia")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)
