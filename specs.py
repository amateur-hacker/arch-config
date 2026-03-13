from enum import Enum
from typing import Callable, Iterable, Literal, TypeAlias, TypedDict

from decman.plugins.aur import CustomPackage

# Package
Package: TypeAlias = str | CustomPackage
PackageSpec: TypeAlias = Package | tuple[str | CustomPackage, list["PackageSpec"]]
PackageSpecs: TypeAlias = Iterable[PackageSpec]
PackageList: TypeAlias = list[PackageSpec]

# Dotfile
DotfileItemSpec: TypeAlias = tuple[str, str] | tuple[str, str, str]
DotfileItemList: TypeAlias = list[DotfileItemSpec]


class TrackedItemSpec(TypedDict):
    key: str
    action: Callable[[], None]


TrackedItemsMap: TypeAlias = dict[str, TrackedItemSpec]


# External package(s)
ExternalPackageManager: TypeAlias = Literal["cargo", "bun", "pipx", "go"]
ExternalPackage: TypeAlias = str | tuple[str, ...]
ExternalPackages: TypeAlias = dict[ExternalPackageManager, list[ExternalPackage]]


# Profile
class Profile(Enum):
    WORKSTATION = "workstation"
