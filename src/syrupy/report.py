from gettext import (
    gettext,
    ngettext,
)
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
)

import attr
from _pytest.mark.expression import Expression

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
    import pytest

    from .assertion import SnapshotAssertion


@attr.s
class SnapshotReport:
    base_dir: str = attr.ib()
    all_items: Dict["pytest.Item", bool] = attr.ib()
    ran_items: Dict["pytest.Item", bool] = attr.ib()
    update_snapshots: bool = attr.ib()
    warn_unused_snapshots: bool = attr.ib()
    assertions: List["SnapshotAssertion"] = attr.ib()
    discovered: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    created: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    failed: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    matched: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    updated: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    used: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    _invocation_args: Tuple[str, ...] = attr.ib(factory=tuple)
    _provided_test_paths: Dict[str, List[str]] = attr.ib(factory=dict)
    _keyword_expressions: Set["Expression"] = attr.ib(factory=set)

    def __attrs_post_init__(self) -> None:
        self.__parse_invocation_args()
        for assertion in self.assertions:
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
        arg_groups: List[Tuple[Optional[str], str]] = []
        path_as_package = False
        maybe_opt_arg = None
        for arg in self._invocation_args:
            if arg.strip() == "--pyargs":
                path_as_package = True
            elif arg.startswith("-"):
                if "=" in arg:
                    arg0, arg1 = arg.split("=")
                    arg_groups.append((arg0.strip(), arg1.strip()))
                elif maybe_opt_arg is None:
                    maybe_opt_arg = arg
                    continue  # do not reset maybe_opt_arg
            else:
                arg_groups.append((maybe_opt_arg, arg.strip()))

            maybe_opt_arg = None

        for maybe_opt_arg, arg_value in arg_groups:
            if maybe_opt_arg == "-k":  # or maybe_opt_arg == "-m":
                self._keyword_expressions.add(Expression.compile(arg_value))
            elif maybe_opt_arg is None:
                import importlib

                parts = arg_value.split(PYTEST_NODE_SEP)
                package_or_filepath = parts[0].strip()
                filepath = Path(
                    importlib.import_module(package_or_filepath).__file__
                    if path_as_package
                    else package_or_filepath
                )
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
    def ran_all_collected_tests(self) -> bool:
        return self.all_items == self.ran_items

    @property
    def unused(self) -> "SnapshotFossils":
        unused_fossils = SnapshotFossils()
        for unused_snapshot_fossil in self._diff_snapshot_fossils(
            self.discovered, self.used
        ):
            snapshot_location = unused_snapshot_fossil.location
            if self._provided_test_paths and not self._selected_items_match_location(
                snapshot_location
            ):
                # Paths/Packages were provided to pytest and the snapshot location
                # does not match therefore ignore this unused snapshot fossil file
                continue

            provided_nodes = self._get_matching_path_nodes(snapshot_location)
            if self.ran_all_collected_tests and not any(provided_nodes):
                # All collected tests were run and files were not filtered by ::node
                # therefore the snapshot fossil file at this location can be deleted
                unused_snapshots = {*unused_snapshot_fossil}
                mark_for_removal = snapshot_location not in self.used
            else:
                unused_snapshots = {
                    snapshot
                    for snapshot in unused_snapshot_fossil
                    if self._selected_items_match_name(snapshot.name)
                    or self._provided_nodes_match_name(snapshot.name, provided_nodes)
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
            if self.update_snapshots:
                for snapshot_fossil in self.unused:
                    filepath = snapshot_fossil.location
                    snapshots = (snapshot.name for snapshot in snapshot_fossil)
                    path_to_file = str(Path(filepath).relative_to(self.base_dir))
                    deleted_snapshots = ", ".join(map(bold, sorted(snapshots)))
                    yield warning_style(gettext("Deleted")) + " {} ({})".format(
                        deleted_snapshots, path_to_file
                    )
            else:
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
        return sum(len(snapshot_fossil) for snapshot_fossil in snapshot_fossils)

    def _is_matching_path(self, snapshot_location: str, provided_path: str) -> bool:
        path = Path(provided_path)
        return str(path if path.is_dir() else path.parent) in snapshot_location

    def _get_matching_path_nodes(self, snapshot_location: str) -> List[List[str]]:
        return [
            self._provided_test_paths[path]
            for path in self._provided_test_paths
            if self._is_matching_path(snapshot_location, path)
        ]

    def _provided_nodes_match_name(
        self, snapshot_name: str, provided_nodes: List[List[str]]
    ) -> bool:
        return any(snapshot_name in ".".join(node_path) for node_path in provided_nodes)

    def _provided_keywords_match_name(self, snapshot_name: str) -> bool:
        names = snapshot_name.split(".")
        return any(
            expr.evaluate(lambda subname: any(subname in name for name in names))
            for expr in self._keyword_expressions
        )

    def _ran_items_match_name(self, snapshot_name: str) -> bool:
        return any(
            PyTestLocation(item).matches_snapshot_name(snapshot_name)
            for item in self.ran_items
        )

    def _selected_items_match_name(self, snapshot_name: str) -> bool:
        if self._keyword_expressions:
            return self._provided_keywords_match_name(snapshot_name)
        return self._ran_items_match_name(snapshot_name)

    def _selected_items_match_location(self, snapshot_location: str) -> bool:
        return any(
            PyTestLocation(item).matches_snapshot_location(snapshot_location)
            for item in self.ran_items
        )
