from __future__ import annotations

import random
from collections import Counter
from collections.abc import Callable
from typing import Protocol, cast

import pytest

from tests._helpers import PROJECT_ROOT, load_module

DAY08_PATH = PROJECT_ROOT / "2025" / "08" / "main.py"


Point3D = tuple[int, int, int]
DistanceFn = Callable[[Point3D, Point3D], int]


class CircuitResultLike(Protocol):
    @property
    def sizes(self) -> list[int]: ...

    @property
    def top_three_product(self) -> int: ...


class Day08Module(Protocol):
    def parse_input(self, lines: list[str]) -> list[Point3D]: ...

    def part1(self, points: list[Point3D], pairs_to_connect: int = 1000) -> int: ...

    def part2(self, points: list[Point3D]) -> int: ...

    def connect_closest(
        self, points: list[Point3D], pairs_to_connect: int, distance: DistanceFn
    ) -> CircuitResultLike: ...

    def last_connection_product(self, points: list[Point3D], distance: DistanceFn) -> int: ...

    def squared_euclidean(self, a: Point3D, b: Point3D) -> int: ...

    def manhattan(self, a: Point3D, b: Point3D) -> int: ...


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


# --- Reference implementation --------------------------------------------------------------
# Kruskal-style: list every pair as (distance, i, j), sort, and merge components in that order.
# Ties are broken by (i, j), which decides which circuits form, so faster ways of picking the
# shortest pairs must reproduce exactly this order.


def _ref_edges(points: list[Point3D], distance: DistanceFn) -> list[tuple[int, int, int]]:
    return sorted(
        (distance(a, b), i, j) for i, a in enumerate(points) for j, b in enumerate(points) if i < j
    )


def _ref_find(parent: list[int], x: int) -> int:
    return x if parent[x] == x else _ref_find(parent, parent[x])


def _ref_sizes(points: list[Point3D], pairs: int, distance: DistanceFn) -> list[int]:
    parent = list(range(len(points)))
    for _, i, j in _ref_edges(points, distance)[:pairs]:
        parent[_ref_find(parent, i)] = _ref_find(parent, j)
    roots = Counter(_ref_find(parent, i) for i in range(len(points)))
    return sorted(roots.values(), reverse=True)


def _ref_last_connection(points: list[Point3D], distance: DistanceFn) -> int:
    if len(points) < 2:
        return 0
    parent = list(range(len(points)))
    components = len(points)
    for _, i, j in _ref_edges(points, distance):
        ri, rj = _ref_find(parent, i), _ref_find(parent, j)
        if ri != rj:
            parent[ri] = rj
            components -= 1
            if components == 1:
                return points[i][0] * points[j][0]
    raise AssertionError("every pair is an edge, so the graph always connects")


def _tie_heavy_point_sets() -> list[list[Point3D]]:
    """Small coordinate ranges give many equal distances and duplicate points."""

    rng = random.Random(20250928)
    point_sets: list[list[Point3D]] = []
    for _ in range(150):
        span = rng.choice([1, 2, 3, 6])
        count = rng.randint(0, 20)
        point_sets.append(
            [
                (rng.randint(0, span), rng.randint(0, span), rng.randint(0, span))
                for _ in range(count)
            ]
        )
    return point_sets


POINT_SETS = _tie_heavy_point_sets()


def test_distance_functions() -> None:
    assert day08.squared_euclidean((0, 0, 0), (1, 2, 2)) == 9
    assert day08.manhattan((0, 0, 0), (1, 2, 2)) == 5
    assert day08.manhattan((1, 2, 3), (3, 2, 1)) == 4


def test_connect_closest_matches_reference() -> None:
    for distance in (day08.squared_euclidean, day08.manhattan):
        for points in POINT_SETS:
            n = len(points)
            for pairs in (0, 1, 3, 10, n, n * n, 1000):
                result = day08.connect_closest(points, pairs, distance)
                assert sorted(result.sizes, reverse=True) == _ref_sizes(points, pairs, distance), (
                    points,
                    pairs,
                )


def test_last_connection_product_matches_reference() -> None:
    for distance in (day08.squared_euclidean, day08.manhattan):
        for points in POINT_SETS:
            assert day08.last_connection_product(points, distance) == _ref_last_connection(
                points, distance
            ), points


def test_parts_match_reference_on_ties() -> None:
    for points in POINT_SETS:
        sizes = _ref_sizes(points, 1000, day08.squared_euclidean)
        largest, second, third, *_ = [*sizes, 1, 1, 1]
        assert day08.part1(points) == largest * second * third
        assert day08.part2(points) == _ref_last_connection(points, day08.squared_euclidean)


LATTICE = [(x, y, z) for x in range(3) for y in range(3) for z in range(2)]


@pytest.mark.parametrize(
    ("pairs", "product"), [(0, 1), (1, 2), (5, 6), (17, 13), (40, 18), (1000, 18)]
)
def test_lattice_part1_pinned(pairs: int, product: int) -> None:
    # 18 points with many equal distances: the tie order decides which circuits form.
    assert day08.part1(LATTICE, pairs) == product


def test_lattice_part2_pinned() -> None:
    assert day08.part2(LATTICE) == 2
    assert day08.last_connection_product(LATTICE, day08.manhattan) == 2


def test_degenerate_inputs() -> None:
    assert day08.connect_closest([], 5, day08.squared_euclidean).sizes == []
    # An empty input is answered before the pair count is validated.
    assert day08.connect_closest([], -1, day08.squared_euclidean).sizes == []
    assert (day08.part1([]), day08.part2([])) == (1, 0)
    assert (day08.part1([(1, 2, 3)]), day08.part2([(1, 2, 3)])) == (1, 0)
    assert (day08.part1([(1, 1, 1)] * 3), day08.part2([(1, 1, 1)] * 3)) == (3, 1)
    with pytest.raises(ValueError, match="pairs_to_connect cannot be negative"):
        day08.connect_closest([(0, 0, 0)], -1, day08.squared_euclidean)
