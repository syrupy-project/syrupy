from invoke import task

@task
def clean(ctx):
    pass

@task
def requirements(ctx):
    ctx.run(f"python -m piptools compile requirements.in", pty=True)
    ctx.run(f"python -m piptools compile dev-requirements.in", pty=True)

@task
def lint(ctx, fix=False):
    ctx.run(f"black --target-version py36 {'--check' if not fix else ''} ./src ./tests")

@task
def test(ctx, update_snapshots=False):
    ctx.run(f"pytest . {'--update-snapshots' if update_snapshots else ''}", pty=True)
