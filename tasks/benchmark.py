from invoke import task


@task(help={"report": "Publish report as github status"})
def benchmark(ctx, report=False):
    """
    Run and generate benchmarks for current code
    """
    import benchmarks

    benchmarks.main(report=report)
