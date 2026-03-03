import decman
from decman.plugins import systemd

from .utils import get_username, is_laptop

SYSTEM_UNITS = {
    "NetworkManager.service",
    "ufw.service",
    "bluetooth.service",
    "sddm.service",
}

LAPTOP_UNITS = {
    "power-profiles-daemon.service",
}

USER_UNITS = {
    "pipewire.service",
    "wireplumber.service",
}


class Systemd(decman.Module):
    """System and user systemd units module."""

    def __init__(self):
        super().__init__("systemd")
        self._username = get_username()
        self._is_laptop = is_laptop()

    @systemd.units
    def systemd_units(self):
        units = set(SYSTEM_UNITS)

        if self._is_laptop:
            units |= LAPTOP_UNITS

        return units

    @systemd.user_units
    def systemd_user_units(self) -> dict[str, set[str]]:
        return {self._username: USER_UNITS}
