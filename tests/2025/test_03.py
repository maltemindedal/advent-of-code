from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import load_day
from utils.io import read_input_lines


class Day03Module(Protocol):
    def parse_input(self, lines: list[str]) -> object: ...

    def part1(self, banks: object) -> int: ...

    def part2(self, banks: object) -> int: ...

    def max_bank_joltage(self, bank: str) -> int: ...

    def _max_joltage_k_digits(self, digits: str, k: int) -> int: ...


day03 = cast(Day03Module, load_day(2025, 3))


def test_sample_total_joltage() -> None:
    lines = read_input_lines(2025, 3, variant="sample")
    banks = day03.parse_input(lines)
    assert day03.part1(banks) == 357
    assert day03.part2(banks) == 3121910778619


def test_bank_maximum_in_order() -> None:
    assert day03.max_bank_joltage("12345") == 45
    assert day03.max_bank_joltage("818181911112111") == 92
    assert day03.max_bank_joltage("21") == 21


def test_max_k_digits_helper_general() -> None:
    helper = day03._max_joltage_k_digits
    # Pick 12 digits from the descending sequence, followed by ones.
    assert helper("987654321111111", 12) == 987654321111
    # Ensure drops trim from the end when no better digit appears.
    assert helper("111234", 3) == 234
    # Ensure the greedy algorithm keeps digits in order across increases and drops.
    assert helper("818181911112111", 12) == 888911112111
