"""
Example: Custom Image Extension

The Single File Snapshot Extension writes each snapshot
to its own file. For images, this produces a cleaner diff
on websites like GitHub.
"""

import base64

import pytest

from syrupy.extensions.single_file import SingleFileSnapshotExtension


class JPEGImageExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "jpg"


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(JPEGImageExtension)


def test_jpeg_image(snapshot):
    reddish_square = base64.b64decode(
        b"/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////"
        b"////////////////////////////////////////////////////////////"
        b"2wBDAf//////////////////////////////////////////////////////"
        b"////////////////////////////////wAARCAAEAAQDASIAAhEBAxEB/8QA"
        b"HwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUF"
        b"BAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkK"
        b"FhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1"
        b"dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXG"
        b"x8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEB"
        b"AQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAEC"
        b"AxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRom"
        b"JygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOE"
        b"hYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU"
        b"1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwBlFFFAz//Z"
    )
    assert reddish_square == snapshot
