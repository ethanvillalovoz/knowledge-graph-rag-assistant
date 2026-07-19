"""Download and verify the pinned embedding matrix and FAISS index."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DATASET_REVISION = "b88b9c93be2943f05485874914af00c47b82fc18"
DATASET_BASE_URL = (
    "https://huggingface.co/datasets/miverson9/"
    f"acme10-he-ragapp-embeddings/resolve/{DATASET_REVISION}"
)


@dataclass(frozen=True)
class Artifact:
    filename: str
    destination: Path
    sha256: str

    @property
    def url(self) -> str:
        return f"{DATASET_BASE_URL}/{self.filename}"


ARTIFACTS = (
    Artifact(
        filename="text_embeddings.npy",
        destination=Path(
            "backend/app/data_processing/embeddings_data/text_embeddings.npy"
        ),
        sha256="98592d86c93dbf474decba8b79426cd3c57c73c607b650692ce2df0398fbad74",
    ),
    Artifact(
        filename="index.faiss",
        destination=Path(
            "backend/app/data_processing/vector_search_data/index.faiss"
        ),
        sha256="1e87e64080acfce1cbc3ecad2b3a8ae80900dde935135042dc2481675d340b1a",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def destination(artifact: Artifact) -> Path:
    return REPOSITORY_ROOT / artifact.destination


def verify(artifact: Artifact) -> bool:
    path = destination(artifact)
    return path.is_file() and sha256(path) == artifact.sha256


def download(artifact: Artifact) -> None:
    target = destination(artifact)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(f"{target.suffix}.part")

    print(f"Downloading {artifact.filename} from revision {DATASET_REVISION}...")
    try:
        with urllib.request.urlopen(artifact.url) as response, temporary.open(
            "wb"
        ) as file:
            shutil.copyfileobj(response, file)
        if sha256(temporary) != artifact.sha256:
            raise RuntimeError(f"Checksum mismatch for {artifact.filename}")
        temporary.replace(target)
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
