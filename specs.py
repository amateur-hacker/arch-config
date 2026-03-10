from enum import Enum
from typing import Callable, Iterable, TypeAlias, TypedDict

import decman
from decman import Directory, File, Symlink
from decman.plugins.aur import CustomPackage

# Package types
PkgSpec: TypeAlias = str | CustomPackage | tuple[str | CustomPackage, list["PkgSpec"]]
PkgList: TypeAlias = list[PkgSpec]

# Dotfile types
DotfileItemSpec: TypeAlias = tuple[str, str] | tuple[str, str, str]
DotfileItemList: TypeAlias = list[DotfileItemSpec]


class TrackedItemSpec(TypedDict):
    key: str
    action: Callable[[], None]


TrackedItemsMap: TypeAlias = dict[str, TrackedItemSpec]

# Dotfile utils types
FileMap: TypeAlias = dict[str, File]
DirectoryMap: TypeAlias = dict[str, Directory]
SymlinkMap: TypeAlias = dict[str, str | Symlink]
DotfileItems: TypeAlias = Iterable[DotfileItemSpec]


# Profile types
class Profile(Enum):
    WORKSTATION = "workstation"


ProfileModules: TypeAlias = list[decman.Module]
ProfilesMap: TypeAlias = dict[Profile, ProfileModules]
