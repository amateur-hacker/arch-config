import hashlib
import logging
import os
import pwd
from pathlib import Path
from typing import Iterable

from decman import Directory, File, Symlink

from modules.utils import (
    get_user_home_dir,
    get_username,
    run_cmd_as_root,
    run_cmd_as_user,
)

logger = logging.getLogger(__name__)
username = get_username()


def ensure_fullname(username: str, fullname: str):
    """Ensure user's fullname"""
    try:
        current = pwd.getpwnam(username).pw_gecos.split(",")[0]
    except KeyError as e:
        raise LookupError(f"User '{username}' does not exist") from e

    if current != fullname:
        logger.info("Setting fullname '%s' for user '%s'", fullname, username)
        run_cmd_as_root(["chfn", "-f", fullname, username])


def ensure_acl(path: Path, acl: str):
    """Ensure ACL entry exists on path."""
    if not path.exists():
        raise FileNotFoundError(f"{path} doesn't exist")

    current = run_cmd_as_user(["getfacl", "-p", str(path)])
    if acl not in current:
        logger.info("Applying ACL '%s' to %s", acl, path)
        run_cmd_as_user(["setfacl", "-m", acl, str(path)])


def update_xdg_user_dirs() -> None:
    """Update XDG user directories."""
    home = Path(get_user_home_dir())
    config_path = home / ".config/user-dirs.dirs"

    if not config_path.exists():
        logger.info("XDG user directories config missing — initializing")
        run_cmd_as_user(["xdg-user-dirs-update"])
        return

    for line in config_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        value = value.strip().strip('"')

        resolved_path = Path(value.replace("$HOME", str(home)))

        if not resolved_path.exists():
            logger.info("Updating XDG user directories.")
            run_cmd_as_user(["xdg-user-dirs-update"])
            run_cmd_as_user(["xdg-user-dirs-gtk-update"])
            return


def apply_graphical_gsettings() -> None:
    """Apply GNOME-related gsettings if in a graphical session."""
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        logger.info("No graphical session detected. Skipping gsettings.")
        return

    wm_button_layout = run_cmd_as_user(
        [
            "gsettings",
            "get",
            "org.gnome.desktop.wm.preferences",
            "button-layout",
        ],
    ).strip()

    if wm_button_layout.strip("'") != ":":
        logger.info("Disabling window decorations")
        run_cmd_as_user(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.wm.preferences",
                "button-layout",
                ":",
            ]
        )

    nautilus_terminal = run_cmd_as_user(
        [
            "gsettings",
            "get",
            "com.github.stunkymonkey.nautilus-open-any-terminal",
            "terminal",
        ],
    ).strip()

    if nautilus_terminal.strip("'") != "kitty":
        logger.info("Setting kitty as default terminal for nautilus file manager")
        run_cmd_as_user(
            [
                "gsettings",
                "set",
                "com.github.stunkymonkey.nautilus-open-any-terminal",
                "terminal",
                "kitty",
            ]
        )


def resolve_source(base: Path, src: str) -> Path:
    """Resolve source path relative to base if not absolute."""
    path = Path(src)
    return path if path.is_absolute() else base / path


def build_files(
    base: Path,
    items: Iterable[tuple[str, str] | tuple[str, str, str]],
) -> dict[str, File]:
    """Build File mappings from (dest, src[, owner]) tuples."""
    result: dict[str, File] = {}

    for dest, src, *rest in items:
        owner = rest[0] if rest else None
        source = resolve_source(base, src)

        if not source.exists():
            raise FileNotFoundError(f"{source} doesn't exist")

        result[dest] = File(str(source), owner=owner)

    return result


def build_directories(
    base: Path,
    items: Iterable[tuple[str, str] | tuple[str, str, str]],
) -> dict[str, Directory]:
    """Build Directory mappings from (dest, src[, owner]) tuples."""
    result: dict[str, Directory] = {}

    for dest, src, *rest in items:
        owner = rest[0] if rest else None
        source = resolve_source(base, src)

        if not source.exists():
            raise FileNotFoundError(f"{source} doesn't exist")

        result[dest] = Directory(
            source_directory=str(source),
            owner=owner,
        )

    return result


def build_symlinks(
    base: Path,
    items: Iterable[tuple[str, str] | tuple[str, str, str]],
    default_owner: str,
) -> dict[str, str | Symlink]:
    """Build Symlink mappings from (dest, src[, owner]) tuples."""
    result: dict[str, str | Symlink] = {}

    for dest, src, *rest in items:
        owner = rest[0] if rest else default_owner
        source = resolve_source(base, src)

        if not source.exists():
            raise FileNotFoundError(f"{source} doesn't exist")

        result[dest] = Symlink(
            str(source),
            owner=owner,
        )

    return result


def file_hash(path: str) -> str:
    """Return SHA-256 hash of file or None if it does not exist."""
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"{p} doesn't exist")

    with p.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def generate_grub_config():
    """Generate GRUB configuration."""
    cmd = ["grub-mkconfig", "-o", "/boot/grub/grub.cfg"]
    logger.info("Generating GRUB config.")
    run_cmd_as_root(cmd)


def build_font_cache():
    """Build system font cache."""
    cmd = ["fc-cache", "-fv"]
    logger.info("Building font cache.")
    run_cmd_as_root(cmd)


def generate_locales():
    """Generate system locales."""
    cmd = ["locale-gen"]
    logger.info("Generating locales.")
    run_cmd_as_root(cmd)


def build_initramfs_images():
    """Build initramfs images."""
    cmd = ["mkinitcpio", "-P"]
    logger.info("Building initramfs images.")
    run_cmd_as_root(cmd)


def sync_pacman_repos():
    """Sync pacman repositories."""
    cmd = ["pacman", "-Sy"]
    logger.info("Syncing pacman repositories.")
    run_cmd_as_root(cmd)


def build_plymouth_theme():
    """Build plymouth theme."""
    cmd = ["plymouth-set-default-theme", "-R"]
    logger.info("Building plymouth theme")
    run_cmd_as_root(cmd)


def get_current_wallpaper() -> str:
    home = Path(get_user_home_dir())
    json_path = home / ".cache/noctalia/wallpapers.json"

    result = run_cmd_as_user(
        [
            "jq",
            "-r",
            """
            .wallpapers[""]
            | select(. != null and . != "")
            // .defaultWallpaper
            """,
            str(json_path),
        ],
    )

    return result.strip()
