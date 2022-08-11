from invoke import task


@task()
def benchmark(ctx, report=False):
    """
    Run and generate benchmarks for current code
    """

    ctx.run(f"pytest benchmarks --benchmark-json=benchmarks.json")
