from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import PROJECT_ROOT, load_module

DAY06_PATH = PROJECT_ROOT / "2025" / "06" / "main.py"


class ProblemLike(Protocol):
    numbers: list[int]
    op: str


class Day06Module(Protocol):
    def parse_input(self, lines: list[str]) -> list[ProblemLike]: ...

    def parse_input_columns(self, lines: list[str]) -> list[ProblemLike]: ...

    def part1(self, problems: list[ProblemLike]) -> int: ...

    def part2(self, lines: list[str]) -> int: ...


day06 = cast(Day06Module, load_module("aoc2025_day06", DAY06_PATH))


def test_sample_grand_total_matches_description() -> None:
    worksheet = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  ",
    ]

    problems = day06.parse_input(worksheet)
    assert len(problems) == 4
    assert day06.part1(problems) == 4_277_556
    assert day06.part2(worksheet) == 3_263_827


def test_parser_handles_extra_spacing_between_problems() -> None:
    lines = [
        " 7    81  ",
        "33    2   ",
        " 5    19  ",
        " *    +   ",
    ]
    problems = day06.parse_input(lines)
    assert [p.numbers for p in problems] == [[7, 33, 5], [81, 2, 19]]
    assert [p.op for p in problems] == ["*", "+"]
    assert day06.part1(problems) == (7 * 33 * 5) + (81 + 2 + 19)


def test_column_parsing_reads_right_to_left() -> None:
    lines = [
        "12 78",
        "34 56",
        " *  +",
    ]

    problems = day06.parse_input_columns(lines)
    # Read columns from right to left, starting with the rightmost problem.
    assert [p.numbers for p in problems] == [[86, 75], [24, 13]]
    assert [p.op for p in problems] == ["+", "*"]
    assert day06.part2(lines) == (86 + 75) + (24 * 13)
