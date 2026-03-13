from typing import TypeAlias

import decman

from modules import (
    CLITools,
    DevTools,
    ExternalPkgs,
    Fonts,
    GUIApps,
    HyprlandWM,
    NoctaliaShell,
    Theming,
    WaylandTools,
)
from specs import Profile

ProfileModules: TypeAlias = list[decman.Module]
ProfilesMap: TypeAlias = dict[Profile, ProfileModules]

WORKSTATION: ProfileModules = [
    HyprlandWM(),
    WaylandTools(),
    NoctaliaShell(),
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
