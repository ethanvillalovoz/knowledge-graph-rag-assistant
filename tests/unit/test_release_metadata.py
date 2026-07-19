import tomllib
from pathlib import Path

from backend.app.main import app


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_release_versions_are_aligned():
    pyproject = tomllib.loads(
        (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    citation_version = next(
        line.removeprefix("version:").strip()
        for line in (REPOSITORY_ROOT / "CITATION.cff")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.startswith("version:")
    )

    assert pyproject["project"]["version"] == "1.1.1"
    assert app.version == pyproject["project"]["version"]
    assert citation_version == pyproject["project"]["version"]
