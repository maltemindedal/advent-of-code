from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from utils.io import read_input_lines

YEAR = 2025
DAY = 2


@dataclass(frozen=True)
class IdRange:
    start: int
    end: int


def parse_input(lines: list[str]) -> list[IdRange]:
    """Parse comma-separated ranges like "11-22,95-115" into IdRange objects."""

    ranges: list[IdRange] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for chunk in line.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            parts = chunk.split("-")
            if len(parts) != 2:
                raise ValueError(f"Invalid range token: {chunk}")
            start, end = map(int, parts)
            if start > end:
                start, end = end, start
            ranges.append(IdRange(start, end))
    return ranges


def _repeated_twice_values(start: int, end: int) -> Iterable[int]:
    """Yield numbers in [start, end] that repeat a digit block exactly twice.

    A valid number has an even digit length 2k and looks like ``dd...dd`` (k digits twice),
    with no leading zeros. Candidate bases avoid scanning every integer in the interval.
    """

    min_len = len(str(start))
    max_len = len(str(end))

    for length in range(min_len, max_len + 1):
        if length % 2:
            continue  # must be even length

        half = length // 2
        factor = 10**half + 1  # repeated value = base * factor

        base_lower_bound = (start + factor - 1) // factor  # ceil(start / factor)
        base_upper_bound = end // factor

        base_min = 10 ** (half - 1)
        base_max = 10**half - 1

        lower = max(base_lower_bound, base_min)
        upper = min(base_upper_bound, base_max)

        if lower > upper:
            continue

        for base in range(lower, upper + 1):
            value = base * factor
            if start <= value <= end:
                yield value


def _repeated_values(start: int, end: int, at_least_repeats: int) -> Iterable[int]:
    """Yield numbers in [start, end] that repeat a digit block at least N times.

    Numbers have no leading zeros. Build candidates by digit length and block size
    instead of scanning every integer.
    """

    min_len = len(str(start))
    max_len = len(str(end))

    for length in range(min_len, max_len + 1):
        seen: set[int] = set()
        for block_len in range(1, length // 2 + 1):
            if length % block_len != 0:
                continue

            repeats = length // block_len
            if repeats < at_least_repeats:
                continue

            factor = (10**length - 1) // (10**block_len - 1)

            base_lower_bound = (start + factor - 1) // factor
            base_upper_bound = end // factor

            base_min = 10 ** (block_len - 1)
            base_max = 10**block_len - 1

            lower = max(base_lower_bound, base_min)
            upper = min(base_upper_bound, base_max)
            if lower > upper:
                continue

            for base in range(lower, upper + 1):
                value = base * factor
                if start <= value <= end and value not in seen:
                    seen.add(value)
                    yield value


def part1(ranges: list[IdRange]) -> int:
    """Return the sum of all invalid IDs across the given ranges."""

    return sum(value for r in ranges for value in _repeated_twice_values(r.start, r.end))


def part2(ranges: list[IdRange]) -> int:
    """Return the sum of invalid IDs repeated at least twice."""

    return sum(value for r in ranges for value in _repeated_values(r.start, r.end, 2))


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    ranges = parse_input(lines)
    print(f"Part 1: {part1(ranges)}")
    print(f"Part 2: {part2(ranges)}")


if __name__ == "__main__":
    run()
