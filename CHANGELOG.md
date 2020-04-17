# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

From v1.0.0 onwards, this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Pre-v1, breaking changes will be indicated via a minor release, while all other changes will fall under patches. At any time, you can see what's in progress for a version by filtering GitHub issues by milestone.

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
