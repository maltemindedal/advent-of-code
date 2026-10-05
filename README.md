# Advent of Code

[![CI](https://github.com/maltemindedal/advent-of-code/actions/workflows/ci.yml/badge.svg)](https://github.com/maltemindedal/advent-of-code/actions/workflows/ci.yml)

Malte Mindedal's Python solutions to [Advent of Code](https://adventofcode.com/) puzzles, kept in one project across years.

Each puzzle day is a standalone script that parses its input, solves both parts and prints the answers. A small shared `utils` package locates and reads input files, and every day has tests that run on the sample input committed with it. The project is managed with [uv](https://docs.astral.sh/uv/), and CI tests it on Python 3.11 to 3.14 under strict ruff and ty checks. It currently contains 2025 days 1 to 12.

## Quick start

Prerequisites: Git, Python 3.11 or later, and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/maltemindedal/advent-of-code.git
cd advent-of-code
uv sync          # create .venv/ and install the locked dependencies
uv run pytest    # run the test suite; every test passes on a fresh clone
```

Run day 1 on its committed sample input:

```bash
uv run python -c "import runpy; runpy.run_path('2025/01/main.py')['run']('sample')"
```

```text
Part 1: 3
Part 2: 6
```

## Usage

Save your own puzzle input as `inputs/<year>/<DD>.txt`, for example `inputs/2025/01.txt`, and run the day as a script:

```bash
uv run python 2025/01/main.py
```

```text
Part 1: <your answer>
Part 2: <your answer>
```

Git ignores real inputs; only `*.sample.txt` files are committed.

## Documentation

| Section | Contents |
| --- | --- |
| [Getting started](docs/getting-started.md) | Tutorial: from a fresh clone to an answer for your own input. |
| [How-to guides](docs/README.md#how-to-guides) | Running a day on any input; adding a day or a year. |
| [Reference](docs/README.md#reference) | Commands, configuration, the `utils` API, the day modules. |
| [Architecture](docs/architecture/overview.md) | How the parts fit together, and why. |

The full index is [docs/README.md](docs/README.md).

## Project structure

```text
2025/            solutions, one folder per day: 2025/01/main.py to 2025/12/main.py
inputs/          puzzle inputs by year; only <DD>.sample.txt files are tracked
utils/           shared package: input file I/O and typed z3 wrappers
tests/           pytest suite: per-day tests in tests/<year>/, plus utils and output tests
docs/            documentation
.github/         CI workflow and Dependabot configuration
.agents/         a vendored skill for AI coding agents
AGENTS.md        guidelines for AI coding agents
pyproject.toml   project metadata and tool configuration
uv.lock          locked dependency versions
```

## Contributing

See [Contributing](docs/contributing.md) for the checks CI runs and the conventions for commits and pull requests.

## License

The repository does not include a license file.
