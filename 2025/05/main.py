from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass

from utils.io import read_input_lines

YEAR = 2025
DAY = 5


@dataclass(frozen=True)
class IdRange:
    start: int
    end: int


def parse_input(lines: list[str]) -> tuple[list[IdRange], list[int]]:
    """Parse fresh ranges and available ingredient IDs.

    The input has two sections separated by a blank line:
    - before the blank line: inclusive ranges in the form ``start-end``
    - after the blank line: one ingredient ID per line
    """

    ranges: list[IdRange] = []
    ids: list[int] = []

    reading_ranges = True
    for raw in lines:
        line = raw.strip()
        if not line:
            reading_ranges = False
            continue

        if reading_ranges:
            parts = line.split("-")
            if len(parts) != 2:
                raise ValueError(f"Invalid range line: {raw}")
            start, end = map(int, parts)
            if start > end:
                start, end = end, start
            ranges.append(IdRange(start, end))
        else:
            ids.append(int(line))

    return ranges, ids


def _merge_ranges(ranges: list[IdRange]) -> list[IdRange]:
    """Merge overlapping or adjacent ranges for efficient membership checks."""

    if not ranges:
        return []

    merged: list[IdRange] = []
    for r in sorted(ranges, key=lambda x: x.start):
        if not merged or r.start > merged[-1].end + 1:
            merged.append(r)
        else:
            last = merged[-1]
            merged[-1] = IdRange(last.start, max(last.end, r.end))
    return merged


def _count_fresh(ranges: list[IdRange], available_ids: list[int]) -> int:
    """Return how many available IDs fall inside any of the ranges."""

    merged = _merge_ranges(ranges)
    if not merged or not available_ids:
        return 0

    starts = [r.start for r in merged]
    fresh = 0
    for value in available_ids:
        idx = bisect_right(starts, value) - 1
        if idx >= 0 and merged[idx].start <= value <= merged[idx].end:
            fresh += 1
    return fresh


def part1(ranges: list[IdRange], available_ids: list[int]) -> int:
    """Count how many available ingredient IDs are fresh."""

    return _count_fresh(ranges, available_ids)


def part2(ranges: list[IdRange], available_ids: list[int] | None = None) -> int:
    """Count the ingredient IDs covered by the ranges.

    The available IDs do not affect this result.
    """

    merged = _merge_ranges(ranges)
    return sum(r.end - r.start + 1 for r in merged)


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    ranges, ids = parse_input(lines)
    print(f"Part 1: {part1(ranges, ids)}")
    print(f"Part 2: {part2(ranges)}")


if __name__ == "__main__":
    run()
