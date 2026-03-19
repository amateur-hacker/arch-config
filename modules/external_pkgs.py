import decman

from modules.utils import (
    get_user_home_dir,
    reconcile_external_pkgs,
    resolve_external_packages,
)
from specs import ExternalPackages

HOME = get_user_home_dir()
EXTERNAL_PACKAGES: ExternalPackages = {
    "pipx": [],
    "cargo": [
        # ("ripgrep", "--locked"),
        # "wlr-which-key",
    ],
    "bun": [
        "yt-search",
    ],
}


class ExternalPkgs(decman.Module):
    """Manage installation and removal of external packages via supported package managers."""

    def __init__(self):
        super().__init__("external_pkgs")
        self._external_pkgs = resolve_external_packages(EXTERNAL_PACKAGES)

    def after_update(self, store):
        _ = store

        for manager, data in self._external_pkgs.items():
            reconcile_external_pkgs(
                manager,
                data["packages"],
                data["install"],
                data["remove"],
            )
