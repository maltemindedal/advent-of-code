from __future__ import annotations

from typing import Protocol, cast

import pytest

from tests._helpers import find_days, load_day

# `run("sample")` output per (year, day). Pins the printed labels and the YEAR/DAY wiring that
# the day-level tests bypass. In 2025, day 8 part 1 is 20 (not the puzzle's 40) because `run`
# uses the default 1000 pairs; day 11 part 2 is 0 because the sample is the part 1 example and
# has no `svr` node; day 12 prints `Solution:` instead of `Part 1:`/`Part 2:`.
EXPECTED_SAMPLE_OUTPUT = {
    (2025, 1): "Part 1: 3\nPart 2: 6\n",
    (2025, 2): "Part 1: 1227775554\nPart 2: 4174379265\n",
    (2025, 3): "Part 1: 357\nPart 2: 3121910778619\n",
    (2025, 4): "Part 1: 13\nPart 2: 43\n",
    (2025, 5): "Part 1: 3\nPart 2: 14\n",
    (2025, 6): "Part 1: 4277556\nPart 2: 3263827\n",
    (2025, 7): "Part 1: 21\nPart 2: 40\n",
    (2025, 8): "Part 1: 20\nPart 2: 25272\n",
    (2025, 9): "Part 1: 50\nPart 2: 24\n",
    (2025, 10): "Part 1: 7\nPart 2: 33\n",
    (2025, 11): "Part 1: 5\nPart 2: 0\n",
    (2025, 12): "Solution: 2\n",
}


class RunnableDay(Protocol):
    YEAR: int
    DAY: int

    def run(self, variant: str | None = None) -> None: ...


def test_every_day_has_pinned_output() -> None:
    # A day missing from the table would otherwise go untested here.
    assert sorted(EXPECTED_SAMPLE_OUTPUT) == find_days()


@pytest.mark.parametrize(("year", "day"), sorted(EXPECTED_SAMPLE_OUTPUT))
def test_run_prints_sample_answers(year: int, day: int, capsys: pytest.CaptureFixture[str]) -> None:
    module = cast(RunnableDay, load_day(year, day))
    # `run` finds its input from these constants, not from its path.
    assert (module.YEAR, module.DAY) == (year, day)
    module.run("sample")
    assert capsys.readouterr().out == EXPECTED_SAMPLE_OUTPUT[year, day]
