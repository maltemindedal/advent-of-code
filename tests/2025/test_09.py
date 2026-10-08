from __future__ import annotations

import random
from bisect import bisect_right
from typing import Protocol, cast

import pytest

from tests._helpers import load_day

Point2D = tuple[int, int]


class Day09Module(Protocol):
    def parse_input(self, lines: list[str]) -> list[Point2D]: ...

    def part1(self, points: list[Point2D]) -> int: ...

    def part2(self, points: list[Point2D]) -> int: ...

    def _build_allowed_prefix(
        self, points: list[Point2D]
    ) -> tuple[list[float], list[float], list[list[int]]]: ...


day09 = cast(Day09Module, load_day(2025, 9))


SAMPLE_INPUT = [
    "7,1",
    "11,1",
    "11,7",
    "9,7",
    "9,5",
    "2,5",
    "2,3",
    "7,3",
]


def test_sample_max_area_two_corners() -> None:
    points = day09.parse_input(SAMPLE_INPUT)
    assert day09.part1(points) == 50


def test_sample_green_limited_area() -> None:
    points = day09.parse_input(SAMPLE_INPUT)
    assert day09.part2(points) == 24


def test_concave_shape_blocks_outside_rectangles() -> None:
    concave = [
        (0, 0),
        (4, 0),
        (4, 2),
        (2, 2),
        (2, 4),
        (0, 4),
    ]
    # Unrestricted rectangle would span the full 5x5 box.
    assert day09.part1(concave) == 25
    # Green-limited rectangle cannot cover the missing quadrant; expect smaller area.
    assert day09.part2(concave) < 25


# --- Reference implementation --------------------------------------------------------------
# The naive algorithm the solution started with: compress the coordinates into cells, decide each
# cell by testing its centre point against every polygon edge, then take 2D prefix sums. The
# production code may compute the same table faster; these tests hold it to this definition.


def _ref_point_on_segment(px: float, py: float, seg: tuple[Point2D, Point2D]) -> bool:
    (x1, y1), (x2, y2) = seg
    if x1 == x2 and y1 == y2:
        return px == x1 and py == y1
    if x1 == x2:
        return px == x1 and min(y1, y2) <= py <= max(y1, y2)
    if y1 == y2:
        return py == y1 and min(x1, x2) <= px <= max(x1, x2)
    return False


def _ref_point_in_polygon(x: float, y: float, poly: list[Point2D]) -> bool:
    inside = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if _ref_point_on_segment(x, y, ((x1, y1), (x2, y2))):
            return True
        if (y1 > y) != (y2 > y):
            cross_x = x1 + (y - y1) / (y2 - y1) * (x2 - x1)
            if cross_x == x:
                return True
            if cross_x > x:
                inside = not inside
    return inside


def _ref_bounds(coords: set[int]) -> list[float]:
    values = sorted(coords)
    bounds = {values[0] - 0.5, values[-1] + 0.5}
    for v in values:
        bounds.update((v - 0.5, v + 0.5))
    return sorted(bounds)


def _ref_allowed_prefix(
    points: list[Point2D],
) -> tuple[list[float], list[float], list[list[int]]]:
    xs = _ref_bounds({p[0] for p in points})
    ys = _ref_bounds({p[1] for p in points})
    prefix = [[0] * len(ys) for _ in range(len(xs))]
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            centre = ((xs[i] + xs[i + 1]) / 2.0, (ys[j] + ys[j + 1]) / 2.0)
            tiles = 0
            if _ref_point_in_polygon(centre[0], centre[1], points):
                tiles = round(xs[i + 1] - xs[i]) * round(ys[j + 1] - ys[j])
            prefix[i + 1][j + 1] = tiles + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]
    return xs, ys, prefix


def _ref_part2(points: list[Point2D]) -> int:
    if len(points) < 2:
        return 0
    xs, ys, prefix = _ref_allowed_prefix(points)
    best = 0
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1 :]:
            if x1 == x2 or y1 == y2:
                continue
            xmin, xmax = sorted((x1, x2))
            ymin, ymax = sorted((y1, y2))
            xi1, xi2 = bisect_right(xs, xmin) - 1, bisect_right(xs, xmax) - 1
            yi1, yi2 = bisect_right(ys, ymin) - 1, bisect_right(ys, ymax) - 1
            allowed = (
                prefix[xi2 + 1][yi2 + 1]
                - prefix[xi1][yi2 + 1]
                - prefix[xi2 + 1][yi1]
                + prefix[xi1][yi1]
            )
            area = (xmax - xmin + 1) * (ymax - ymin + 1)
            if allowed == area:
                best = max(best, area)
    return best


# --- Generated polygons ---------------------------------------------------------------------


def _histogram_polygon(rng: random.Random) -> list[Point2D]:
    """A rectilinear polygon shaped like a histogram (equal heights make zero-length edges)."""

    columns = rng.randint(1, 5)
    xs = sorted(rng.sample(range(30), columns + 1))
    heights = [rng.randint(1, 12) for _ in range(columns)]
    points: list[Point2D] = [(xs[0], 0)]
    for k, height in enumerate(heights):
        points.extend([(xs[k], height), (xs[k + 1], height)])
    points.append((xs[-1], 0))
    return points


def _walk_polygon(rng: random.Random) -> list[Point2D]:
    """Closed walk of vertical, horizontal and occasional diagonal steps (repeats allowed)."""

    x, y = rng.randint(0, 10), rng.randint(0, 10)
    points: list[Point2D] = [(x, y)]
    for _ in range(rng.randint(2, 9)):
        step = rng.random()
        if step < 0.4:
            y = rng.randint(0, 10)
        elif step < 0.8:
            x = rng.randint(0, 10)
        else:
            x, y = rng.randint(0, 10), rng.randint(0, 10)
        points.append((x, y))
    return points


def _scramble(points: list[Point2D], rng: random.Random) -> list[Point2D]:
    """Rotate the start vertex, maybe reverse the winding, maybe swap the axes."""

    shift = rng.randrange(len(points))
    points = points[shift:] + points[:shift]
    if rng.random() < 0.5:
        points.reverse()
    if rng.random() < 0.5:
        points = [(y, x) for x, y in points]
    return points


def _generated_polygons() -> list[list[Point2D]]:
    rng = random.Random(20250928)
    polygons = [_scramble(_histogram_polygon(rng), rng) for _ in range(120)]
    # Arbitrary point lists: diagonals, duplicates, self-intersections, collinear runs.
    polygons += [
        [(rng.randint(0, 12), rng.randint(0, 12)) for _ in range(rng.randint(2, 8))]
        for _ in range(120)
    ]
    polygons += [_walk_polygon(rng) for _ in range(160)]
    return polygons


GENERATED_POLYGONS = _generated_polygons()


def test_allowed_prefix_matches_naive_reference() -> None:
    for points in GENERATED_POLYGONS:
        assert day09._build_allowed_prefix(points) == _ref_allowed_prefix(points), points


def test_part2_matches_naive_reference() -> None:
    for points in GENERATED_POLYGONS:
        assert day09.part2(points) == _ref_part2(points), points


@pytest.mark.parametrize(
    ("points", "expected"),
    [
        pytest.param([(0, 0), (0, 3), (2, 3), (2, 1), (5, 1), (5, 0)], (24, 12), id="l-shape"),
        pytest.param([(0, 0), (0, 3), (0, 3), (4, 3), (4, 0)], (20, 20), id="zero-length-edge"),
        pytest.param([(0, 0), (4, 0), (0, 4)], (25, 0), id="diagonal-edge"),
        pytest.param(
            [(0, 0), (0, 4), (1, 4), (1, 1), (3, 1), (3, 4), (4, 4), (4, 0)], (25, 10), id="u-shape"
        ),
        pytest.param([(3, 3)], (0, 0), id="single-point"),
    ],
)
def test_pinned_shapes(points: list[Point2D], expected: tuple[int, int]) -> None:
    assert (day09.part1(points), day09.part2(points)) == expected
