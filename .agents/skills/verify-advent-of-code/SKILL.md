---
name: verify-advent-of-code
description: Verify the Advent of Code solutions by running CI's gate and every `<year>/<DD>/main.py` in its own process on its committed sample, compared byte for byte with the answers pinned in tests/test_cli.py. Use after changing a day, utils/, tests, the lockfile or tooling config.
---

# verify-advent-of-code

The surface is one standalone script per day, `<year>/<DD>/main.py`, whose
`run(variant)` reads `inputs/<year>/<DD>[.<variant>].txt` and prints exactly
`Part 1: <answer>` and `Part 2: <answer>`. There is no app to keep alive:
launch means `uv sync --locked --all-groups`, and each drive is one Python
process per day, started from the repo root through uv (a bare `python` cannot
import `utils`).

## Launch

```bash
.agents/skills/verify-advent-of-code/scripts/verify.sh doctor
```

Ready means the sync exited 0 and Python is at least 3.11. Doctor also counts
the day scripts.

## Doctor

`verify.sh doctor` checks uv, syncs `.venv` as CI does and checks the
interpreter. `all` stops if it fails.

## Drive

```bash
.agents/skills/verify-advent-of-code/scripts/verify.sh test   # pytest, ruff check, ruff format --check, ty (CI order)
.agents/skills/verify-advent-of-code/scripts/verify.sh days   # every day on its sample vs EXPECTED_SAMPLE_OUTPUT
.agents/skills/verify-advent-of-code/scripts/verify.sh real   # every day that has a real input; SKIP when none
.agents/skills/verify-advent-of-code/scripts/verify.sh all    # doctor, test, days, real, cleanup
```

`days` runs `runpy.run_path('<year>/<DD>/main.py')['run']('sample')` in a new
process per day and compares its stdout with that day's entry in
`EXPECTED_SAMPLE_OUTPUT`. A day without an entry fails as `<unpinned>`.

`real` runs only days whose git-ignored `inputs/<year>/<DD>.txt` exists and
checks they exit 0. The repo and CI never hold real inputs, so on a fresh
checkout it reports SKIP and the run ends `RESULT: PASS with SKIP`. There are
no known real answers to compare against, so leave answer checks to the owner.

## Evidence

Each step leaves `<name>.cmd`, `.stdout`, `.stderr` and `.exit` under
`/tmp/advent-of-code-verify/<run-id>/` (override with `VERIFY_RUN` or
`VERIFY_ARTIFACTS`). Each day also gets `day-<year>-<DD>.expected` next to its
stdout, so `diff` shows any mismatch. Quote the `RESULT:` line, the pytest
summary and `N of M days match`.

## Cleanup

`verify.sh cleanup` starts nothing and deletes nothing. Evidence stays.

## Feature map

See [features/README.md](features/README.md).
