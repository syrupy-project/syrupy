import os
from typing import (
    Any,
    Union,
)

import colored

from .constants import DISABLE_COLOR_ENV_VARS


def _is_color_disabled() -> bool:
    for env_var_name in DISABLE_COLOR_ENV_VARS:
        if os.environ.get(env_var_name) is not None:
            return True
    return False


def _stylize(text: Union[str, int], *args: Any) -> str:
    if _is_color_disabled():
        return str(text)
    return colored.stylize(text, *args)


def reset(text: Union[str, int]) -> str:
    return _stylize(text, colored.attr("reset"))


def red(text: Union[str, int]) -> str:
    return _stylize(text, colored.fg("red"))


def yellow(text: Union[str, int]) -> str:
    return _stylize(text, colored.fg("yellow"))


def green(text: Union[str, int]) -> str:
    return _stylize(text, colored.fg("green"))


def bold(text: Union[str, int]) -> str:
    return _stylize(text, colored.attr("bold"))


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))


def snapshot_style(text: Union[str, int]) -> str:
    return _stylize(text, colored.bg(225) + colored.fg(90))


def snapshot_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, colored.bg(90) + colored.fg(225))


def received_style(text: Union[str, int]) -> str:
    return _stylize(text, colored.bg(195) + colored.fg(23))


def received_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, colored.bg(23) + colored.fg(195))


def context_style(text: Union[str, int]) -> str:
    return _stylize(text, colored.attr("dim"))
