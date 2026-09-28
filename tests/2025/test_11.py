from __future__ import annotations

from typing import Protocol, cast

import pytest

from tests._helpers import PROJECT_ROOT, load_module
from utils.io import read_input_lines

DAY11_PATH = PROJECT_ROOT / "2025" / "11" / "main.py"


Graph = dict[str, list[str]]


class Day11Module(Protocol):
    def parse_input(self, lines: list[str]) -> Graph: ...

    def part1(self, graph: Graph, start: str = "you", end: str = "out") -> int: ...

    def part2(
        self,
        graph: Graph,
        start: str = "svr",
        end: str = "out",
        required: tuple[str, ...] = ("dac", "fft"),
    ) -> int: ...


day11 = cast(Day11Module, load_module("aoc2025_day11", DAY11_PATH))


def test_sample_paths_part1() -> None:
    lines = read_input_lines(2025, 11, variant="sample")
    graph = day11.parse_input(lines)
    assert day11.part1(graph) == 5


def test_sample_paths_part2_required_nodes() -> None:
    lines = [
        "svr: dac fft",
        "dac: fft",
        "fft: mid out",
        "mid: out",
        "out:",
    ]
    graph = day11.parse_input(lines)
    assert day11.part2(graph) == 2


def test_unreachable_output() -> None:
    graph = day11.parse_input(
        [
            "you: a",
            "a: b",
            "b: c",
            "c: d",
        ]
    )
    assert day11.part1(graph) == 0
    # Part 2 starts at "svr" by default, so this graph returns 0.
    assert day11.part2(graph) == 0


def test_cycle_detection() -> None:
    graph = day11.parse_input(
        [
            "you: a dac",
            "a: you fft",
            "dac: out",
            "fft: out",
            "out:",
        ]
    )
    with pytest.raises(ValueError):
        day11.part1(graph)
    with pytest.raises(ValueError):
        day11.part2(graph, start="you")
