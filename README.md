# 🏠 Arch Linux Declarative Config

> Declarative system configuration for Hyprland using [decman](https://github.com/kiviktnm/decman)

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
- **Hyprland** — Wayland compositor with plugins
- **Fish Shell** — Modern CLI shell with plugins
- **Neovim** — Configured with dependencies
- **Dev Tools** — Node.js, Python, Rust, Go, Bun, Docker, Lazygit
- **GUI Apps** — Chrome, Spotify, Telegram, Kitty, MPV
- **Theming** — Catppuccin, SDDM, GTK themes

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

Edit any module in `modules/` — for example, to add packages to Hyprland:

```python
# modules/hyprland.py
PKGS: PkgList = [
    ("hyprland", {"hyprland-protocols", "hyprpicker"}),
    "new-package",  # Add your package here
]
```

Package format:
- `"package"` — single package
- `("package", {"dep1", "dep2"})` — package with dependencies

## 📁 Adding Dotfiles

Edit `modules/dotfiles.py` — add to `symlinks()` or `files()`:

```python
def symlinks(self):
    return build_symlinks(base=self._base, items=[
        (f"{self._home}/.config/newapp", "config/newapp"),
    ])
```

Dotfile format:
- `(destination, source)` — relative to dotfiles/ directory
- `(destination, source, owner)` — with specific owner

## 💻 Useful Commands

| Command | Description |
|---------|-------------|
| `decman --dry-run` | Preview changes without applying |
| `decman --debug` | Show debug output |
| `decman --skip files` | Skip dotfiles step |
| `decman --only aur` | Only run AUR packages |

## 🔧 Creating a New Module

```python
# modules/my_module.py
import decman
from decman.plugins import pacman

from specs import PkgList

PKGS: PkgList = ["my-package"]


class MyModule(decman.Module):
    """Description of what this module does."""

    def __init__(self):
        super().__init__("my-module")

    @pacman.packages
    def pkgs(self):
        return PKGS
```

Then add it to `main.py`:
```python
from modules.my_module import MyModule

decman.modules += [MyModule()]
```

## ⚠️ Tips

- Always run with `--dry-run` first to preview changes
- Review what `initial-setup.sh` does before running
- Backup important configs before applying new ones
