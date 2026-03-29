import decman
from decman.plugins import aur, pacman
from decman.plugins.aur import CustomPackage

from modules.utils import resolve_pkgs, split_pkgs
from shared_types import PackageList

PKGS: PackageList = [
    "7zip",
    "acpi",
    "age",
    "ain-bin",
    "bat",
    "bottom",
    "cava",
    ("cbonsai", ["scdoc"]),
    ("chess-tui", ["stockfish"]),
    "cowsay",
    "curl",
    (
        "decman",
        [
            # build deps
            "python-build",
            "python-installer",
            "python-setuptools",
            "python-wheel",
            # test deps
            "python-pytest",
            "python-pytest-mock",
        ],
    ),
    "duf",
    "dysk",
    "fastfetch",
    "fd",
    "ffmpeg",
    "figlet",
    (
        "fish",
        [
            "fisher",
            "fzf",
            "kitty-shell-integration",
        ],
    ),
    "fzf",
    "geoip",
    ("gowall", ["go"]),
    "httpie",
    "imagemagick",
    "inxi",
    "jq",
    "libinput-tools",
    "less",
    "lolcat",
    "lsd",
    "net-tools",
    CustomPackage(
        "nitch++-git",
        "https://github.com/amateur-hacker/nitchplusplus",
    ),
    "perl-file-mimeinfo",
    "pipes.sh",
    "plocate",
    "qrencode",
    "ripgrep",
    "rsync",
    "scrntime-git",
    "sops",
    "spotdl",
    ("starship", ["ttf-cascadia-mono-nerd"]),
    "tealdeer",
    "television",
    "toilet",
    "trash-cli",
    "tty-clock",
    "ufw",
    (
        "unp",
        [
            "7zip",
            "bzip2",
            "unrar",
            "unzip",
        ],
    ),
    "unrar",
    "unzip",
    (
        "usbutils",
        [
            "coreutils",
            "python",
        ],
    ),
    "wireless_tools",
    "wget",
    (
        "yazi",
        [
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
        ],
    ),
    "yq",
    (
        "yt-dlp",
        [
            "ffmpeg",
            "python-mutagen",
        ],
    ),
    "zip",
    ("zoxide", ["fzf"]),
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
