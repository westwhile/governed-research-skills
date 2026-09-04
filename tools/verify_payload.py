#!/usr/bin/env python3
"""Verify the frozen release payload without modifying it."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
RELEASE_PATH = REPOSITORY / "governance" / "RELEASE.json"
MANIFEST_PATH = REPOSITORY / "governance" / "PAYLOAD-MANIFEST.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    payload = REPOSITORY / release["payload"]["path"]
    with MANIFEST_PATH.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    issues: list[str] = []
    expected = {row["relative_path"] for row in rows}
    actual: set[str] = set()

    for directory, directory_names, file_names in os.walk(payload, followlinks=False):
        base = Path(directory)
        for name in directory_names:
            child = base / name
            if child.is_symlink():
                issues.append(f"symlink-directory:{child.relative_to(payload).as_posix()}")
        for name in file_names:
            child = base / name
            relative = child.relative_to(payload).as_posix()
            actual.add(relative)
            if child.is_symlink():
                issues.append(f"symlink-file:{relative}")

    for relative in sorted(expected - actual):
        issues.append(f"missing:{relative}")
    for relative in sorted(actual - expected):
        issues.append(f"extra:{relative}")

    normalized: list[str] = []
    for row in rows:
        relative = row["relative_path"]
        path = payload / Path(relative)
        if relative not in actual:
            continue
        size = path.stat().st_size
        observed = sha256(path)
        if size != int(row["size"]):
            issues.append(f"size:{relative}")
        if observed != row["sha256"]:
            issues.append(f"sha256:{relative}")
        normalized.append(f"{relative}|{size}|{observed}")

    digest = hashlib.sha256("\n".join(normalized).encode("utf-8")).hexdigest()
    if len(rows) != release["payload"]["file_count"]:
        issues.append("manifest-file-count")
    if len(actual) != release["payload"]["file_count"]:
        issues.append("actual-file-count")
    if digest != release["payload"]["normalized_sha256"]:
        issues.append("normalized-sha256")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "payload": str(payload),
        "manifest_rows": len(rows),
        "actual_files": len(actual),
        "normalized_sha256": digest,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
