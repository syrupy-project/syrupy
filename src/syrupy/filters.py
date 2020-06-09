from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyName,
        PropertyPath,
    )


def paths(path_string: str, *path_strings: str) -> "PropertyFilter":
    """
    Factory to create a filter using list of paths
    """

    def path_filter(prop: "PropertyName", path: "PropertyPath") -> bool:
        sep = "."
        path_str = f"{sep.join(str(p) for p, _ in path)}{sep}{prop}"
        return any(path_str == p for p in (path_string, *path_strings))

    return path_filter
