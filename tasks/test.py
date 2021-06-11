import os
from pathlib import Path

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
):
    """
    Run entire test suite
    """
    flags = {
        "-s -vv": verbose,
        f"-k {test_pattern}": test_pattern,
        "--snapshot-update": update_snapshots,
    }
    coverage_module = "coverage run -m " if coverage else ""
    test_flags = " ".join(flag for flag, enabled in flags.items() if enabled)
    ctx_run(ctx, f"python -m {coverage_module}pytest {test_flags} .")

    CI = os.environ.get("CI")
    ARTIFACT_DIR = os.environ.get("ARTIFACT_DIR", "./artifacts")
    if coverage:
        if CI:
            coverage_path = Path(ARTIFACT_DIR, "coverage.xml").absolute()
            ctx_run(ctx, f"coverage xml -o {coverage_path}")
        else:
            ctx_run(ctx, "coverage report")
