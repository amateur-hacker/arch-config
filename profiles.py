from enum import Enum

import decman

from modules.cli import CLI
from modules.dev import Dev
from modules.fonts import Fonts
from modules.gui import GUI
from modules.hyprland import Hyprland
from modules.noctalia import Noctalia
from modules.theming import Theming

WORKSTATION = [
    CLI(),
    Dev(),
    GUI(),
    Fonts(),
    Theming(),
    Noctalia(),
    Hyprland(),
]


class Profile(Enum):
    WORKSTATION = "workstation"
    # GAMING = "gaming"


PROFILES: dict[Profile, list[decman.Module]] = {
    Profile.WORKSTATION: WORKSTATION,
}
