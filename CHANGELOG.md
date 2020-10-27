# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

From v1.0.0 onwards, this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Pre-v1, breaking changes will be indicated via a minor release, while all other changes will fall under patches. At any time, you can see what's in progress for a version by filtering GitHub issues by milestone.

# [0.8.0](https://github.com/tophat/syrupy/compare/v0.7.2...v0.8.0) (2020-10-27)


### Features

* **amber:** normalise line endings between operating systems ([#377](https://github.com/tophat/syrupy/issues/377)) ([82b624d](https://github.com/tophat/syrupy/commit/82b624d94259422d2f5d5a4d955b615514d0d060))

## [0.7.2](https://github.com/tophat/syrupy/compare/v0.7.1...v0.7.2) (2020-09-20)


### Bug Fixes

* add support for no colors mode ([#359](https://github.com/tophat/syrupy/issues/359)) ([ec39b80](https://github.com/tophat/syrupy/commit/ec39b80b14189032b1b61a4959809737c56ea149))

## [0.7.1](https://github.com/tophat/syrupy/compare/v0.7.0...v0.7.1) (2020-09-05)


### Bug Fixes

* support attrs <21.0.0 ([#350](https://github.com/tophat/syrupy/issues/350)) ([d327168](https://github.com/tophat/syrupy/commit/d327168af96385bc2c2eb97f73233ccfd9513226))

# [0.7.0](https://github.com/tophat/syrupy/compare/v0.6.1...v0.7.0) (2020-08-24)


### Features

* bugfix, pass indent to multiline open tag, close [#332](https://github.com/tophat/syrupy/issues/332) ([#334](https://github.com/tophat/syrupy/issues/334)) ([3b06a98](https://github.com/tophat/syrupy/commit/3b06a98928a64729bad7c2113e6390136bfbc512))

## [0.6.1](https://github.com/tophat/syrupy/compare/v0.6.0...v0.6.1) (2020-07-29)


### Bug Fixes

* support pytest v6 ([#307](https://github.com/tophat/syrupy/issues/307)) ([ef6496f](https://github.com/tophat/syrupy/commit/ef6496fb50d8cfea5c9ae1c5954ae546024e28cc))

# [0.6.0](https://github.com/tophat/syrupy/compare/v0.5.2...v0.6.0) (2020-07-12)


### Features

* add simple props filter helper ([#290](https://github.com/tophat/syrupy/issues/290)) ([d76cc07](https://github.com/tophat/syrupy/commit/d76cc07fa5b9eb7d6cbbbe4b7894e0ba29bd0df6))

## [0.5.2](https://github.com/tophat/syrupy/compare/v0.5.1...v0.5.2) (2020-07-09)


### Bug Fixes

* **amber:** Do not add empty line to empty iterables ([#287](https://github.com/tophat/syrupy/issues/287)) ([0b4a9b0](https://github.com/tophat/syrupy/commit/0b4a9b065a235f8c62ad08e29f3f36f80b3a25d6))

## [0.5.1](https://github.com/tophat/syrupy/compare/v0.5.0...v0.5.1) (2020-06-12)


### Bug Fixes

* support ignoring fields when serializing ([#262](https://github.com/tophat/syrupy/issues/262)) ([f67268e](https://github.com/tophat/syrupy/commit/f67268e23de477c6cc0912f34d6c6d0f70548683))

# [0.5.0](https://github.com/tophat/syrupy/compare/v0.4.4...v0.5.0) (2020-06-09)


### Features

* **amber:** add property matcher support ([#245](https://github.com/tophat/syrupy/issues/245)) ([83ded3c](https://github.com/tophat/syrupy/commit/83ded3c73917673fcb46857eb291e26704c2c0f6))

## [0.4.4](https://github.com/tophat/syrupy/compare/v0.4.3...v0.4.4) (2020-06-02)


### Bug Fixes

* only process valid test nodes in report, close [#246](https://github.com/tophat/syrupy/issues/246) ([#247](https://github.com/tophat/syrupy/issues/247)) ([8ed194c](https://github.com/tophat/syrupy/commit/8ed194cc9e7365c6c4fbd9fcd45d403646334b18))

## [0.4.3](https://github.com/tophat/syrupy/compare/v0.4.2...v0.4.3) (2020-05-27)


### Bug Fixes

* Update setup.py, so that it allows for any Python 3.6+ version to be used ([25c2688](https://github.com/tophat/syrupy/commit/25c26881629589949e5877f829f54249deec05b2))

## [0.4.2](https://github.com/tophat/syrupy/compare/v0.4.1...v0.4.2) (2020-04-22)


### Bug Fixes

* Handle dotted parameters in classname ([#200](https://github.com/tophat/syrupy/issues/200)) ([d961f7c](https://github.com/tophat/syrupy/commit/d961f7cfdde4d3eb36777acce7d2926968531447))

## [0.4.1](https://github.com/tophat/syrupy/compare/v0.4.0...v0.4.1) (2020-04-19)


### Bug Fixes

* specify encoding when reading and writing amber fossils ([#198](https://github.com/tophat/syrupy/issues/198)) ([a6a53c4](https://github.com/tophat/syrupy/commit/a6a53c4065880433953b1372e6057e2c8ec03768))

# [0.4.0](https://github.com/tophat/syrupy/compare/v0.3.12...v0.4.0) (2020-04-19)


### Bug Fixes

* remove added trailing whitespace from multiline string ([24f3d57](https://github.com/tophat/syrupy/commit/24f3d577726bc9c9b09433780f1647adc8fd35a4))


### Features

* **amber:** indent multiline strings, close [#193](https://github.com/tophat/syrupy/issues/193) ([#194](https://github.com/tophat/syrupy/issues/194)) ([de5af3e](https://github.com/tophat/syrupy/commit/de5af3e233712e1db3132b0cdbcc6325dcb9a625))

## [0.3.12](https://github.com/tophat/syrupy/compare/v0.3.11...v0.3.12) (2020-04-19)


### Bug Fixes

* use the test node location when determining snapshot class name ([#197](https://github.com/tophat/syrupy/issues/197)) ([1010c94](https://github.com/tophat/syrupy/commit/1010c94378dbf325fe3fda6a2f563ae152c640ca))

## [0.3.11](https://github.com/tophat/syrupy/compare/v0.3.10...v0.3.11) (2020-04-17)


### Bug Fixes

* show snapshot data in report when does not exist ([#191](https://github.com/tophat/syrupy/issues/191)) ([7ebdca2](https://github.com/tophat/syrupy/commit/7ebdca2d5537ce6f311b09e812aa54ffc141222e))

## [0.3.10](https://github.com/tophat/syrupy/compare/v0.3.9...v0.3.10) (2020-04-15)


### Bug Fixes

* parsing identifiers from snapshot names ([#186](https://github.com/tophat/syrupy/issues/186)) ([#187](https://github.com/tophat/syrupy/issues/187)) ([45a2931](https://github.com/tophat/syrupy/commit/45a29312a8a416db420cb2c9a839069dfc289c46))

## [0.3.9](https://github.com/tophat/syrupy/compare/v0.3.8...v0.3.9) (2020-04-08)


### Bug Fixes

* correctly track unused snapshots in classes ([#177](https://github.com/tophat/syrupy/issues/177)) ([f780501](https://github.com/tophat/syrupy/commit/f7805015ac874843fbd996d209a6a6851f5d0ba2))

## [0.3.8](https://github.com/tophat/syrupy/compare/v0.3.7...v0.3.8) (2020-04-03)


### Performance Improvements

* only clear assertion `_extension` when overridden ([#172](https://github.com/tophat/syrupy/issues/172)) ([82eae91](https://github.com/tophat/syrupy/commit/82eae91a2156556753ced22eb9b6cc97594b6f9c))

## [0.3.7](https://github.com/tophat/syrupy/compare/v0.3.6...v0.3.7) (2020-03-24)


### Bug Fixes

* support call syntax for snapshot fixture overriding ([#160](https://github.com/tophat/syrupy/issues/160)) ([4cf051c](https://github.com/tophat/syrupy/commit/4cf051c808da59d7b5a4dcad6cae440dae262541))

## [0.3.6](https://github.com/tophat/syrupy/compare/v0.3.5...v0.3.6) (2020-03-10)


### Bug Fixes

* specify correct min version of pytest ([#157](https://github.com/tophat/syrupy/issues/157)) ([858bec7](https://github.com/tophat/syrupy/commit/858bec7e3205679eb0099bde66af564002c4af8d))

## [0.3.5](https://github.com/tophat/syrupy/compare/v0.3.4...v0.3.5) (2020-03-08)


### Bug Fixes

* snapshot name warning showing on false negatives ([#151](https://github.com/tophat/syrupy/issues/151)) ([d56860b](https://github.com/tophat/syrupy/commit/d56860b9005ee21a04f36f0ea7550fe8c4d7323a))

## [0.3.4](https://github.com/tophat/syrupy/compare/v0.3.3...v0.3.4) (2020-03-08)


### Bug Fixes

* show hidden line characters and accessible colors ([#126](https://github.com/tophat/syrupy/issues/126)) ([fa442df](https://github.com/tophat/syrupy/commit/fa442df2981406b31065938c57b6ee8eaed2e724)), closes [#150](https://github.com/tophat/syrupy/issues/150)

## [v0.3.3](https://github.com/tophat/syrupy/compare/v0.3.2...v0.3.3)

- Conversion of all `os.path` and `os.walk` calls to use `pathlib` instead, setting `pathlib` as the new preferred way of doing path operations (#130)
- Add `--snapshot-default-extension` option to specify extension class via pytest cli (#132)
- Fix bug where snapshot diffs were erroneously printed (#135)
- Fix bug where snapshot names were incorrectly matching tests (#136)
- Fix bug where deleted snapshots where incorrectly colored (#136)
- Fix bug where targeting specific test nodes did not filter out unused snapshots (#139)
- Fix bug where snapshot report was printed out before the pytest report (#144)

## [v0.3.2](https://github.com/tophat/syrupy/compare/v0.3.1...v0.3.2)

- Fix bug where untargeted snapshots would be deleted when using pytest in targeted mode (#123)
- Fix bug where snapshot files were not cleaned up when running specific test files (#127)
- Fix bug where targeting specific test nodes in a test file was not supported (#127)
- Fix bug where targeting specific test modules using pyargs was not supported (#127)

## [v0.3.1](https://github.com/tophat/syrupy/compare/v0.3.0...v0.3.1)

- Fix bug where newline control characters were being translated based on platform (#113)

## [v0.3.0](https://github.com/tophat/syrupy/compare/v0.2.0...v0.3.0)

- Adds support for named tuple fields (#108)
- Add trailing commas to class fields (#108)
- Specify explicit version range for pytest peer dependency (#111)

## [v0.2.0](https://github.com/tophat/syrupy/compare/v0.1.0...v0.2.0)

- Fix issue with using hashables as dict keys or in sets (#103)
- Add support for custom objects repr (#101)
- Add support for nested test classes (#99)
- Remove `_snapshot_subdirectory_name` from `SnapshotFossilizer` (#99)

## [v0.1.0](https://github.com/tophat/syrupy/tree/v0.1.0)

- Initial release respecting [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
