import decman
from decman.plugins import aur, pacman

from specs import PackageList

from .utils import resolve_pkgs, split_pkgs

PKGS: PackageList = [
    "bun",
    "clang",
    "cmake",
    "devtools",
    "docker",
    "docker-compose",
    "gcc",
    ("github-cli", ["git"]),
    "go",
    "ghq",
    "jdk-openjdk",
    "julia",
    "lazydocker",
    "lazygit",
    "meson",
    "neovide",
    (
        "neovim",
        [
            "luarocks",
            "wl-clipboard",
            "tree-sitter-cli",
        ],
    ),
    "ninja",
    ("nodejs", ["npm"]),
    "opencode",
    ("php", ["composer"]),
    (
        "python",
        [
            "python-pipx",
            "python-rich",
        ],
    ),
    ("ruby", ["rubygems"]),
    "rust",
    "sqlite",
]


class DevTools(decman.Module):
    """Development tools package profile."""

    def __init__(self):
        super().__init__("dev_tools")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, _ = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs
