# 🏠 Arch Linux Declarative Config

> A Declarative system configuration for **Arch Linux** using [decman](https://github.com/kiviktnm/decman)

## 🚀 Quick Start

```bash
# Step 1: Run initial setup (installs decman, AUR helper, etc.)
./initial-setup.sh

# Step 2: Apply your configuration
sudo decman --source main.py

# Step 3: Explore more options
decman --help
```

## ✨ Features

- **Declarative Package Management** — Define packages in Python, let decman handle installation
- **Declarative Dotfile Management** — Symlink/copy dotfiles from repo to system
- **AUR Support** — Chaotic AUR + Paru + custom AUR packages
- **Hyprland** — Wayland compositor with noctalia shell
- **Fish Shell** — Modern CLI shell with plugins
- **Neovim** — LazyVim with customizations
- **Dev Tools** — Node.js, Python, Rust, Go, Bun, Docker, Lazygit, Lazydocker
- **GUI Apps** — Chrome, Spotify, Telegram, Kitty, MPV
- **Theming** — Catppuccin Mocha Lavender, SDDM, GRUB, GTK themes

## 📂 Project Structure

```
.
├── main.py              # Entry point — decman source file
├── profiles.py          # Profile definitions
├── specs.py             # Type definitions
├── settings.py          # User settings
├── logging_config.py   # Logging setup
├── modules/             # Package & dotfile modules
│   ├── base.py         # Base system packages
│   ├── hardware.py    # Hardware drivers
│   ├── hyprland.py    # Hyprland compositor
│   ├── aur.py         # AUR packages
│   ├── cli_tools.py   # CLI utilities
│   ├── dev_tools.py   # Development tools
│   ├── fonts.py       # Fonts
│   ├── gui_tools.py   # GUI applications
│   ├── theming_tools.py # Themes
│   ├── wayland_tools.py # Wayland tools
│   ├── dotfiles.py    # Dotfile management
│   └── users.py       # User management
└── dotfiles/           # Source dotfiles
    ├── config/        # ~/.config files
    ├── etc/           # /etc files
    └── home/          # ~/ files
```

## 📦 Adding Packages

Edit any module in `modules/` — for example, to add packages to CLI tools:

```python
# modules/cli_tools.py
PKGS: PkgList = [
    ("zoxide", {"fzf"}), # Package with deps
    "pipes.sh",  # AUR package support
    CustomPackage(
        "nitch++-git",
        "https://github.com/amateur-hacker/nitchplusplus",
    ),  # Custom Package support
    "new_package"  # Add your package here
]
```

Package format:

- `"package"` — single package
- `("package", {"dep1", "dep2"})` — package with dependencies

## 📁 Adding Dotfiles

Edit `modules/dotfiles.py` — use the module-level variables:

```python
# modules/dotfiles.py

# Copy files to system locations (/etc, /usr, etc.)
FILE_ITEMS: DotfileItemList = [
    ("/etc/default/grub", "etc/default/grub"),
    ("/etc/pacman.conf", "etc/pacman.conf"),
    # (destination, source) or (destination, source, owner)
]

# Copy directories to system
DIRECTORY_ITEMS: DotfileItemList = [
    ("/usr/share/plymouth/themes/anonymous", "usr/share/plymouth/themes/anonymous"),
]

# Create symlinks in user's home directory
SYMLINK_ITEMS: DotfileItemList = [
    (f"{HOME}/.config/hypr", "config/hypr"),
    (f"{HOME}/.config/kitty", "config/kitty"),
    # (destination, source) — destination is relative to home
]

# Run commands when tracked files change (by hash)
TRACKED_ITEMS: TrackedItemsMap = {
    "/etc/default/grub": {
        "key": "grub_hash",
        "action": generate_grub_config,  # function that runs grub-mkconfig
    },
    "/etc/fonts/local.conf": {
        "key": "fonts_hash",
        "action": build_font_cache,  # function that runs fc-cache
    },
}
```

Dotfile format:

- `(destination, source)` — relative to dotfiles/ directory
- `(destination, source, owner)` — with specific owner

> **Note:** For symlinks, if a folder already exists at the destination, remove it first before running decman — otherwise it will warn you.

## 🔧 Creating a New Module

```python
# modules/my_module.py
import decman
from decman.plugins import pacman, aur
from decman.plugins.aur import CustomPackage

from specs import PkgList

from .utils import resolve_pkgs, split_pkgs

PKGS: PkgList = [
  "pacman_pkg1",
  (
      "pacman_pkg2",
      {
          "deps1",
          "deps2",
      },
  ),
  ("aur_pkg1", {"deps1"}),
  "aur_pkg2",
  (
      CustomPackage("pkg_name", "git_url"),
      {
          "deps1",
          "deps2",
      },
   ),
  CustomPackage("pkg_name", None, "path"),
]


class MyModule(decman.Module):
    """Description of what this module does."""

    def __init__(self):
        super().__init__("my-module")

        _resolved_pkgs = resolve_pkgs(PKGS)
        # Use _, if you don't want any field.
        self._pkgs, self._aur_pkgs, self._aur_custom_pkgs = split_pkgs(_resolved_pkgs)

    @pacman.packages
    def pkgs(self):
        return self._pkgs

    @aur.packages
    def aur_pkgs(self):
        return self._aur_pkgs

    @aur.custom_packages
    def aur_custom_pkgs(self):
        return self._aur_custom_pkgs
```

Then add it to `main.py`:

```python
from modules.my_module import MyModule

decman.modules += [MyModule()]
```

## 💻 Useful Commands

| Command | Description |
|---------|-------------|
| `decman --dry-run` | Preview changes without applying |
| `decman --debug` | Show debug output |
| `decman --skip files` | Skip dotfiles step |
| `decman --only aur` | Only run AUR packages |
| `decman --params aur-upgrade-devel` | Upgrade devel packages (*-git, etc.) |
| `decman --params aur-force` | Force rebuild cached AUR packages |
