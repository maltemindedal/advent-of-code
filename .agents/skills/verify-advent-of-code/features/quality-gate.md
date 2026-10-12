# Pre-PR gate

## Sub-features

- `pytest`, `ruff check`, `ruff format --check` (also fenced python blocks in Markdown), and `ty check`, in CI's order.

## How to get to it (user POV)

The gate in `AGENTS.md`. CI runs it on Python 3.11 to 3.14.

## Driving it with verify.sh

`verify.sh test`. Every step must exit 0. The pytest summary line is printed.

## Gotchas

- Locally only the `.venv` interpreter runs.
