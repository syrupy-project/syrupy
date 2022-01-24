import importlib
from collections import defaultdict
from gettext import (
    gettext,
    ngettext,
)
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    DefaultDict,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Set,
)

import attr

from .constants import PYTEST_NODE_SEP
from .data import (
    Snapshot,
    SnapshotFossil,
    SnapshotFossils,
    SnapshotUnknownFossil,
)
from .location import PyTestLocation
from .terminal import (
    bold,
    error_style,
    green,
    success_style,
    warning_style,
)

if TYPE_CHECKING:
    import argparse

    import pytest

    from .assertion import SnapshotAssertion


@attr.s
class SnapshotReport:
    """
    This class is responsible for determining the test summary and post execution
    results. It will provide the lines of the report to be printed as well as the
    information used for removal of unused or orphaned snapshots and fossils.
    """

    base_dir: str = attr.ib()
    collected_items: Set["pytest.Item"] = attr.ib()
    selected_items: Dict[str, bool] = attr.ib()
    options: "argparse.Namespace" = attr.ib()
    assertions: List["SnapshotAssertion"] = attr.ib()
    discovered: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    created: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    failed: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    matched: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    updated: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    used: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    _provided_test_paths: Dict[str, List[str]] = attr.ib(factory=dict)
    _keyword_expressions: Set["Expression"] = attr.ib(factory=set)
    _collected_items_by_nodeid: Dict[str, "pytest.Item"] = attr.ib(
        factory=dict, init=False
    )

    @property
    def update_snapshots(self) -> bool:
        return bool(self.options.update_snapshots)

    @property
    def warn_unused_snapshots(self) -> bool:
        return bool(self.options.warn_unused_snapshots)

    @property
    def include_snapshot_details(self) -> bool:
        return bool(self.options.include_snapshot_details)

    def __attrs_post_init__(self) -> None:
        self.__parse_invocation_args()
        self._collected_items_by_nodeid = {
            getattr(item, "nodeid"): item for item in self.collected_items  # noqa: B009
        }

        # We only need to discover snapshots once per test file, not once per assertion.
        locations_discovered: DefaultDict[str, Set[Any]] = defaultdict(set)
        for assertion in self.assertions:
            test_location = assertion.extension.test_location.filepath
            extension_class = assertion.extension.__class__
            if extension_class not in locations_discovered[test_location]:
                locations_discovered[test_location].add(extension_class)
                self.discovered.merge(assertion.extension.discover_snapshots())

            for result in assertion.executions.values():
                snapshot_fossil = SnapshotFossil(location=result.snapshot_location)
                snapshot_fossil.add(
                    Snapshot(name=result.snapshot_name, data=result.final_data)
                )
                self.used.update(snapshot_fossil)
                if result.created:
                    self.created.update(snapshot_fossil)
                elif result.updated:
                    self.updated.update(snapshot_fossil)
                elif result.success:
                    self.matched.update(snapshot_fossil)
                else:
                    self.failed.update(snapshot_fossil)

    def __parse_invocation_args(self) -> None:
        """
        Parse the invocation arguments to extract some information for test selection
        This compiles and saves values from `-k`, `--pyargs` and test dir path

        https://docs.pytest.org/en/stable/reference.html#command-line-flags
        https://docs.pytest.org/en/stable/reference.html#config

        Summary
        -k: is evaluated and used to match against snapshot names when present
        -m: is ignored for now as markers are not matched to snapshot names
        --pyargs: arguments are imported to get their file locations
        [args]: a path provided e.g. tests/test_file.py::TestClass::test_method
        would result in `"tests/test_file.py"` being stored as the location in a
        dictionary with `["TestClass", "test_method"]` being the test node path
        """

        if self.options.keyword:
            self._keyword_expressions.add(Expression.compose(self.options.keyword))
        for file_or_dir in self.options.file_or_dir:
            parts = file_or_dir.split(PYTEST_NODE_SEP)
            package_or_filepath = parts[0].strip()
            filepath = Path(package_or_filepath)
            if self.options.pyargs:
                try:
                    mod = importlib.import_module(package_or_filepath)
                    if mod.__file__ is not None:
                        filepath = Path(mod.__file__)
                except Exception:
                    pass
            filepath_abs = str(
                filepath if filepath.is_absolute() else filepath.absolute()
            )
            self._provided_test_paths[filepath_abs] = parts[1:]

    @property
    def num_created(self) -> int:
        return self._count_snapshots(self.created)

    @property
    def num_failed(self) -> int:
        return self._count_snapshots(self.failed)

    @property
    def num_matched(self) -> int:
        return self._count_snapshots(self.matched)

    @property
    def num_updated(self) -> int:
        return self._count_snapshots(self.updated)

    @property
    def num_unused(self) -> int:
        return self._count_snapshots(self.unused)

    @property
    def selected_all_collected_items(self) -> bool:
        return self._collected_items_by_nodeid.keys() == self.selected_items.keys()

    @property
    def ran_items(self) -> Iterator["pytest.Item"]:
        return (
            self._collected_items_by_nodeid[nodeid]
            for nodeid in self.selected_items
            if self.selected_items[nodeid]
        )

    @property
    def unused(self) -> "SnapshotFossils":
        """
        Iterate over each snapshot that was discovered but never used and compute
        if the snapshot was unused because the test attached to it was never run,
        or if the snapshot is obsolete and therefore is a candidate for removal.

        Summary, if a snapshot was supposed to be run based on the invocation args
        and it was not, then it should be marked as unused otherwise ignored.
        """
        unused_fossils = SnapshotFossils()
        for unused_snapshot_fossil in self._diff_snapshot_fossils(
            self.discovered, self.used
        ):
            snapshot_location = unused_snapshot_fossil.location
            if self._provided_test_paths and not self._ran_items_match_location(
                snapshot_location
            ):
                # Paths/Packages were provided to pytest and the snapshot location does
                # not match any of ran tests therefore ignore this unused snapshot file
                continue

            provided_nodes = self._get_matching_path_nodes(snapshot_location)
            if self.selected_all_collected_items and not any(provided_nodes):
                # All collected tests were run and files were not filtered by ::node
                # therefore the snapshot fossil file at this location can be deleted
                unused_snapshots = {*unused_snapshot_fossil}
                mark_for_removal = snapshot_location not in self.used
            else:
                unused_snapshots = {
                    snapshot
                    for snapshot in unused_snapshot_fossil
                    if self._selected_items_match_name(
                        snapshot_location=snapshot_location, snapshot_name=snapshot.name
                    )
                    and self._provided_nodes_match_name(
                        snapshot_location=snapshot_location,
                        snapshot_name=snapshot.name,
                        provided_nodes=provided_nodes,
                    )
                }
                mark_for_removal = False

            if unused_snapshots:
                marked_unused_snapshot_fossil = SnapshotFossil(
                    location=snapshot_location
                )
                for snapshot in unused_snapshots:
                    marked_unused_snapshot_fossil.add(snapshot)
                unused_fossils.add(marked_unused_snapshot_fossil)
            elif mark_for_removal:
                unused_fossils.add(SnapshotUnknownFossil(location=snapshot_location))
        return unused_fossils

    @property
    def lines(self) -> Iterator[str]:
        """
        These are the lines printed at the end of a test run. Example:
        ```
        2 snaphots passed. 5 snapshots generated. 1 unused snapshot deleted.

        Re-run pytest with --snapshot-update to delete unused snapshots.
        ```
        """
        summary_lines: List[str] = []
        if self.num_failed:
            summary_lines.append(
                ngettext(
                    "{} snapshot failed.",
                    "{} snapshots failed.",
                    self.num_failed,
                ).format(error_style(self.num_failed))
            )
        if self.num_matched:
            summary_lines.append(
                ngettext(
                    "{} snapshot passed.",
                    "{} snapshots passed.",
                    self.num_matched,
                ).format(success_style(self.num_matched))
            )
        if self.num_created:
            summary_lines.append(
                ngettext(
                    "{} snapshot generated.",
                    "{} snapshots generated.",
                    self.num_created,
                ).format(green(self.num_created))
            )
        if self.num_updated:
            summary_lines.append(
                ngettext(
                    "{} snapshot updated.",
                    "{} snapshots updated.",
                    self.num_updated,
                ).format(green(self.num_updated))
            )
        if self.num_unused:
            if self.update_snapshots:
                text_singular = "{} unused snapshot deleted."
                text_plural = "{} unused snapshots deleted."
            else:
                text_singular = "{} snapshot unused."
                text_plural = "{} snapshots unused."
            if self.update_snapshots or self.warn_unused_snapshots:
                text_count = warning_style(self.num_unused)
            else:
                text_count = error_style(self.num_unused)
            summary_lines.append(
                ngettext(text_singular, text_plural, self.num_unused).format(text_count)
            )
        yield " ".join(summary_lines)

        if self.num_unused:
            yield ""
            if self.update_snapshots or self.include_snapshot_details:
                base_message = "Deleted" if self.update_snapshots else "Unused"
                for snapshot_fossil in self.unused:
                    filepath = snapshot_fossil.location
                    snapshots = (snapshot.name for snapshot in snapshot_fossil)
                    path_to_file = str(Path(filepath).relative_to(self.base_dir))
                    unused_snapshots = ", ".join(map(bold, sorted(snapshots)))
                    yield warning_style(gettext(base_message)) + " {} ({})".format(
                        unused_snapshots, path_to_file
                    )
            if not self.update_snapshots:
                message = gettext(
                    "Re-run pytest with --snapshot-update to delete unused snapshots."
                )
                if self.warn_unused_snapshots:
                    yield warning_style(message)
                else:
                    yield error_style(message)

    def _diff_snapshot_fossils(
        self, snapshot_fossils1: "SnapshotFossils", snapshot_fossils2: "SnapshotFossils"
    ) -> "SnapshotFossils":
        """
        Find the difference between two collections of snapshot fossils. While
        preserving the location site to all fossils in the first collections. That is
        a collection with fossil sites {A{1,2}, B{3,4}, C{5,6}} with snapshot fossils
        when diffed with another collection with snapshots {A{1,2}, B{3,4}, D{7,8}}
        will result in a collection with the contents {A{}, B{}, C{5,6}}.
        """
        diffed_snapshot_fossils: "SnapshotFossils" = SnapshotFossils()
        for snapshot_fossil1 in snapshot_fossils1:
            snapshot_fossil2 = snapshot_fossils2.get(
                snapshot_fossil1.location
            ) or SnapshotFossil(location=snapshot_fossil1.location)
            diffed_snapshot_fossil = SnapshotFossil(location=snapshot_fossil1.location)
            for snapshot in snapshot_fossil1:
                if not snapshot_fossil2.get(snapshot.name):
                    diffed_snapshot_fossil.add(snapshot)
            diffed_snapshot_fossils.add(diffed_snapshot_fossil)
        return diffed_snapshot_fossils

    def _count_snapshots(self, snapshot_fossils: "SnapshotFossils") -> int:
        """
        Count all the snapshots at all the locations in the snapshot fossil collection
        """
        return sum(len(snapshot_fossil) for snapshot_fossil in snapshot_fossils)

    def _is_matching_path(self, snapshot_location: str, provided_path: str) -> bool:
        """
        Check if a snapshot location matches the path provided by checking that the
        provided path folder is in a parent position relative to the snapshot location
        """
        path = Path(provided_path)
        return str(path if path.is_dir() else path.parent) in snapshot_location

    def _get_matching_path_nodes(self, snapshot_location: str) -> List[List[str]]:
        """
        For the snapshot location provided, get the nodes of the test paths provided to
        pytest on invocation. If there were no paths provided then this list should be
        empty. If there are paths without nodes provided then this is a list of empties
        """
        return [
            self._provided_test_paths[path]
            for path in self._provided_test_paths
            if self._is_matching_path(snapshot_location, path)
        ]

    def _provided_nodes_match_name(
        self,
        snapshot_location: str,
        snapshot_name: str,
        provided_nodes: List[List[str]],
    ) -> bool:
        """
        Check that a snapshot name matches the node paths provided.
        If no nodes are filtered, provided_nodes is empty, which means
        all nodes should be matched.
        """
        if not provided_nodes:
            return True
        for node_path in provided_nodes:
            if snapshot_name in ".".join(node_path):
                return True
        return False

    def _provided_keywords_match_name(self, snapshot_name: str) -> bool:
        """
        Check that a snapshot name would have been included by the keyword
        expression parsed from the invocation arguments
        """
        names = snapshot_name.split(".")
        return any(
            expr.evaluate(lambda subname: any(subname in name for name in names))
            for expr in self._keyword_expressions
        )

    def _ran_items_match_name(self, snapshot_location: str, snapshot_name: str) -> bool:
        """
        Check that a snapshot name would match a test node using the Pytest location
        """
        for item in self.ran_items:
            location = PyTestLocation(item)
            if location.matches_snapshot_location(
                snapshot_location
            ) and location.matches_snapshot_name(snapshot_name):
                return True
        return False

    def _selected_items_match_name(
        self, snapshot_location: str, snapshot_name: str
    ) -> bool:
        """
        Check that a snapshot name should be treated as selected by the current session
        This being true means that if the snapshot was not used then it will be deleted
        """
        if self._keyword_expressions:
            return self._provided_keywords_match_name(snapshot_name)
        return self._ran_items_match_name(
            snapshot_location=snapshot_location, snapshot_name=snapshot_name
        )

    def _ran_items_match_location(self, snapshot_location: str) -> bool:
        """
        Check if any test run in the current session should match the snapshot location
        This being true means that if no snapshot in the fossil was used then it should
        be discarded as obsolete
        """
        return any(
            PyTestLocation(item).matches_snapshot_location(snapshot_location)
            for item in self.ran_items
        )


@attr.s(frozen=True)
class Expression:
    """
    Dumbed down version of _pytest.mark.expression.Expression not available in < 6.0
    https://github.com/pytest-dev/pytest/blob/6.0.x/src/_pytest/mark/expression.py
    Added for pared down support on older pytest version and because the expression
    module is not public. This only supports inclusion based on simple string matching.
    """

    code: FrozenSet[str] = attr.ib(factory=frozenset)

    def evaluate(self, matcher: Callable[[str], bool]) -> bool:
        return any(map(matcher, self.code))

    @staticmethod
    def compose(value: str) -> "Expression":
        delim = " "
        replace_str = {" or ", " and ", " not ", "(", ")"}
        for r in replace_str:
            value = value.replace(f" {r} ", delim)
        return Expression(code=frozenset(value.split(delim)))
