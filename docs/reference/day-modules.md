# Day modules reference

The layout every solution module follows, and an index of the functions each day exposes. To create a new module, follow [Adding a day](../guides/adding-a-day.md).

## Module layout

Each puzzle day is one file, `<year>/<DD>/main.py`, for example `2025/01/main.py`. The year and day folders are plain directories, not Python packages. Their names are not valid identifiers, so `import 2025.01.main` is a syntax error; load a module by file path instead (see [Running a day](../guides/running-a-day.md#call-the-functions-from-python)).

Every 2025 module defines:

| Name | Signature | Purpose |
| --- | --- | --- |
| `YEAR` | `int` | Puzzle year, passed to `read_input_lines`. |
| `DAY` | `int` | Puzzle day, passed to `read_input_lines`. |
| `parse_input` | `(lines) -> <parsed>` | Turns input lines into the day's data structure. Day 7 has none. |
| `part1` | `(<parsed>, ...) -> int` | Answer to part 1. |
| `part2` | `(<parsed>, ...) -> int` | Answer to part 2. |
| `run` | `(variant: str \| None = None) -> None` | Reads `inputs/<YEAR>/<DD>[.<variant>].txt` with `read_input_lines`, parses it and prints the answers. |

A module run as a script calls `run()` with no arguments, so it always reads the real input.

`run` prints exactly two lines, `Part 1: <answer>` and `Part 2: <answer>`. Day 12 is the exception: it prints one line, `Solution: <answer>`. `tests/test_cli.py` pins this output for every day.

Names starting with `_` are internal helpers.

## 2025 entry points

| Day | `parse_input` returns | `part1` | `part2` |
| --- | --- | --- | --- |
| 1 | `list[Rotation]` | `(rotations, start=50)` | `(rotations, start=50)` |
| 2 | `list[IdRange]` | `(ranges)` | `(ranges)` |
| 3 | `list[str]` | `(banks)` | `(banks)` |
| 4 | `list[str]` | `(grid)` | `(grid)` |
| 5 | `tuple[list[IdRange], list[int]]` | `(ranges, available_ids)` | `(ranges, available_ids=None)`: `available_ids` does not affect the result |
| 6 | `list[Problem]` | `(problems)` | `(lines)`: takes the raw input lines and parses them with `parse_input_columns` |
| 7 | (no `parse_input`) | `(lines)` | `(lines)` |
| 8 | `list[Point3D]` | `(points, pairs_to_connect=1000)` | `(points)` |
| 9 | `list[Point]` | `(points)` | `(points)` |
| 10 | `list[Machine]` | `(machines)` | `(machines)`: solved as an integer program with `utils.z3_helpers` |
| 11 | `Graph` (`dict[str, list[str]]`) | `(graph, start="you", end="out")` | `(graph, start="svr", end="out", required=("dac", "fft"))` |
| 12 | `ParsedInput` | `(parsed)` | `(parsed)`: returns the same value as `part1` |

`parse_input` accepts `list[str]` on days 1 to 9 and any `Iterable[str]` on days 10 to 12.

## 2025 sample output

What `run("sample")` prints for each day, as pinned in `tests/test_cli.py`:

| Day | Output | Note |
| --- | --- | --- |
| 1 | `Part 1: 3` / `Part 2: 6` | |
| 2 | `Part 1: 1227775554` / `Part 2: 4174379265` | |
| 3 | `Part 1: 357` / `Part 2: 3121910778619` | |
| 4 | `Part 1: 13` / `Part 2: 43` | |
| 5 | `Part 1: 3` / `Part 2: 14` | |
| 6 | `Part 1: 4277556` / `Part 2: 3263827` | |
| 7 | `Part 1: 21` / `Part 2: 40` | |
| 8 | `Part 1: 20` / `Part 2: 25272` | `run` uses the default 1000 pairs. The puzzle's example answer, 40, comes from `part1(points, pairs_to_connect=10)`. |
| 9 | `Part 1: 50` / `Part 2: 24` | |
| 10 | `Part 1: 7` / `Part 2: 33` | |
| 11 | `Part 1: 5` / `Part 2: 0` | The sample is the part 1 example and has no `svr` node, so part 2 finds no paths. |
| 12 | `Solution: 2` | Single line; see [Module layout](#module-layout). |

## Other public functions

Functions without a leading `_` beyond the entry points above. The tests call several of them directly.

| Day | Function | Description |
| --- | --- | --- |
| 1 | `apply_rotation(position, rotation) -> int` | Apply a rotation and return the new position on a dial numbered 0 to 99. |
| 3 | `max_bank_joltage(bank) -> int` | Return the maximum two-digit joltage that can be formed from a bank. |
| 6 | `parse_input_columns(lines) -> list[Problem]` | Parse problems whose numbers run top-to-bottom within columns. |
| 7 | `count_splits(lines) -> int` | Count beam splits while traversing the manifold. |
| 8 | `squared_euclidean(a, b) -> int`, `manhattan(a, b) -> int` | Squared Euclidean and Manhattan distance between two `Point3D`s. `part1` and `part2` use `squared_euclidean`. |
| 8 | `connect_closest(points, pairs_to_connect, distance) -> CircuitResult` | Connect the closest pairs and return the circuit sizes. |
| 8 | `last_connection_product(points, distance) -> int` | Return the X-coordinate product of the edge that finishes connectivity. |
| 9 | `largest_rectangle_two_corners(points) -> int` | Largest area using any two red tiles as opposite corners. |
| 12 | `can_fit_region(shapes, region) -> bool` | Return True if a region can fit all requested presents. |
