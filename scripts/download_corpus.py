"""Download and verify the versioned Wikipedia corpus artifacts."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_BASE_URL = (
    "https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant/"
    "releases/download/data-v1"
)


@dataclass(frozen=True)
class Artifact:
    filename: str
    destination: Path
    sha256: str

    @property
    def url(self) -> str:
        return f"{RELEASE_BASE_URL}/{self.filename}"


ARTIFACTS = (
    Artifact(
        filename="simpleWikiData.parquet",
        destination=Path("backend/app/data_processing/simpleWikiData.parquet"),
        sha256="668d11a63e5c30f60e483b63b947edc2f2918f8d5c25857710abbdcf7e74b933",
    ),
    Artifact(
        filename="clean_wiki_data.parquet",
        destination=Path(
            "backend/app/data_processing/embeddings_data/clean_wiki_data.parquet"
        ),
        sha256="b9d5e7e184d3b47818ac996e35bab75478e87ef4a871ff66dfb5556aff8d6723",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(artifact: Artifact) -> bool:
    path = REPOSITORY_ROOT / artifact.destination
    return path.is_file() and sha256(path) == artifact.sha256


def download(artifact: Artifact) -> None:
    destination = REPOSITORY_ROOT / artifact.destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(f"{destination.suffix}.part")

    print(f"Downloading {artifact.filename}...")
    try:
        with urllib.request.urlopen(artifact.url) as response, temporary.open("wb") as file:
            shutil.copyfileobj(response, file)
        if sha256(temporary) != artifact.sha256:
            raise RuntimeError(f"Checksum mismatch for {artifact.filename}")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Check local artifacts without downloading missing files.",
    )
    args = parser.parse_args()

    failed = False
    for artifact in ARTIFACTS:
        if verify(artifact):
            print(f"Verified {artifact.destination}")
            continue
        if args.verify_only:
            print(f"Missing or invalid: {artifact.destination}")
            failed = True
            continue
        download(artifact)
        print(f"Verified {artifact.destination}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
