import os
import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
)

from github import Github  # type: ignore


if TYPE_CHECKING:
    from subprocess import CompletedProcess
    from github.Commit import Commit  # type: ignore
    from github.CommitStatus import CommitStatus  # type: ignore

BENCH_COMMAND = "pytest -qq"
BENCH_PERF_FILE = ".perf.bench.json"
BENCH_REF_FILE = ".ref.bench.json"
GH_REPO = "tophat/syrupy"
GH_STATUS_CONTEXT = "ci/benchmark/syrupy"
GH_STATUS_DESC_DELIM = "\n" * 3


def report_pending(github: Optional["Github"] = None) -> None:
    if not github:
        return


def default_runner(cmd: str) -> "CompletedProcess[bytes]":
    return subprocess.run(cmd, shell=True, check=True)


def measure_perf(run: Callable[..., Any] = default_runner) -> None:
    run(f"python -m pyperf command -o {BENCH_PERF_FILE} -- {BENCH_COMMAND}")
    run(f"python -m pyperf check {BENCH_PERF_FILE}")


def get_commit(github: "Github") -> "Commit":
    github_sha = os.environ.get("GITHUB_SHA")
    return github.get_repo(GH_REPO).get_commit(github_sha) if github_sha else None


def get_branch_status(github: "Github", branch: str) -> "CommitStatus":
    head = github.get_repo(GH_REPO).get_branch(branch)
    for status in head.commit.get_statuses():
        if status.context == GH_STATUS_CONTEXT:
            return status
    return None


def parse_status(commit_status: "CommitStatus") -> str:
    return str(commit_status.description).split(GH_STATUS_DESC_DELIM)[1]


def fetch_bench_ref_json(github: "Github", head: str = "master") -> bool:
    head_status = get_branch_status(github, head)
    if not head_status:
        return False
    with open(BENCH_REF_FILE, "w") as ref_json_file:
        ref_json_file.write(parse_status(head_status))
    return True


def compare_status(
    run: Callable[..., Any] = default_runner,
    *,
    perf_file: str = BENCH_PERF_FILE,
    ref_file: Optional[str] = BENCH_REF_FILE,
) -> None:
    run(f"python -m perf compare_to {ref_file} {perf_file}")


def report_status(github: Optional["Github"] = None) -> None:
    if not github:
        return
    commit = get_commit(github)
    if not commit:
        return
    if fetch_bench_ref_json(github):
        compare_status()
    else:
        compare_status(ref_file=None)


def main(report: bool = False) -> None:
    github = Github(os.environ["GITHUB_TOKEN"]) if report else None
    report_pending(github)
    measure_perf()
    report_status(github)
