from typing import TypeAlias
import decman
from modules import (
    CLITools,
    DevTools,
    Fonts,
    GUIApps,
    Hyprland,
    Noctalia,
    Theming,
    WaylandTools,
    ExternalPkgs,
)
from specs import Profile

ProfileModules: TypeAlias = list[decman.Module]
ProfilesMap: TypeAlias = dict[Profile, ProfileModules]

WORKSTATION: ProfileModules = [
    Hyprland(),
    WaylandTools(),
    Noctalia(),
    CLITools(),
    DevTools(),
    GUIApps(),
    Fonts(),
    Theming(),
    ExternalPkgs(),
]


PROFILES: ProfilesMap = {
    Profile.WORKSTATION: WORKSTATION,
}
