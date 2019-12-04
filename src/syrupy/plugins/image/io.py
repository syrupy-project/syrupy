from typing import Any, Set, Optional
from abc import ABC, abstractmethod
import re

import os

from syrupy.io import SnapshotIO
from syrupy.exceptions import SnapshotDoesNotExist
from syrupy.types import SnapshotFiles


class AbstractImageSnapshotIO(ABC, SnapshotIO):
    @property
    @abstractmethod
    def extension(self) -> str:
        pass

    def discover_snapshots(self, filepath: str) -> Set[str]:
        return {os.path.splitext(os.path.basename(filepath))[0]}

    def get_file_basename(self, index: int) -> str:
        maybe_extension = f".{self.extension}" if self.extension else ""
        sanitized_name = self._clean_filename(self.get_snapshot_name(index=index))
        return f"{sanitized_name}{maybe_extension}"

    def _get_snapshot_dirname(self):
        return os.path.splitext(os.path.basename(str(self.test_location.filename)))[0]

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
        max_filename_length = 255 - len(self.extension or "")
        return re.sub(r"(?u)[^-\w.]", "", filename)[:max_filename_length]
