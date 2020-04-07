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

BENCH_COMMAND = "pytest -qq"
BENCH_PERF_FILE = ".perf.bench.json"
BENCH_REF_FILE = ".ref.bench.json"
GH_BENCH_FILE_PATH = "runs"
GH_BENCH_BRANCH = "benchmarks"
GH_BRANCH_REF = "master"
GH_REPO = "tophat/syrupy"
GH_STATUS_CONTEXT = "Syrupy CICD / Benchmark"
GH_STATUS_DESC_DELIM = "\n" * 3


def get_req_env(var_name: str) -> str:
    """
    Try to get environment variable and exits if not available
    """
    try:
        return os.environ[var_name]
    except KeyError:
        print(f"Missing required environment variable '{var_name}'.")
        exit(1)


def get_commit(github: "Github") -> "Commit":
    """
    Get current commit the github ci run is for
    """
    github_sha = get_req_env("GITHUB_SHA")
    return github.get_repo(GH_REPO).get_commit(github_sha)


def get_branch() -> Optional[str]:
    """
    Get current branch the github ci run is for
    """
    github_ref = get_req_env("GITHUB_REF")
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


def get_commit_bench_path(commit_sha: str) -> str:
    return f"{GH_BENCH_FILE_PATH}/{commit_sha}.json"


def measure_perf(github: "Github", run: Callable[..., Any] = default_runner) -> None:
    """
    Measure benchmark command performance and save results in file
    Checks that the benchmark run was stable
    Saves the benchmark results to github
    """
    run(f"python -m pyperf command -o {BENCH_PERF_FILE} -- {BENCH_COMMAND}")
    run(f"python -m pyperf check {BENCH_PERF_FILE}")
    if not github:
        return
    repo = github.get_repo(GH_REPO)
    commit_sha = get_commit(github).sha
    with open(BENCH_PERF_FILE, "r") as bench_file:
        repo.create_file(
            path=get_commit_bench_path(commit_sha),
            message=f"build: benchmark run {commit_sha[:7]}",
            content=bench_file.read(),
            branch=GH_BENCH_BRANCH,
        )


def fetch_branch_bench_json(github: "Github", branch: str) -> Optional[str]:
    """
    Retrieve the benchmark results for the head commit of the given branch
    """
    repo = github.get_repo(GH_REPO)
    commit_sha = repo.get_branch(branch).commit.sha
    commit_bench_path = get_commit_bench_path(commit_sha)
    try:
        return str(repo.get_contents(commit_bench_path, commit_sha).content)
    except github.GithubException.UnknownObjectException:
        return None


def fetch_ref_bench_json(github: "Github", ref_branch: str = GH_BRANCH_REF) -> bool:
    """
    Retrieve and save the benchmark results on the reference branch
    Skipping the current branch is the reference branch
    """
    if get_branch() == ref_branch:
        return False

    ref_json = fetch_branch_bench_json(github, ref_branch)
    if not ref_json:
        return False

    with open(BENCH_REF_FILE, "w") as ref_json_file:
        ref_json_file.write(ref_json)
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
    return default_runner(cmd, stdout=subprocess.PIPE).stdout.decode().strip(), True


def report_status(github: Optional["Github"] = None) -> None:
    """
    Report benchmark run results to github as the commit status
    """
    if not github:
        return

    commit = get_commit(github)
    if not commit:
        return

    if fetch_ref_bench_json(github):
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
    github = Github(get_req_env("GH_TOKEN")) if report else None
    report_pending(github)
    measure_perf(github)
    report_status(github)
