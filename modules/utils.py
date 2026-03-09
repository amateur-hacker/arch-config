import os
import pwd
from typing import Iterable

import decman
from decman.plugins.aur import CustomPackage

from specs import PkgSpec


def is_laptop():
    """Return True if laptop battery exists."""
    power_path = "/sys/class/power_supply"
    if not os.path.exists(power_path):
        return False

    for item in os.listdir(power_path):
        if item.lower().startswith("bat"):
            return True
    return False


def get_username() -> str:
    """Return the username"""
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return sudo_user

    try:
        return pwd.getpwuid(os.getuid()).pw_name
    except KeyError:
        raise RuntimeError("Cannot determine username.")


def get_user_home_dir():
    """Return the home directory of the effective non-root user."""
    username = get_username()

    try:
        return pwd.getpwnam(username).pw_dir
    except KeyError:
        raise RuntimeError(f"Cannot determine home directory for user '{username}'.")


def run_cmd_as_root(cmd: list[str], **kwargs):
    return decman.prg(cmd, pty=False, **kwargs)


def run_cmd_as_user(cmd: list[str], **kwargs):
    return decman.prg(
        cmd,
        user=get_username(),
        mimic_login=True,
        pty=False,
        **kwargs,
    )


def resolve_pkgs(raw: Iterable[PkgSpec]):
    result: set[str | CustomPackage] = set()

    for item in raw:
        if isinstance(item, str):
            result.add(item)

        elif isinstance(item, CustomPackage):
            result.add(item)

        elif isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError(f"Invalid package tuple format: {item}")

            pkg, deps = item

            if not isinstance(deps, set):
                raise TypeError(f"Dependencies must be set[str], got {type(deps)}")

            for dep in deps:
                if not isinstance(dep, str):
                    raise TypeError(f"Dependency must be str, got {type(dep)}")

            if not isinstance(pkg, (str, CustomPackage)):
                raise TypeError(
                    f"Package must be str or CustomPackage, got {type(pkg)}"
                )

            result.add(pkg)
            result.update(deps)

        else:
            raise TypeError(f"Unsupported package type: {type(item)}")

    return result


def is_repo_pkg(pkg: str) -> bool:
    try:
        decman.sh(f"pacman -Si {pkg}", pty=False)
        return True
    except Exception:
        return False


def split_pkgs(pkgs: Iterable[str | CustomPackage]):
    pacman_pkgs: set[str] = set()
    aur_pkgs: set[str] = set()
    aur_custom_pkgs: list[CustomPackage] = []

    for pkg in pkgs:
        if isinstance(pkg, CustomPackage):
            aur_custom_pkgs.append(pkg)

        elif isinstance(pkg, str):
            if is_repo_pkg(pkg):
                pacman_pkgs.add(pkg)
            else:
                aur_pkgs.add(pkg)

        else:
            raise TypeError(f"Unsupported package type: {type(pkg)}")

    return pacman_pkgs, aur_pkgs, aur_custom_pkgs
