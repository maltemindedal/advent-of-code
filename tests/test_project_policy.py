from __future__ import annotations

import tomllib

from tests._helpers import PROJECT_ROOT


def _read(relative: str) -> str:
    return (PROJECT_ROOT / relative).read_text(encoding="utf-8")


def test_z3_floor_stays_at_the_oldest_verified_version() -> None:
    dependencies = tomllib.loads(_read("pyproject.toml"))["project"]["dependencies"]
    assert "z3-solver>=4.12.4" in dependencies, (
        "Keep the z3-solver floor at >=4.12.4 (the suite passes on 4.12.4.0). "
        "Dependabot raises it with each bump: restore the specifier in pyproject.toml, "
        "run `uv lock`, and keep the new locked version."
    )


def test_dependabot_sets_no_cooldown() -> None:
    assert "cooldown" not in _read(".github/dependabot.yml"), (
        "The owner removed the Dependabot cooldown in b9f512f: leave release timing "
        "to Dependabot's default and delete the cooldown block."
    )


def test_uv_sets_no_release_age_rule() -> None:
    assert "exclude-newer" not in _read("pyproject.toml"), (
        "No release-age rule for uv (b9f512f): delete `exclude-newer` from pyproject.toml "
        "and run `uv lock`."
    )
