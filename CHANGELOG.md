# Change Log

All notable changes to this project will be documented in this file. This
change log follows the conventions of
[keepachangelog.com](https://keepachangelog.com/).

## [Unreleased]

[Unreleased]: https://github.com/ligurio/litclock/compare/0.1.0...HEAD

### Added

- Option for setting language in a script.

### Fixed

- Compatibility with dash(1) by removing  pipefail option in litclock(1).

### Changed

- Sync English quotes.
- Script searches file with quotes in a system path, not a current directory.
- Makefile installs files with quotes.
- Format build script according to Python PEP8 style.
- Check Python PEP8 style in GH Actions.

## [0.1.0]

[0.1.0]: https://github.com/ligurio/litclock/compare/9936c762...0.1.0

### Added

- English quotes.
- Manual page for a shell script.
- Shell script for displaying clock in a terminal.
- Russian quotes.
