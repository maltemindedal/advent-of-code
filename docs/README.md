# Documentation

Every documentation page in this repository, grouped by what you are trying to do. If you are new, start with [Getting started](getting-started.md).

## Tutorials

Learning by doing, for newcomers.

| Page | Covers |
| --- | --- |
| [Getting started](getting-started.md) | Install the tools, run the tests, run a day on its sample, then on your own input. About ten minutes. |

## How-to guides

Steps for a specific task, for anyone who has the project running.

| Page | Covers |
| --- | --- |
| [Running a day](guides/running-a-day.md) | Run a solution on your real input, the sample or another file; call `part1`/`part2` with non-default arguments; common errors. |
| [Adding a day](guides/adding-a-day.md) | Create a day module, its inputs and its tests, including the first day of a new year. |

## Reference

Facts to look up, for readers who know what they need.

| Page | Covers |
| --- | --- |
| [Commands](reference/cli.md) | Every `uv`, pytest, ruff and ty command, in its local and CI forms, and how to run a day. |
| [Configuration](reference/configuration.md) | Every key in `pyproject.toml`, `.gitignore`, `.editorconfig`, the CI workflow and Dependabot. |
| [`utils` API](reference/api.md) | The input file layout, `utils.io` and `utils.z3_helpers`: signatures, behaviour and errors. |
| [Day modules](reference/day-modules.md) | The layout every day module follows; 2025 signatures, sample output and quirks. |

## Explanation

Background and reasoning, for readers who want to understand the design.

| Page | Covers |
| --- | --- |
| [Architecture overview](architecture/overview.md) | Components, data flow, how imports resolve, the testing approach and the reasoning behind the main design decisions. |

## Outside `docs/`

| File | Covers |
| --- | --- |
| [`README.md`](../README.md) | Project summary, quick start and links into these pages. |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Reproduce CI locally; conventions for inputs, dependencies, commits, pull requests and docs. |
| [`SECURITY.md`](../SECURITY.md) | Supported versions and how to report a vulnerability privately. |
| [`LICENSE`](../LICENSE) | MIT License for the code; the README's License section says what it does not cover. |
| [`AGENTS.md`](../AGENTS.md) | Behavioural guidelines for AI coding agents working in the repository. |
