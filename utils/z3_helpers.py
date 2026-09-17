from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast

try:
    import z3  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover - dependency should be installed
    raise ImportError("z3-solver is required. Install with `uv add z3-solver`.") from exc

ArithExpr = z3.ArithRef
Expr = z3.ExprRef
SolverLike = z3.Solver | z3.Optimize
SAT = z3.sat


def make_solver() -> z3.Solver:
    """Create a z3 solver."""

    return z3.Solver()


def make_optimizer() -> z3.Optimize:
    """Create a z3 optimizer."""

    return z3.Optimize()


def int_var(name: str) -> z3.ArithRef:
    """Create an integer variable."""

    return cast(z3.ArithRef, z3.Int(name))


def add_constraints(solver: SolverLike, *constraints: object) -> None:
    """Add constraints to a solver."""

    cast(Any, solver).add(*constraints)


def sum_expr(terms: Sequence[z3.ArithRef]) -> z3.ArithRef | int:
    """Build a sum expression from z3 arithmetic terms."""

    return cast(z3.ArithRef | int, z3.Sum(terms))


def minimize_expr(solver: z3.Optimize, expr: z3.ArithRef | int) -> None:
    """Add a minimization objective to a z3 optimizer."""

    cast(Any, solver).minimize(expr)


def check_solver(solver: SolverLike) -> z3.CheckSatResult:
    """Check whether the solver's constraints are satisfiable."""

    return cast("z3.CheckSatResult", cast(Any, solver).check())


def eval_int(model: z3.ModelRef, expr: z3.ExprRef) -> int:
    """Evaluate an integer expression in a z3 model."""

    value = cast("z3.IntNumRef", cast(Any, model).eval(expr, model_completion=True))
    return int(value.as_long())
