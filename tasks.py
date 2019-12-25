import os

import semver
from invoke import (
    exceptions,
    task,
)


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
    input_files = ["requirements.in", "dev-requirements.in"]
    for input_file in input_files:
        ctx.run(f"python -m piptools compile {input_file}", pty=True)


@task
def lint(ctx, fix=False):
    """
    Check and fix syntax
    """
    lint_commands = {
        "isort": f"python -m isort {'' if fix else '--check-only --diff'} -y",
        "black": f"python -m black {'' if fix else '--check'} .",
        "flake8": "python -m flake8 src tests *.py",
        "mypy": "python -m mypy --strict src",
    }
    last_error = None
    for section, command in lint_commands.items():
        print(f"\033[1m[{section}]\033[0m")
        try:
            ctx.run(command, pty=True)
        except exceptions.Failure as ex:
            if not fix:
                raise
            last_error = ex
        print()
    if last_error:
        raise last_error


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
        "test-pattern": "Pattern used to select test files to run",
        "update-snapshots": "Create, update or delete snapshot files",
        "verbose": "Verbose output e.g. non captured logs etc.",
    }
)
def test(
    ctx,
    coverage=False,
    dev=False,
    test_pattern=None,
    update_snapshots=False,
    verbose=False,
):
    """
    Run entire test suite
    """
    env = {"PYTHONPATH": "./src"} if dev else {}
    flags = {
        "-s -vv": verbose,
        f"-k {test_pattern}": test_pattern,
        "--snapshot-update": update_snapshots,
    }
    coverage_module = "coverage run -m " if coverage else ""
    test_flags = " ".join(flag for flag, enabled in flags.items() if enabled)
    ctx.run(f"python -m {coverage_module}pytest {test_flags} .", env=env, pty=True)
    if coverage:
        if not os.environ.get("CI"):
            ctx.run("coverage report", pty=True)
        else:
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
    repo_url = "--repository-url https://test.pypi.org/legacy/" if dry_run else ""
    ctx.run(f"twine upload {repo_url} dist/*")


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
