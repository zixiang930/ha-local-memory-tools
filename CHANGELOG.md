# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Changed
- Improved Chinese memory tokenization so related phrases are matched more reliably.
- Updated CI actions to current releases.

### Fixed
- Hardened persistent memory loading so malformed stored entries are skipped instead of breaking startup.
- Fixed Ruff lint and import-ordering issues in LLM tooling.

### Added
- Added regression coverage for Chinese tokenization.
- Added repository CODEOWNERS metadata.

### Planned
- Integration tests against Home Assistant.
- Retention and namespace options.

## [0.1.0] - 2026-08-12

### Added
- Initial local persistent memory store.
- LLM tools for remember, recall, forget, and memory statistics.
- UI config flow.
- English and Simplified Chinese translations.
