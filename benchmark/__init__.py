import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
)


if TYPE_CHECKING:
    from subprocess import CompletedProcess

OUTPUT_FILE = ".bench.perf.json"


def default_runner(cmd: str) -> "CompletedProcess":
    return subprocess.run(cmd, shell=True, check=True)


def measure_perf(run: Callable[..., Any] = default_runner) -> None:
    run(
        "python -m pyperf timeit '"
        'import pytest; pytest.main(["-qqq"])'
        f"' -o {OUTPUT_FILE}"
    )


def report_status() -> None:
    pass
