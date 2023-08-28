from dataclasses import dataclass
from typing import Union

from .constants import DISABLE_COLOR_ENV_VARS
from .utils import get_env_value


def _is_color_disabled() -> bool:
    return any(map(get_env_value, DISABLE_COLOR_ENV_VARS))


@dataclass
class TerminalCodes:
    ESC: str = "\x1b["
    END: str = "m"
    FOREGROUND_256: str = f"{ESC}38;5;"
    BACKGROUND_256: str = f"{ESC}48;5;"

    STYLES = {
        "bold": "1",
        "dim": "2",
        "italic": "3",
        "underline": "4",
        "reset": "0",
    }

    COLORS = {
        "black": "0",
        "red": "1",
        "green": "2",
        "yellow": "3",
    }


def _attr(style: str) -> str:
    if _is_color_disabled():
        return ""
    return f"{TerminalCodes.ESC}{TerminalCodes.STYLES[style]}{TerminalCodes.END}"


def _fg(color: Union[int, str]) -> str:
    if _is_color_disabled():
        return ""
    color_code = TerminalCodes.COLORS[color] if isinstance(color, (str,)) else color
    return f"{TerminalCodes.FOREGROUND_256}{str(color_code)}{TerminalCodes.END}"


def _bg(color: int) -> str:
    if _is_color_disabled():
        return ""
    return f"{TerminalCodes.BACKGROUND_256}{str(color)}{TerminalCodes.END}"


def _stylize(text: Union[str, int], formatting: str) -> str:
    if _is_color_disabled():
        return str(text)
    return f"{formatting}{text}{_attr('reset')}"


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
