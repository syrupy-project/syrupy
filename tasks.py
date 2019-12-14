import os

import semver
from invoke import task


@task
def clean(ctx):
    """
    Remove build files e.g. package, distributable, compiled etc.
    """
    ctx.run(f"rm -rf *.egg-info dist build __pycache__ .pytest_cache artifacts/*")


@task
def requirements(ctx):
    """
    Build requirements lock file
    """
    ctx.run(f"python -m piptools compile dev-requirements.in", pty=True)


@task
def lint(ctx, fix=False):
    """
    Check and fix syntax
    """
    lint_commands = {
        "mypy": "python -m mypy --strict src",
        "isort": f"python -m isort {'' if fix else '--check-only --diff'} -y",
        "black": f"python -m black {'' if fix else '--check'} .",
    }

    for section, command in lint_commands.items():
        print(f"\033[1m{section}\033[0m")
        ctx.run(command, pty=True)
        print()


@task
def install(ctx):
    """
    Install the current development version of syrupy
    """
    ctx.run("python -m pip install -U .", pty=True)


@task(
    help={
        "coverage": "Build and report on test coverage",
        "dev": "Use syrupy development version",
        "update-snapshots": "Create, update or delete snapshot files",
        "verbose": "Verbose output e.g. non captured logs etc.",
    }
)
def test(ctx, coverage=False, dev=False, update_snapshots=False, verbose=False):
    """
    Run entire test suite
    """
    env = {"PYTHONPATH": "./src"} if dev else {}
    flags = {
        "-s": verbose,
        "--cov=./src": coverage,
        "--snapshot-update": update_snapshots,
    }
    test_flags = " ".join(flag for flag, enabled in flags.items() if enabled)
    ctx.run(f"python -m pytest {test_flags} .", env=env, pty=True)
    if coverage:
        ctx.run("codecov", pty=True)


@task(pre=[clean])
def build(ctx):
    """
    Generate version from scm and build package distributable
    """
    ctx.run("python setup.py sdist bdist_wheel")


@task
def publish(ctx, dry_run=True):
    """
    Upload built package to pypi
    """
    ctx.run(
        f"twine upload {'--repository-url https://test.pypi.org/legacy/' if dry_run else ''} dist/*"
    )


@task(pre=[build])
def release(ctx, dry_run=True):
    """
    Build and publish package to pypi index based on scm version
    """
    if not dry_run and not os.environ.get("CI"):
        print("This is a CI only command")
        exit(1)

    # get version created in build
    with open("version.txt", "r") as f:
        version = str(f.read())

    try:
        should_publish_to_pypi = not dry_run and semver.parse_version_info(version)
    except ValueError:
        should_publish_to_pypi = False

    # publish to test to verify builds
    publish(ctx, dry_run=True)

    # publish to pypi if test succeeds
    if should_publish_to_pypi:
        publish(ctx, dry_run=False)
