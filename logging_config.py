import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


def setup_logging() -> None:
    custom_theme = Theme(
        {
            "logging.level.info": "white",
            "logging.level.warning": "yellow",
            "logging.level.error": "red",
        }
    )

    console = Console(theme=custom_theme)

    handler = RichHandler(
        console=console,
        show_time=False,
        show_path=False,
        show_level=False,
        markup=True,
    )

    formatter = logging.Formatter(
        "[bold magenta][CUSTOM][/bold magenta] "
        "[logging.level.%(levelname)s]%(levelname)s[/logging.level.%(levelname)s]: "
        "%(message)s"
    )

    handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
    )
