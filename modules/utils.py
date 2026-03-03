import os
import pwd
from typing import Iterable, Union

import decman


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


def get_user_home_dir() -> str:
    """Return the home directory of the effective non-root user."""
    username = get_username()

    try:
        return pwd.getpwnam(username).pw_dir
    except KeyError:
        raise RuntimeError(f"Cannot determine home directory for user '{username}'.")


PkgSpec = Union[
    str,
    tuple[str, set[str]],
]


def resolve_pkgs(raw: Iterable[PkgSpec]) -> set[str]:
    result: set[str] = set()

    for item in raw:
        if isinstance(item, str):
            result.add(item)

        elif isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError(f"Invalid package tuple format: {item}")

            name, deps = item

            if not isinstance(name, str):
                raise TypeError(f"Package name must be str, got {type(name)}")

            if not isinstance(deps, set):
                raise TypeError(f"Dependencies must be set[str], got {type(deps)}")

            for dep in deps:
                if not isinstance(dep, str):
                    raise TypeError(f"Dependency must be str, got {type(dep)}")

            result.add(name)
            result.update(deps)

        else:
            raise TypeError(f"Unsupported package type: {type(item)}")

    return result


def run_cmd_as_root(cmd: list[str], **kwargs) -> str:
    return decman.prg(cmd, pty=False, **kwargs)


def run_cmd_as_user(cmd: list[str], **kwargs) -> str:
    return decman.prg(
        cmd,
        user=get_username(),
        mimic_login=True,
        pty=False,
        **kwargs,
    )
