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
)

import attr
import pytest

from .data import (
    Snapshot,
    SnapshotFossil,
    SnapshotFossils,
    SnapshotUnknownFossil,
)
from .location import TestLocation
from .terminal import (
    bold,
    error_style,
    green,
    success_style,
    warning_style,
)


if TYPE_CHECKING:
    from .assertion import SnapshotAssertion  # noqa: F401


@attr.s
class SnapshotReport:
    base_dir: str = attr.ib()
    all_items: Dict["pytest.Item", bool] = attr.ib()
    ran_items: Dict["pytest.Item", bool] = attr.ib()
    update_snapshots: bool = attr.ib()
    is_providing_paths: bool = attr.ib()
    is_providing_nodes: bool = attr.ib()
    warn_unused_snapshots: bool = attr.ib()
    assertions: List["SnapshotAssertion"] = attr.ib()
    discovered: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    created: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    failed: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    matched: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    updated: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)
    used: "SnapshotFossils" = attr.ib(factory=SnapshotFossils)

    def __attrs_post_init__(self) -> None:
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
        return self.all_items == self.ran_items and not self.is_providing_nodes

    @property
    def unused(self) -> "SnapshotFossils":
        unused_fossils = SnapshotFossils()
        for unused_snapshot_fossil in self._diff_snapshot_fossils(
            self.discovered, self.used
        ):
            snapshot_location = unused_snapshot_fossil.location
            if self.is_providing_paths and not any(
                TestLocation(node).matches_snapshot_location(snapshot_location)
                for node in self.ran_items
            ):
                continue

            if self.ran_all_collected_tests:
                unused_snapshots = {*unused_snapshot_fossil}
                mark_for_removal = snapshot_location not in self.used
            else:
                unused_snapshots = {
                    snapshot
                    for snapshot in unused_snapshot_fossil
                    if any(
                        TestLocation(node).matches_snapshot_name(snapshot.name)
                        for node in self.ran_items
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
        summary_lines: List[str] = []
        if self.num_failed:
            summary_lines.append(
                ngettext(
                    "{} snapshot failed.", "{} snapshots failed.", self.num_failed,
                ).format(error_style(self.num_failed))
            )
        if self.num_matched:
            summary_lines.append(
                ngettext(
                    "{} snapshot passed.", "{} snapshots passed.", self.num_matched,
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
                    "{} snapshot updated.", "{} snapshots updated.", self.num_updated,
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
