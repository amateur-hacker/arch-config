from pathlib import Path

import decman

from modules.dotfiles_utils import (
    apply_graphical_gsettings,
    build_directories,
    build_files,
    build_font_cache,
    build_initramfs_images,
    build_plymouth_theme,
    build_symlinks,
    # decrypt_sops_age_key,
    # decrypt_ssh_private_key,
    ensure_acl,
    ensure_git_config,
    ensure_wheel_sudo_privileges,
    ensure_xhost_root_access,
    generate_grub_config,
    generate_locales,
    get_current_wallpaper_path,
    run_tracked_actions,
    set_papirus_folder_color,
    sync_pacman_repos,
    update_locate_db,
    update_tldr_cache,
    update_xdg_user_dirs,
)
from shared_types import DotfileItemList, TrackedItemsMap
from variables import GIT_USER_EMAIL, GIT_USER_NAME

from .utils import get_user_home_dir, get_username

HOME = get_user_home_dir()
USER = get_username()
CURRENT_WALLPAPER_PATH = get_current_wallpaper_path()

FILE_ITEMS: DotfileItemList = [
    # (
    #     "/path/to/dst/file",
    #     "/path/to/src/file",
    #     "your_user_name(optional)",
    # ),
    ("/etc/default/grub", "etc/default/grub"),
    ("/etc/environment", "etc/environment"),
    ("/etc/fonts/local.conf", "etc/fonts/local.conf"),
    ("/etc/locale.conf", "etc/locale.conf"),
    ("/etc/mkinitcpio.conf", "etc/mkinitcpio.conf"),
    ("/etc/pacman.conf", "etc/pacman.conf"),
    ("/etc/plymouth/plymouthd.conf", "etc/plymouth/plymouthd.conf"),
    ("/etc/X11/xorg.conf.d/10-touchpad.conf", "etc/X11/xorg.conf.d/10-touchpad.conf"),
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
        "/usr/share/sddm/themes/silent/backgrounds/current_wall",
        CURRENT_WALLPAPER_PATH,
    ),
]

DIRECTORY_ITEMS: DotfileItemList = [
    # (
    #     "/path/to/dst/dir",
    #     "/path/to/src/dir",
    #     "your_user_name(optional and default is root)",
    # ),
    (
        "/usr/share/plymouth/themes/anonymous",
        "usr/share/plymouth/themes/anonymous",
    ),
    (
        f"{HOME}/pictures/wallpapers/my-walls",
        "home/pictures/wallpapers/my-walls",
        USER,
    ),
]

SYMLINK_ITEMS: DotfileItemList = [
    # (
    #     "/path/to/dst/file",
    #     "/path/to/src/file",
    #     "your_user_name(optional and default is your username.)",
    # ),
    (f"{HOME}/.config/atac", "config/atac"),
    (f"{HOME}/.config/bottom", "config/bottom"),
    (f"{HOME}/.config/cava", "config/cava"),
    (f"{HOME}/.config/chrome-flags.conf", "config/chrome-flags.conf"),
    (f"{HOME}/.config/dircolors", "config/dircolors"),
    (f"{HOME}/.config/fastfetch", "config/fastfetch"),
    (f"{HOME}/.config/fish", "config/fish"),
    (f"{HOME}/.config/git", "config/git"),
    (f"{HOME}/.config/gtk-3.0", "config/gtk-3.0"),
    (f"{HOME}/.config/gtk-4.0", "config/gtk-4.0"),
    (f"{HOME}/.config/hypr", "config/hypr"),
    (f"{HOME}/.config/kitty", "config/kitty"),
    (f"{HOME}/.config/Kvantum", "config/Kvantum"),
    (f"{HOME}/.config/lsd", "config/lsd"),
    (f"{HOME}/.config/mimeapps.list", "config/mimeapps.list"),
    (f"{HOME}/.config/mpv", "config/mpv"),
    (f"{HOME}/.config/neovide", "config/neovide"),
    (f"{HOME}/.config/nitch++", "config/nitch++"),
    (f"{HOME}/.config/noctalia", "config/noctalia"),
    (f"{HOME}/.config/nvim", "config/nvim"),
    (f"{HOME}/.config/opencode/themes", "config/opencode/themes"),
    (f"{HOME}/.local/state/opencode/kv.json", "config/opencode/kv.json"),
    (f"{HOME}/.config/qt5ct", "config/qt5ct"),
    (f"{HOME}/.config/qt6ct", "config/qt6ct"),
    (f"{HOME}/.config/satty", "config/satty"),
    (f"{HOME}/.config/starship.toml", "config/starship.toml"),
    (f"{HOME}/.config/user-dirs.dirs", "config/user-dirs.dirs"),
    (f"{HOME}/.config/yazi", "config/yazi"),
    (f"{HOME}/.config/zathura", "config/zathura"),
    (f"{HOME}/.face", "home/.face"),
    (f"{HOME}/.face.icon", "home/.face"),
    ("/root/.config/gtk-3.0", "config/gtk-3.0"),
    ("/root/.config/gtk-4.0", "config/gtk-4.0"),
    ("/root/.config/Kvantum", "config/Kvantum"),
    ("/root/.config/qt5ct", "config/qt5ct"),
    ("/root/.config/qt6ct", "config/qt6ct"),
]

TRACKED_ITEMS: TrackedItemsMap = {
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


class Dotfiles(decman.Module):
    """Apply managed dotfiles from repository to system via symlink or copy."""

    def __init__(self):
        super().__init__("dotfiles")
        self._root = Path(__file__).resolve().parent.parent
        self._base = Path(self._root) / "dotfiles"

    def files(self):
        return build_files(base=self._base, items=FILE_ITEMS)

    def directories(self):
        return build_directories(base=self._base, items=DIRECTORY_ITEMS)

    def symlinks(self):
        return build_symlinks(base=self._base, items=SYMLINK_ITEMS, default_owner=USER)

    def after_update(self, store):
        run_tracked_actions(TRACKED_ITEMS, store)

        ensure_wheel_sudo_privileges()
        ensure_acl(path=Path(HOME), acl="user:sddm:--x")
        ensure_acl(path=Path(HOME) / ".face.icon", acl="user:sddm:r--")
        ensure_acl(
            path=Path("/usr/share/sddm/themes/silent/backgrounds"),
            acl=f"user:{USER}:rwx",
        )
        update_xdg_user_dirs()
        apply_graphical_gsettings()
        update_tldr_cache()
        update_locate_db()
        set_papirus_folder_color(desired_color="cat-mocha-lavender")
        ensure_xhost_root_access()
        # decrypt_sops_age_key(
        #     encrypted_path=Path(self._root) / "secrets/sops-keys.txt.age"
        # )
        # decrypt_ssh_private_key(
        #     encrypted_path=Path(self._root) / "secrets/ssh-id_rsa.enc"
        # )
        ensure_git_config(user_name=GIT_USER_NAME, user_email=GIT_USER_EMAIL)
