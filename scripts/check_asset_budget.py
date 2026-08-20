#!/usr/bin/env python3
"""Fail when local paper figures exceed the repository image budget."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "content" / "images"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-file-kb", type=int, default=500)
    parser.add_argument("--max-total-mb", type=int, default=25)
    args = parser.parse_args()

    images = [path for path in IMAGE_DIR.rglob("*") if path.suffix.casefold() in EXTENSIONS]
    oversized = [path for path in images if path.stat().st_size > args.max_file_kb * 1024]
    total = sum(path.stat().st_size for path in images)
    if oversized:
        names = ", ".join(str(path.relative_to(ROOT)) for path in oversized)
        raise SystemExit(f"Images over {args.max_file_kb} KB: {names}")
    if total > args.max_total_mb * 1024 * 1024:
        raise SystemExit(f"Image total exceeds {args.max_total_mb} MB")
    print(f"Validated {len(images)} images: {total / 1024:.1f} KB total.")


if __name__ == "__main__":
    main()
