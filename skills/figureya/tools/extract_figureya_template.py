#!/usr/bin/env python3
import argparse
import shutil
import zipfile
from pathlib import Path


def safe_target(destination: Path, member: str) -> Path:
    target = (destination / member).resolve()
    destination_resolved = destination.resolve()
    if destination_resolved not in target.parents and target != destination_resolved:
        raise ValueError(f"Unsafe archive member path: {member}")
    return target


def extract_template(zip_path: Path, destination: Path) -> Path:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        members = [name for name in archive.namelist() if name and not name.endswith("/")]
        top_dirs = sorted({name.split("/", 1)[0] for name in members if "/" in name})
        extracted_root = destination / (top_dirs[0] if top_dirs else Path(zip_path).stem)
        for member in members:
            target = safe_target(destination, member)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open("wb") as handle:
                shutil.copyfileobj(source, handle)
    return extracted_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract one FigureYa template ZIP safely.")
    parser.add_argument("zip_path", type=Path, help="Path to one FigureYa*.zip template archive")
    parser.add_argument("destination", type=Path, help="Destination directory")
    args = parser.parse_args()
    print(extract_template(args.zip_path, args.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())