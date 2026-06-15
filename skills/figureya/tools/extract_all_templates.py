#!/usr/bin/env python3
import argparse
from pathlib import Path

from extract_figureya_template import extract_template


def extract_all(source_dir: Path, destination: Path) -> list[Path]:
    source_dir = Path(source_dir)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    zip_paths = sorted(source_dir.glob("FigureYa*.zip"), key=lambda path: path.name.lower())
    return [extract_template(zip_path, destination) for zip_path in zip_paths]


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract all nested FigureYa*.zip template archives into one directory.")
    parser.add_argument("source_dir", type=Path, help="Directory containing nested FigureYa*.zip template archives")
    parser.add_argument("destination", type=Path, help="Directory for extracted template folders")
    args = parser.parse_args()
    extracted = extract_all(args.source_dir, args.destination)
    print(f"Extracted {len(extracted)} templates to {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())