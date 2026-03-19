import logging
import os
import pwd
import shutil
from typing import Callable, TypeAlias, TypedDict

import decman
from decman.plugins.aur import CustomPackage

from settings import SHELL
from specs import (
    ExternalPackageManager,
    ExternalPackages,
    PackageSpec,
    PackageSpecs,
)

InstallCommand: TypeAlias = Callable[[str, list[str]], list[str]]
RemoveCommand: TypeAlias = Callable[[str], list[str]]


class ManagerOps(TypedDict):
    install: InstallCommand
    remove: RemoveCommand


class ResolvedManagerOps(ManagerOps):
    packages: dict[str, list[str]]


ResolvedExternalPackages: TypeAlias = dict[ExternalPackageManager, ResolvedManagerOps]

logger = logging.getLogger(__name__)


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


def get_user_env(user: str) -> dict[str, str]:
    """Return environment variables for the given user."""
    try:
        result = decman.prg(
            ["sudo", "-u", user, SHELL, "-lc", "env"],
            pty=False,
            check=True,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to get environment for user '{user}': {e}") from e

    env: dict[str, str] = {}

    for line in result.splitlines():
        if "=" not in line:
            continue

        k, v = line.split("=", 1)

        if not k:
            continue

        env[k] = v

    return env


def ensure_cmd(cmd: str):
    """Ensure the command exists in PATH."""
    if not cmd:
        raise ValueError("Empty command")
    if shutil.which(cmd) is None:
        raise RuntimeError(f"Required command '{cmd}' not found in PATH")


def run_cmd_as_root(cmd: list[str], **kwargs):
    """Execute a command as root using decman."""
    ensure_cmd(cmd[0])

    return decman.prg(cmd, **kwargs)


def run_cmd_as_user(cmd: list[str], **kwargs):
    """Execute a command as the invoking user."""
    ensure_cmd(cmd[0])

    kwargs.setdefault("mimic_login", True)

    user = get_username()
    user_env = get_user_env(user)

    return decman.prg(
        cmd,
        user=user,
        env_overrides=user_env,
        **kwargs,
    )


def resolve_pkgs(raw: PackageSpecs):
    """Resolve package specs including nested dependencies."""
    result: set[str | CustomPackage] = set()

    def resolve(item: PackageSpec):
        if isinstance(item, (str, CustomPackage)):
            result.add(item)
        else:
            pkg, deps = item
            result.add(pkg)

            for dep in deps:
                resolve(dep)

    for item in raw:
        resolve(item)

    return result


repo_cache: set[str] | None = None


def get_repo_pkgs():
    """Return cached list of pacman repository packages."""
    global repo_cache
    if repo_cache is None:
        out = run_cmd_as_user(["expac", "-S", "%n"], pty=False)
        repo_cache = set(out.splitlines())

    return repo_cache


def split_pkgs(pkgs: PackageSpecs):
    """Split packages into pacman, AUR, and custom AUR groups."""
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


def resolve_external_packages(spec: ExternalPackages):
    """Resolve external package specs into structured manager operations."""

    managers: dict[ExternalPackageManager, ManagerOps] = {
        "pipx": {
            "install": lambda pkg, args: ["pipx", "install", pkg, *args],
            "remove": lambda pkg: ["pipx", "uninstall", pkg],
        },
        "cargo": {
            "install": lambda pkg, args: ["cargo", "install", pkg, *args],
            "remove": lambda pkg: ["cargo", "uninstall", pkg],
        },
        "bun": {
            "install": lambda pkg, args: ["bun", "add", "-g", pkg, *args],
            "remove": lambda pkg: ["bun", "remove", "-g", pkg],
        },
    }

    result: ResolvedExternalPackages = {}

    for manager, packages in spec.items():
        manager_ops = managers.get(manager)
        if manager_ops is None:
            raise ValueError(f"Unsupported package manager: {manager}")

        install_cmd = manager_ops["install"]
        remove_cmd = manager_ops["remove"]

        pkgs: dict[str, list[str]] = {}

        for item in packages:
            if isinstance(item, str):
                pkg = item
                args: list[str] = []
            else:
                pkg, *args = item

            pkgs[pkg] = args

        result[manager] = {
            "install": install_cmd,
            "remove": remove_cmd,
            "packages": pkgs,
        }

    return result


external_pkg_cache: dict[ExternalPackageManager, set[str]] = {}


def get_external_installed(manager: ExternalPackageManager):
    """Return installed packages for the given external manager."""

    if manager in external_pkg_cache:
        return external_pkg_cache[manager]

    pkgs: set[str] = set()

    if manager == "cargo":
        out = run_cmd_as_user(["cargo", "install", "--list"], pty=False)
        pkgs = {line.split()[0] for line in out.splitlines() if line.endswith(":")}

    elif manager == "bun":
        out = run_cmd_as_user(["bun", "pm", "ls", "-g"], pty=False)

        for line in out.splitlines():
            line = line.strip()

            if "@" not in line:
                continue

            pkg = line.split()[1]
            pkgs.add(pkg.split("@")[0])

    elif manager == "pipx":
        out = run_cmd_as_user(["pipx", "list"], pty=False)

        for line in out.splitlines():
            line = line.strip()

            if not line or "package" in line:
                continue

            if "(" in line:
                pkg = line.split()[0]
                pkgs.add(pkg)

    external_pkg_cache[manager] = pkgs
    return pkgs


def reconcile_external_pkgs(
    manager: ExternalPackageManager,
    declared: dict[str, list[str]],
    install_cmd: InstallCommand,
    remove_cmd: RemoveCommand,
):
    """Ensure external packages match declared state."""

    installed = get_external_installed(manager)

    declared_pkgs = set(declared.keys())

    to_install = declared_pkgs - installed
    to_remove = installed - declared_pkgs

    if to_install:
        logger.info("Installing external packages")

    for pkg in to_install:
        args = declared[pkg]
        logger.info("Installing %s (%s)", pkg, manager)
        run_cmd_as_user(install_cmd(pkg, args))

    if to_remove:
        logger.info("Removing unmanaged external packages")

    for pkg in to_remove:
        logger.info("Removing %s (%s)", pkg, manager)

        if remove_cmd:
            run_cmd_as_user(remove_cmd(pkg))
