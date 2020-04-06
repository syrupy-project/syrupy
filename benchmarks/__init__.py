import os
import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Tuple,
)

from github import Github


if TYPE_CHECKING:
    from subprocess import CompletedProcess
    from github.CommitStatus import CommitStatus

BENCH_COMMAND = "pytest -qq"
BENCH_PREF_FILE = ".bench.perf.json"
GH_REPO = "tophat/syrupy"
GH_STATUS_CONTEXT = "ci/benchmark/syrupy"


def report_pending(github=None) -> None:
    if not github:
        return


def default_runner(cmd: str) -> "CompletedProcess":
    return subprocess.run(cmd, shell=True, check=True)


def measure_perf(run: Callable[..., Any] = default_runner) -> None:
    run(f"python -m pyperf command -o {BENCH_PREF_FILE} -- {BENCH_COMMAND}")


def get_branch_status(github, branch) -> Optional["CommitStatus"]:
    head = github.get_repo(GH_REPO).get_branch(branch)
    for status in head.commit.get_statuses():
        if status.context == GH_STATUS_CONTEXT:
            return status
    return None


def compare_status(github, head="master") -> Tuple[bool, str]:
    head_status = get_branch_status(github, head)
    return (True, "benchmark successful")


def report_status(github=None) -> None:
    if not github:
        return
    status = compare_status(github)


def main(report=False) -> None:
    github = Github(os.environ["GITHUB_TOKEN"]) if report else None
    report_pending(github)
    measure_perf()
    report_status(github)
