from modules import (
    CLITools,
    Development,
    Fonts,
    GUIApps,
    Hyprland,
    NoctaliaShell,
    Theming,
    WaylandUtils,
)
from specs import Profile, ProfileModules, ProfilesMap

WORKSTATION: ProfileModules = [
    Hyprland(),
    WaylandUtils(),
    NoctaliaShell(),
    CLITools(),
    Development(),
    GUIApps(),
    Fonts(),
    Theming(),
]


PROFILES: ProfilesMap = {
    Profile.WORKSTATION: WORKSTATION,
}
