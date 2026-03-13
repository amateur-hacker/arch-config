import decman

from logging_config import setup_logging
from modules import AUR, Base, Dotfiles, Hardware, SystemdServices, Users
from profiles import PROFILES
from specs import Profile

setup_logging()

decman.modules += [
    Users(),
    Base(),
    Hardware(),
    AUR(),
    *PROFILES[Profile.WORKSTATION],
    SystemdServices(),
    Dotfiles(),
]

decman.execution_order = [
    "pacman",
    "aur",
    "systemd",
    "files",
]
