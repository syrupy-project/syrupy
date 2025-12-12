from invoke import task

from .utils import ctx_run


@task(default=True)
def dev(ctx):
    """
    Install the current development version of syrupy
    """
    ctx_run(ctx, "uv sync --locked --all-extras --dev")
