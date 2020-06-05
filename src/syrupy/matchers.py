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
    mapping: Optional[Dict[str, Tuple["PropertyValueType", ...]]] = None,
    *,
    types: Tuple["PropertyValueType", ...] = (),
    strict: bool = True,
) -> "PropertyMatcher":
    """
    Factory to create a matcher using path and type mapping
    """
    if not mapping and not types:
        raise ValueError("Both mapping and types argument cannot be empty")

    def path_type_matcher(
        data: "SerializableData", path: "PropertyPath"
    ) -> Optional["SerializableData"]:
        path_str = ".".join(str(p) for p, _ in path)
        if mapping:
            for path_to_match in mapping:
                if path_to_match == path_str:
                    for type_to_match in mapping[path_to_match]:
                        if isinstance(data, type_to_match):
                            return Repr(DataSerializer.object_type(data))
                    if strict:
                        raise ValueError(
                            f"{data} at '{path_str}' of type {data.__class__} "
                            f"does not match any of the expected types {types}"
                        )
        for type_to_match in types:
            if isinstance(data, type_to_match):
                return Repr(DataSerializer.object_type(data))
        return data

    return path_type_matcher
