from modules import (
    CLITools,
    Development,
    Fonts,
    GUIApps,
    Hyprland,
    Noctalia,
    Theming,
    WaylandUtils,
)
from specs import Profile, ProfileModules, ProfilesMap

WORKSTATION: ProfileModules = [
    Hyprland(),
    WaylandUtils(),
    Noctalia(),
    CLITools(),
    Development(),
    GUIApps(),
    Fonts(),
    Theming(),
]


PROFILES: ProfilesMap = {
    Profile.WORKSTATION: WORKSTATION,
}
