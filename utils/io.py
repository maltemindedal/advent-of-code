from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_INPUT_ROOT = _ROOT / "inputs"


def _day_str(day: int | str) -> str:
    day_int = int(day)
    if not 1 <= day_int <= 25:
        raise ValueError(f"Day must be between 1 and 25, got {day}")
    return f"{day_int:02d}"


def _year_str(year: int | str) -> str:
    year_int = int(year)
    if year_int < 2015:
        # Advent of Code began in 2015
        raise ValueError(f"Year must be 2015 or later, got {year}")
    return str(year_int)


def get_input_path(year: int | str, day: int | str, variant: str | None = None) -> Path:
    """Return the input path for a year and day.

    Parameters
    ----------
    year: int | str
        Advent of Code year, such as 2025.
    day: int | str
        Day number, such as 1 or "01".
    variant: str | None
        Optional filename suffix, such as "sample".
    """

    year_part = _year_str(year)
    day_part = _day_str(day)

    filename = day_part
    if variant:
        filename = f"{filename}.{variant}"

    return _INPUT_ROOT / year_part / f"{filename}.txt"


def read_input(year: int | str, day: int | str, variant: str | None = None) -> str:
    """Read the entire input file as a string."""

    path = get_input_path(year, day, variant)
    if not path.exists():
        raise FileNotFoundError(
            f"Input for {year} day {day} not found at {path}. Create it or adjust the path."
        )
    return path.read_text(encoding="utf-8").rstrip("\n")


def read_input_lines(year: int | str, day: int | str, variant: str | None = None) -> list[str]:
    """Read the input file and return its lines."""

    content = read_input(year, day, variant)
    return [line.rstrip("\n") for line in content.splitlines()]
