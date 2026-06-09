"""
Example: Snapshotting PySpark DataFrames as Parquet files

The ``ParquetSnapshotExtension`` writes each snapshot to its own ``.parquet``
file (one file per assertion). A PySpark ``DataFrame`` is collected, its rows are
sorted so the snapshot is deterministic regardless of partitioning, and the data
is stored as Parquet. Comparison happens on the *logical* table contents, so
re-partitioning or row reordering never causes a spurious mismatch.

Run with ``--snapshot-update`` once to generate the ``.parquet`` snapshots, then
normally on subsequent runs to assert against them.

Requires ``pyarrow`` (and ``pyspark`` for the Spark ``DataFrame`` path); both are
skipped automatically if not installed.
"""

import pytest

pytest.importorskip("pyarrow")
pyspark = pytest.importorskip("pyspark")

from pyspark.sql import SparkSession  # noqa: E402

from syrupy.extensions.parquet import ParquetSnapshotExtension  # noqa: E402


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("syrupy-parquet-example")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(ParquetSnapshotExtension)


def test_pyspark_dataframe(spark, snapshot):
    df = spark.createDataFrame(
        [
            (1, "alice", 9.5),
            (2, "bob", 7.0),
            (3, "carol", 8.25),
        ],
        schema=["id", "name", "score"],
    )
    assert df == snapshot


def test_pyspark_dataframe_is_order_independent(spark, snapshot):
    # Spark gives no ordering guarantee; the snapshot still matches because the
    # extension sorts rows into a canonical order before writing/comparing.
    rows = [(2, "bob", 7.0), (3, "carol", 8.25), (1, "alice", 9.5)]
    df = spark.createDataFrame(rows, schema=["id", "name", "score"]).repartition(3)
    assert df == snapshot
