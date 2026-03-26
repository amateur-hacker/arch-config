import shutil
from decman.extras.users import Group, User, UserManager

from modules.dotfiles_utils import ensure_fullname

from .utils import get_username, get_user_home_dir
from settings import FULL_NAME, SHELL

USER_NAME = get_username()
USER_HOME_DIR = get_user_home_dir()
GROUPS = (Group("users"), Group(USER_NAME))
USERS = (
    User(
        username=USER_NAME,
        group=USER_NAME,
        home=USER_HOME_DIR,
        shell=shutil.which(SHELL),
        groups=(
            "audio",
            "docker",
            "input",
            "lp",
            "network",
            "optical",
            "power",
            "rfkill",
            "storage",
            "sys",
            "users",
            "video",
            "wheel",
        ),
    ),
)


class Users(UserManager):
    """Manage primary system user and base group memberships."""

    def __init__(self):
        super().__init__()

        for group in GROUPS:
            self.add_group(group)

        for user in USERS:
            self.add_user(user)

    def after_update(self, store):
        _ = store
        ensure_fullname(username=USER_NAME, fullname=FULL_NAME)
