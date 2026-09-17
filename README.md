# Advent of Code (multi-year)

Monorepo for Advent of Code solutions using Python and [uv](https://docs.astral.sh/uv/).

## Layout

- `2025/01/`, `2025/02/`, ...: year/day solution folders. Add another top-level folder for a new year.
- `inputs/<year>/<day>.txt`: puzzle inputs. Add variants such as `01.sample.txt` with a `.<variant>.txt` suffix.
- `utils/`: reusable I/O and algorithm helpers.
- `tests/`: regression tests for each day.
- `uv.lock`: locked dependency graph managed by `uv`.

## Requirements

- Python 3.11 or later. Python 3.12 is supported.
- Install uv with `pipx install uv` or follow the documentation linked above.

## Getting started

```bash
uv sync                        # install dependencies (project + dev)
uv run pytest                  # run tests
uv run ruff check .            # lint the repo
uv run ruff format .           # format the repo
uv run ty check                # strict type checking
uv run python 2025/01/main.py  # run a day from the repo root
```

## Adding a new day/year

1. Copy an existing day folder such as `2025/01` into the appropriate year and day slot.
2. Drop your input into `inputs/<year>/<day>.txt` (and `<day>.sample.txt` for samples).
3. Implement `part1` and `part2`, and add typed tests under `tests/`.

## Quality checks

This repo uses `uv`, `ruff` for formatting and linting, and `ty` for type checking with all rules enabled. Run these checks locally:

```bash
uv sync
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
```
