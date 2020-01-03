from typing import Union

import colored


def reset(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.attr("reset"))


def red(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.fg("red"))


def yellow(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.fg("yellow"))


def green(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.fg("green"))


def bold(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.attr("bold"))


def mute(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.attr("dim"))


def emphasize(text: Union[str, int]) -> str:
    return colored.stylize(bold(text), colored.attr("underlined"))


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))
