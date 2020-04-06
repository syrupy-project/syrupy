import os
import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Tuple,
)

from github import Github


if TYPE_CHECKING:
    from subprocess import CompletedProcess

OUTPUT_FILE = ".bench.perf.json"


def report_pending(github=None) -> None:
    if not github:
        return


def default_runner(cmd: str) -> "CompletedProcess":
    return subprocess.run(cmd, shell=True, check=True)


def measure_perf(run: Callable[..., Any] = default_runner) -> None:
    run(
        "python -m pyperf timeit '"
        'import pytest; pytest.main(["-qqq"])'
        f"' -o {OUTPUT_FILE}"
    )


def compare_status(head="master") -> Tuple[bool, str]:
    return (True, "benchmark successful")


def report_status(github=None) -> None:
    if not github:
        return


def main(report=False) -> None:
    github = Github(os.environ["GITHUB_TOKEN"]) if report else None
    report_pending(github)
    measure_perf()
    compare_status(github)
    report_status(github)
