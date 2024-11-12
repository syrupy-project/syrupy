from invoke import (
    exceptions,
    task,
)

from .utils import ctx_run

lint_commands = {
    "mypy": lambda _: "python -m mypy --strict src benchmarks",
    "ruff": lambda fix: f"python -m ruff check {'--fix' if fix else ''} .",
    "ruff-format": lambda fix: f"python -m ruff format {'' if fix else '--diff'} .",
}


def run_lint(ctx, section, fix):
    print(f"\033[1m[{section}]\033[0m")
    ctx_run(ctx, lint_commands[section](fix))


@task(default=True)
def all(ctx, fix=False):  # noqa: A001
    """
    Check and fix syntax using various linters
    """
    last_error = None
    for section in lint_commands:
        try:
            run_lint(ctx, section, fix)
            print()
        except exceptions.Failure as ex:
            last_error = ex
    if last_error:
        raise last_error


def add_individual_task(name: str):
    @task(name=name)
    def lint(ctx, fix=False):
        run_lint(ctx, name, fix)

    globals()[name] = lint


for section in lint_commands:
    add_individual_task(section)
