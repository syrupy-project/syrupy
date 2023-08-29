from typing import (
    TYPE_CHECKING,
    List,
    Set,
    Tuple,
    Union,
)

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyName,
        PropertyPath,
    )


def paths(*path_parts: str) -> "PropertyFilter":
    """
    Factory to create a filter using list of path strings.

    This filter does not work well when combined with "include" and
    nested paths, since "include" oeprates per key as an object is traversed
    for serialization. For nested paths, we must include all parents. To accomplish
    this, we provide an alternative "paths_include" filter which does this
    automatically.
    """

    if not path_parts:
        raise TypeError("At least 1 path argument is required.")

    parts: Set[str] = set(path_parts)

    def path_filter(*, prop: "PropertyName", path: "PropertyPath") -> bool:
        path_str = ".".join(str(p) for p, _ in (*path, (prop, None)))
        return path_str in parts

    return path_filter


def paths_include(*path_parts: Union[Tuple[str, ...], List[str]]) -> "PropertyFilter":
    """
    Factory to create a filter using list of path tuples.
    """

    if not path_parts:
        raise TypeError("At least 1 path argument is required.")

    # "include" operates per key as an object is traversed for serialization.
    # This means, if matching a nested path, we must also include all parents.
    parts: Set[Tuple[str, ...]] = set()
    for path_part in path_parts:
        if isinstance(path_part, (list, tuple)):
            for idx in range(len(path_part)):
                parts.add(tuple(path_part[: idx + 1]))
        else:
            raise TypeError("Unexpected argument. Expected list/tuple.")

    def path_filter(*, prop: "PropertyName", path: "PropertyPath") -> bool:
        path_tuple = tuple(str(p) for p, _ in (*path, (prop, None)))
        return path_tuple in parts

    return path_filter


def props(*prop_names: str) -> "PropertyFilter":
    """
    Factory to create filter using list of props
    """

    if not prop_names:
        raise TypeError("At least 1 prop name is required.")

    def prop_filter(*, prop: "PropertyName", path: "PropertyPath") -> bool:
        return any(str(prop) == p for p in prop_names)

    return prop_filter
