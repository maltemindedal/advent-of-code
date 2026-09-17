from __future__ import annotations

from dataclasses import dataclass
from math import prod

from utils.io import read_input_lines

YEAR = 2025
DAY = 6


@dataclass(frozen=True)
class Problem:
    numbers: list[int]
    op: str


def _segments_from_columns(padded: list[str]) -> list[tuple[int, int]]:
    """Return column spans for each problem.

    A separator column contains only spaces. Each run of other columns is one
    problem.
    """

    if not padded:
        return []

    rows = len(padded)
    width = len(padded[0])

    separator = [all(padded[r][c] == " " for r in range(rows)) for c in range(width)]

    segments: list[tuple[int, int]] = []
    c = 0
    while c < width:
        if separator[c]:
            c += 1
            continue
        start = c
        while c < width and not separator[c]:
            c += 1
        segments.append((start, c))
    return segments


def _pad_lines(lines: list[str]) -> list[str]:
    if not lines:
        return []
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines]


def parse_input(lines: list[str]) -> list[Problem]:
    """Parse row-oriented problems from the input lines.

    Each column of the input represents a digit (or space). A full column of
    spaces separates problems. The bottom row contains the operator (`+` or
    `*`) for the problem above it. All other rows contain the problem's
    operands, one row per number.
    """

    if not lines:
        return []
    if len(lines) < 2:
        raise ValueError("Expected at least one row of numbers and one row of operators")

    padded = _pad_lines(lines)

    segments = _segments_from_columns(padded)

    problems: list[Problem] = []
    for start, end in segments:
        operand_slices = [padded[r][start:end].strip() for r in range(len(padded) - 1)]
        numbers: list[int] = []
        for idx, chunk in enumerate(operand_slices):
            if not chunk:
                raise ValueError(f"Missing operand in row {idx} for columns {start}-{end}")
            numbers.append(int(chunk))

        op_slice = padded[-1][start:end]
        op_chars = [ch for ch in op_slice if ch in {"+", "*"}]
        if not op_chars:
            raise ValueError(f"Missing operator for columns {start}-{end}")
        op = op_chars[0]
        problems.append(Problem(numbers, op))

    return problems


def parse_input_columns(lines: list[str]) -> list[Problem]:
    """Parse problems whose numbers run top-to-bottom within columns.

    Problems are still separated by a full column of spaces; within each
    problem, *each column* forms one number whose most significant digit is at
    the top and least significant at the bottom. The operator is still the
    bottom row within the problem span.
    """

    if not lines:
        return []
    if len(lines) < 2:
        raise ValueError("Expected at least one row of numbers and one row of operators")

    padded = _pad_lines(lines)
    segments = _segments_from_columns(padded)

    problems: list[Problem] = []
    for start, end in segments:
        numbers: list[int] = []
        for c in range(start, end):
            digits = "".join(padded[r][c] for r in range(len(padded) - 1)).strip()
            if not digits:
                raise ValueError(f"Missing digits in column {c} for columns {start}-{end}")
            numbers.append(int(digits))

        op_slice = padded[-1][start:end]
        op_chars = [ch for ch in op_slice if ch in {"+", "*"}]
        if not op_chars:
            raise ValueError(f"Missing operator for columns {start}-{end}")
        op = op_chars[0]

        # Read each problem from right to left.
        problems.append(Problem(list(reversed(numbers)), op))

    # Read the worksheet from right to left as well.
    return list(reversed(problems))


def _evaluate(problem: Problem) -> int:
    if problem.op == "+":
        return sum(problem.numbers)
    if problem.op == "*":
        return prod(problem.numbers)
    raise ValueError(f"Unsupported operator: {problem.op}")


def part1(problems: list[Problem]) -> int:
    """Compute the grand total of all problem results."""

    return sum(_evaluate(p) for p in problems)


def part2(lines: list[str]) -> int:
    """Compute grand total using column-wise (right-to-left) reading rules."""

    problems = parse_input_columns(lines)
    return part1(problems)


def run(variant: str | None = None) -> None:
    """Read the input and print both answers."""

    lines = read_input_lines(YEAR, DAY, variant)
    problems_lr = parse_input(lines)
    print(f"Part 1: {part1(problems_lr)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    run()
