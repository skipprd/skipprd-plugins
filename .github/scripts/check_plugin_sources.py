#!/usr/bin/env python3
"""Plugin crates must not import skipprd, skippr-core, or host internals."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_MANIFEST = (
    re.compile(r"(?m)^\s*skippr\s*="),
    re.compile(r"(?m)^\s*skippr-core(?:\.workspace|\s*=)"),
)

FORBIDDEN_SOURCE = {
    "direct skippr_core import": re.compile(r"\bskippr_core::"),
    "skipprd crate import": re.compile(r"\bskipprd::"),
    "core ingest import": re.compile(r"\b(?:crate::|skippr_runtime_sdk::)ingest_work\b"),
    "core metadata singleton import": re.compile(
        r"\b(?:crate::|skippr_runtime_sdk::)(?:METADATA|PIPELINE_SCHEMA_VERSION)\b"
    ),
    "core buffer module import": re.compile(r"\b(?:crate::|skippr_runtime_sdk::)buffer\b"),
    "core compactor module import": re.compile(r"\b(?:crate::|skippr_runtime_sdk::)engine\b"),
    "core runtime host import": re.compile(
        r"\b(?:crate::|skippr_runtime_sdk::)runtime_plugins::host\b"
    ),
    "deleted sink_compat import": re.compile(r"\bsink_compat\b"),
    "deleted source_compat import": re.compile(r"\bsource_compat\b"),
    "SDK RUNNING is AtomicBool": re.compile(r"\bRUNNING\.read\s*\("),
}


def collect_violations() -> list[str]:
    hits: list[str] = []
    for manifest in sorted((ROOT / "plugins").glob("**/Cargo.toml")):
        text = manifest.read_text(encoding="utf-8")
        relative = manifest.relative_to(ROOT)
        for pattern in FORBIDDEN_MANIFEST:
            if pattern.search(text):
                hits.append(str(relative))
                break
    for source in sorted((ROOT / "plugins").rglob("*")):
        if not source.is_file() or source.suffix not in {".rs", ".toml"}:
            continue
        text = source.read_text(encoding="utf-8", errors="ignore")
        relative = source.relative_to(ROOT)
        for label, pattern in FORBIDDEN_SOURCE.items():
            if pattern.search(text):
                hits.append(f"{relative}: {label}")
    return hits


def main() -> int:
    hits = collect_violations()
    if hits:
        print("plugin source boundary violated:", file=sys.stderr)
        for hit in hits:
            print(f"  - {hit}", file=sys.stderr)
        return 1
    print("plugin source boundary check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
