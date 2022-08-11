# type: ignore
import shutil
from pathlib import Path


def test_1000x_reads(testdir, benchmark):
    test_contents = """
        import pytest

        @pytest.mark.parametrize("x", range(1000))
        def test_performance(x, snapshot):
            assert x == snapshot
        """
    testdir.makepyfile(test=test_contents)

    # This test benchmarks reads not writes, so we'll pre-write the snapshots.
    testdir.runpytest("test.py", "--snapshot-update")

    # Run benchmark
    benchmark(lambda: testdir.runpytest("test.py"))


def test_1000x_writes(testdir, benchmark):
    test_contents = """
        import pytest

        @pytest.mark.parametrize("x", range(1000))
        def test_performance(x, snapshot):
            assert x == snapshot
        """

    def fn():
        test_path = testdir.makepyfile(test=test_contents)
        testdir.runpytest("test.py", "--snapshot-update")
        shutil.rmtree(Path(test_path).parent / "__snapshots__", ignore_errors=True)

    # Run benchmark
    benchmark(fn)
