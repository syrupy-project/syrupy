# syrupy

<span><img align="right" width="200" height="200" src="https://user-images.githubusercontent.com/2528959/69500147-85d71400-0ec6-11ea-867a-277881278e57.png" alt="Logo"></span>

> _/ˈsirəpē/_

| Category | Badges |
| --- | --- |
| Project | [![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors) [![Maturity badge - level 1](https://img.shields.io/badge/Maturity-Level%201%20--%20New%20Project-yellow.svg)](https://github.com/tophat/getting-started/blob/master/scorecard.md) ![Stage](https://img.shields.io/pypi/status/syrupy) [![Slack workspace](https://slackinvite.dev.tophat.com/badge.svg)](https://opensource.tophat.com/slack) |
| Package | [![Pypi](https://img.shields.io/pypi/v/syrupy)](https://pypi.org/project/syrupy/) ![Wheel](https://img.shields.io/pypi/wheel/syrupy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/syrupy) ![PyPI - Downloads](https://img.shields.io/pypi/dm/syrupy) ![PyPI - License](https://img.shields.io/pypi/l/syrupy) |
| Testing | ![Build Status](https://github.com/tophat/syrupy/workflows/Syrupy%20CICD/badge.svg) [![codecov](https://codecov.io/gh/tophat/syrupy/branch/master/graph/badge.svg)](https://codecov.io/gh/tophat/syrupy) |

## Overview

Syrupy is a pytest snapshot plugin. It enables developers to write tests which assert immutability of computed results.

## Motivation

The most popular snapshot test plugin compatible with pytest has some core limitations which this package attempts to address by upholding some keys values:

- Extensible: If a particular data type is not supported, users should be able to easily and quickly add support.
- Idiomatic: Snapshot testing should fit naturally among other tests cases in pytest, e.g. `assert x == snapshot` vs. `snapshot.assert_match(x)`.
- Soundness: Snapshot tests should uncover even the most minute issues. Unlike other snapshot libraries, Syrupy will fail a test suite if a snapshot does not exist, not just on snapshot differences.

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
pytest --snapshot-update
```

A snapshot file should be generated under a `__snapshots__` directory in the same directory as `test_file.py`. The `__snapshots__` directory and all its children should be committed along with your test code.

### Advanced Usage, Plugin Support

```python
import pytest

@pytest.fixture
def snapshot_custom(snapshot):
    return snapshot.with_class(
        serializer_class=CustomSerializerClass,
    )

def test_image(snapshot_custom):
    actual = "..."
    assert actual == snapshot_custom
```

`CustomSerializerClass` should extend `syrupy.serializers.base.AbstractSnapshotSerializer`.

## Uninstalling

```python
pip uninstall syrupy
```

## Contributing

Feel free to open a PR. This project is still in a very early stage, and we're still figuring out what direction we want to move towards.

To develop locally, clone this repository and run `. script/bootstrap` to install test dependencies. You can then use `invoke --list` to see available commands.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://noahnu.com"><img src="https://avatars0.githubusercontent.com/u/1297096?v=4" width="100px;" alt=""/><br /><sub><b>Noah</b></sub></a><br /><a href="#infra-noahnu" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#ideas-noahnu" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Documentation">📖</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://emmanuel.ogbizi.com"><img src="https://avatars0.githubusercontent.com/u/2528959?v=4" width="100px;" alt=""/><br /><sub><b>Emmanuel Ogbizi</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Code">💻</a> <a href="#design-iamogbz" title="Design">🎨</a> <a href="#infra-iamogbz" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Documentation">📖</a> <a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
This section is automatically generated via tagging the all-contributors bot in a PR:

```text
@all-contributors please add <username> for <contribution type>
```
