import decman

from logging_config import setup_logging
from modules.aur import AUR
from modules.base import Base
from modules.dotfiles import Dotfiles
from modules.hardware import Hardware
from modules.systemd import Systemd
from modules.users import Users
from profiles import PROFILES, Profile

setup_logging()

decman.modules += [
    Users(),
    Base(),
    Hardware(),
    AUR(),
    *PROFILES[Profile.WORKSTATION],
    Systemd(),
    Dotfiles(),
]

decman.execution_order = [
    "pacman",
    "aur",
    "systemd",
    "files",
]
