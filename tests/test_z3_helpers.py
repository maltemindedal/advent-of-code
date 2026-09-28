from __future__ import annotations

import z3

from utils.z3_helpers import (
    SAT,
    add_constraints,
    check_solver,
    eval_int,
    int_var,
    make_optimizer,
    make_solver,
    minimize_expr,
    sum_expr,
)


def test_sat_is_z3_sat() -> None:
    assert SAT is z3.sat


def test_int_var_keeps_its_name() -> None:
    assert str(int_var("x0")) == "x0"


def test_int_var_is_an_integer_not_a_real() -> None:
    x = int_var("x")
    assert x.is_int()
    solver = make_solver()
    add_constraints(solver, x > 1, x < 2)
    assert check_solver(solver) == z3.unsat  # satisfiable over the reals


def test_solver_finds_model() -> None:
    x = int_var("x")
    solver = make_solver()
    add_constraints(solver, x > 1, x < 3)
    assert check_solver(solver) == SAT
    assert eval_int(solver.model(), x) == 2


def test_solver_reports_unsat() -> None:
    x = int_var("x")
    solver = make_solver()
    add_constraints(solver, x > 1, x < 1)
    assert check_solver(solver) == z3.unsat


def test_optimizer_minimizes_objective() -> None:
    x = int_var("x")
    y = int_var("y")
    optimizer = make_optimizer()
    add_constraints(optimizer, x >= 3, x <= 20, y >= 4, y <= 20, x + y >= 10)
    minimize_expr(optimizer, sum_expr([x, y]))
    assert check_solver(optimizer) == SAT
    model = optimizer.model()
    assert eval_int(model, x) + eval_int(model, y) == 10


def test_empty_sum_is_plain_zero() -> None:
    # Day 10 builds `sum_expr(contrib) == target` for counters that no button touches.
    total = sum_expr([])
    assert total == 0
    assert isinstance(total, int)


def test_python_bool_is_an_accepted_constraint() -> None:
    # `0 == 0` from an empty sum arrives as a plain bool.
    solver = make_solver()
    add_constraints(solver, True)
    assert check_solver(solver) == SAT


def test_eval_int_completes_unconstrained_variables() -> None:
    solver = make_solver()
    add_constraints(solver, True)
    assert check_solver(solver) == SAT
    assert eval_int(solver.model(), int_var("free")) == 0
