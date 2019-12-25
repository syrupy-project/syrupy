from typing import Union


def red(text: Union[str, int]) -> str:
    return f"\033[31m{text}\033[0m"


def yellow(text: Union[str, int]) -> str:
    return f"\033[33m{text}\033[0m"


def green(text: Union[str, int]) -> str:
    return f"\033[32m{text}\033[0m"


def bold(text: Union[str, int]) -> str:
    return f"\033[1m{text}\033[0m"


def error_style(text: Union[str, int]) -> str:
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    return bold(green(text))
