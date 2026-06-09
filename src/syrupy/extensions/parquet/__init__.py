"""Snapshot extension for PySpark DataFrames stored as Parquet files.

Each snapshot is written as a standalone ``.parquet`` file (one file per test
assertion) using the :class:`SingleFileSnapshotExtension` machinery. A PySpark
``DataFrame`` is collected to the driver, canonicalised (rows are sorted so the
snapshot is deterministic regardless of partitioning), and written through
``pyarrow``.

Comparison is performed on the *logical* contents of the Parquet data, not on
the raw bytes. Parquet files embed environment specific metadata such as the
writer version and the physical row-group / compression layout, so two files
with identical data can have different bytes. Reading both sides back into an
``pyarrow.Table`` and comparing those avoids spurious snapshot mismatches.

``pandas.DataFrame`` and ``pyarrow.Table`` inputs are also accepted, which makes
the extension usable (and testable) without a running Spark session.

``pyarrow`` is required at runtime; ``pyspark`` is only required if you pass a
Spark ``DataFrame``. Both are optional dependencies of syrupy:

    pip install "syrupy[parquet]"   # pyarrow only
    pip install "syrupy[pyspark]"   # pyarrow + pyspark
"""

import io
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
    )


def _require_pyarrow() -> tuple[Any, Any]:
    """Import pyarrow lazily so syrupy has no hard dependency on it."""
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            "The Parquet snapshot extension requires 'pyarrow'. "
            'Install it with `pip install pyarrow` or `pip install "syrupy[parquet]"`.'
        ) from exc
    return pa, pq


def _is_spark_dataframe(data: Any) -> bool:
    """Detect a (classic or Spark Connect) PySpark DataFrame without importing it."""
    return any(
        klass.__module__.startswith("pyspark.sql") and klass.__name__ == "DataFrame"
        for klass in type(data).__mro__
    )


class ParquetSnapshotExtension(SingleFileSnapshotExtension):
    """Serialize tabular data (PySpark DataFrames) to ``.parquet`` snapshots."""

    file_extension = "parquet"
    _write_mode = WriteMode.BINARY

    # -- serialization ------------------------------------------------------

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        """Return ``data`` as canonical Parquet bytes.

        ``exclude`` / ``include`` / ``matcher`` are not applied to Parquet
        snapshots; column selection should be done on the DataFrame before it is
        passed to the snapshot assertion.
        """
        _, pq = _require_pyarrow()
        table = self._to_arrow_table(data)
        sink = io.BytesIO()
        pq.write_table(table, sink, compression="snappy")
        return sink.getvalue()

    def _to_arrow_table(self, data: Any) -> Any:
        """Convert supported inputs into a canonical (row-sorted) pyarrow Table."""
        pa, _ = _require_pyarrow()

        if _is_spark_dataframe(data):
            pdf = data.toPandas()
        elif isinstance(data, pa.Table):
            pdf = data.to_pandas()
        else:
            pdf = self._as_pandas(data)

        return pa.Table.from_pandas(self._canonicalize(pdf), preserve_index=False)

    @staticmethod
    def _as_pandas(data: Any) -> Any:
        try:
            import pandas as pd
        except ModuleNotFoundError as exc:  # pragma: no cover - import guard
            raise ModuleNotFoundError(
                "The Parquet snapshot extension requires 'pandas' to serialize "
                "pandas-like data. Install it with `pip install pandas`."
            ) from exc
        if isinstance(data, pd.DataFrame):
            return data.copy()
        raise TypeError(
            "ParquetSnapshotExtension can only serialize a PySpark DataFrame, a "
            "pandas DataFrame or a pyarrow Table, got "
            f"'{type(data).__name__}'."
        )

    @staticmethod
    def _canonicalize(pdf: Any) -> Any:
        """Sort rows deterministically so snapshots are stable across runs.

        Spark does not guarantee row ordering, so we sort by every column. When a
        column holds unsortable values (lists, dicts, structs) we fall back to
        sorting by the string representation of each row.
        """
        if len(pdf.columns) == 0:
            return pdf.reset_index(drop=True)
        try:
            ordered = pdf.sort_values(by=list(pdf.columns), kind="stable")
        except TypeError:
            keys = pdf.astype(str).agg("\x1f".join, axis=1)
            ordered = pdf.iloc[keys.argsort(kind="stable").to_numpy()]
        return ordered.reset_index(drop=True)

    # -- comparison ---------------------------------------------------------

    def matches(
        self,
        *,
        serialized_data: "SerializableData",
        snapshot_data: "SerializableData",
    ) -> bool:
        """Compare the logical Parquet contents rather than the raw bytes."""
        try:
            produced = self._read_table(serialized_data)
            stored = self._read_table(snapshot_data)
        except Exception:  # pragma: no cover - defensive fallback
            return bool(serialized_data == snapshot_data)
        return produced.equals(stored)

    @staticmethod
    def _read_table(content: Any) -> Any:
        _, pq = _require_pyarrow()
        return pq.read_table(io.BytesIO(bytes(content)))

    # -- reporting ----------------------------------------------------------

    def diff_lines(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> "Iterator[str]":
        """Render a human readable diff of the two Parquet payloads."""
        return super().diff_lines(
            self._to_text(serialized_data),
            self._to_text(snapshot_data),
        )

    @classmethod
    def _to_text(cls, content: Any) -> str:
        try:
            table = cls._read_table(content)
        except Exception:  # pragma: no cover - defensive fallback
            return repr(content)
        schema = "\n".join(f"  {field.name}: {field.type}" for field in table.schema)
        body = table.to_pandas().to_string(index=False)
        return f"schema:\n{schema}\n\ndata ({table.num_rows} rows):\n{body}\n"


__all__ = ["ParquetSnapshotExtension"]
