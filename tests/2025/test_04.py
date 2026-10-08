from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import load_day
from utils.io import read_input_lines


class Day04Module(Protocol):
    def parse_input(self, lines: list[str]) -> object: ...

    def part1(self, grid: object) -> int: ...

    def part2(self, grid: object) -> int: ...


day04 = cast(Day04Module, load_day(2025, 4))


def test_sample_accessible_rolls() -> None:
    lines = read_input_lines(2025, 4, variant="sample")
    grid = day04.parse_input(lines)
    assert day04.part1(grid) == 13
    assert day04.part2(grid) == 43


def test_edge_cells_count_neighbours_correctly() -> None:
    # Only the center has eight neighbours; the other cells have fewer.
    grid = day04.parse_input(
        [
            "@@@",
            "@@@",
            "@@@",
        ]
    )
    # The center has eight neighbours and is not accessible. The corners have three,
    # while the edges have five. Only the four corners are accessible.
    assert day04.part1(grid) == 4


def test_iterative_removal_clears_full_block() -> None:
    grid = day04.parse_input(
        [
            "@@@",
            "@@@",
            "@@@",
        ]
    )
    # Removals cascade until all nine rolls are gone.
    assert day04.part2(grid) == 9
