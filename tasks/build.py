from invoke import task

from .utils import ctx_run


@task
def install(ctx, upgrade=False):
    """
    Install dependencies and update lock file.
    """
    if upgrade:
        pass
    else:
        ctx_run(ctx, "uv sync --locked --all-extras --dev")


@task
def clean(ctx):
    """
    Remove build files e.g. package, distributable, compiled etc.
    """
    ctx_run(ctx, "rm -rf *.egg-info dist build __pycache__ .pytest_cache artifacts/*")
