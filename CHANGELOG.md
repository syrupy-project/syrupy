# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

From v1.0.0 onwards, this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Pre-v1, breaking changes will be indicated via a minor release, while all other changes will fall under patches. At any time, you can see what's in progress for a version by filtering GitHub issues by milestone.

## Master (Unreleased)

- Up to date with releases.

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
