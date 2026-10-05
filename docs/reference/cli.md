# Command reference

Every command this repository uses, what it reads, and the exact form CI runs. Run all commands from the repository root unless noted.

The project defines no custom scripts (no Makefile, task runner or `[project.scripts]` entry). Every command is a `uv` invocation of a standard tool.

## Summary

| Task | Local command | CI command (`.github/workflows/ci.yml`) |
| --- | --- | --- |
| Install dependencies | `uv sync` | `uv sync --locked --all-groups` |
| Run tests | `uv run pytest` | `uv run --no-sync pytest` |
| Lint | `uv run ruff check .` | `uv run --no-sync ruff check .` |
| Format | `uv run ruff format .` | `uv run --no-sync ruff format --check .` |
| Type-check | `uv run ty check` | `uv run --no-sync ty check` |
| Run a day | `uv run python 2025/01/main.py` | not run in CI |

### `uv run` versus `uv run --no-sync`

Plain `uv run` re-locks and syncs the environment before it runs the command. If `pyproject.toml` changed, it rewrites `uv.lock` without saying so. `uv run --no-sync` runs against the environment as it is. CI pairs `--no-sync` with `uv sync --locked`, so a lock file that no longer matches `pyproject.toml` fails the build instead of being repaired silently.

## `uv sync`

Creates `.venv/` and installs the locked dependencies.

- Installs the runtime dependency (`z3-solver`) and the `dev` dependency group (`pytest`, `ruff`, `ty`). The `dev` group is the only group, so `uv sync` and `uv sync --all-groups` install the same packages.
- Installs the project itself in editable mode. This puts the repository root on `sys.path`, which is what lets `2025/NN/main.py` run `from utils.io import ...`. See [Architecture overview](../architecture/overview.md#how-imports-resolve).
- `--locked` fails with "The lockfile at `uv.lock` needs to be updated" when `uv.lock` does not match `pyproject.toml`.

## `uv run pytest`

Runs the test suite under `tests/` in strict mode, with warnings treated as errors. The settings are listed under [`[tool.pytest]`](configuration.md#toolpytest).

Run a subset with the usual pytest arguments:

```bash
uv run pytest tests/2025/test_01.py   # one file
uv run pytest tests/test_cli.py       # every day's printed sample output
```

The suite does not need any real puzzle input; it reads only the committed `*.sample.txt` files.

## `uv run ruff check .`

Lints every Python file in the repository with the rule families listed under [`[tool.ruff]`](configuration.md#toolruff).

## `uv run ruff format .`

Formats Python files in place. With `--check` (the CI form) it reports unformatted files and changes nothing.

> **Note:** ruff 0.16 also formats fenced `python` code blocks inside Markdown files, including everything under `docs/`. A badly formatted snippet in a `.md` file fails CI's `ruff format --check`.

## `uv run ty check`

Type-checks the repository with every ty rule set to `error`. The settings, including which suppression comments count, are listed under [`[tool.ty]`](configuration.md#toolty).

## Running a day

```bash
uv run python 2025/01/main.py
```

Each `main.py` calls `run()` with no arguments, which reads the real input `inputs/2025/01.txt` and prints the answers. The command works from any directory inside the repository (adjust the path to `main.py`): `uv run` finds the project by searching upward, and input paths are resolved relative to the `utils` package, not the current directory. Run from outside the repository, `uv run` does not find the project and the import of `utils` fails.

If the real input is missing, the script exits with a traceback that ends in:

```text
FileNotFoundError: Input for 2025 day 1 not found at <repo>/inputs/2025/01.txt. Create it or adjust the path.
```

The script has no command-line flags. To run a day against a sample or another variant input, call `run(variant)` instead:

```bash
uv run python -c "import runpy; runpy.run_path('2025/01/main.py')['run']('sample')"
```

```text
Part 1: 3
Part 2: 6
```

`runpy.run_path` loads the file without triggering its `if __name__ == "__main__":` block, so only the explicit `run('sample')` call executes. More ways to run a day are in [Running a day](../guides/running-a-day.md).
