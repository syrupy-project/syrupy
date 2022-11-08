from typing import (
    Any,
    Union,
)

import colored

from .constants import DISABLE_COLOR_ENV_VARS
from .utils import get_env_value


def _is_color_disabled() -> bool:
    return any(map(get_env_value, DISABLE_COLOR_ENV_VARS))


def _attr(color: Any) -> str:
    if _is_color_disabled():
        return ""
    return colored.attr(color)


def _fg(color: Any) -> str:
    if _is_color_disabled():
        return ""
    return colored.fg(color)


def _bg(color: Any) -> str:
    if _is_color_disabled():
        return ""
    return colored.bg(color)


def _stylize(text: Union[str, int], *args: Any) -> str:
    if _is_color_disabled():
        return str(text)
    return colored.stylize(text, *args)


def reset(text: Union[str, int]) -> str:
    return _stylize(text, _attr("reset"))


def red(text: Union[str, int]) -> str:
    return _stylize(text, _fg("red"))


def yellow(text: Union[str, int]) -> str:
    return _stylize(text, _fg("yellow"))


def green(text: Union[str, int]) -> str:
    return _stylize(text, _fg("green"))


def bold(text: Union[str, int]) -> str:
    return _stylize(text, _attr("bold"))


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))


def snapshot_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(225) + _fg(90))


def snapshot_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(90) + _fg(225))


def received_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(195) + _fg(23))


def received_diff_style(text: Union[str, int]) -> str:
    return _stylize(text, _bg(23) + _fg(195))


def context_style(text: Union[str, int]) -> str:
    return _stylize(text, _attr("dim"))
