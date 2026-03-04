import decman
from decman.plugins import pacman, aur
from decman.plugins.aur import CustomPackage

from specs import PkgList

from .utils import resolve_pkgs

PKGS: PkgList = [
    "acpi",
    "bat",
    "bottom",
    "cava",
    ("chess-tui", {"stockfish"}),
    "cowsay",
    "curl",
    "dysk",
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
    ("github-cli", {"git"}),
    "httpie",
    "imagemagick",
    "inxi",
    "jq",
    "less",
    "lolcat",
    "lsd",
    "perl-file-mimeinfo",
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
    ("unp", {"unrar", "unzip", "bzip2", "p7zip"}),
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
    "yt-dlp",
    "7zip",
    "zip",
    ("zoxide", {"fzf"}),
]

AUR_PKGS: PkgList = [
    "ain-bin",
    "cbonsai",
    "decman",
    "gowall",
    "pipes.sh",
]

AUR_CUSTOM_PKGS = [
    CustomPackage(
        "nitch++-git",
        "https://github.com/amateur-hacker/nitchplusplus",
    )
]


class CLITools(decman.Module):
    """CLI tools package profile."""

    def __init__(self):
        super().__init__("cli_tools")

    @pacman.packages
    def pkgs(self):
        return resolve_pkgs(PKGS)

    @aur.packages
    def aur_pkgs(self):
        return resolve_pkgs(AUR_PKGS)

    @aur.custom_packages
    def aur_custom_pkgs(self):
        return AUR_CUSTOM_PKGS
