import decman
from decman.plugins import aur, pacman
from decman.plugins.aur import CustomPackage

from specs import PkgList

from .utils import resolve_pkgs, split_pkgs

PKGS: PkgList = [
    "acpi",
    "ain-bin",
    "bat",
    "bottom",
    "cava",
    ("cbonsai", {"scdoc"}),
    ("chess-tui", {"stockfish"}),
    "cowsay",
    "curl",
    (
        "decman",
        {
            "python-setuptools",
            "python-build",
            "python-installer",
            "python-wheel",
        },
    ),
    "duf",
    "dysk",
    "fastfetch",
    "fd",
    "ffmpeg",
    "figlet",
    (
        "fish",
        {
            "fisher",
            "fzf",
            "kitty-shell-integration",
        },
    ),
    "fzf",
    "geoip",
    ("gowall", {"go"}),
    ("github-cli", {"git"}),
    "httpie",
    "imagemagick",
    "inxi",
    "jq",
    "less",
    "lolcat",
    "lsd",
    CustomPackage(
        "nitch++-git",
        "https://github.com/amateur-hacker/nitchplusplus",
    ),
    "perl-file-mimeinfo",
    "pipes.sh",
    "plocate",
    "ripgrep",
    "rsync",
    "spotdl",
    ("starship", {"ttf-cascadia-mono-nerd"}),
    "tealdeer",
    "toilet",
    "trash-cli",
    "tty-clock",
    "ufw",
    (
        "unp",
        {
            "unrar",
            "unzip",
            "bzip2",
            "7zip",
        },
    ),
    "unrar",
    "unzip",
    "wget",
    "wtype",
    (
        "yazi",
        {
            "7zip",
            "fd",
            "ffmpeg",
            "fzf",
            "git",
            "imagemagick",
            "jq",
            "mediainfo",
            "poppler",
            "resvg",
            "ripgrep",
            "wl-clipboard",
            "zoxide",
        },
    ),
    (
        "yt-dlp",
        {
            "ffmpeg",
            "python-mutagen",
        },
    ),
    "7zip",
    "zip",
    ("zoxide", {"fzf"}),
]


class CLITools(decman.Module):
    """CLI tools package profile."""

    def __init__(self):
        super().__init__("cli_tools")

        _resolved_pkgs = resolve_pkgs(PKGS)
        self._pkgs, self._aur_pkgs, self._aur_custom_pkgs = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs

    @aur.custom_packages
    def aur_custom_pkgs(self):
        return self._aur_custom_pkgs
