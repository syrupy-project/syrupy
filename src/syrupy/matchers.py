from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
    Tuple,
)

from syrupy.extensions.amber.serializer import (
    DataSerializer,
    Repr,
)

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyMatcher,
        PropertyPath,
        PropertyValueType,
        SerializableData,
    )


class PathTypeError(TypeError):
    pass


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
        raise PathTypeError(gettext("Both mapping and types argument cannot be empty"))

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
                        raise PathTypeError(
                            gettext(
                                "{} at '{}' of type {} does not "
                                "match any of the expected types: {}"
                            ).format(data, path_str, data.__class__, types)
                        )
        for type_to_match in types:
            if isinstance(data, type_to_match):
                return Repr(DataSerializer.object_type(data))
        return data

    return path_type_matcher
