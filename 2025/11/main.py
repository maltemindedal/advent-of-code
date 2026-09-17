from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from utils.io import read_input_lines

YEAR = 2025
DAY = 11
START_PART1 = "you"
START_PART2 = "svr"
END = "out"
REQUIRED_PART2 = ("dac", "fft")

Graph = dict[str, list[str]]


def parse_input(lines: Iterable[str]) -> Graph:
    """Parse device connections into an adjacency list.

    Each line is of the form ``src: dst1 dst2 ...``. Blank lines are ignored.
    """

    graph: Graph = {}
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Missing ':' separator in line: {line}")

        src_part, targets_part = line.split(":", 1)
        src = src_part.strip()
        if not src:
            raise ValueError(f"Missing source device in line: {line}")

        targets = [t for t in targets_part.strip().split() if t]
        graph[src] = targets

    return graph


def _collect_reachable(graph: Graph, start: str) -> set[str]:
    reachable = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for nxt in graph.get(node, []):
            if nxt not in reachable:
                reachable.add(nxt)
                stack.append(nxt)
    return reachable


def _check_for_cycles(graph: Graph, start: str, reachable: set[str]) -> None:
    visited: set[str] = set()
    stack: set[str] = set()

    def dfs(node: str) -> None:
        stack.add(node)
        for nxt in graph.get(node, []):
            if nxt not in reachable:
                continue
            if nxt in stack:
                raise ValueError("Cycle detected in graph reachable from start")
            if nxt not in visited:
                dfs(nxt)
        stack.remove(node)
        visited.add(node)

    dfs(start)


def _count_paths_dfs(graph: Graph, start: str, end: str, reachable: set[str]) -> int:
    memo: dict[str, int] = {}
    active: set[str] = set()

    def dfs(node: str) -> int:
        if node == end:
            return 1
        if node in memo:
            return memo[node]

        active.add(node)
        total = 0
        for nxt in graph.get(node, []):
            if nxt not in reachable:
                continue
            if nxt in active:
                raise ValueError("Cycle detected while counting paths")
            total += dfs(nxt)
        active.remove(node)
        memo[node] = total
        return total

    return dfs(start)


def _topo_order(graph: Graph, start: str, reachable: set[str]) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()

    def dfs(node: str) -> None:
        seen.add(node)
        for nxt in graph.get(node, []):
            if nxt in reachable and nxt not in seen:
                dfs(nxt)
        order.append(node)

    dfs(start)
    order.reverse()
    return order


def _count_paths_with_required_dag(
    graph: Graph, start: str, end: str, reachable: set[str], required: tuple[str, ...]
) -> int:
    if not required:
        return _count_paths_dfs(graph, start, end, reachable)

    if end not in reachable or any(r not in reachable for r in required):
        return 0

    order = _topo_order(graph, start, reachable)
    k = len(required)
    all_mask = (1 << k) - 1
    req_bits = {name: 1 << i for i, name in enumerate(required)}

    def bit_for(node: str) -> int:
        return req_bits.get(node, 0)

    dp: dict[str, list[int]] = defaultdict(lambda: [0] * (1 << k))
    start_mask = bit_for(start)
    dp[start][start_mask] = 1

    for node in order:
        node_state = dp[node]
        for nxt in graph.get(node, []):
            if nxt not in reachable:
                continue
            nxt_bit = bit_for(nxt)
            nxt_state = dp[nxt]
            for mask, count in enumerate(node_state):
                if count == 0:
                    continue
                nxt_state[mask | nxt_bit] += count

    end_state = dp[end]
    return sum(count for mask, count in enumerate(end_state) if mask & all_mask == all_mask)


def part1(graph: Graph, start: str = START_PART1, end: str = END) -> int:
    """Count distinct paths from ``start`` to ``end`` in a DAG using DFS with memoization."""

    reachable = _collect_reachable(graph, start)
    if end not in reachable:
        return 0
    _check_for_cycles(graph, start, reachable)
    return _count_paths_dfs(graph, start, end, reachable)


def part2(
    graph: Graph,
    start: str = START_PART2,
    end: str = END,
    required: tuple[str, ...] = REQUIRED_PART2,
) -> int:
    """Count paths that visit every required node in a DAG.

    Tracks reachable states with a bitmask DP over a topological ordering,
    avoiding the need for a general-purpose solver.
    """

    reachable = _collect_reachable(graph, start)
    if end not in reachable:
        return 0
    _check_for_cycles(graph, start, reachable)
    return _count_paths_with_required_dag(graph, start, end, reachable, required)


def run(variant: str | None = None) -> None:
    lines = read_input_lines(YEAR, DAY, variant)
    graph = parse_input(lines)
    print(f"Part 1: {part1(graph)}")
    print(f"Part 2: {part2(graph)}")


if __name__ == "__main__":
    run()
