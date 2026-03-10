import hashlib
import logging
import os
import pwd
from pathlib import Path

from decman import Directory, File, Store, Symlink

from modules.utils import (
    get_user_home_dir,
    get_username,
    run_cmd_as_root,
    run_cmd_as_user,
)
from specs import DirectoryMap, DotfileItems, FileMap, SymlinkMap, TrackedItemsMap

USERNAME = get_username()
HOME = Path(get_user_home_dir())

logger = logging.getLogger(__name__)


def get_current_wallpaper_path():
    """Return the path of the current active wallpaper."""
    json_path = HOME / ".cache/noctalia/wallpapers.json"
    default_wall = "/etc/xdg/quickshell/noctalia-shell/Assets/Wallpaper/noctalia.png"

    if not json_path.exists():
        raise FileNotFoundError(f"{json_path} doesn't exist")

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

    if not result:
        return default_wall

    return result.strip()


def ensure_fullname(username: str, fullname: str):
    """Ensure the user's fullname."""
    try:
        current = pwd.getpwnam(username).pw_gecos.split(",")[0]
    except KeyError as e:
        raise LookupError(f"User '{username}' does not exist") from e

    if current != fullname:
        logger.info("Setting fullname '%s' for user '%s'", fullname, username)
        run_cmd_as_root(["chfn", "-f", fullname, username])


def ensure_acl(path: Path, acl: str):
    """Ensure the ACL entry exists on the path."""
    if not path.exists():
        raise FileNotFoundError(f"{path} doesn't exist")

    current = run_cmd_as_root(["getfacl", "-p", str(path)])
    if acl not in current:
        logger.info("Applying ACL '%s' to %s", acl, path)
        run_cmd_as_root(["setfacl", "-m", acl, str(path)])


def update_xdg_user_dirs():
    """Update XDG user directories."""
    config_path = HOME / ".config/user-dirs.dirs"

    if not config_path.exists():
        raise FileNotFoundError(f"{config_path} doesn't exist")

    for line in config_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        _, value = line.split("=", 1)
        value = value.strip().strip('"')

        resolved_path = Path(value.replace("$HOME", str(HOME)))

        if not resolved_path.exists():
            logger.info("Updating XDG user directories.")
            run_cmd_as_user(["xdg-user-dirs-update"])
            run_cmd_as_user(["xdg-user-dirs-gtk-update"])
            return


def apply_graphical_gsettings():
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


def resolve_source(base: Path, src: str):
    """Resolve source path relative to base if not absolute."""
    path = Path(src)
    return path if path.is_absolute() else base / path


def build_files(
    base: Path,
    items: DotfileItems,
):
    """Build File mappings from (dest, src[, owner]) tuples."""
    result: FileMap = {}

    for dest, src, *rest in items:
        owner = rest[0] if rest else None
        source = resolve_source(base, src)

        if not source.exists():
            raise FileNotFoundError(f"{source} doesn't exist")

        result[dest] = File(str(source), owner=owner)

    return result


def build_directories(
    base: Path,
    items: DotfileItems,
):
    """Build Directory mappings from (dest, src[, owner]) tuples."""
    result: DirectoryMap = {}

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
    items: DotfileItems,
    default_owner: str,
):
    """Build Symlink mappings from (dest, src[, owner]) tuples."""
    result: SymlinkMap = {}

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


def file_hash(path: Path):
    """Return the SHA-256 hash of file."""
    if not path.exists():
        raise FileNotFoundError(f"{path} doesn't exist")

    with path.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_tracked_actions(tracked_items: TrackedItemsMap, store: Store):
    """Run actions when tracked files change."""
    for path, config in tracked_items.items():
        key = config["key"]
        action = config["action"]

        store.ensure(key, None)
        p = Path(path)

        if not p.exists():
            continue

        current = file_hash(p)

        if store[key] != current:
            action()
            store[key] = current


def generate_grub_config():
    """Generate GRUB configuration."""
    logger.info("Generating GRUB config.")
    run_cmd_as_root(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])


def build_font_cache():
    """Build system font cache."""
    logger.info("Building font cache.")
    run_cmd_as_root(["fc-cache", "-fv"])


def generate_locales():
    """Generate system locales."""
    logger.info("Generating locales.")
    run_cmd_as_root(["locale-gen"])


def build_initramfs_images():
    """Build initramfs images."""
    logger.info("Building initramfs images.")
    run_cmd_as_root(["mkinitcpio", "-P"])


def sync_pacman_repos():
    """Sync pacman repositories."""
    logger.info("Syncing pacman repositories.")
    run_cmd_as_root(["pacman", "-Sy"])


def build_plymouth_theme():
    """Build plymouth theme."""
    logger.info("Building plymouth theme")
    run_cmd_as_root(["plymouth-set-default-theme", "-R"])


def set_papirus_folder_color(desired_color: str = "cat-mocha-lavender"):
    """Set Papirus folder color for Papirus-Dark theme."""
    config_file = Path("/var/lib/papirus-folders/keep")
    theme = "Papirus-Dark"

    if config_file.exists():
        settings = dict(
            line.split("=", 1)
            for line in config_file.read_text().splitlines()
            if "=" in line
        )

        if settings.get("theme") == theme and settings.get("color") == desired_color:
            return

    logger.info("Setting Papirus folder color to '%s'.", desired_color)

    run_cmd_as_user(["papirus-folders", "-t", theme, "-C", desired_color])
