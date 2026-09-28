from __future__ import annotations

from bisect import bisect_right

from utils.io import read_input_lines

YEAR = 2025
DAY = 9

Point = tuple[int, int]


def _point_on_segment(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> bool:
    if x1 == x2 and y1 == y2:
        return px == x1 and py == y1
    if x1 == x2:  # vertical
        if px != x1:
            return False
        return min(y1, y2) <= py <= max(y1, y2)
    if y1 == y2:  # horizontal
        if py != y1:
            return False
        return min(x1, x2) <= px <= max(x1, x2)
    return False


def _point_in_polygon(point: tuple[float, float], poly: list[Point]) -> bool:
    """Return True if point is inside or on the boundary of the polygon."""

    x, y = point
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if _point_on_segment(x, y, x1, y1, x2, y2):
            return True  # boundary is inside

        if (y1 > y) != (y2 > y):
            t = (y - y1) / (y2 - y1)
            cross_x = x1 + t * (x2 - x1)
            if cross_x == x:
                return True
            if cross_x > x:
                inside = not inside
    return inside


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

    prefix = [[0] * (len(ys)) for _ in range(len(xs))]

    for i in range(len(xs) - 1):
        sample_x = (xs[i] + xs[i + 1]) / 2.0
        for j in range(len(ys) - 1):
            sample_y = (ys[j] + ys[j + 1]) / 2.0
            if _point_in_polygon((sample_x, sample_y), points):
                tiles = widths[i] * heights[j]
            else:
                tiles = 0

            prefix[i + 1][j + 1] = tiles + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]
        # carry top row accumulation for next i
        prefix[i + 1][0] = 0

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

    max_area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue

            xmin, xmax = sorted((x1, x2))
            ymin, ymax = sorted((y1, y2))

            xi1 = _tile_index(xmin, xs)
            xi2 = _tile_index(xmax, xs)
            yi1 = _tile_index(ymin, ys)
            yi2 = _tile_index(ymax, ys)

            area = (xmax - xmin + 1) * (ymax - ymin + 1)
            allowed = _rect_sum(prefix, xi1, xi2, yi1, yi2)
            if allowed == area:
                max_area = max(max_area, area)

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
