# Contributing

How to set up a development environment, the checks a change must pass, and the conventions the history follows. AI coding agents should also follow [`AGENTS.md`](AGENTS.md).

Everyone who takes part in this project is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Set up

Follow [Getting started](docs/getting-started.md) through step 4. To add a solution, follow [Adding a day](docs/guides/adding-a-day.md).

## Checks

CI runs these five commands on every pull request and every push to `main`, on Python 3.11, 3.12, 3.13 and 3.14. To reproduce CI exactly, run them in this form:

```bash
uv sync --locked --all-groups
uv run --no-sync pytest
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync ty check
```

If the format check fails, `uv run ruff format .` rewrites the files in place. What each command reads and enforces is in the [command reference](docs/reference/cli.md), and why CI uses `--locked` and `--no-sync` is in [Architecture: CI enforces the lock file](docs/architecture/overview.md#ci-enforces-the-lock-file).

A local run tests one Python version, the one in `.venv/`; CI covers all four.

## Inputs

Never commit a real puzzle input. `.gitignore` already ignores everything under `inputs/` except `*.sample.txt`; do not override it with `git add -f`.

## Dependencies

- `uv.lock` pins every package. Commit it together with any change to `pyproject.toml`; after editing `pyproject.toml` by hand, run `uv lock` to update it. CI fails if the two disagree.
- Dependabot opens a pull request each week for newer releases of the locked packages and of the CI actions, once a release is at least 7 days old. Manual upgrades follow the same 7-day rule.

## Commit messages

The history uses [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, with the summary in the imperative mood.

| Type | Used for | Example from the history |
| --- | --- | --- |
| `feat` | A new solution or feature | `feat(day05): Implement Day 05 solution with input parsing, range merging, and tests` |
| `fix` | A bug fix | `fix(pytest): use importlib import mode so a second year's tests collect` |
| `perf` | A faster algorithm with the same answers | `perf(day08): pick the shortest pairs with a heap instead of sorting all of them` |
| `test` | Tests only | `test(day10): pin part 2's sentinel, minimality and error paths` |
| `build` | Tooling, dependencies, `.gitignore` | `build(deps): bump pytest 9.0.3 -> 9.1.1` |
| `ci` | `.github/` workflows and Dependabot | `ci: pin the runner image to ubuntu-24.04` |
| `docs`, `style`, `chore` | Prose, formatting, housekeeping | `docs: tighten prose across solutions` |

Scopes name the area touched: a day (`day08`), a tool (`ruff`, `ty`, `pytest`, `git`) or `deps`. The body explains why the change is needed and how it was verified.

## Pull requests

Work on a branch and open a pull request against `main`. CI must pass before merging. Pull requests are merged with a merge commit.

## Documentation

- Update the affected page under `docs/` in the same pull request as the change it describes.
- [`docs/README.md`](docs/README.md) lists every documentation file. Add a line there when you add a page.
- `ruff format --check` also checks fenced `python` blocks in Markdown files, so format code examples the same way as code.
