# syrupy

<img align="right" width="100px" height="100px" src="https://user-images.githubusercontent.com/2528959/69500147-85d71400-0ec6-11ea-867a-277881278e57.png" alt="Logo">

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors) [![Maturity badge - level 4](https://img.shields.io/badge/Maturity-Level%204%20--%20Critical-brightgreen.svg)](https://github.com/tophat/getting-started/blob/master/scorecard.md) [![Stage](https://img.shields.io/pypi/status/syrupy)](https://pypi.org/project/syrupy/) [![Discord](https://img.shields.io/discord/809577721751142410?label=community%20chat)](https://discord.gg/YhK3GFcZrk)

![Pytest>=5.1.0,<8.0.0](https://img.shields.io/badge/pytest-%3E%3D5.1.0,%20%3C8.0.0-green) [![Pypi](https://img.shields.io/pypi/v/syrupy)](https://pypi.org/project/syrupy/) [![Wheel](https://img.shields.io/pypi/wheel/syrupy)](https://pypi.org/project/syrupy/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/syrupy) [![PyPI - Downloads](https://img.shields.io/pypi/dm/syrupy)](https://pypi.org/project/syrupy/) [![PyPI - License](https://img.shields.io/pypi/l/syrupy)](./LICENSE)

![Build Status](https://github.com/tophat/syrupy/workflows/Syrupy%20CICD/badge.svg) [![codecov](https://codecov.io/gh/tophat/syrupy/branch/master/graph/badge.svg)](https://codecov.io/gh/tophat/syrupy)

![Next Status](https://github.com/tophat/syrupy/workflows/Next%20Version/badge.svg)

## Overview

Syrupy is a [pytest](https://docs.pytest.org/en/latest/) snapshot plugin. It enables developers to write tests which assert immutability of computed results.

## Motivation

The most popular snapshot test plugin compatible with pytest has some core limitations which this package attempts to address by upholding some key values:

- Extensible: If a particular data type is not supported, users should be able to easily and quickly add support.
- Idiomatic: Snapshot testing should fit naturally among other test cases in pytest, e.g. `assert x == snapshot` vs. `snapshot.assert_match(x)`.
- Soundness: Snapshot tests should uncover even the most minute issues. Unlike other snapshot libraries, Syrupy will fail a test suite if a snapshot does not exist, not just on snapshot differences.

## Installation

```shell
python -m pip install syrupy
```

### Migration from snapshottest

You cannot use syrupy alongside snapshottest due to argument conflicts. To ease migration, we've made syrupy aware of snapshottest call syntax. Simply uninstall snapshottest and remove old snapshots:

```shell
pip uninstall snapshottest -y;
find . -type d ! -path '*/\.*' -name 'snapshots' | xargs rm -r
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

[![Usage Demo](https://tophat.github.io/syrupy/assets/usage_demo.gif)](https://asciinema.org/a/369462)

#### Custom Objects

The default serializer supports all python built-in types and provides a sensible default for custom objects.

#### Representation

If you need to customise your object snapshot, it is as easy as overriding the default `__repr__` implementation.

```python
def __repr__(self) -> str:
    return "MyCustomClass(...)"
```

#### Attributes

If you want to limit what properties are serialized at a class type level you could either:

**A**. Provide a filter function to the snapshot [exclude](#exclude) configuration option.

```py
def limit_foo_attrs(prop, path):
  allowed_foo_attrs = {"only", "serialize", "these", "attrs"}
  return isinstance(path[-1][1], Foo) and prop in allowed_foo_attrs

def test_bar(snapshot):
    actual = new Foo(...)
    assert actual == snapshot(exclude=limit_foo_attrs)
```

**B**. Or override the `__dir__` implementation to control the attribute list.

```py
class Foo:
  def __dir__(self):
    return ["only", "serialize", "these", "attrs"]

def test_bar(snapshot):
    actual = new Foo(...)
    assert actual == snapshot
```

Both options will generate equivalent snapshots but the latter is only viable when you have control over the class implementation and do not need to share the exclusion logic with other objects.

### CLI Options

These are the cli options exposed to `pytest` by the plugin.

| Option                         | Description                                                                                                                    | Default                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| `--snapshot-update`            | Snapshots will be updated to match assertions and unused snapshots will be deleted.                                            | `False`                                          |
| `--snapshot-details`           | Includes details of unused snapshots (test name and snapshot location) in the final report.                                    | `False`                                          |
| `--snapshot-warn-unused`       | Prints a warning on unused snapshots rather than fail the test suite.                                                          | `False`                                          |
| `--snapshot-default-extension` | Use to change the default snapshot extension class.                                                                            | [AmberSnapshotExtension](https://github.com/tophat/syrupy/blob/master/src/syrupy/extensions/amber/__init__.py) |
| `--snapshot-no-colors`         | Disable test results output highlighting. Equivalent to setting the environment variables `ANSI_COLORS_DISABLED` or `NO_COLOR` | Disabled by default if not in terminal.          |

### Assertion Options

These are the options available on the `snapshot` assertion fixture.
Use of these options are one shot and do not persist across assertions.
For more persistent options see [advanced usage](#advanced-usage).

#### `matcher`

This allows you to match on a property path and value to control how specific object shapes are serialized.

The matcher is a function that takes two keyword arguments.
It should return the replacement value to be serialized or the original unmutated value.

| Argument | Description                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| `data`   | Current serializable value being matched on                                                                        |
| `path`   | Ordered path traversed to the current value e.g. `(("a", dict), ("b", dict))` from `{ "a": { "b": { "c": 1 } } }`} |

**NOTE:** Do not mutate the value received as it could cause unintended side effects.

##### Built-In Matchers

Syrupy comes with built-in helpers that can be used to make easy work of using property matchers.

###### `path_type(mapping=None, *, types=(), strict=True, regex=False)`

Easy way to build a matcher that uses the path and value type to replace serialized data.
When strict, this will raise a `ValueError` if the types specified are not matched.

| Argument  | Description                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `mapping` | Dict of path string to tuples of class types, including primitives e.g. (MyClass, UUID, datetime, int, str)                        |
| `types`   | Tuple of class types used if none of the path strings from the mapping are matched                                                 |
| `strict`  | If a path is matched but the value at the path does not match one of the class types in the tuple then a `PathTypeError` is raised |
| `regex`   | If true, the `mapping` key is treated as a regular expression when matching paths                                                  |

```py
from syrupy.matchers import path_type

def test_bar(snapshot):
    actual = {
      "date_created": datetime.now(),
      "value": "Some computed value!!",
    }
    assert actual == snapshot(matcher=path_type({
      "date_created": (datetime,),
      "nested.path.id": (int,),
    }))
```

```ambr
# name: test_bar
  <class 'dict'> {
    'date_created': <class 'datetime'>,
    'value': 'Some computed value!!',
  }
---
```

#### `exclude`

This allows you to filter out object properties from the serialized snapshot.

The exclude parameter takes a filter function that accepts two keyword arguments.
It should return `true` or `false` if the property should be excluded or included respectively.

| Argument | Description                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `prop`   | Current property on the object, could be any hashable value that can be used to retrieve a value e.g. `1`, `"prop_str"`, `SomeHashableObject` |
| `path`   | Ordered path traversed to the current value e.g. `(("a", dict), ("b", dict))` from `{ "a": { "b": { "c": 1 } } }`}                            |

##### Built-In Filters

Syrupy comes with built-in helpers that can be used to make easy work of using the filter options.

###### `props(prop_name, *prop_name)`

Easy way to build a filter that excludes based on string based property names.

Takes an argument list of property names, with support for indexed iterables.

```py
from syrupy.filters import props

def test_bar(snapshot):
    actual = {
      "id": uuid.uuid4(),
      "list": [1,2,3],
    }
    assert actual == snapshot(exclude=props("id", "1"))
```

```ambr
# name: test_bar
  <class 'dict'> {
    'list': <class 'list'> [
      1,
      3,
    ],
  }
---
```

###### `paths(path_string, *path_strings)`

Easy way to build a filter that uses full path strings delimited with `.`.

Takes an argument list of path strings.

```py
from syrupy.filters import paths

def test_bar(snapshot):
    actual = {
      "date": datetime.now(),
      "list": [1,2,3],
    }
    assert actual == snapshot(exclude=paths("date", "list.1"))
```

```ambr
# name: test_bar
  <class 'dict'> {
    'list': <class 'list'> [
      1,
      3,
    ],
  }
---
```

#### `extension_class`

This is a way to modify how the snapshot matches and serializes your data in a single assertion.

```py
def test_foo(snapshot):
    actual_svg = "<svg></svg>"
    assert actual_svg == snapshot(extension_class=SVGImageSnapshotExtension)
```

##### Built-In Extensions

Syrupy comes with a few built-in preset configurations for you to choose from. You should also feel free to extend the `AbstractSyrupyExtension` if your project has a need not captured by one our built-ins.

- **`AmberSnapshotExtension`**: This is the default extension which generates `.ambr` files. Serialization of most data types are supported.
  - Line control characters are normalised when snapshots are generated i.e. `\r` and `\n` characters are all written as `\n`. This is to allow interoperability of snapshots between operating systems that use disparate line control characters.
- **`SingleFileSnapshotExtension`**: Unlike the `AmberSnapshotExtension`, which groups all tests within a single test file into a singular snapshot file, this extension creates one `.raw` file per test case.
- **`PNGSnapshotExtension`**: An extension of single file, this should be used to produce `.png` files from a byte string.
- **`SVGSnapshotExtension`**: Another extension of single file. This produces `.svg` files from an svg string.
- **`JSONSnapshotExtension`**: Another extension of single file. This produces `.json` files from dictionaries and lists.

#### `name`

By default, if you make multiple snapshot assertions within a single test case, an auto-increment identifier will be used to index the snapshots. You can override this behaviour by specifying a custom snapshot name to use in place of the auto-increment number.

```py
def test_case(snapshot):
    assert "actual" == snapshot(name="case_a")
    assert "other" == snapshot(name="case_b")
```

> _Warning_: If you use a custom name, you must make sure the name is not re-used within a test case.

### Advanced Usage

By overriding the provided [`AbstractSnapshotExtension`](https://github.com/tophat/syrupy/tree/master/src/syrupy/extensions/base.py) you can implement varied custom behaviours.

See examples of how syrupy can be used and extended in the [test examples](https://github.com/tophat/syrupy/tree/master/tests/examples).

#### JSONSnapshotExtension

This extension can be useful when testing API responses, or when you have to deal with long dictionaries that are cumbersome to validate inside a test. For example:

```python
import pytest

from syrupy.extensions.json import JSONSnapshotExtension

@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension) 


def test_api_call(client, snapshot_json):
    resp = client.post("/endpoint")
    assert resp.status_code == 200
    assert snapshot_json == resp.json()
```

API responses often contain dynamic data, like IDs or dates. You can still validate and store other data of a response by leveraging syrupy matchers. For example:

```py
from datetime import datetime

from syrupy.matchers import path_type

def test_api_call(client, snapshot_json):
    resp = client.post("/user", json={"name": "Jane"})
    assert resp.status_code == 201

    matcher = path_type({
      "id": (int,),
      "registeredAt": (datetime,)
    })
    assert snapshot_json(matcher=matcher) == resp.json()
```

The generated snapshot:

```json
{
  "id": "<class 'int'>",
  "registeredAt": "<class 'datetime'>",
  "name": "Jane"
}
```

### Extending Syrupy

- [Custom snapshot directory 1](https://github.com/tophat/syrupy/tree/master/tests/examples/test_custom_snapshot_directory.py)
- [Custom snapshot directory 2](https://github.com/tophat/syrupy/tree/master/tests/examples/test_custom_snapshot_directory_2.py)
- [Custom snapshot name](https://github.com/tophat/syrupy/tree/master/tests/examples/test_custom_snapshot_name.py)
- [Custom object snapshots](https://github.com/tophat/syrupy/tree/master/tests/examples/test_custom_object_repr.py)
- [Custom comparator](https://github.com/tophat/syrupy/tree/master/tests/integration/test_custom_comparator.py)
- [JPEG image extension](https://github.com/tophat/syrupy/tree/master/tests/examples/test_custom_image_extension.py)
- [Built-in image extensions](https://github.com/tophat/syrupy/blob/master/tests/syrupy/extensions/image/test_image_svg.py)

## Uninstalling

```python
pip uninstall syrupy
```

If you have decided not to use Syrupy for your project after giving us a try, we'd love to get your feedback. Please create a GitHub issue if applicable, or drop a comment in our [Discord server](https://discord.gg/YhK3GFcZrk).

## Contributing

Feel free to open a PR or GitHub issue. Contributions welcome!

To develop locally, clone this repository and run `. script/bootstrap` to install test dependencies. You can then use `invoke --list` to see available commands.

### See contributing [guide](https://github.com/tophat/syrupy/tree/master/CONTRIBUTING.md)

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://noahnu.com"><img src="https://avatars0.githubusercontent.com/u/1297096?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Noah</b></sub></a><br /><a href="#infra-noahnu" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#ideas-noahnu" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Documentation">📖</a> <a href="https://github.com/tophat/syrupy/commits?author=noahnu" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://emmanuel.ogbizi.com"><img src="https://avatars0.githubusercontent.com/u/2528959?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Emmanuel Ogbizi</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Code">💻</a> <a href="#design-iamogbz" title="Design">🎨</a> <a href="#infra-iamogbz" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Documentation">📖</a> <a href="https://github.com/tophat/syrupy/commits?author=iamogbz" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/adamlazz"><img src="https://avatars3.githubusercontent.com/u/453811?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adam Lazzarato</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=adamlazz" title="Documentation">📖</a></td>
    <td align="center"><a href="https://mcataford.github.io"><img src="https://avatars2.githubusercontent.com/u/6210361?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Marc Cataford</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=mcataford" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=mcataford" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://msrose.github.io"><img src="https://avatars3.githubusercontent.com/u/3495264?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Michael Rose</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=msrose" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=msrose" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://fashionablenonsense.com/"><img src="https://avatars0.githubusercontent.com/u/3112159?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jimmy Jia</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=taion" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=taion" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://stevenloria.com"><img src="https://avatars2.githubusercontent.com/u/2379650?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Steven Loria</b></sub></a><br /><a href="#infra-sloria" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/arturbalabanov"><img src="https://avatars1.githubusercontent.com/u/3062003?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Artur Balabanov</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=arturbalabanov" title="Code">💻</a></td>
    <td align="center"><a href="http://huonw.github.io/"><img src="https://avatars1.githubusercontent.com/u/1203825?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Huon Wilson</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=huonw" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/issues?q=author%3Ahuonw" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/eaculb"><img src="https://avatars.githubusercontent.com/u/31480498?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Elizabeth Culbertson</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=eaculb" title="Code">💻</a> <a href="https://github.com/tophat/syrupy/commits?author=eaculb" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/joakimnordling"><img src="https://avatars.githubusercontent.com/u/6637576?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Joakim Nordling</b></sub></a><br /><a href="https://github.com/tophat/syrupy/issues?q=author%3Ajoakimnordling" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/bendidi"><img src="https://avatars.githubusercontent.com/u/22003440?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ouail</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=bendidi" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/fbjorn"><img src="https://avatars.githubusercontent.com/u/9670990?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Denis</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=fbjorn" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/N0124"><img src="https://avatars.githubusercontent.com/u/29734397?v=4?s=100" width="100px;" alt=""/><br /><sub><b>N0124</b></sub></a><br /><a href="https://github.com/tophat/syrupy/commits?author=N0124" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/dtczest"><img src="https://avatars.githubusercontent.com/u/97055299?v=4?s=100" width="100px;" alt=""/><br /><sub><b>dtczest</b></sub></a><br /><a href="https://github.com/tophat/syrupy/issues?q=author%3Adtczest" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This section is automatically generated via tagging the all-contributors bot in a PR:

```text
@all-contributors please add <username> for <contribution type>
```

## License


Syrupy is licensed under [Apache License Version 2.0](https://github.com/tophat/syrupy/tree/master/LICENSE).
