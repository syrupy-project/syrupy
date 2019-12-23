"""
Utility methods for styling terminal output
"""

from typing import Union


def red(text: Union[str, int]) -> str:
    """Apply red styling"""
    return f"\033[31m{text}\033[0m"


def yellow(text: Union[str, int]) -> str:
    """Apply yellow styling"""
    return f"\033[33m{text}\033[0m"


def green(text: Union[str, int]) -> str:
    """Apply green styling"""
    return f"\033[32m{text}\033[0m"


def bold(text: Union[str, int]) -> str:
    """Apply bold styling"""
    return f"\033[1m{text}\033[0m"


def error_style(text: Union[str, int]) -> str:
    """Apply error styling"""
    return bold(red(text))


def warning_style(text: Union[str, int]) -> str:
    """Apply warning styling"""
    return bold(yellow(text))


def success_style(text: Union[str, int]) -> str:
    """Apply success styling"""
    return bold(green(text))
