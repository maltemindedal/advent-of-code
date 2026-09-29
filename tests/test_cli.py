from __future__ import annotations

from typing import Protocol, cast

import pytest

from tests._helpers import PROJECT_ROOT, load_module

# `run("sample")` output per day. Pins the printed labels and the YEAR/DAY wiring that the
# day-level tests bypass. Day 8 part 1 is 20 (not the puzzle's 40) because `run` uses the
# default 1000 pairs; day 11 part 2 is 0 because the sample is the part 1 example and has no
# `svr` node; day 12 prints `Solution:` instead of `Part 1:`/`Part 2:`.
EXPECTED_SAMPLE_OUTPUT = {
    1: "Part 1: 3\nPart 2: 6\n",
    2: "Part 1: 1227775554\nPart 2: 4174379265\n",
    3: "Part 1: 357\nPart 2: 3121910778619\n",
    4: "Part 1: 13\nPart 2: 43\n",
    5: "Part 1: 3\nPart 2: 14\n",
    6: "Part 1: 4277556\nPart 2: 3263827\n",
    7: "Part 1: 21\nPart 2: 40\n",
    8: "Part 1: 20\nPart 2: 25272\n",
    9: "Part 1: 50\nPart 2: 24\n",
    10: "Part 1: 7\nPart 2: 33\n",
    11: "Part 1: 5\nPart 2: 0\n",
    12: "Solution: 2\n",
}


class RunnableDay(Protocol):
    def run(self, variant: str | None = None) -> None: ...


@pytest.mark.parametrize("day", sorted(EXPECTED_SAMPLE_OUTPUT))
def test_run_prints_sample_answers(day: int, capsys: pytest.CaptureFixture[str]) -> None:
    path = PROJECT_ROOT / "2025" / f"{day:02d}" / "main.py"
    module = cast(RunnableDay, load_module(f"aoc2025_day{day:02d}_cli", path))
    module.run("sample")
    assert capsys.readouterr().out == EXPECTED_SAMPLE_OUTPUT[day]
