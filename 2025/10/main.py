from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from utils.io import read_input_lines
from utils.z3_helpers import (
    SAT,
    ArithExpr,
    add_constraints,
    check_solver,
    eval_int,
    int_var,
    make_optimizer,
    minimize_expr,
    sum_expr,
)

YEAR = 2025
DAY = 10
INF = 10**18

_DIAGRAM_RE = re.compile(r"\[([^\]]+)\]")
_BUTTON_RE = re.compile(r"\(([^)]*)\)")
_TARGET_RE = re.compile(r"\{([^}]*)\}")


@dataclass(frozen=True)
class Machine:
    lights_mask: int
    button_masks: list[int]
    button_indices: list[list[int]]
    joltage_targets: list[int]


def _diagram_to_mask(diagram: str) -> int:
    mask = 0
    for i, ch in enumerate(diagram):
        if ch == "#":
            mask |= 1 << i
        elif ch != ".":
            raise ValueError(f"Unexpected indicator character: {ch!r}")
    return mask


def _button_to_mask_and_indices(indices: str) -> tuple[int, list[int]]:
    mask = 0
    idxs: list[int] = []
    seen: set[int] = set()
    for part in indices.split(","):
        part = part.strip()
        if not part:
            continue
        idx = int(part)
        if idx < 0:
            raise ValueError("Indicator index cannot be negative")
        if idx in seen:
            raise ValueError("Indicator indices within a single button must be unique")
        seen.add(idx)
        mask ^= 1 << idx
        idxs.append(idx)
    return mask, idxs


def _parse_targets(line: str) -> list[int]:
    target_match = _TARGET_RE.search(line)
    if not target_match:
        return []
    return [int(x.strip()) for x in target_match.group(1).split(",") if x.strip()]


def parse_input(lines: Iterable[str]) -> list[Machine]:
    """Parse machine definitions from the input lines.

    Each line contains an indicator diagram in ``[]``, one or more button
    definitions in ``()``, and joltage targets in ``{}``.
    """

    machines: list[Machine] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        diagram_match = _DIAGRAM_RE.search(line)
        if not diagram_match:
            raise ValueError(f"Missing indicator diagram in line: {line}")
        diagram = diagram_match.group(1)
        target_mask = _diagram_to_mask(diagram)

        button_strs = _BUTTON_RE.findall(line)
        if not button_strs:
            raise ValueError(f"No buttons found in line: {line}")

        button_masks: list[int] = []
        button_indices: list[list[int]] = []
        for b in button_strs:
            mask, idxs = _button_to_mask_and_indices(b)
            button_masks.append(mask)
            button_indices.append(idxs)

        targets = _parse_targets(line)
        machines.append(Machine(target_mask, button_masks, button_indices, targets))

    return machines


def _min_presses(target_mask: int, buttons: list[int]) -> int:
    """Return the minimum number of button presses to reach ``target_mask``.

    A subset dynamic program checks every set of buttons. Each button needs at most
    one press because pressing it twice cancels out over GF(2).
    """

    n = len(buttons)
    if target_mask == 0:
        return 0
    if n == 0:
        raise ValueError("No buttons available to toggle lights")

    states = [0] * (1 << n)
    best: int | None = None

    for mask in range(1, 1 << n):
        lsb = mask & -mask
        idx = lsb.bit_length() - 1
        states[mask] = states[mask ^ lsb] ^ buttons[idx]

    for mask, state in enumerate(states):
        if state == target_mask:
            presses = mask.bit_count()
            if best is None or presses < best:
                best = presses

    if best is None:
        raise ValueError("Target configuration is unreachable with the available buttons")
    return best


def _compress_vectors(vectors: list[list[int]]) -> list[tuple[int, ...]]:
    """Remove duplicate button vectors; order by descending coverage size."""

    unique: dict[tuple[int, ...], None] = {}
    for vec in vectors:
        t = tuple(vec)
        unique[t] = None
    return sorted(unique.keys(), key=lambda v: sum(v), reverse=True)


def _min_presses_counters(targets: list[int], buttons: list[list[int]]) -> int:
    """Return minimal presses to reach exact joltage targets via ILP (z3)."""

    if not targets:
        return 0

    m = len(targets)

    vectors: list[list[int]] = []
    for idxs in buttons:
        vec = [0] * m
        for idx in idxs:
            if idx >= m:
                raise ValueError("Button index exceeds number of counters")
            vec[idx] = 1
        if any(vec):
            vectors.append(vec)

    if not vectors:
        raise ValueError("No buttons affect any counters")

    compressed_vectors = _compress_vectors(vectors)

    solver = make_optimizer()
    vars_: list[ArithExpr] = [int_var(f"x{j}") for j in range(len(compressed_vectors))]
    for v in vars_:
        add_constraints(solver, v >= 0)

    for i in range(m):
        contrib: list[ArithExpr] = [vars_[j] for j, vec in enumerate(compressed_vectors) if vec[i]]
        if not contrib and targets[i] != 0:
            return INF
        add_constraints(solver, sum_expr(contrib) == targets[i])

    minimize_expr(solver, sum_expr(vars_))
    if check_solver(solver) != SAT:
        return INF
    model = solver.model()
    total = 0
    for v in vars_:
        total += eval_int(model, v)
    return total


def part1(machines: list[Machine]) -> int:
    """Sum the fewest button presses required for every machine."""

    return sum(_min_presses(machine.lights_mask, machine.button_masks) for machine in machines)


def part2(machines: list[Machine]) -> int:
    """Fewest presses to satisfy all joltage requirements."""

    return sum(_min_presses_counters(m.joltage_targets, m.button_indices) for m in machines)


def run(variant: str | None = None) -> None:
    lines = read_input_lines(YEAR, DAY, variant)
    machines = parse_input(lines)
    print(f"Part 1: {part1(machines)}")
    print(f"Part 2: {part2(machines)}")


if __name__ == "__main__":
    run()
