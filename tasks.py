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
