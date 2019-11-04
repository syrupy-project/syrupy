def red(text):
    return f"\033[31m{text}\033[0m"


def yellow(text):
    return f"\033[33m{text}\033[0m"


def bold(text):
    return f"\033[1m{text}\033[0m"


def error_style(text):
    return bold(red(text))
