from __future__ import annotations

from utils.io import read_input_lines

YEAR = 2025
DAY = 7


def _prepare_grid(lines: list[str]) -> tuple[list[str], tuple[int, int]]:
    """Pad the grid and find the start position.

    Missing characters at the end of a row become empty space (`.`). Return
    the padded grid and the (row, col) of `S`.
    """

    if not lines:
        raise ValueError("Input is empty; expected a manifold diagram.")

    width = max(len(line) for line in lines)
    grid = [line.ljust(width, ".") for line in lines]

    start_row = start_col = None
    for r, row in enumerate(grid):
        if "S" in row:
            start_row = r
            start_col = row.index("S")
            break

    if start_row is None or start_col is None:
        raise ValueError("No start position 'S' found in the diagram.")

    return grid, (start_row, start_col)


def count_splits(lines: list[str]) -> int:
    """Count beam splits while traversing the manifold.

    Beams move downward. A splitter (`^`) stops a beam and sends two beams to
    the adjacent columns. Empty space (`.`) lets a beam continue. Overlapping
    beams count as one path.
    """

    grid, (start_row, start_col) = _prepare_grid(lines)
    rows = len(grid)
    width = len(grid[0])

    active: set[int] = {start_col}  # columns with beams entering the current row
    splits = 0

    for r in range(start_row, rows):
        next_row: set[int] = set()

        for c in active:
            cell = grid[r][c]
            if cell == "^":
                splits += 1
                for nc in (c - 1, c + 1):
                    if 0 <= nc < width:
                        next_row.add(nc)
            else:
                next_row.add(c)

        active = next_row
        if not active:
            break

    return splits


def part1(lines: list[str]) -> int:
    return count_splits(lines)


def part2(lines: list[str]) -> int:
    grid, (start_row, start_col) = _prepare_grid(lines)
    rows = len(grid)
    width = len(grid[0])

    active: dict[int, int] = {start_col: 1}  # columns -> timeline count

    for r in range(start_row, rows):
        next_row: dict[int, int] = {}

        for c, count in active.items():
            cell = grid[r][c]
            if cell == "^":
                for nc in (c - 1, c + 1):
                    if 0 <= nc < width:
                        next_row[nc] = next_row.get(nc, 0) + count
            else:
                next_row[c] = next_row.get(c, 0) + count

        active = next_row
        if not active:
            break

    # Count timelines that leave the bottom of the grid.
    return sum(active.values())


def run(variant: str | None = None) -> None:
    lines = read_input_lines(YEAR, DAY, variant)
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    run()
