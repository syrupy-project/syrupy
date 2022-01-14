import re
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
    regex: bool = False,
) -> "PropertyMatcher":
    """
    Factory to create a matcher using path and type mapping
    """
    if not mapping and not types:
        raise PathTypeError(gettext("Both mapping and types argument cannot be empty"))

    def _path_match(path: str, pattern: str) -> bool:
        if regex:
            return re.fullmatch(pattern, path) is not None
        return path == pattern

    def path_type_matcher(
        *, data: "SerializableData", path: "PropertyPath"
    ) -> Optional["SerializableData"]:
        path_str = ".".join(str(p) for p, _ in path)
        if mapping:
            for pattern in mapping:
                if _path_match(path_str, pattern):
                    for type_to_match in mapping[pattern]:
                        if isinstance(data, type_to_match):
                            return Repr(DataSerializer.object_type(data))
                    if strict:
                        raise PathTypeError(
                            gettext(
                                "{} at '{}' of type {} does not "
                                "match any of the expected types: {}"
                            ).format(data, path_str, data.__class__, mapping[pattern])
                        )
        for type_to_match in types:
            if isinstance(data, type_to_match):
                return Repr(DataSerializer.object_type(data))
        return data

    return path_type_matcher
