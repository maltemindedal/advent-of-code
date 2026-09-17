from __future__ import annotations

from typing import Protocol, cast

from tests._helpers import PROJECT_ROOT, load_module

DAY08_PATH = PROJECT_ROOT / "2025" / "08" / "main.py"


Point3D = tuple[int, int, int]


class Day08Module(Protocol):
    def parse_input(self, lines: list[str]) -> list[Point3D]: ...

    def part1(self, points: list[Point3D], pairs_to_connect: int = 1000) -> int: ...

    def part2(self, points: list[Point3D]) -> int: ...


day08 = cast(Day08Module, load_module("aoc2025_day08", DAY08_PATH))


EXAMPLE_INPUT = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]


def test_example_matches_described_product() -> None:
    points = day08.parse_input(EXAMPLE_INPUT)
    assert len(points) == 20
    assert day08.part1(points, pairs_to_connect=10) == 40
    assert day08.part2(points) == 25_272


def test_last_connection_product_simple_triangle() -> None:
    points = [
        (0, 0, 0),
        (10, 0, 0),
        (0, 10, 0),
    ]

    # The second distance-10 edge completes connectivity, so the product is 0.
    assert day08.part2(points) == 0
