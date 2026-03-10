import os
import pwd
import shutil
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


def ensure_cmd(cmd: str):
    if not cmd:
        raise ValueError("Empty command")
    if shutil.which(cmd) is None:
        raise RuntimeError(f"Required command '{cmd}' not found in PATH")


def run_cmd_as_root(cmd: list[str], **kwargs):
    ensure_cmd(cmd[0])
    return decman.prg(cmd, pty=False, **kwargs)


def run_cmd_as_user(cmd: list[str], **kwargs):
    ensure_cmd(cmd[0])
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


repo_cache: set[str] | None = None


def get_repo_pkgs() -> set[str]:
    global repo_cache
    if repo_cache is None:
        out = decman.sh("expac -S %n", pty=False)
        repo_cache = set(out.splitlines())

    return repo_cache


def split_pkgs(pkgs: Iterable[str | CustomPackage]):
    pacman_pkgs: set[str] = set()
    aur_pkgs: set[str] = set()
    aur_custom_pkgs: set[CustomPackage] = set()

    repo_pkgs = get_repo_pkgs()

    for pkg in pkgs:
        if isinstance(pkg, CustomPackage):
            aur_custom_pkgs.add(pkg)

        elif isinstance(pkg, str):
            if pkg in repo_pkgs:
                pacman_pkgs.add(pkg)
            else:
                aur_pkgs.add(pkg)

        else:
            raise TypeError(f"Unsupported package type: {type(pkg)}")

    return (
        sorted(pacman_pkgs),
        sorted(aur_pkgs),
        sorted(aur_custom_pkgs, key=lambda p: p.pkgname),
    )
