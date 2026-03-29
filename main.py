import decman

from logging_config import setup_logging
from modules import AURTools, Base, Dotfiles, Hardware, SystemdServices, Users
from profiles import PROFILES
from shared_types import Profile

setup_logging()

decman.modules += [
    Users(),
    Base(),
    Hardware(),
    AURTools(),
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
