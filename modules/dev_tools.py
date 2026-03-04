import decman
from decman.plugins import pacman

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    "bun",
    "cmake",
    "devtools",
    "docker",
    "docker-compose",
    "gcc",
    "go",
    "jdk-openjdk",
    "julia",
    "lazydocker",
    "lazygit",
    "meson",
    "neovide",
    (
        "neovim",
        {
            "luarocks",
            "wl-clipboard",
            "tree-sitter-cli",
        },
    ),
    "ninja",
    ("nodejs", {"npm"}),
    "opencode",
    ("php", {"composer"}),
    ("python", {"python-pipx", "python-rich"}),
    ("ruby", {"rubygems"}),
    "rust",
    "sqlite",
]


class DevTools(decman.Module):
    """Development tools package profile."""

    def __init__(self):
        super().__init__("dev_tools")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)
