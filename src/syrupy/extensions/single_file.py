from enum import StrEnum
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
)
from unicodedata import category

from syrupy.constants import TEXT_ENCODING
from syrupy.data import (
    Snapshot,
    SnapshotCollection,
)
from syrupy.exceptions import TaintedSnapshotError
from syrupy.extensions.amber.serializer import AmberDataSerializer
from syrupy.location import PyTestLocation
from syrupy.types import PropertyFilter, PropertyMatcher, SerializableData

from .base import AbstractSyrupyExtension

if TYPE_CHECKING:
    from syrupy.types import (
        SerializedData,
        SnapshotIndex,
    )


class WriteMode(StrEnum):
    BINARY = "b"
    TEXT = "t"


class SingleFileSnapshotExtension(AbstractSyrupyExtension):
    _text_encoding = TEXT_ENCODING
    _write_mode = WriteMode.BINARY
    file_extension = "raw"
    write_immediately = True

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: PropertyFilter | None = None,
        include: PropertyFilter | None = None,
        matcher: PropertyMatcher | None = None,
    ) -> "SerializedData":
        supported_dataclass = self.get_supported_dataclass()
        if supported_dataclass is bytes:
            try:
                memoryview(data)
            except TypeError:
                raise TypeError(
                    gettext(
                        "Can't serialize '{}' to '{}'. You must convert the data first."
                    ).format(type(data).__name__, supported_dataclass.__name__)
                ) from None
        return supported_dataclass(data)

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex" = 0
    ) -> str:
        return cls.__clean_filename(
            AbstractSyrupyExtension.get_snapshot_name(
                test_location=test_location, index=index
            )
        )

    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: set[str]
    ) -> None:
        Path(snapshot_location).unlink()

    @classmethod
    def get_file_basename(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        return cls.get_snapshot_name(test_location=test_location, index=index)

    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        original_dirname = AbstractSyrupyExtension.dirname(test_location=test_location)
        return str(Path(original_dirname).joinpath(test_location.basename))

    @classmethod
    def discovery_dirname(cls, *, test_location: "PyTestLocation") -> str:
        dirname = cls.dirname(test_location=test_location)
        if Path(dirname).name != test_location.basename:
            # Layouts that do not nest collections under the test file's
            # basename keep file-scoped discovery.
            return dirname
        return str(Path(dirname).parent)

    def is_snapshot_location(self, *, location: str) -> bool:
        """
        Match this extension's snapshot files.

        ``str.endswith("")`` is true for every path, so an empty
        ``file_extension`` would otherwise claim every nested single-file
        snapshot during directory-scoped discovery (including ``.json``,
        ``.raw``, images, etc.) and treat them as unused.
        """
        if self.file_extension:
            return super().is_snapshot_location(location=location)
        name = Path(location).name
        return not any(
            name.endswith(f".{ext}") for ext in self._concrete_file_extensions()
        )

    @classmethod
    def _concrete_file_extensions(cls) -> frozenset[str]:
        # Import built-ins so they count even when this session never used them.
        from syrupy.extensions.image import (  # noqa: F401
            PNGImageSnapshotExtension,
            SVGImageSnapshotExtension,
        )
        from syrupy.extensions.json import JSONSnapshotExtension  # noqa: F401

        extensions: set[str] = set()
        if SingleFileSnapshotExtension.file_extension:
            extensions.add(SingleFileSnapshotExtension.file_extension)
        stack: list[type[SingleFileSnapshotExtension]] = list(
            SingleFileSnapshotExtension.__subclasses__()
        )
        while stack:
            sub = stack.pop()
            stack.extend(sub.__subclasses__())
            if sub.file_extension:
                extensions.add(sub.file_extension)
        return frozenset(extensions)

    def owns_snapshot_collection(
        self, *, filepath: str, test_location: "PyTestLocation"
    ) -> bool:
        if not self.is_snapshot_location(location=filepath):
            return False
        dirname = Path(self.dirname(test_location=test_location))
        if Path(self.discovery_dirname(test_location=test_location)) == dirname:
            # File-scoped discovery (custom layouts): claim matching files
            # anywhere under the collection directory, as before.
            return True
        # Directory-scoped discovery covers the shared snapshot directory;
        # this extension's collections are the files nested one level inside
        # it, e.g. ``__snapshots__/test_file/test_case.json``.
        return Path(filepath).parent.parent == Path(
            self.discovery_dirname(test_location=test_location)
        )

    def read_snapshot_collection(
        self, *, snapshot_location: str
    ) -> "SnapshotCollection":
        file_ext_len = len(self.file_extension) + 1 if self.file_extension else 0
        filename_wo_ext = (
            snapshot_location[:-file_ext_len] if file_ext_len else snapshot_location
        )
        basename = Path(filename_wo_ext).parts[-1]

        snapshot_collection = SnapshotCollection(location=snapshot_location)
        snapshot_collection.add(Snapshot(name=basename))
        return snapshot_collection

    def read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> SerializableData | None:
        try:
            with open(
                snapshot_location,
                f"r{self._write_mode}",
                encoding=self.get_write_encoding(),
            ) as f:
                return f.read()
        except FileNotFoundError:
            return None

    @classmethod
    def get_supported_dataclass(cls) -> type[str] | type[bytes]:
        if cls._write_mode == WriteMode.TEXT:
            return str
        return bytes

    @classmethod
    def get_write_encoding(cls) -> str | None:
        if cls._write_mode == WriteMode.TEXT:
            return TEXT_ENCODING
        return None

    @classmethod
    def write_snapshot_collection(
        cls,
        *,
        snapshot_collection: "SnapshotCollection",
        name_order: dict[str, int] | None = None,
    ) -> None:
        filepath, data = (
            snapshot_collection.location,
            next(iter(snapshot_collection)).data,
        )
        if not isinstance(data, cls.get_supported_dataclass()):
            error_text = gettext(
                "Can't write non supported data. Expected '{}', got '{}'"
            )
            raise TypeError(
                error_text.format(
                    cls.get_supported_dataclass().__name__, type(data).__name__
                )
            )
        with open(
            filepath, f"w{cls._write_mode}", encoding=cls.get_write_encoding()
        ) as f:
            f.write(data)

    @classmethod
    def matches_test_location(
        cls, *, test_location: "PyTestLocation", snapshot_location: str
    ) -> bool:
        """
        Match a single-file snapshot, including one truncated to 255 characters.

        ``PyTestLocation`` requires the filename to start with the full
        parametrized id. A long id is stored as a prefix of that id, so the
        generic check never claims the file and unused-snapshot cleanup can
        delete it.
        """
        if test_location.matches_snapshot_location(snapshot_location):
            return True
        loc = Path(snapshot_location)
        if not test_location.is_item_parametrized:
            return False
        if test_location.basename != loc.parent.name:
            return False
        if not test_location.matches_snapshot_site(snapshot_location):
            return False
        stem = cls._snapshot_stem(loc.name)
        if stem is None:
            return False
        sanitized = cls._sanitize_filename(test_location.snapshot_name_parametrized)
        max_stem = cls._max_stem_length()
        # Exact budget-length prefix only. ``test[a]`` must not claim the
        # snapshot for ``test[aaa...]`` just because one id starts the other.
        if max_stem <= 0 or len(sanitized) <= max_stem:
            return False
        return stem == sanitized[:max_stem]

    @classmethod
    def _snapshot_suffix(cls) -> str:
        if not cls.file_extension:
            return ""
        return f".{cls.file_extension}"

    @classmethod
    def _max_stem_length(cls) -> int:
        return 255 - len(cls._snapshot_suffix())

    @classmethod
    def _snapshot_stem(cls, filename: str) -> str | None:
        suffix = cls._snapshot_suffix()
        if not suffix:
            return filename
        if not filename.endswith(suffix):
            return None
        return filename[: -len(suffix)]

    @classmethod
    def _sanitize_filename(cls, filename: str) -> str:
        exclude_chars = '\\/?*:|"<>'
        exclude_categ = ("C",)
        return "".join(
            c
            for c in filename
            if c not in exclude_chars
            and not any(categ in category(c) for categ in exclude_categ)
        )

    @classmethod
    def __clean_filename(cls, filename: str) -> str:
        return cls._sanitize_filename(filename)[: cls._max_stem_length()]


class SingleFileAmberSnapshotExtension(SingleFileSnapshotExtension):
    file_extension = "ambr"
    _write_mode = WriteMode.TEXT

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: PropertyFilter | None = None,
        include: PropertyFilter | None = None,
        matcher: PropertyMatcher | None = None,
    ) -> "SerializedData":
        return AmberDataSerializer.serialize(
            data, exclude=exclude, include=include, matcher=matcher
        )

    def read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> SerializableData | None:
        snapshot_collection = AmberDataSerializer.read_file(snapshot_location)
        if not snapshot_collection or not snapshot_collection.has_snapshots:
            return None

        snapshot = next(iter(snapshot_collection), None)
        if not snapshot:
            return None

        if snapshot_collection.tainted or snapshot.tainted:
            raise TaintedSnapshotError(snapshot_data=snapshot.data)

        return snapshot.data

    @classmethod
    def write_snapshot_collection(
        cls,
        *,
        snapshot_collection: "SnapshotCollection",
        name_order: dict[str, int] | None = None,
    ) -> None:
        AmberDataSerializer.write_file(snapshot_collection, merge=False)
