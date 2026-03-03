import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
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


class NoctaliaShell(decman.Module):
    """Noctalia shell package profile."""

    def __init__(self):
        super().__init__("noctalia_shell")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
