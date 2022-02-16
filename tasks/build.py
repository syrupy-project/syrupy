import os
from datetime import datetime

from invoke import task

from .utils import ctx_run


@task
def requirements(ctx, upgrade=False):
    """
    Build test & dev requirements lock file
    """
    if upgrade:
        ctx_run(ctx, f"poetry update")
    else:
        ctx_run(ctx, f"poetry install")


@task
def clean(ctx):
    """
    Remove build files e.g. package, distributable, compiled etc.
    """
    ctx_run(ctx, "rm -rf *.egg-info dist build __pycache__ .pytest_cache artifacts/*")


def version_scheme(v):
    if v.exact:
        return v.format_with("{tag}")
    return datetime.now().strftime("%Y.%m.%d.%H%M%S%f")


@task(pre=[clean])
def dist(ctx):
    """
    Generate version from scm and build package distributable
    """
    from setuptools_scm import get_version

    version = get_version(version_scheme=version_scheme, local_scheme=lambda _: "")
    ctx_run(ctx, f"poetry version {version}")
    ctx_run(ctx, "poetry build")


@task
def publish(ctx, dry_run=True):
    """
    Upload built package to pypi
    """
    repo_url = "--repository-url https://test.pypi.org/legacy/" if dry_run else ""
    ctx_run(ctx, f"twine upload --skip-existing {repo_url} dist/*")


@task(pre=[dist])
def release(ctx, dry_run=True):
    """
    Build and publish package to pypi index based on scm version
    """
    from semver import parse_version_info

    if not dry_run and not os.environ.get("CI"):
        print("This is a CI only command")
        exit(1)

    version = ctx_run(ctx, "poetry version --short").stdout.strip()

    try:
        should_publish_to_pypi = not dry_run and parse_version_info(version)
    except ValueError:
        should_publish_to_pypi = False

    # publish to test to verify builds
    if dry_run:
        publish(ctx, dry_run=True)

    # publish to pypi if test succeeds
    if should_publish_to_pypi:
        publish(ctx, dry_run=False)
