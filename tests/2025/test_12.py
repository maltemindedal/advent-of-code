from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, cast

import pytest

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


SQUARE = {0: ["##", "##"]}  # 2x2, area 4


def test_large_region_is_decided_by_area_and_bounds_only() -> None:
    # More than 220 cells or 14 pieces skips the exact search. 49 squares really do fit in 15x15
    # (a 7x7 grid of them), so the shortcut agrees with the truth here.
    assert day12.can_fit_region(SQUARE, (15, 15, [49])) is True
    # 57 * 4 = 228 > 225 cells: rejected by the area check.
    assert day12.can_fit_region(SQUARE, (15, 15, [57])) is False
    # A 2x120 region has 240 cells, but a 3x3 shape cannot fit its width.
    assert day12.can_fit_region({0: ["###", "###", "###"]}, (2, 120, [1])) is False


def test_area_check_is_exact_at_the_boundary() -> None:
    single_cell = {0: ["#"]}
    assert day12.can_fit_region(single_cell, (15, 15, [225])) is True  # exactly fills the region
    assert day12.can_fit_region(single_cell, (15, 15, [226])) is False  # one cell too many


def test_mirror_images_are_allowed() -> None:
    # Three S-tetrominoes fit in 4x4 only if some are mirrored into Z shapes (brute-forced).
    assert day12.can_fit_region({0: ["##.", ".##"]}, (4, 4, [3])) is True


def test_small_region_uses_the_exact_search() -> None:
    assert day12.can_fit_region(SQUARE, (4, 4, [4])) is True  # four squares tile 4x4
    assert day12.can_fit_region(SQUARE, (5, 5, [5])) is False  # area fits (20 <= 25), packing not
    assert day12.can_fit_region({0: ["###"]}, (1, 3, [1])) is True  # rotated to fit
    # 14x15 = 210 cells is still under the 220-cell cutoff, so the exact search runs: two 8x8
    # squares cannot both fit (that would need 16 free columns or rows), which only it can tell.
    assert day12.can_fit_region({0: ["#" * 8] * 8}, (14, 15, [2])) is False


def test_shapes_with_the_same_id_are_not_confused() -> None:
    bar = {0: ["###"]}  # 1x3
    region = (3, 1, [1])
    assert day12.can_fit_region(bar, region) is True
    assert day12.can_fit_region(SQUARE, region) is False  # 2x2 is too tall for a 3x1 region
    assert day12.can_fit_region(bar, region) is True


def test_invalid_shapes_raise_every_time() -> None:
    for _ in range(2):
        with pytest.raises(ValueError, match="Shape has no occupied cells"):
            day12.can_fit_region({0: ["..", ".."]}, (2, 2, [1]))
        with pytest.raises(ValueError, match="Missing shape 1"):
            day12.can_fit_region(SQUARE, (4, 4, [1, 1]))
