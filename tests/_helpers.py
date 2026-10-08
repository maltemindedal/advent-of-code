from __future__ import annotations

import sys
from functools import cache
from importlib import util
from pathlib import Path
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, module_path: Path) -> ModuleType:
    """Load a test module from a file path."""

    spec = util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {module_name!r} from {module_path}")

    module = util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@cache
def load_day(year: int, day: int) -> ModuleType:
    """Load ``<year>/<DD>/main.py`` once, registered as ``aoc<year>_day<DD>``."""

    path = PROJECT_ROOT / str(year) / f"{day:02d}" / "main.py"
    return load_module(f"aoc{year}_day{day:02d}", path)


def find_days() -> list[tuple[int, int]]:
    """Return ``(year, day)`` for every ``<year>/<DD>/main.py`` in the repository, sorted."""

    return sorted(
        (int(path.parent.parent.name), int(path.parent.name))
        for path in PROJECT_ROOT.glob("[0-9][0-9][0-9][0-9]/[0-9][0-9]/main.py")
    )
