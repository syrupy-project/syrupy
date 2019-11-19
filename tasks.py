from invoke import task


@task
def lint(ctx, fix=False):
    ctx.run(f"black --target-version py36 {'--check' if not fix else ''} ./src ./tests")

@task
def test(ctx, update_snapshots=False):
    ctx.run(f"pytest . {'--update-snapshots' if update_snapshots else ''}", pty=True)
