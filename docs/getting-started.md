# Getting started

This tutorial takes you from a fresh clone to running a solution on your own puzzle input, in about ten minutes. You need a terminal and an [Advent of Code](https://adventofcode.com/) account for the last step.

## 1. Install the prerequisites

| Tool | Version | Check with |
| --- | --- | --- |
| Git | any | `git --version` |
| Python | 3.11 or later | `python3 --version` |
| uv | no minimum is pinned; verified with 0.8.17 | `uv --version` |

> **TODO(verify):** the oldest uv release that can read this repository's `uv.lock` (lock format `version = 1`, `revision = 3`) has not been established.

To install uv, follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/). Two of the methods it lists (checked 2026-10-05):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # standalone installer (macOS, Linux)
pipx install uv                                  # from PyPI
```

## 2. Clone the repository

```bash
git clone https://github.com/maltemindedal/advent-of-code.git
cd advent-of-code
```

Every later command runs from this directory.

## 3. Install the dependencies

```bash
uv sync
```

uv creates a virtual environment in `.venv/` and installs the solver library `z3-solver` and the development tools `pytest`, `ruff` and `ty`, at the versions locked in `uv.lock`. It also installs the repository itself, which is what lets every solution import the shared `utils` package.

## 4. Run the tests

```bash
uv run pytest
```

The run ends with a summary line such as:

```text
============================= 112 passed in 8.27s ==============================
```

The count was 112 on 2026-10-05 and grows as days and tests are added. The tests need no puzzle input of your own: they use the sample inputs committed under `inputs/2025/`.

## 5. Run a solution on the sample input

Each day's solution lives in `2025/<DD>/main.py`. Its `run` function takes the name of an input variant. Run day 1 against its sample:

```bash
uv run python -c "import runpy; runpy.run_path('2025/01/main.py')['run']('sample')"
```

```text
Part 1: 3
Part 2: 6
```

This read `inputs/2025/01.sample.txt`, the sample input committed with the repository.

## 6. Run a solution on your own input

Real puzzle inputs are not committed to the repository, so you add your own.

1. Sign in at [adventofcode.com](https://adventofcode.com/), open the 2025 day 1 puzzle and open its input.
2. Save the page's text as `inputs/2025/01.txt`.
3. Run the day as a script:

   ```bash
   uv run python 2025/01/main.py
   ```

   It prints the same two lines, `Part 1: <answer>` and `Part 2: <answer>`, with your answers.

Git ignores the file you saved, so it cannot be committed by accident:

```bash
git status --short inputs/
```

prints nothing. Puzzle inputs are not meant to be republished; only files ending in `.sample.txt` are tracked.

## Next steps

- [Running a day](guides/running-a-day.md): other input variants, and calling `part1`/`part2` directly.
- [Adding a day](guides/adding-a-day.md): write your own solution with tests.
- [Contributing](../CONTRIBUTING.md): the checks CI runs.
