from pathlib import Path
from typing import Callable, TypedDict

import decman
from decman import Directory, File, Symlink

from .dotfiles_utils import (
    apply_graphical_gsettings,
    build_directories,
    build_files,
    build_symlinks,
    ensure_acl,
    file_hash,
    generate_locales,
    build_font_cache,
    build_initramfs_images,
    build_plymouth_theme,
    generate_grub_config,
    get_current_wallpaper,
    sync_pacman_repos,
    update_xdg_user_dirs,
)
from .utils import get_user_home_dir, get_username


class Dotfiles(decman.Module):
    """Apply managed dotfiles from repository to system via symlink or copy."""

    def __init__(self):
        super().__init__("dotfiles")
        self._base = Path(__file__).resolve().parent.parent / "dotfiles"
        self._home = Path(get_user_home_dir())
        self._user = get_username()

    def files(self) -> dict[str, File]:
        current_wallpaper_path = get_current_wallpaper()
        file_items: list[tuple[str, str] | tuple[str, str, str]] = [
            # (
            #     "/path/to/dst/file",
            #     "/path/to/src/file",
            #     "your_user_name",
            # ),  # NOTE: Just an example
            ("/etc/default/grub", "etc/default/grub"),
            ("/etc/fonts/local.conf", "etc/fonts/local.conf"),
            ("/etc/locale.conf", "etc/locale.conf"),
            ("/etc/mkinitcpio.conf", "etc/mkinitcpio.conf"),
            ("/etc/pacman.conf", "etc/pacman.conf"),
            ("/etc/sddm.conf.d/10-theme.conf", "etc/sddm.conf.d/10-theme.conf"),
            (
                "/usr/share/icons/default/index.theme",
                "usr/share/cursor/default/index.theme",
            ),
            (
                "/usr/share/sddm/themes/silent/configs/catppuccin-mocha.conf",
                "usr/share/sddm/themes/silent/configs/catppuccin-mocha.conf",
            ),
            (
                "/usr/share/sddm/themes/silent/metadata.desktop",
                "usr/share/sddm/themes/silent/metadata.desktop",
            ),
            (
                "/usr/share/sddm/themes/silent/backgrounds/bg.png",
                current_wallpaper_path,
            ),
        ]

        return build_files(base=self._base, items=file_items)

    def directories(self) -> dict[str, Directory]:
        directory_items: list[tuple[str, str] | tuple[str, str, str]] = [
            (
                "/usr/share/plymouth/themes/anonymous",
                "usr/share/plymouth/themes/anonymous",
            ),
        ]

        return build_directories(base=self._base, items=directory_items)

    def symlinks(self) -> dict[str, str | Symlink]:
        symlink_items: list[tuple[str, str] | tuple[str, str, str]] = [
            (f"{self._home}/.config/atac", "config/atac"),
            (f"{self._home}/.config/bottom", "config/bottom"),
            (f"{self._home}/.config/cava", "config/cava"),
            (f"{self._home}/.config/chrome-flags.conf", "config/chrome-flags.conf"),
            (f"{self._home}/.config/fish", "config/fish"),
            (f"{self._home}/.config/gtk-3.0", "config/gtk-3.0"),
            (f"{self._home}/.config/gtk-4.0", "config/gtk-4.0"),
            (f"{self._home}/.config/hypr", "config/hypr"),
            (f"{self._home}/.config/kitty", "config/kitty"),
            (f"{self._home}/.config/lsd", "config/lsd"),
            (f"{self._home}/.config/mimeapps.list", "config/mimeapps.list"),
            (f"{self._home}/.config/mpv/mpv.conf", "config/mpv/mpv.conf"),
            (f"{self._home}/.config/neovide", "config/neovide"),
            (f"{self._home}/.config/nitch++", "config/nitch++"),
            (f"{self._home}/.config/noctalia", "config/noctalia"),
            (f"{self._home}/.config/nvim", "config/nvim"),
            (f"{self._home}/.config/starship", "config/starship"),
            (f"{self._home}/.config/user-dirs.dirs", "config/user-dirs.dirs"),
            (f"{self._home}/.config/yazi", "config/yazi"),
            (f"{self._home}/.config/zathura", "config/zathura"),
            (f"{self._home}/.face", "home/.face"),
            (f"{self._home}/.face.icon", "home/.face"),
            # (f"{self._home}/.face.icon1", "home/.face1"),
        ]

        # NOTE: can use .extend method for conditional logic.

        return build_symlinks(
            base=self._base, items=symlink_items, default_owner=self._user
        )

    def after_update(self, store):
        TrackedItem = TypedDict(
            "TrackedItem",
            {
                "key": str,
                "action": Callable[[], None],
            },
        )

        tracked_items: dict[str, TrackedItem] = {
            "/etc/default/grub": {
                "key": "grub_hash",
                "action": generate_grub_config,
            },
            "/etc/fonts/local.conf": {
                "key": "fonts_hash",
                "action": build_font_cache,
            },
            "/etc/locale.conf": {
                "key": "locale_hash",
                "action": generate_locales,
            },
            "/etc/mkinitcpio.conf": {
                "key": "mkinitcpio_hash",
                "action": build_initramfs_images,
            },
            "/etc/pacman.conf": {
                "key": "pacman_hash",
                "action": sync_pacman_repos,
            },
            "/etc/plymouth/plymouthd.conf": {
                "key": "plymouth_hash",
                "action": build_plymouth_theme,
            },
        }

        for path, config in tracked_items.items():
            key = config["key"]
            action = config["action"]

            store.ensure(key, None)

            if not Path(path).exists():
                continue

            current = file_hash(path)

            if store[key] != current:
                action()
                store[key] = current

        ensure_acl(path=self._home, acl="user:sddm:--x")
        ensure_acl(path=self._home / ".face.icon", acl="user:sddm:r--")
        update_xdg_user_dirs()
        apply_graphical_gsettings()
