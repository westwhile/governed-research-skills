#!/usr/bin/env python3
"""Audit v1.0.1 licensing metadata and synthetic citation fixtures."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PAYLOAD = REPOSITORY / "payload" / "runtime-receiver"
REFERENCES = (
    PAYLOAD
    / ".agents"
    / "skills"
    / "nature-academic-search"
    / "references"
)
CONVERTERS = REFERENCES.parent / "scripts" / "converters.py"
APACHE_2_LICENSE_SHA256 = (
    "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
)
SYNTHETIC_FIXTURES = {
    "nbib": REFERENCES / "pubmed-synthetic-record.nbib",
    "ris": REFERENCES / "pubmed-synthetic-record.ris",
    "bib": REFERENCES / "pubmed-synthetic-record.bib",
}
REMOVED_FIXTURES = [
    REFERENCES / "pubmed-28344011.nbib",
    REFERENCES / "pubmed-28344011.ris",
    REFERENCES / "pubmed-28344011.bib",
]
FORBIDDEN_PUBLISHER_BYTES = [
    b"Copyright (c) 2017 Elsevier Ltd. All rights reserved.",
    b"Global tuberculosis incidence has declined marginally",
    b"10.1016/S2213-2600(17)30079-6",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_converters():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("release_audit_converters", CONVERTERS)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load citation converters")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    issues: list[str] = []

    license_path = REPOSITORY / "LICENSE"
    if not license_path.is_file() or sha256(license_path) != APACHE_2_LICENSE_SHA256:
        issues.append("apache-license-bytes")
    if not (REPOSITORY / "NOTICE").is_file():
        issues.append("notice-missing")

    try:
        release = json.loads(
            (REPOSITORY / "governance" / "RELEASE.json").read_text(encoding="utf-8")
        )
        license_info = release.get("license", {})
        if license_info.get("identifier") != "Apache-2.0":
            issues.append("release-license-identifier")
        if license_info.get("open_source") is not True:
            issues.append("release-open-source-flag")
        if license_info.get("publisher_abstracts_included") is not False:
            issues.append("publisher-abstract-flag")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        issues.append(f"release-metadata:{type(exc).__name__}")

    for path in REMOVED_FIXTURES:
        if path.exists():
            issues.append(f"removed-fixture-present:{path.name}")
    for path in SYNTHETIC_FIXTURES.values():
        if not path.is_file():
            issues.append(f"synthetic-fixture-missing:{path.name}")

    scanned_files = 0
    reparse_items: list[str] = []
    for directory, directory_names, file_names in os.walk(PAYLOAD, followlinks=False):
        base = Path(directory)
        for name in directory_names:
            child = base / name
            if child.is_symlink():
                reparse_items.append(child.relative_to(PAYLOAD).as_posix())
        for name in file_names:
            child = base / name
            relative = child.relative_to(PAYLOAD).as_posix()
            scanned_files += 1
            if child.is_symlink():
                reparse_items.append(relative)
            content = child.read_bytes()
            for marker in FORBIDDEN_PUBLISHER_BYTES:
                if marker in content:
                    issues.append(f"publisher-content:{relative}")
    if reparse_items:
        issues.append(f"reparse-items:{len(reparse_items)}")

    if all(path.is_file() for path in SYNTHETIC_FIXTURES.values()):
        try:
            converters = load_converters()
            source = SYNTHETIC_FIXTURES["nbib"].read_text(encoding="utf-8")
            for format_name in ("ris", "bib"):
                generated = converters.convert_from_medline(source, format_name)
                committed = SYNTHETIC_FIXTURES[format_name].read_text(encoding="utf-8")
                if generated != committed:
                    issues.append(f"fixture-conversion:{format_name}")
        except Exception as exc:  # fail closed and report the exception class
            issues.append(f"fixture-conversion-error:{type(exc).__name__}")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "payload_files_scanned": scanned_files,
        "license_sha256": sha256(license_path) if license_path.is_file() else None,
        "synthetic_fixtures": {
            name: {
                "path": path.relative_to(REPOSITORY).as_posix(),
                "sha256": sha256(path) if path.is_file() else None,
            }
            for name, path in SYNTHETIC_FIXTURES.items()
        },
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
