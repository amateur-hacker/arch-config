import decman
from decman.plugins import pacman, aur
from decman.plugins.aur import CustomPackage

from specs import PackageList

from .utils import resolve_pkgs, split_pkgs

PKGS: PackageList = [
    (
        # "noctalia-shell",
        CustomPackage(
            "noctalia-shell-git",
            "https://github.com/amateur-hacker/noctalia-shell",
        ),
        [
            "cliphist",
            "ddcutil",
            "evtest",
            "evolution-data-server",
            "fastfetch",
            "gpu-screen-recorder",
            "grim",
            "imagemagick",
            "libnotify",
            # "mission-center",
            "pavucontrol",
            "power-profiles-daemon",
            "resources",
            ("tesseract", ["tesseract-data-eng"]),
            "upower",
            "wl-clipboard",
            "wlsunset",
            "satty",
        ],
    ),
    # (
    #     "noctalia-shell-git",
    #     [
    #         # Optional Deps
    #         "cava",
    #         "cliphist",
    #         "ddcutil",
    #         "fastfetch",
    #         "gpu-screen-recorder",
    #         "grim",
    #         "imagemagick",
    #         "libnotify",
    #         ("tesseract", ["tesseract-data-eng"]),
    #         "wl-clipboard",
    #         "wlsunset",
    #         "satty",
    #         # Make deps of 'noctalia-shell-git' and 'noctalia-qs'
    #         "cli11",
    #         "cmake",
    #         "git",
    #         "ninja",
    #         "qt6-shadertools",
    #         "spirv-tools",
    #     ],
    # ),
]


class NoctaliaShell(decman.Module):
    """Noctalia shell package profile."""

    def __init__(self):
        super().__init__("noctalia_shell")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, self._custom_pkgs = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs

    @aur.custom_packages
    def custom_packages(self):
        return self._custom_pkgs
