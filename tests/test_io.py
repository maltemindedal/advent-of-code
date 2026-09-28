from __future__ import annotations

from pathlib import Path

import pytest

import utils.io as utils_io
from tests._helpers import PROJECT_ROOT
from utils import get_input_path, read_input, read_input_lines

INPUT_ROOT = PROJECT_ROOT / "inputs"


@pytest.fixture
def input_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point utils.io at an empty temporary inputs directory with a 2025 folder."""

    monkeypatch.setattr(utils_io, "_INPUT_ROOT", tmp_path)
    (tmp_path / "2025").mkdir()
    return tmp_path


@pytest.mark.parametrize(
    ("year", "day", "variant", "expected"),
    [
        (2025, 1, None, "2025/01.txt"),
        ("2025", "01", None, "2025/01.txt"),
        (2025, 12, "sample", "2025/12.sample.txt"),
        (2025, 5, "", "2025/05.txt"),
        (2015, 25, None, "2015/25.txt"),
    ],
)
def test_get_input_path_layout(
    year: int | str, day: int | str, variant: str | None, expected: str
) -> None:
    assert get_input_path(year, day, variant) == INPUT_ROOT / expected


@pytest.mark.parametrize("day", [0, 26, -1])
def test_day_out_of_range(day: int) -> None:
    with pytest.raises(ValueError, match=rf"^Day must be between 1 and 25, got {day}$"):
        get_input_path(2025, day)


def test_day_bounds_are_inclusive() -> None:
    assert get_input_path(2025, 1).name == "01.txt"
    assert get_input_path(2025, 25).name == "25.txt"


def test_year_before_first_event() -> None:
    with pytest.raises(ValueError, match=r"^Year must be 2015 or later, got 2014$"):
        get_input_path(2014, 1)


def test_missing_input_message(input_root: Path) -> None:
    expected = (
        f"Input for 2025 day 3 not found at {input_root / '2025' / '03.txt'}. "
        "Create it or adjust the path."
    )
    with pytest.raises(FileNotFoundError) as excinfo:
        read_input(2025, 3)
    assert str(excinfo.value) == expected


def test_read_input_strips_only_trailing_newlines(input_root: Path) -> None:
    # Leading and trailing spaces are significant (day 6 aligns columns on them).
    (input_root / "2025" / "01.txt").write_text("  a\n\nb \n\n\n", encoding="utf-8")
    assert read_input(2025, 1) == "  a\n\nb "


def test_read_input_decodes_utf8(input_root: Path) -> None:
    (input_root / "2025" / "01.txt").write_bytes("café\n".encode())
    assert read_input(2025, 1) == "café"


def test_read_input_selects_variant(input_root: Path) -> None:
    (input_root / "2025" / "02.txt").write_text("real\n", encoding="utf-8")
    (input_root / "2025" / "02.sample.txt").write_text("sample\n", encoding="utf-8")
    assert read_input(2025, 2) == "real"
    assert read_input(2025, 2, "sample") == "sample"


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("", []),
        ("\n\n", []),
        ("a\nb\n", ["a", "b"]),
        ("a\n\nb\n", ["a", "", "b"]),
        ("a\r\nb\r\n", ["a", "b"]),
        (" x \n", [" x "]),
    ],
)
def test_read_input_lines(input_root: Path, body: str, expected: list[str]) -> None:
    (input_root / "2025" / "02.sample.txt").write_bytes(body.encode())
    assert read_input_lines(2025, 2, "sample") == expected
