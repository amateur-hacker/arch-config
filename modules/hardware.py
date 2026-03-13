import subprocess

import decman
from decman.plugins import pacman

from .utils import is_laptop
from settings import ENABLE_GAME_SUPPORT


def read_file(path):
    """Read file safely. Return stripped content or None."""
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def detect_chassis_vendor():
    """Return system vendor from DMI or 'unknown'."""
    candidates = [
        "/sys/class/dmi/id/chassis_vendor",
        "/sys/class/dmi/id/board_vendor",
        "/sys/class/dmi/id/sys_vendor",
    ]
    for path in candidates:
        value = read_file(path)
        if value:
            return value.lower()
    return "unknown"


def detect_cpu_vendor():
    """Detect CPU vendor: 'intel', 'amd', or 'unknown'."""
    try:
        output = subprocess.check_output(["lscpu"], encoding="utf-8")
        if "GenuineIntel" in output:
            return "intel"
        elif "AuthenticAMD" in output:
            return "amd"
    except Exception:
        return "unknown"


def detect_gpu_vendors():
    """Return GPU vendors detected via lspci."""
    try:
        output = subprocess.check_output(
            ["lspci"],
            encoding="utf-8",
        ).lower()

        vendors = []
        if "nvidia" in output:
            vendors.append("nvidia")
        if "amd" in output or "radeon" in output:
            vendors.append("amd")
        if "intel" in output:
            vendors.append("intel")
        return vendors
    except Exception:
        return []


def chassis_type():
    """Return chassis type, e.g., 'desktop' or 'laptop'."""
    chassis = read_file("/sys/class/dmi/id/chassis_type") or ""
    return "desktop" if chassis == "3" else "laptop"


def get_cpu_packages():
    """Return CPU microcode package set."""
    cpu = detect_cpu_vendor()
    if cpu == "intel":
        return {"intel-ucode"}
    elif cpu == "amd":
        return {"amd-ucode"}
    return set()


def get_gpu_packages():
    """Return GPU-related packages based on hardware and game support."""
    packages = {"vulkan-icd-loader"}
    vendors = detect_gpu_vendors()

    is_game_support_enabled = ENABLE_GAME_SUPPORT

    has_nvidia = "nvidia" in vendors
    has_amd = "amd" in vendors
    has_intel = "intel" in vendors
    hybrid = has_nvidia and (has_amd or has_intel)

    if has_nvidia:
        packages |= {
            "libva-nvidia-driver",
            "nvidia-dkms",
            "nvidia-settings",
            "nvidia-utils",
            "opencl-nvidia",
        }

        if is_game_support_enabled:
            packages |= {
                "lib32-nvidia-utils",
                "lib32-opencl-nvidia",
                "lib32-vulkan-icd-loader",
            }

        if hybrid:
            packages |= {
                "mesa",
                "nvidia-prime",
            }

    if has_amd:
        packages |= {
            "mesa",
            "vulkan-radeon",
        }

        if is_game_support_enabled:
            packages |= {
                "lib32-mesa",
                "lib32-vulkan-icd-loader",
                "lib32-vulkan-mesa-layers",
                "lib32-vulkan-radeon",
            }

    if has_intel:
        packages |= {
            "intel-media-driver",
            "mesa",
            "vulkan-intel",
        }

        if is_game_support_enabled:
            packages |= {
                "lib32-mesa",
                "lib32-vulkan-icd-loader",
                "lib32-vulkan-intel",
            }

    return packages


def get_laptop_packages():
    """Return laptop-specific packages if applicable."""
    if is_laptop():
        return {"power-profiles-daemon", "powertop"}
    return set()


def get_vendor_packages():
    """Return vendor-specific packages (e.g., ASUS tools)."""
    packages = set()
    vendor = detect_chassis_vendor()
    if "asus" in vendor:
        packages |= {
            "asusctl",
            "rog-control-center",
            "supergfxctl",
        }
    return packages


def get_all_packages():
    """Return all combined detected packages."""
    packages = set()
    packages |= get_cpu_packages()
    packages |= get_gpu_packages()
    packages |= get_laptop_packages()
    packages |= get_vendor_packages()
    packages |= {
        "linux-firmware",
        "mesa-utils",
        "vulkan-tools",
    }
    return packages


def has_lib32_packages() -> bool:
    """Return True if any lib32-* packages are installed."""
    try:
        decman.sh("pacman -Qq | grep -q '^lib32-'", pty=False)
        return True
    except Exception:
        return False


def remove_lib32_packages() -> None:
    """Remove all installed lib32-* packages if any exist."""
    try:
        output = decman.prg(["pacman", "-Qq"], pty=False)
    except Exception as e:
        raise RuntimeError(f"Failed to query installed packages: {e}")

    lib32_pkgs = [pkg for pkg in output.splitlines() if pkg.startswith("lib32-")]

    if not lib32_pkgs:
        print("[Hardware] No lib32 packages installed")
        return

    print(f"[Hardware] Removing {len(lib32_pkgs)} lib32 packages")

    decman.prg(
        ["pacman", "-Rns", "--noconfirm", *lib32_pkgs],
        pty=False,
    )


def is_multilib_enabled() -> bool:
    """Return True if the multilib repo is enabled in pacman.conf."""
    try:
        with open("/etc/pacman.conf", "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped == "[multilib]":
                    return True
                if stripped in ("#[multilib]", "# [multilib]"):
                    return False
        return False
    except Exception:
        return False


def toggle_multilib(enable: bool):
    """Enable or disable the multilib repo in pacman.conf."""
    pacman_conf = "/etc/pacman.conf"

    try:
        with open(pacman_conf, "r") as f:
            lines = f.readlines()

        new_lines = []
        inside_multilib = False

        for line in lines:
            stripped = line.strip()

            if stripped in ("[multilib]", "#[multilib]", "# [multilib]"):
                inside_multilib = True
                new_lines.append("[multilib]\n" if enable else "# [multilib]\n")
                continue

            if inside_multilib and stripped.lstrip("# ").startswith("Include"):
                if enable:
                    new_lines.append("Include = /etc/pacman.d/mirrorlist\n")
                else:
                    new_lines.append("# Include = /etc/pacman.d/mirrorlist\n")
                inside_multilib = False
                continue

            new_lines.append(line)

        with open(pacman_conf, "w") as f:
            f.writelines(new_lines)

    except Exception as e:
        raise RuntimeError(f"Failed to toggle multilib: {e}")


class Hardware(decman.Module):
    """Hardware-aware module that installs CPU, GPU, and vendor-specific packages."""

    def __init__(self):
        super().__init__("hardware")

    @pacman.packages
    def pkgs(self):
        return get_all_packages()

    def before_update(self, store):
        _ = store
        if ENABLE_GAME_SUPPORT:
            if not is_multilib_enabled():
                print("[Hardware] Enabling multilib")
                toggle_multilib(True)

    def after_update(self, store):
        _ = store
        if not ENABLE_GAME_SUPPORT:
            multilib_enabled = is_multilib_enabled()
            lib32_present = has_lib32_packages()

            if lib32_present:
                print("[Hardware] Removing lib32 packages")
                remove_lib32_packages()

            if multilib_enabled:
                print("[Hardware] Disabling multilib")
                toggle_multilib(False)
                decman.prg(
                    ["pacman", "-Sy", "--noconfirm"],
                    pty=False,
                )
