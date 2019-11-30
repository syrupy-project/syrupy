from typing import Any, Set
from abc import ABC, abstractmethod
import re

import os

from syrupy.io import SnapshotIO
from syrupy.exceptions import SnapshotDoesNotExist
from syrupy.types import SnapshotFiles


class AbstractImageSnapshotIO(ABC, SnapshotIO):
    @property
    @abstractmethod
    def extension(self):
        return None

    def discover_snapshots(self, index: int = 0) -> SnapshotFiles:
        return {self.get_filepath(index): {self.get_snapshot_name(index)}}

    def discover_snapshots_in_file(self, filepath: str) -> Set[str]:
        return set()

    def get_file_basename(self, index: int) -> str:
        ext = f".{self.extension}"
        sanitized_name = self._clean_filename(self.get_snapshot_name(index=index))[
            : 255 - len(ext)
        ]
        return f"{sanitized_name}{ext}"

    def _get_snapshot_dirname(self):
        return os.path.basename(str(self.test_location.filename)[: -len(".py")])

    def _read_snapshot_from_file(self, snapshot_file: str, _):
        return self._read_file(snapshot_file)

    def _read_file(self, filepath: str) -> Any:
        try:
            with open(filepath, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _write_snapshot_or_remove_file(self, snapshot_file: str, _: str, data: Any):
        if data:
            self._write_file(snapshot_file, data)
        else:
            os.remove(snapshot_file)

    def _write_file(self, filepath: str, data: Any):
        with open(filepath, "wb") as f:
            f.write(data)

    def _clean_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", filename)
