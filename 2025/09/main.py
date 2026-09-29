from __future__ import annotations

from bisect import bisect_left, bisect_right
from itertools import accumulate

from utils.io import read_input_lines

YEAR = 2025
DAY = 9

Point = tuple[int, int]


def _row_spans(poly: list[Point], y: float) -> list[tuple[float, float]]:
    """Return the closed x-intervals where the line at ``y`` is inside or on the polygon.

    A point (x, y) is inside or on the boundary exactly when x lies in one of these intervals.
    Vertical, horizontal and zero-length edges lying on the line contribute their own span (edges
    with any other slope are never "on" the boundary). Every other edge that crosses the line, by
    the half-open rule ``(y1 > y) != (y2 > y)``, contributes a crossing; a closed polygon has an
    even number of them, and consecutive pairs of the sorted crossings bound the interior.
    """

    spans: list[tuple[float, float]] = []
    crossings: list[float] = []
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1], strict=True):
        if x1 == x2:
            if min(y1, y2) <= y <= max(y1, y2):
                spans.append((x1, x1))
        elif y1 == y2 and y == y1:
            spans.append((min(x1, x2), max(x1, x2)))
        if (y1 > y) != (y2 > y):
            crossings.append(x1 + (y - y1) / (y2 - y1) * (x2 - x1))
    crossings.sort()
    spans.extend(zip(crossings[0::2], crossings[1::2], strict=True))
    return spans


def _make_bounds(coords: set[int]) -> list[float]:
    values = sorted(coords)
    bounds = {values[0] - 0.5, values[-1] + 0.5}
    for v in values:
        bounds.add(v - 0.5)
        bounds.add(v + 0.5)
    return sorted(bounds)


def _tile_index(value: int, bounds: list[float]) -> int:
    return bisect_right(bounds, value) - 1


def _build_allowed_prefix(points: list[Point]) -> tuple[list[float], list[float], list[list[int]]]:
    xs = _make_bounds({p[0] for p in points})
    ys = _make_bounds({p[1] for p in points})

    widths = [round(xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
    heights = [round(ys[j + 1] - ys[j]) for j in range(len(ys) - 1)]
    sample_xs = [(xs[i] + xs[i + 1]) / 2.0 for i in range(len(widths))]

    # A cell is allowed when its centre is inside or on the polygon. Sweep one row of cells at a
    # time: find the allowed columns from the row's x-intervals, then add the row's tiles to the
    # running 2D prefix sums. rows[j][i] covers the cells left of column i and above row j.
    rows = [[0] * len(xs)]
    for j, height in enumerate(heights):
        sample_y = (ys[j] + ys[j + 1]) / 2.0
        allowed = [0] * len(widths)
        for start, end in _row_spans(points, sample_y):
            lo = bisect_left(sample_xs, start)
            hi = bisect_right(sample_xs, end)
            allowed[lo:hi] = widths[lo:hi]
        row = [0]
        row.extend(
            above + height * tiles
            for above, tiles in zip(rows[-1][1:], accumulate(allowed), strict=True)
        )
        rows.append(row)

    # Transpose so that prefix[i][j] is indexed by column, then row, like _rect_sum expects.
    prefix: list[list[int]] = [list(column) for column in zip(*rows, strict=True)]
    return xs, ys, prefix


def _rect_sum(prefix: list[list[int]], x1: int, x2: int, y1: int, y2: int) -> int:
    return prefix[x2 + 1][y2 + 1] - prefix[x1][y2 + 1] - prefix[x2 + 1][y1] + prefix[x1][y1]


def parse_input(lines: list[str]) -> list[Point]:
    """Parse ``x,y`` coordinate pairs into a list of points.

    Empty lines are ignored. Coordinates may appear multiple times; duplicates
    are preserved in the returned list but are deduplicated when helpful for
    set-based lookups.
    """

    points: list[Point] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate line: {line}")
        x, y = map(int, parts)
        points.append((x, y))
    return points


def _area(a: Point, b: Point) -> int:
    """Inclusive rectangle area between two opposite corners."""

    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def largest_rectangle_two_corners(points: list[Point]) -> int:
    """Largest area using any two red tiles as opposite corners.

    The rectangle sides are aligned to the axes. Degenerate rectangles where
    the two corners share an x or y coordinate are ignored.
    """

    max_area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue
            max_area = max(max_area, _area((x1, y1), (x2, y2)))
    return max_area


def _largest_rectangle_green(points: list[Point]) -> int:
    """Largest rectangle using red corners and only red/green tiles inside."""

    if len(points) < 2:
        return 0

    xs, ys, prefix = _build_allowed_prefix(points)
    tile_x = [_tile_index(x, xs) for x, _ in points]
    tile_y = [_tile_index(y, ys) for _, y in points]

    max_area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue

            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area <= max_area:
                continue  # cannot beat the best rectangle found so far

            xi1, xi2 = sorted((tile_x[i], tile_x[j]))
            yi1, yi2 = sorted((tile_y[i], tile_y[j]))
            if _rect_sum(prefix, xi1, xi2, yi1, yi2) == area:
                max_area = area

    return max_area


def part1(points: list[Point]) -> int:
    return largest_rectangle_two_corners(points)


def part2(points: list[Point]) -> int:
    return _largest_rectangle_green(points)


def run(variant: str | None = None) -> None:
    lines = read_input_lines(YEAR, DAY, variant)
    points = parse_input(lines)
    print(f"Part 1: {part1(points)}")
    print(f"Part 2: {part2(points)}")


if __name__ == "__main__":
    run()
