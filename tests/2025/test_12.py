from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, cast

from tests._helpers import PROJECT_ROOT, load_module
from utils.io import read_input_lines

DAY12_PATH = PROJECT_ROOT / "2025" / "12" / "main.py"


class ParsedInputLike(Protocol):
    shapes: object
    regions: Sequence[object]


class Day12Module(Protocol):
    def parse_input(self, lines: list[str]) -> ParsedInputLike: ...

    def part1(self, parsed: ParsedInputLike) -> int: ...

    def can_fit_region(self, shapes: object, region: object) -> bool: ...


day12 = cast(Day12Module, load_module("aoc2025_day12", DAY12_PATH))


def test_sample_part1_count_fit_regions() -> None:
    lines = read_input_lines(2025, 12, variant="sample")
    parsed = day12.parse_input(lines)
    assert day12.part1(parsed) == 2


def test_sample_third_region_is_impossible_exact() -> None:
    lines = read_input_lines(2025, 12, variant="sample")
    parsed = day12.parse_input(lines)

    # The sample input has three regions, and the third is impossible.
    assert len(parsed.regions) == 3
    assert day12.can_fit_region(parsed.shapes, parsed.regions[0]) is True
    assert day12.can_fit_region(parsed.shapes, parsed.regions[1]) is True
    assert day12.can_fit_region(parsed.shapes, parsed.regions[2]) is False


def test_area_pruning_rejects_obvious_overflow() -> None:
    # Single 3x3 full shape in a 2x2 region cannot fit.
    parsed = day12.parse_input(
        [
            "0:",
            "###",
            "###",
            "###",
            "",
            "2x2: 1",
        ]
    )
    assert day12.part1(parsed) == 0
