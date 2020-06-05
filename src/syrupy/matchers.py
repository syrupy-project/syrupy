from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
    Tuple,
)

from syrupy.extensions.amber import DataSerializer


if TYPE_CHECKING:
    from syrupy.types import (
        PropertyMatcher,
        PropertyPath,
        PropertyValueType,
        SerializableData,
    )


class Repr:
    """
    Easily generate custom representation objects
    """

    def __init__(self, repr_str: str):
        self._repr = repr_str

    def __repr__(self) -> str:
        return self._repr


def path_type(
    mapping: Dict[str, Tuple["PropertyValueType", ...]], *, strict: bool = True
) -> "PropertyMatcher":
    """
    Factory to create a matcher using path and type mapping
    e.g.
    {
        "*": (datetime.datetime, uuid.UUID),
        "some.deep.path.id": (int,),
    }
    """
    path_any = "*"
    ordered_mapping = [
        *((p, t) for p, t in mapping.items() if p != path_any),
        (path_any, mapping.get(path_any) or ()),
    ]

    def path_type_matcher(
        data: "SerializableData", path: "PropertyPath"
    ) -> Optional["SerializableData"]:
        path_str = ".".join(str(p) for p, _ in path)
        for path_to_match, types in ordered_mapping:
            if path_to_match == path_str or path_to_match == path_any:
                for type_to_match in types:
                    if isinstance(data, type_to_match):
                        return Repr(DataSerializer.object_type(data))
                if path_to_match != path_any and strict:
                    raise ValueError(
                        f"{data} at '{path_str}' of type {data.__class__} "
                        f"does not match any of the expected types {types}"
                    )
        return data

    return path_type_matcher
