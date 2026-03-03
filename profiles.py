from modules.cli_tools import CLITools
from modules.dev_tools import DevTools
from modules.fonts import Fonts
from modules.gui_tools import GUITools
from modules.hyprland import Hyprland
from modules.noctalia_shell import NoctaliaShell
from modules.theming_tools import ThemingTools
from modules.wayland_tools import WaylandTools
from specs import Profile, ProfileModules, ProfilesMap

WORKSTATION: ProfileModules = [
    Hyprland(),
    WaylandTools(),
    NoctaliaShell(),
    CLITools(),
    DevTools(),
    GUITools(),
    Fonts(),
    ThemingTools(),
]


PROFILES: ProfilesMap = {
    Profile.WORKSTATION: WORKSTATION,
}
