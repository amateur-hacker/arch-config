import decman
from decman.plugins import pacman

from .utils import resolve_pkgs

PKGS: list[str | tuple[str, set[str]]] = [
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
    ("php", {"composer"}),
    ("python", {"python-pipx", "python-rich"}),
    ("ruby", {"rubygems"}),
    "rust",
    "sqlite",
]


class Dev(decman.Module):
    """Development tools package profile."""

    def __init__(self):
        super().__init__("dev")

    @pacman.packages
    def pkgs(self) -> set[str]:
        return resolve_pkgs(PKGS)
