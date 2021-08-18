import os

from invoke import task

from .utils import ctx_run


@task(
    help={
        "coverage": "Build and report on test coverage",
        "test-pattern": "Pattern used to select test files to run",
        "update-snapshots": "Create, update or delete snapshot files",
        "verbose": "Verbose output e.g. non captured logs etc.",
    }
)
def test(
    ctx,
    coverage=False,
    test_pattern=None,
    update_snapshots=False,
    verbose=False,
    debug=False,
):
    """
    Run entire test suite
    """
    flags = {
        "-s -vv": verbose,
        f"-k {test_pattern}": test_pattern,
        "--snapshot-update": update_snapshots,
        "--pdb": debug,
    }
    coverage_module = "coverage run -m " if coverage else ""
    test_flags = " ".join(flag for flag, enabled in flags.items() if enabled)
    ctx_run(ctx, f"python -m {coverage_module}pytest {test_flags} .")
    if coverage:
        if not os.environ.get("CI") or not os.environ.get("CODECOV_TOKEN"):
            ctx_run(ctx, "coverage report")
        else:
            ctx_run(ctx, "codecov")
