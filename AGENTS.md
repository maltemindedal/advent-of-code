# AGENTS.md

Malte Mindedal's Advent of Code solutions in one uv project: each day is a standalone script, `<year>/<DD>/main.py`, that reads `inputs/<year>/<DD>[.<variant>].txt` and prints its answers, with `utils/` as the only shared code. A change has to keep every day's printed answers, keep real puzzle inputs out of git, and pass ruff and ty at full strictness against the committed `uv.lock`.

## Commands

Run everything from the repo root through `uv`: day scripts import `utils` via the project's editable install, so a bare `python 2025/01/main.py` fails with `ModuleNotFoundError`.

Pre-PR gate, exactly what CI runs (`.github/workflows/ci.yml` runs it on Python 3.11 to 3.14; locally it covers only the `.venv` interpreter):

```bash
uv sync --locked --all-groups
uv run --no-sync pytest
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync ty check
```

- One test: `uv run --no-sync pytest tests/2025/test_01.py::test_sample_parts`
- One day's printed output: `uv run --no-sync pytest 'tests/test_cli.py::test_run_prints_sample_answers[7]'` (the id is the unpadded day).
- A day on its committed sample: `uv run python -c "import runpy; runpy.run_path('2025/01/main.py')['run']('sample')"`

## Conventions

Day modules:

- A new day touches `<year>/<DD>/main.py`, `inputs/<year>/<DD>.sample.txt`, `tests/<year>/test_<DD>.py`, (for 2025) an entry in `EXPECTED_SAMPLE_OUTPUT` in `tests/test_cli.py`, the tables in `docs/reference/day-modules.md`, and the day count in `README.md`.
- Set `YEAR` and `DAY` to match the folder, also when copying an existing day: `run()` finds the input from them, not from the path.
- `run(variant: str | None = None)` is the only function that prints, exactly `Part 1: <answer>` and `Part 2: <answer>`. Put tuning knobs in keyword defaults on `part1`/`part2` (day 8's `pairs_to_connect=1000`); scripts take no command-line flags.
- Model parsed records as `@dataclass(frozen=True)`, prefix helpers with `_`, and reject malformed input with a descriptive `ValueError`, the only exception type day code raises.
- Start every `.py` file except `__init__.py` with `from __future__ import annotations`. Keep the `sys.modules` registration in `tests/_helpers.py`'s `load_module`: frozen dataclasses with postponed annotations need their module registered.
- Docstrings are optional; when a function has one, follow it with one blank line.
- Pin before you optimise: a `test(dayNN)` commit adds a naive reference implementation to the test file and compares against it on inputs from `random.Random(20250928)`, then a separate `perf(dayNN)` commit changes the solution (`cc760bb`, then `123d67a`).
- Report unused public code (day 8's `manhattan`, `make_solver` and `Expr` in `utils/z3_helpers.py`, the `available_ids` parameter of day 5's `part2`) instead of deleting it; remove only what your own change left unused.

Commits and pull requests:

- Conventional Commits, `type(scope): summary`, with a lowercase imperative summary (`perf(day08): pick the shortest pairs with a heap instead of sorting all of them`); types and scopes are in `CONTRIBUTING.md`. One logical change per commit.
- The body says why, then ends with a `Verified:` paragraph naming the commands run and the test count. Every number in a commit message or doc must be reproducible from the commands it names.
- Open a PR against `main`: CI runs only on PRs and pushes to `main`, so a pushed branch alone runs nothing. Shape the body on `.github/pull_request_template.md`; `gh pr create --body` does not insert it.
- Merge with a merge commit (`gh pr merge --merge`): docs and commit messages cite commits by hash. Confirm `gh pr checks` is green first, since no branch rule stops a red PR from merging.
- Update the affected `docs/` page in the same PR, and list any new page in `docs/README.md`. Community files (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`) live at the root.
- When a doc states an outside fact (a tool default, a third-party page), add the date you checked it ("checked 2026-10-05"); write `TODO(verify)` where you could not confirm it.

Dependencies:

- Run `uv lock` after editing `pyproject.toml` and commit both files together; CI's `--locked` install fails on a mismatch.
- ty is 0.0.x with `all = "error"`, so a ty bump can add failing rules: read its changelog and raise the floor to the version you verified. Keep the `z3-solver>=4.12.4` floor low: the suite passes on 4.12.4.0.
- Leave release timing to Dependabot's default cooldown. The owner removed the 7-day `cooldown` and the waiting rule for manual upgrades in `b9f512f`; add no cooldown, `exclude-newer` or release-age rule.

## Gotchas

- Commit only the puzzle's example input, saved as `inputs/<year>/<DD>.sample.txt`. `.gitignore` ignores every other file under `inputs/`, so the filename is the only protection; never `git add -f` there. Copy no puzzle text beyond the example: the samples are a deliberate exception, excluded from the MIT license.
- No real input, fetch tool or session cookie exists in the repo or CI. Verify on samples and tests, and leave real-input runs to the owner.
- Plain `uv run` silently rewrites `uv.lock` after a `pyproject.toml` edit, so check `git status` for it before committing.
- `ruff format --check .` also checks fenced `python` blocks in every Markdown file, this one and `docs/` included. Write code examples already formatted.
- Suppress a ty diagnostic only with `# ty: ignore[<rule>]`; `# type: ignore` is not honoured. The tree has no ty suppressions; fix the type where you can.
- Deliberate behaviour pinned by tests, not bugs: on the sample, day 8 prints `Part 1: 20` (`run` uses 1000 pairs; the puzzle's 40 needs `pairs_to_connect=10`), day 11 prints `Part 2: 0`, and day 12 prints one `Solution:` line. Day 10's `INF = 10**18` sentinel and day 12's area-only shortcut for regions over 220 cells or 14 pieces are deliberate too.
- Treat `.agents/skills/` as vendored: `skills-lock.json` holds a hash of its files, so editing or reformatting them leaves the lock stale.

## Docs

- Before adding a day or the first day of a new year, read `docs/guides/adding-a-day.md`: skeletons for `main.py` and its test that already pass ruff and ty, including the `load_day` call and `Protocol` the test needs.
- Before changing a day's signature or printed output, read `docs/reference/day-modules.md`, and update it in the same change.
- Before changing `utils/`, read `docs/reference/api.md`.
- Before changing structure, imports, test layout or CI, read `docs/architecture/overview.md`; each design decision names the commit holding its full rationale (`git show <hash>`).
- When changing `pyproject.toml` (dependencies included), `.gitignore`, `.editorconfig`, CI or Dependabot, update `docs/reference/configuration.md`; its locked-version table lags Dependabot's bumps.
- To call `part1`/`part2` with other arguments (day folders are not importable packages) or to debug an input-path error, read `docs/guides/running-a-day.md`.
