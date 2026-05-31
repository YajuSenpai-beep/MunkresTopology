# Changelog

## [1.0.0] — 2026-06-01

### Added
- **Core engine** (`engine.py`): Config-driven LaTeX index insertion with math/comment/verbatim/command-arg skipping
- **Index parser** (`parser.py`): OCR index text → JSON converter (indented + run-in formats)
- **LaTeX utils** (`tex_utils.py`): Math mode detection, comment/verbatim skipping, makeindex special char escaping, brace matching
- **Multi-pattern matcher** (`matcher.py`): Aho-Corasick automaton for O(n) multi-term search
- **Multi-file support** (`project.py`): `\input`/`\include` resolution, encoding detection, line ending preservation
- **Index scanner** (`scanner.py`): Auto-discovery of existing `\index{}`/`\idx{}` commands
- **CLI**: `insert`, `parse`, `scan` subcommands with `--dry-run`, `--interactive`, `--main`, `--fast`
- **Safety**: Atomic writes (tempfile + replace), three-level logging
- **Config**: YAML-driven, project-agnostic
- **Tests**: 82 pytest cases (unit, integration, regression, exception, performance)
- **CI**: GitHub Actions (test + lint + Docker build on tag)
- **Docker**: Minimal Python 3.11-slim image
- **Makefile**: `make test`, `make lint`, `make clean`, `make build`

### Preserved
- Node.js `core/` engine (backward compatible)
- `tools/` batch scripts (21 utilities for chapter processing)
