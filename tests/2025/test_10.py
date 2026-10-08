from __future__ import annotations

from typing import Protocol, cast

import pytest

from tests._helpers import load_day
from utils.io import read_input_lines


class Day10Module(Protocol):
    INF: int

    def parse_input(self, lines: list[str]) -> object: ...

    def part1(self, machines: object) -> int: ...

    def part2(self, machines: object) -> int: ...


day10 = cast(Day10Module, load_day(2025, 10))


def test_sample_parts() -> None:
    lines = read_input_lines(2025, 10, variant="sample")
    machines = day10.parse_input(lines)
    assert day10.part1(machines) == 7
    assert day10.part2(machines) == 33


def test_single_button_machine() -> None:
    machines = day10.parse_input(["[#] (0) {5}"])
    assert day10.part1(machines) == 1


def test_combo_button_shortcut() -> None:
    machines = day10.parse_input(["[##] (0) (1) (0,1) {1,1}"])
    assert day10.part1(machines) == 1


# Part 2 solves a small integer program per machine with z3. Machines without a solution do not
# raise, unlike Part 1: they contribute the `INF` sentinel (10**18). That is a deliberate but
# debatable design; if it ever changes, these expectations change in the same commit.


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        pytest.param("[#] (0) {5}", 5, id="single-button"),
        pytest.param("[##] (0) (1) (0,1) {1,1}", 1, id="combo-button-beats-two-presses"),
        pytest.param("[#] (0) (0) {4}", 4, id="duplicate-buttons-collapse"),
        pytest.param("[##] (0) {3,0}", 3, id="uncovered-counter-with-zero-target"),
        pytest.param("[#] (0)", 0, id="no-joltage-section"),
        pytest.param("[#] (0) {}", 0, id="empty-joltage-section"),
    ],
)
def test_part2_pinned_machines(line: str, expected: int) -> None:
    assert day10.part2(day10.parse_input([line])) == expected


@pytest.mark.parametrize(
    "line",
    [
        pytest.param("[##] (0) {3,2}", id="uncovered-counter-with-positive-target"),
        pytest.param("[.] (0,1) {1,2}", id="contradictory-equations"),
    ],
)
def test_part2_unsolvable_machine_is_the_inf_sentinel(line: str) -> None:
    assert day10.INF == 10**18
    machines = day10.parse_input([line])
    assert day10.part2(machines) == day10.INF
    # The sentinel is simply summed with the other machines.
    both = day10.parse_input([line, "[#] (0) {5}"])
    assert day10.part2(both) == day10.INF + 5


def _fewest_presses(buttons: list[tuple[int, ...]], targets: list[int]) -> int:
    """Smallest number of presses that reaches ``targets`` exactly (breadth-first search)."""

    start = tuple(targets)
    seen = {start}
    frontier = [start]
    presses = 0
    while frontier:
        if any(not any(state) for state in frontier):
            return presses
        presses += 1
        next_frontier: list[tuple[int, ...]] = []
        for state in frontier:
            for button in buttons:
                after = tuple(v - 1 if i in button else v for i, v in enumerate(state))
                if min(after) >= 0 and after not in seen:
                    seen.add(after)
                    next_frontier.append(after)
        frontier = next_frontier
    raise AssertionError(f"{targets} cannot be reached with {buttons}")


# Without its objective z3 still returns a valid plan, and on tiny machines that is often the
# smallest one. These machines are ones where it is not, whatever z3 has solved before (picked
# by trying random machines under several solver histories on Python 3.11, 3.12 and 3.14).
MINIMALITY_MACHINES = (
    ([(2,), (1, 2), (0, 1), (0, 2), (2,)], [3, 5, 8]),
    ([(0, 1), (2,), (0,), (0, 2), (0,), (0, 1, 2), (1, 2), (0, 1, 2)], [6, 3, 4]),
    ([(0, 2), (0, 1), (0, 2), (1,), (1, 2), (1, 2), (0, 1), (1, 2)], [8, 9, 8]),
    ([(0, 1, 2), (0, 1, 2), (2,), (1, 2), (0,), (2,), (2,), (0, 1, 2), (0, 2)], [6, 3, 7]),
    ([(2,), (1,), (2, 3), (0, 1), (0, 2, 3), (3,), (1, 2, 3), (1, 2, 3)], [4, 3, 10, 10]),
    ([(0, 1, 3), (1, 2), (1, 2, 3), (0, 1), (1, 2), (2,), (0, 1), (0, 1, 2, 3)], [4, 9, 8, 6]),
    ([(1, 3, 4), (1, 2), (2,), (3,), (4,), (1, 3, 4), (2,)], [0, 3, 4, 2, 3]),
)


def _machine_line(buttons: list[tuple[int, ...]], targets: list[int]) -> str:
    diagram = "[" + "." * len(targets) + "]"
    wiring = " ".join("(" + ",".join(map(str, button)) + ")" for button in buttons)
    return f"{diagram} {wiring} {{{','.join(map(str, targets))}}}"


def test_part2_minimises_presses_rather_than_returning_any_solution() -> None:
    # Counter 3 (target 77) is touched by every button except (0,1), so at least 77 presses are
    # needed. 8 x (0,1,2,3) + 36 x (0,2,3) + 25 x (0,1,3) + 8 x (1,3) reaches {69,41,44,77} with
    # exactly 77. A solver that returned just any valid plan would return a longer one, but how
    # much longer depends on z3's internal state, so this single case is not enough on its own.
    line = "[.#.#] (0,3) (0,1) (0,1,2,3) (0,2,3) (0,1,3) (1,3) {69,41,44,77}"
    assert day10.part2(day10.parse_input([line])) == 77

    for buttons, targets in MINIMALITY_MACHINES:
        machine = _machine_line(buttons, targets)
        expected = _fewest_presses(buttons, targets)
        assert day10.part2(day10.parse_input([machine])) == expected, machine


def test_part2_rejects_impossible_button_definitions() -> None:
    with pytest.raises(ValueError, match="Button index exceeds number of counters"):
        day10.part2(day10.parse_input(["[#] (3) {1}"]))
    with pytest.raises(ValueError, match="No buttons affect any counters"):
        day10.part2(day10.parse_input(["[#] () {1}"]))


def test_part1_unreachable_lights_raise() -> None:
    with pytest.raises(ValueError, match="Target configuration is unreachable"):
        day10.part1(day10.parse_input(["[##] (0) {1,1}"]))
