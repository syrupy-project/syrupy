"""
Syrupy serializers module
"""

from .yaml import YAMLSnapshotSerializer


DEFAULT_SERIALIZER = YAMLSnapshotSerializer  # pylint: disable=invalid-name
