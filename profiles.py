from modules import (
    CLITools,
    Development,
    Fonts,
    GUIApps,
    Hyprland,
    NoctaliaShell,
    Theming,
    WaylandTools,
)
from specs import Profile, ProfileModules, ProfilesMap

WORKSTATION: ProfileModules = [
    Hyprland(),
    WaylandTools(),
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
