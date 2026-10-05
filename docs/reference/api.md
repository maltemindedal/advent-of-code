# `utils` API reference

The `utils` package holds the code shared by every day: input-file I/O in `utils.io` and typed z3 wrappers in `utils.z3_helpers`. For the functions each day module exposes, see [Day modules](day-modules.md).

`utils` re-exports the three `utils.io` functions:

```python
from utils import get_input_path, read_input, read_input_lines
```

It does not re-export `utils.z3_helpers`, and importing `utils` does not import z3.

## Input file layout

All inputs live under `inputs/` at the repository root:

```text
inputs/<year>/<DD>.txt             real input, for example inputs/2025/01.txt
inputs/<year>/<DD>.<variant>.txt   variant, for example inputs/2025/01.sample.txt
```

| Part | Rule |
| --- | --- |
| `<year>` | Integer 2015 or later, written in full. |
| `<DD>` | Day 1 to 25, zero-padded to two digits. |
| `<variant>` | Any string. An empty string means no variant. |

Git tracks only files ending in `.sample.txt`. Real inputs and every other variant stay on your machine (see [Configuration: `.gitignore`](configuration.md#gitignore)).

The path is resolved from the location of `utils/io.py`, not from the current working directory.

## `utils.io`

### `get_input_path(year, day, variant=None) -> Path`

Returns the absolute path of an input file. It does not check that the file exists.

| Parameter | Type | Description |
| --- | --- | --- |
| `year` | `int \| str` | Puzzle year, such as `2025` or `"2025"`. |
| `day` | `int \| str` | Day number, such as `1`, `"1"` or `"01"`. |
| `variant` | `str \| None` | Filename suffix, such as `"sample"`. `None` or `""` selects the real input. |

| Raises | When | Message |
| --- | --- | --- |
| `ValueError` | `day` is outside 1 to 25 | `Day must be between 1 and 25, got <day>` |
| `ValueError` | `year` is before 2015 | `Year must be 2015 or later, got <year>` |
| `ValueError` | `year` or `day` is not an integer string | Raised by `int()`, for example `invalid literal for int() with base 10: 'x'` |

```python
get_input_path(2025, 1)  # <repo>/inputs/2025/01.txt
get_input_path("2025", "12", "sample")  # <repo>/inputs/2025/12.sample.txt
```

### `read_input(year, day, variant=None) -> str`

Reads the whole input file as UTF-8 text and returns it as one string.

- Line endings are normalised: `\r\n` becomes `\n`.
- Trailing newlines are removed. All other whitespace, including leading and trailing spaces on a line, is kept, because some puzzles align columns with spaces.

Parameters are the same as `get_input_path`. It raises the same `ValueError`s, plus:

| Raises | When | Message |
| --- | --- | --- |
| `FileNotFoundError` | The file does not exist | `Input for <year> day <day> not found at <path>. Create it or adjust the path.` |

### `read_input_lines(year, day, variant=None) -> list[str]`

Returns `read_input(...)` split into lines, without line terminators. Blank lines inside the file are kept as `""`; trailing blank lines are dropped. An empty file returns `[]`.

| File contents | Result |
| --- | --- |
| `"a\nb\n"` | `["a", "b"]` |
| `"a\n\nb\n"` | `["a", "", "b"]` |
| `"a\r\nb\r\n"` | `["a", "b"]` |
| `" x \n"` | `[" x "]` |
| `"\n\n"` | `[]` |

## `utils.z3_helpers`

Typed wrappers around the [z3-solver](https://pypi.org/project/z3-solver/) Python API. z3's own API is largely untyped; these functions give callers concrete types so they pass ty's strict checks. 2025 day 10 part 2 is the only caller.

Importing the module raises ``ImportError("z3-solver is required. Install with `uv add z3-solver`.")`` if z3 is not installed. `z3-solver` is already a project dependency, so `uv sync` installs it.

### Type aliases and constants

| Name | Value |
| --- | --- |
| `ArithExpr` | `z3.ArithRef` |
| `Expr` | `z3.ExprRef` |
| `SolverLike` | `z3.Solver \| z3.Optimize` |
| `SAT` | `z3.sat`, the result `check_solver` returns when the constraints are satisfiable |

### Functions

| Function | Returns | Description |
| --- | --- | --- |
| `make_solver()` | `z3.Solver` | New satisfiability solver. |
| `make_optimizer()` | `z3.Optimize` | New optimizer, for problems with an objective. |
| `int_var(name: str)` | `z3.ArithRef` | Integer (not real) variable named `name`. |
| `add_constraints(solver: SolverLike, *constraints: object)` | `None` | Adds constraints. A plain Python `bool` is accepted. |
| `sum_expr(terms: Sequence[z3.ArithRef])` | `z3.ArithRef \| int` | Sum of `terms`. An empty sequence returns the Python `int` `0`. |
| `minimize_expr(solver: z3.Optimize, expr: z3.ArithRef \| int)` | `None` | Adds a minimisation objective. |
| `check_solver(solver: SolverLike)` | `z3.CheckSatResult` | Runs the solver: `SAT`, `z3.unsat` or `z3.unknown`. |
| `eval_int(model: z3.ModelRef, expr: z3.ExprRef)` | `int` | Value of `expr` in `model`. Variables the model leaves unconstrained evaluate to `0`. |

### Example

```python
from utils.z3_helpers import (
    SAT,
    add_constraints,
    check_solver,
    eval_int,
    int_var,
    make_optimizer,
    minimize_expr,
    sum_expr,
)

x = int_var("x")
y = int_var("y")
optimizer = make_optimizer()
add_constraints(optimizer, x >= 3, y >= 4, x + y >= 10)
minimize_expr(optimizer, sum_expr([x, y]))
assert check_solver(optimizer) == SAT
model = optimizer.model()
print(eval_int(model, x) + eval_int(model, y))  # 10
```
