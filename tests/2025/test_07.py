from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import PROJECT_ROOT, load_day

SAMPLE_PATH = PROJECT_ROOT / "inputs" / "2025" / "07.sample.txt"


class Day07Module(Protocol):
    def part1(self, lines: list[str]) -> int: ...

    def part2(self, lines: list[str]) -> int: ...


day07 = cast(Day07Module, load_day(2025, 7))


def test_sample_splits_match_description() -> None:
    lines = SAMPLE_PATH.read_text(encoding="utf-8").splitlines()
    assert day07.part1(lines) == 21
    assert day07.part2(lines) == 40


def test_chain_reaction_with_adjacent_splitters() -> None:
    diagram = [
        "..S..",
        "..^..",
        ".^^^.",
        ".....",
    ]

    # The first splitter creates two beams. The next row produces three.
    assert day07.part1(diagram) == 3
    # Part 2 keeps both timelines when paths converge in the middle column.
    assert day07.part2(diagram) == 4


def test_timelines_preserved_on_merge() -> None:
    diagram = [
        ".S.",
        ".^.",
        "^.^",
        "...",
    ]

    # Both splitters send beams into the center column. Part 2 adds the paths.
    assert day07.part1(diagram) == 3
    assert day07.part2(diagram) == 2
