import os

import semver
from invoke import task


@task
def clean(ctx):
    ctx.run(f"rm -rf *.egg-info dist build __pycache__ .pytest_cache artifacts/*")


@task
def requirements(ctx):
    ctx.run(f"python -m piptools compile dev-requirements.in", pty=True)


@task
def lint(ctx, fix=False):
    ctx.run(
        f"python -m black --target-version py36 {'--check' if not fix else ''} ./*.py ./src ./tests",
        pty=True,
    )

    if fix:
        print("\nSkipping type check as there is no fixer")
    else:
        print("\nRunning type check")
        ctx.run("python -m mypy --ignore-missing-imports src", pty=True)


@task
def test(ctx, update_snapshots=False, verbose=False):
    ctx.run(
        "python -m pytest ."
        f"{' -s' if verbose else ''}"
        f"{' --update-snapshots' if update_snapshots else ''}",
        env={"PYTHONPATH": "./src"},
        pty=True,
    )


@task(pre=[clean])
def build(ctx):
    ctx.run("python setup.py sdist bdist_wheel")


@task
def publish(ctx, dry_run=True):
    ctx.run(
        f"twine upload {'--repository-url https://test.pypi.org/legacy/' if dry_run else ''} dist/*"
    )


@task(pre=[build])
def release(ctx, dry_run=True):
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
