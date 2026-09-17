from __future__ import annotations

from dataclasses import dataclass

from utils.io import read_input_lines

YEAR = 2025
DAY = 1


@dataclass(frozen=True)
class Rotation:
    direction: str  # "L" or "R"
    steps: int


def parse_input(lines: list[str]) -> list[Rotation]:
    """Parse lines like `L68` into Rotation objects."""

    rotations: list[Rotation] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        if direction not in {"L", "R"}:
            raise ValueError(f"Unexpected direction in line: {line}")
        steps = int(line[1:])
        rotations.append(Rotation(direction, steps))
    return rotations


def apply_rotation(position: int, rotation: Rotation) -> int:
    """Apply a rotation and return the new position on a dial numbered 0 to 99."""

    if rotation.direction == "L":
        return (position - rotation.steps) % 100
    return (position + rotation.steps) % 100


def part1(rotations: list[Rotation], start: int = 50) -> int:
    """Count how many times the dial lands on 0 after a rotation."""

    position = start
    zeros = 0
    for rotation in rotations:
        position = apply_rotation(position, rotation)
        if position == 0:
            zeros += 1
    return zeros


def part2(rotations: list[Rotation], start: int = 50) -> int:
    """Count how many clicks land on 0 during all rotations.

    Count clicks that land on 0, including those before each rotation finishes.
    The dial has values 0 to 99.
    """

    def zero_hits(position: int, rotation: Rotation) -> int:
        """Return how many clicks during this rotation land on 0.

        The first time the dial reaches 0 happens after ``first`` clicks;
        subsequent hits occur every 100 clicks because the dial size is 100.
        """

        if rotation.steps == 0:
            return 0

        if rotation.direction == "L":
            first = position % 100
        else:  # "R"
            first = (-position) % 100  # equivalently (100 - position) % 100

        if first == 0:
            first = 100  # must complete a full circle to hit 0

        if rotation.steps < first:
            return 0

        return 1 + (rotation.steps - first) // 100

    position = start
    zeros = 0
    for rotation in rotations:
        zeros += zero_hits(position, rotation)
        position = apply_rotation(position, rotation)
    return zeros


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    rotations = parse_input(lines)
    print(f"Part 1: {part1(rotations)}")
    print(f"Part 2: {part2(rotations)}")


if __name__ == "__main__":
    run()
