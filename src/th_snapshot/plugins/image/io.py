from typing import Any
from abc import ABC
import re

import os

from th_snapshot.io import SnapshotIO
from th_snapshot.exceptions import SnapshotDoesNotExist


class AbstractImageSnapshotIO(ABC, SnapshotIO):
    def write(self, data, index: int = 0):
        with open(self.get_filepath(index), "wb") as f:
            f.write(data)

    def read(self, index: int = 0) -> Any:
        try:
            with open(self.get_filepath(index), "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise SnapshotDoesNotExist()

    def get_snapshot_dirname(self) -> str:
        return os.path.basename(str(self.test_location.filename)[: -len(".py")])

    def get_file_basename(self, index: int) -> str:
        ext = f".{self.extension}"
        sanitized_name = self.get_valid_filename(self.get_snapshot_name(index=index))[
            : 255 - len(ext)
        ]
        return f"{sanitized_name}{ext}"

    def get_valid_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", filename)
