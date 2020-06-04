from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Tuple,
    Type,
)

from syrupy.extensions.amber import DataSerializer


if TYPE_CHECKING:
    from syrupy.types import (
        PropertyMatcher,
        PropertyPath,
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
    mapping: Dict[str, Tuple[Type[Any], ...]], *, strict: bool = True
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
    strict_mapping = {**mapping}
    types_any = strict_mapping.pop(path_any) if path_any in mapping else ()

    def path_type_matcher(
        data: "SerializableData", paths: "PropertyPath"
    ) -> Optional["SerializableData"]:
        path_str = ".".join(str(p) for p in paths)
        for path, types in (*strict_mapping.items(), (path_any, types_any)):
            if path == path_str or path == path_any:
                for class_type in types:
                    if isinstance(data, class_type):
                        return Repr(DataSerializer.object_type(data))
                if path != path_any and strict:
                    raise ValueError(
                        f"{data} at '{path_str}' of type {data.__class__} "
                        f"does not match any of the expected types {types}"
                    )
        return data

    return path_type_matcher
