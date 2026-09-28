from __future__ import annotations

import heapq
from collections.abc import Callable
from dataclasses import dataclass

from utils.io import read_input_lines

YEAR = 2025
DAY = 8

Point3D = tuple[int, int, int]
DistanceFn = Callable[[Point3D, Point3D], int]


@dataclass(frozen=True)
class CircuitResult:
    sizes: list[int]

    @property
    def top_three_product(self) -> int:
        top = sorted(self.sizes, reverse=True)
        while len(top) < 3:
            top.append(1)
        return top[0] * top[1] * top[2]


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.size: list[int] = [1] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

    def component_sizes(self) -> list[int]:
        return [self.size[i] for i in range(len(self.parent)) if self.parent[i] == i]


def parse_input(lines: list[str]) -> list[Point3D]:
    """Parse junction box coordinates."""

    points: list[Point3D] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 3:
            raise ValueError(f"Invalid coordinate line: {line}")
        x, y, z = map(int, parts)
        points.append((x, y, z))
    return points


def squared_euclidean(a: Point3D, b: Point3D) -> int:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz


def manhattan(a: Point3D, b: Point3D) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def _edges(points: list[Point3D], distance: DistanceFn) -> list[tuple[int, int, int]]:
    """Return every pair as ``(distance, i, j)``, in no particular order.

    Ties on distance break by ``(i, j)``, so ``heapq`` yields the same order as a full sort.
    """

    edges: list[tuple[int, int, int]] = []
    for i in range(len(points)):
        pi = points[i]
        for j in range(i + 1, len(points)):
            edges.append((distance(pi, points[j]), i, j))
    return edges


def connect_closest(
    points: list[Point3D],
    pairs_to_connect: int,
    distance: DistanceFn,
) -> CircuitResult:
    """Connect the closest pairs and return the circuit sizes."""

    n = len(points)
    if n == 0:
        return CircuitResult([])
    if pairs_to_connect < 0:
        raise ValueError("pairs_to_connect cannot be negative")

    dsu = DisjointSet(n)
    for _, i, j in heapq.nsmallest(pairs_to_connect, _edges(points, distance)):
        dsu.union(i, j)

    return CircuitResult(dsu.component_sizes())


def last_connection_product(points: list[Point3D], distance: DistanceFn) -> int:
    """Return the X-coordinate product of the edge that finishes connectivity.

    Edges are processed from shortest to longest. The first edge that joins
    all circuits determines the answer.
    """

    n = len(points)
    if n < 2:
        return 0

    edges = _edges(points, distance)
    heapq.heapify(edges)  # the loop below stops early, so ordering everything would be wasted work
    dsu = DisjointSet(n)
    components = n

    while edges:
        _, i, j = heapq.heappop(edges)
        ri, rj = dsu.find(i), dsu.find(j)
        if ri == rj:
            continue
        dsu.union(ri, rj)
        components -= 1
        if components == 1:
            return points[i][0] * points[j][0]

    raise ValueError("Graph did not fully connect; check input data")


def part1(points: list[Point3D], pairs_to_connect: int = 1000) -> int:
    """Product of the three largest circuits after connecting closest pairs (Euclidean)."""

    return connect_closest(points, pairs_to_connect, squared_euclidean).top_three_product


def part2(points: list[Point3D]) -> int:
    """Product of X coordinates of the last connection that unifies all circuits."""

    return last_connection_product(points, squared_euclidean)


def run(variant: str | None = None) -> None:
    lines = read_input_lines(YEAR, DAY, variant)
    points = parse_input(lines)
    print(f"Part 1: {part1(points)}")
    print(f"Part 2: {part2(points)}")


if __name__ == "__main__":
    run()
