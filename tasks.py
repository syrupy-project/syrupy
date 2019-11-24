import os

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
        f"python -m black --target-version py36 {'--check' if not fix else ''} ./*.py ./src ./tests"
    )


@task
def test(ctx, update_snapshots=False):
    ctx.run(
        f"python -m pytest . {'--update-snapshots' if update_snapshots else ''}",
        pty=True,
    )


@task
def build(ctx):
    ctx.run("python setup.py sdist bdist_wheel")


@task
def publish(ctx, dry_run=True):
    # ctx.run(f"twine upload {'--repository-url https://test.pypi.org/legacy/' if dry_run else ''} dist/*")
    pass


@task(pre=[clean, build])
def release(ctx, dry_run=True):
    if not dry_run and not os.environ.get("CI"):
        ctx.run("This is a CI only command")
        return

    # get version
    with open("version.txt", "r") as f:
        version = str(f.read())

    should_release_to_prod = (
        not dry_run
        and semver.parse_version_info(version)
    )

    # publish to test for dry run
    publish(ctx, dry_run=True)

    # publish to prod if test succeeds
    if should_release_to_prod:
        publish(ctx, dry_run=False)
