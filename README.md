# syrupy

> _/ˈsirəpē/_

## Overview

TODO

## Motivation

The python package `snapshottest` has some core limitations which this package attempts to address:
- TODO

## Installation

```shell
python -m pip install syrupy
```

## Usage

### Basic Usage

In a pytest test file `test_file.py`:

```python
def test_foo(snapshot):
    actual = "Some computed value!"
    assert actual == snapshot
```

when you run `pytest`, the above test should fail due to a missing snapshot. Re-run pytest with the update snapshots flag like so:

```shell
pytest --update-snapshots
```

A snapshot file should be generated under a `__snapshots__` directory in the same directory as `test_file.py`. The `__snapshots__` directory and all its children should be committed along with your test code.

### Advanced Usage, Plugin Support

```python
import pytest

@pytest.fixture
def snapshot_custom(snapshot):
    return snapshot.with_class(
        io_class=CustomIOClass,
        serializer_class=CustomSerializerClass,
    )

def test_image(snapshot_custom):
    actual = "..."
    assert actual == snapshot_custom
```

Both `CustomIOClass` and `CustomSerializerClass` should extend `syrupy.io.SnapshotIO` and `syrupy.io.SnapshotSerializer` respectively.

## Uninstalling

```python
pip uninstall syrupy
```

## Contributing

Feel free to open a PR. This project is still in a very early stage, and we're still figuring out what direction we want to move towards.

To develop locally, clone this repository and run `. script/bootstrap` to install test dependencies. You can then use `invoke --help` to see a list of commands.

## Contributors

This section is automatically generated via tagging the all-contributors bot in a PR:

```
@all-contributors please add <username> for <contribution type>
```
