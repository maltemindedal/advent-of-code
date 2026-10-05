# Configuration reference

Every configuration file and key in the repository, with its value and effect.

The solutions read no environment variables and no configuration files at runtime. Their only runtime input is puzzle files under `inputs/`, whose naming rules are in [API reference: input file layout](api.md#input-file-layout).

## `pyproject.toml`

### `[project]`

| Key | Value | Effect |
| --- | --- | --- |
| `name` | `"advent-of-code"` | Distribution name of the editable install. |
| `version` | `"1.0.0"` | Package version in the install metadata. No code reads it. |
| `license` | `"MIT"` | SPDX license expression, written to the install metadata as `License-Expression`. |
| `license-files` | `["LICENSE"]` | Bundles `LICENSE` into the built wheel. |
| `requires-python` | `">=3.11"` | Lowest supported Python. ty assumes this floor when type-checking. |
| `dependencies` | `["z3-solver>=4.12.4"]` | The only runtime dependency, used by `utils.z3_helpers` (2025 day 10). |

### `[build-system]` and `[tool.hatch.build.targets.wheel]`

| Key | Value | Effect |
| --- | --- | --- |
| `build-system.requires` | `["hatchling"]` | Build backend for the editable install. |
| `build-system.build-backend` | `"hatchling.build"` | Same. |
| `tool.hatch.build.targets.wheel.packages` | `["utils"]` | `utils` is the only package in the built wheel. The year folders and `tests/` are not packaged. |

### `[tool.uv]`

| Key | Value | Effect |
| --- | --- | --- |
| `package` | `true` | `uv sync` installs the project itself in editable mode, which puts the repository root on `sys.path`. |

No `required-version` is set, so uv does not enforce a minimum uv version.

### `[dependency-groups]`

| Group | Members | Locked version (`uv.lock`, 2026-10-05) |
| --- | --- | --- |
| `dev` | `pytest>=9.0.3` | 9.1.1 |
| | `ruff>=0.16.8` | 0.16.8 |
| | `ty>=0.0.83` | 0.0.83 |

The runtime dependency `z3-solver` is locked at 5.1.0.0. `uv.lock` is the source of truth for locked versions; Dependabot proposes updates weekly (see [`.github/dependabot.yml`](#githubdependabotyml)).

### `[tool.pytest]`

| Key | Value | Effect |
| --- | --- | --- |
| `strict` | `true` | Enables `strict_config`, `strict_markers`, `strict_xfail` and `strict_parametrization_ids`: config warnings, unregistered markers, unexpectedly passing `xfail` tests and duplicate parametrize IDs are errors. |
| `filterwarnings` | `["error"]` | Every warning raised during a test fails it. |
| `addopts` | `["--import-mode=importlib"]` | Each test file gets a module name derived from its path, so `tests/2025/test_01.py` and a future `tests/2026/test_01.py` can coexist. |
| `pythonpath` | `["."]` | Adds the repository root to `sys.path`, so tests can import `tests._helpers` and `utils`. |
| `testpaths` | `["tests"]` | A bare `pytest` collects only `tests/`. |

### `[tool.ruff]`

| Key | Value | Effect |
| --- | --- | --- |
| `line-length` | `100` | Maximum line length for the formatter and for `E501`. |
| `target-version` | `"py311"` | Lint and format for Python 3.11 syntax. |
| `lint.select` | `ANN`, `B`, `BLE`, `C4`, `E`, `F`, `I`, `ISC`, `PGH`, `PIE`, `PLE`, `PLW`, `PT`, `PTH`, `RUF`, `S`, `T10`, `UP`, `W` | Enabled rule families. `ANN` requires annotations on every function's parameters and return type. |
| `lint.ignore` | `["PLW2901"]` | Allows reassigning a loop variable, for example `line = line.strip()`, the parsing idiom the solutions use. |
| `lint.per-file-ignores` | `"tests/**" = ["S101", "S311"]` | Tests may use plain `assert` and the non-cryptographic `random` module. |
| `format.quote-style` | `"double"` | Formatter uses double quotes. |
| `format.indent-style` | `"space"` | Formatter indents with spaces. |

ruff 0.16 includes Markdown files when formatting and reformats their fenced `python` code blocks.

### `[tool.ty]`

| Key | Value | Effect |
| --- | --- | --- |
| `analysis.respect-type-ignore-comments` | `false` | `# type: ignore` comments suppress nothing. The only suppression is `# ty: ignore[<rule>]`, and ty reports one that no longer suppresses anything. |
| `rules.all` | `"error"` | Every ty rule is enabled at error severity. |

## `.gitignore`

| Pattern | Effect |
| --- | --- |
| `inputs/**`, `!inputs/**/`, `!inputs/**/*.sample.txt` | Everything under `inputs/` is ignored except files ending in `.sample.txt`. Real inputs (`01.txt`) and any other variant (`01.example.txt`) stay local. |
| `.env`, `.env.*`, `!.env.example` | Local secret files, such as an Advent of Code session cookie, are ignored. `.env.example` stays trackable. No code in the repository reads `.env`. |
| `__pycache__/`, `*.py[cod]`, `.venv/`, `.uv/`, `build/`, `dist/`, `*.egg-info/`, `.coverage`, `htmlcov/`, `.pytest_cache/`, `.ruff_cache/`, `.vscode/`, `.idea/` | Build, cache, virtual environment and editor files. |

## `.editorconfig`

| Section | Settings |
| --- | --- |
| `[*]` | 4-space indentation, UTF-8, trim trailing whitespace, final newline. |
| `[*.md]` | No maximum line length; trailing whitespace is kept. |

## `.github/workflows/ci.yml`

| Setting | Value |
| --- | --- |
| Triggers | Pushes to `main`; every pull request. |
| Token permissions | `contents: read`. Checkout runs with `persist-credentials: false`. |
| Concurrency | Group `ci-<head ref or run id>`. A new push to a pull request cancels its previous run; pushes to `main` are never cancelled. |
| Runner | `ubuntu-24.04`, 15-minute timeout per job. |
| Matrix | Python `3.11`, `3.12`, `3.13`, `3.14`, with `fail-fast: false`. |
| Environment | `UV_PYTHON` is set to the matrix Python, so uv uses the interpreter that `actions/setup-python` installed. |
| Actions | `actions/checkout` v7.0.1, `actions/setup-python` v7.0.0, `astral-sh/setup-uv` v10.2.0 (uv cache enabled and pruned), each pinned by commit SHA. |
| Steps | Install, test, lint, format check, type check: the CI column of the [command reference](cli.md#summary). |

The uv version CI uses is not pinned. With no `version` input and no `required-version` in `pyproject.toml`, `setup-uv` installs the latest uv release (per the [setup-uv README](https://github.com/astral-sh/setup-uv), checked 2026-10-05).

## `.github/dependabot.yml`

| Ecosystem | Schedule | Cooldown |
| --- | --- | --- |
| `uv` (updates `uv.lock`) | Weekly | 7 days after a release before it is proposed |
| `github-actions` (updates the pinned SHAs and their version comments) | Weekly | 7 days |

The cooldown applies to version updates only; security updates are not delayed.

## `skills-lock.json`

Records the source (`wshobson/agents` on GitHub) and content hash of the AI-agent skill vendored under `.agents/skills/python-performance-optimization/`. No tool in this repository reads it.
