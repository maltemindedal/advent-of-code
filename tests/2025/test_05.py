from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import load_day
from utils.io import read_input_lines


class IdRangeFactory(Protocol):
    def __call__(self, start: int, end: int) -> object: ...


class Day05Module(Protocol):
    IdRange: IdRangeFactory

    def parse_input(self, lines: list[str]) -> tuple[list[object], list[int]]: ...

    def part1(self, ranges: list[object], ids: list[int]) -> int: ...

    def part2(self, ranges: list[object]) -> int: ...


day05 = cast(Day05Module, load_day(2025, 5))


def test_sample_fresh_and_spoiled_counts() -> None:
    lines = read_input_lines(2025, 5, variant="sample")
    ranges, ids = day05.parse_input(lines)
    assert day05.part1(ranges, ids) == 3
    assert day05.part2(ranges) == 14


def test_overlapping_ranges_merge_and_count() -> None:
    ranges = [
        day05.IdRange(1, 3),
        day05.IdRange(5, 7),
        day05.IdRange(3, 5),
    ]
    ids = [1, 3, 4, 5, 7, 8]
    assert day05.part1(ranges, ids) == 5
    assert day05.part2(ranges) == 7


def test_empty_ranges_or_ids_handle() -> None:
    empty_ranges: list[object] = []
    empty_ids: list[int] = []

    assert day05.part1(empty_ranges, [1, 2, 3]) == 0
    assert day05.part2(empty_ranges) == 0
    assert day05.part1([day05.IdRange(10, 20)], empty_ids) == 0
