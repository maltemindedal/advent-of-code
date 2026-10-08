# Adding a day

How to add a solution for a new puzzle day, including the first day of a new year. The examples add 2026 day 1; substitute your year and day. Run every command from the repository root.

The structure the module must follow is specified in [Day modules: module layout](../reference/day-modules.md#module-layout).

## 1. Create the module

```bash
mkdir -p 2026/01
```

Create `2026/01/main.py` with this skeleton. It already satisfies ruff and ty, so you can start with a green check run:

```python
from __future__ import annotations

from utils.io import read_input_lines

YEAR = 2026
DAY = 1


def parse_input(lines: list[str]) -> list[str]:
    """Return the non-empty input lines."""

    return [line for line in lines if line.strip()]


def part1(data: list[str]) -> int:
    """Solve part 1."""

    return 0


def part2(data: list[str]) -> int:
    """Solve part 2."""

    return 0


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    data = parse_input(lines)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")


if __name__ == "__main__":
    run()
```

Set `YEAR` and `DAY` to match the folder: `run` uses them, not the path, to find the input.

## 2. Add the inputs

```bash
mkdir -p inputs/2026
```

- Paste the example from the puzzle description into `inputs/2026/01.sample.txt`. Git tracks it, and the tests use it.
- Save your own input as `inputs/2026/01.txt`. Git ignores it.

## 3. Write the tests

Create `tests/2026/test_01.py`. No `__init__.py` is needed in `tests/2026/`; pytest's importlib import mode keeps `tests/2026/test_01.py` apart from `tests/2025/test_01.py`.

```python
from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import load_day
from utils.io import read_input_lines


class Day01Module(Protocol):
    def parse_input(self, lines: list[str]) -> list[str]: ...

    def part1(self, data: list[str]) -> int: ...

    def part2(self, data: list[str]) -> int: ...


day01 = cast(Day01Module, load_day(2026, 1))


def test_sample_parts() -> None:
    data = day01.parse_input(read_input_lines(2026, 1, variant="sample"))
    assert day01.part1(data) == 0  # replace 0 with the example answer from the puzzle
    assert day01.part2(data) == 0
```

Two details matter:

- `load_day(2026, 1)` loads `2026/01/main.py` and registers it in `sys.modules` as `aoc2026_day01`, so two years' modules never replace each other. It loads each day once per test session, so every test file that asks for the same day gets the same module.
- The `Protocol` gives ty the module's types. Declare every function the tests call.

Then replace the `0`s with the example answers from the puzzle description and run the test. It fails until the solution is right:

```bash
uv run pytest tests/2026/test_01.py
```

## 4. Pin the printed output

`tests/test_cli.py` runs `run("sample")` for every day in its `EXPECTED_SAMPLE_OUTPUT` table, checks that the module's `YEAR` and `DAY` match its folder, and compares the printed text. Add an entry keyed by year and day:

```python
EXPECTED_SAMPLE_OUTPUT = {
    # ...
    (2025, 12): "Solution: 2\n",
    (2026, 1): "Part 1: <answer>\nPart 2: <answer>\n",
}
```

The entry is required: `test_every_day_has_pinned_output` finds every `<year>/<DD>/main.py` in the repository and fails until each one has an entry.

## 5. Implement and check

Implement `parse_input`, `part1` and `part2` until the tests pass, run the day on your input, and then run the full set of checks in [Contributing: checks](../../CONTRIBUTING.md#checks):

```bash
uv run python 2026/01/main.py
```
