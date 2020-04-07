import os
import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Tuple,
)

from github import Github  # type: ignore


if TYPE_CHECKING:
    from subprocess import CompletedProcess
    from github.Commit import Commit  # type: ignore
    from github.CommitStatus import CommitStatus  # type: ignore

BENCH_COMMAND = "pytest -qq"
BENCH_PERF_FILE = ".perf.bench.json"
BENCH_REF_FILE = ".ref.bench.json"
GH_BRANCH_REF = "master"
GH_REPO = "tophat/syrupy"
GH_STATUS_CONTEXT = "Syrupy CICD / Benchmark"
GH_STATUS_DESC_DELIM = "\n" * 3


def get_commit(github: "Github") -> "Commit":
    """
    Get current commit the github ci run is for
    """
    github_sha = os.environ.get("GITHUB_SHA")
    return github.get_repo(GH_REPO).get_commit(github_sha) if github_sha else None


def get_branch() -> Optional[str]:
    """
    Get current branch the github ci run is for
    """
    github_ref = os.environ.get("GITHUB_REF")
    return github_ref.replace("refs/heads/", "") if github_ref else None


def get_target_url() -> str:
    """
    Get url to current repo branch
    """
    repo_url = f"https://github.com/{GH_REPO}"
    branch = get_branch()
    return f"{repo_url}/tree/{branch}" if branch else repo_url


def report_pending(github: Optional["Github"] = None) -> None:
    """
    Set the commit benchmark status to pending
    """
    if not github:
        return
    commit = get_commit(github)
    commit.create_status(
        state="pending",
        target_url=get_target_url(),
        description="Running benchmarks",
        context=GH_STATUS_CONTEXT,
    )


def default_runner(cmd: str, **kwargs: Any) -> "CompletedProcess[bytes]":
    """
    Default code runner, interchangeable with invoke context runner
    """
    return subprocess.run(cmd, shell=True, check=True, **kwargs)


def measure_perf(run: Callable[..., Any] = default_runner) -> None:
    """
    Measure benchmark command performance and save results in file
    Also checks that the benchmark run was stable
    """
    run(f"python -m pyperf command -o {BENCH_PERF_FILE} -- {BENCH_COMMAND}")
    run(f"python -m pyperf check {BENCH_PERF_FILE}")


def get_branch_status(github: "Github", branch: str) -> "CommitStatus":
    """
    Get the commit status of a branch for the benchmark context
    """
    head = github.get_repo(GH_REPO).get_branch(branch)
    for status in head.commit.get_statuses():
        if status.context == GH_STATUS_CONTEXT:
            return status
    return None


def parse_status(commit_status: "CommitStatus") -> str:
    """
    Get the benchmark results from a github commit status
    """
    return str(commit_status.description).split(GH_STATUS_DESC_DELIM)[1]


def fetch_bench_ref_json(github: "Github", ref_branch: str = GH_BRANCH_REF) -> bool:
    """
    Retrieve and save the benchmark results on the reference branch
    Skipping the current branch is the reference branch
    """
    if get_branch() == ref_branch:
        return False

    head_status = get_branch_status(github, ref_branch)
    if not head_status:
        return False

    with open(BENCH_REF_FILE, "w") as ref_json_file:
        ref_json_file.write(parse_status(head_status))
    return True


def compare_bench_status(
    perf_file: str = BENCH_PERF_FILE, ref_file: str = BENCH_REF_FILE,
) -> Tuple[str, bool]:
    """
    Compare benchmarks for current branch to reference and return results
    indicating success or failure and the github status description
    """
    cmd = f"python -m pyperf compare_to -q {ref_file} {perf_file}"
    return default_runner(cmd, stdout=subprocess.PIPE).stdout.decode().strip(), True


def get_bench_status(bench_file: str = BENCH_PERF_FILE) -> Tuple[str, bool]:
    """
    Get the status of the benchmark file indicating success or failure
    and the github status description
    """
    cmd = f"python -m pyperf show -q {bench_file}"
    output = default_runner(cmd, stdout=subprocess.PIPE).stdout.decode().strip()
    with open(bench_file, "r") as bench_file_stream:
        bench_file_json = bench_file_stream.read()
        print(bench_file_json)
    return output, True


def report_status(github: Optional["Github"] = None) -> None:
    """
    Report benchmark run results to github as the commit status
    """
    if not github:
        return

    commit = get_commit(github)
    if not commit:
        return

    if fetch_bench_ref_json(github):
        description, success = compare_bench_status()
    else:
        description, success = get_bench_status()

    commit.create_status(
        state="success" if success else "failure",
        target_url=get_target_url(),
        description=description,
        context=GH_STATUS_CONTEXT,
    )


def main(report: bool = False) -> None:
    github = Github(os.environ["GITHUB_TOKEN"]) if report else None
    report_pending(github)
    measure_perf()
    report_status(github)
