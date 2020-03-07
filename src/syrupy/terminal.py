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


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))


def snapshot_style(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.bg(225) + colored.fg(90))


def snapshot_diff_style(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.bg(90) + colored.fg(225))


def received_style(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.bg(195) + colored.fg(23))


def received_diff_style(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.bg(23) + colored.fg(195))


def context_style(text: Union[str, int]) -> str:
    return colored.stylize(text, colored.attr("dim"))
