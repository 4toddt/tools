#!/usr/bin/env python3
"""
Scan LB/Storefront + LB/Commerce for evidence lines tied to ACTIVE coverSku fields.
Stdlib only; writes data/trace-active-field-hits.json for human classification.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT.parent.parent.parent  # .../lzb-workspace
ROOTS = [
    WORKSPACE / "atg/la-z-boy/modules/LB/Storefront",
    WORKSPACE / "atg/la-z-boy/modules/LB/Commerce",
]
EXT = {".jsp", ".jspf", ".java", ".properties", ".xml"}
INVENTORY = PROJECT / "bcc-field-inventory.md"
OUT_JSON = PROJECT / "data" / "trace-active-field-hits.json"

# Bare-name search is noisy for these; still record coverSku./sku. hits only unless line has cover context.
BARE_SKIP = {
    "ID",
    "status",
    "description",
    "grade",
    "series",
    "quantity",
    "startDate",
    "endDate",
    "listPrice",
    "salePrice",
    "onSale",
    "wholesalePrice",
}

# Alternate spellings / record keys seen in JSPs
ALIASES: dict[str, list[str]] = {
    "patternName": ["coverSku.patternName", "patternName"],
    "archwayID": ["archwayID", "archwayId", "archway_id"],
}


def active_fields_from_inventory() -> list[str]:
    text = INVENTORY.read_text(encoding="utf-8", errors="replace")
    found: list[str] = []
    for m in re.finditer(r"\| `([^`]+)` \| ACTIVE \|", text):
        found.append(m.group(1))
    out: list[str] = []
    seen: set[str] = set()
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def iter_files():
    for root in ROOTS:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() in EXT and path.is_file():
                yield path


def scan_field(field: str) -> list[dict]:
    tokens: set[str] = {field}
    for a in ALIASES.get(field, []):
        tokens.add(a)
    hits: list[dict] = []
    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(WORKSPACE))
        for i, line in enumerate(text.splitlines(), 1):
            L = line.strip()
            if len(L) > 240:
                L = L[:237] + "..."
            matched = False
            reason = ""
            for tok in tokens:
                if f"coverSku.{tok}" in line or f"sku.{tok}" in line:
                    matched, reason = True, f"record_or_repo:{tok}"
                    break
                if f"['\"]sku.{tok}" in line or f'["\']sku.{tok}' in line:
                    matched, reason = True, f"record_key:{tok}"
                    break
            if matched:
                hits.append({"file": rel, "line": i, "reason": reason, "text": L})
                continue
            # RQL / query style (archCoverAvlb, archwayId)
            if field not in BARE_SKIP and re.search(rf"\b{re.escape(field)}\b", line):
                if any(
                    k in line
                    for k in (
                        "coverSku",
                        "sku.",
                        "repository",
                        "RQL",
                        "queryRQL",
                        "ItemDescriptor",
                        "SecureProductCatalog",
                    )
                ):
                    hits.append(
                        {
                            "file": rel,
                            "line": i,
                            "reason": "bare_in_repo_context",
                            "text": L,
                        }
                    )
    # de-dup exact file+line
    key = {(h["file"], h["line"], h["text"]) for h in hits}
    uniq = []
    seen2: set[tuple[str, int, str]] = set()
    for h in hits:
        t = (h["file"], h["line"], h["text"])
        if t not in seen2:
            seen2.add(t)
            uniq.append(h)
    return sorted(uniq, key=lambda x: (x["file"], x["line"]))


def main() -> None:
    if not INVENTORY.is_file():
        print("Missing", INVENTORY, file=sys.stderr)
        sys.exit(1)
    fields = active_fields_from_inventory()
    report: dict[str, list[dict]] = {}
    for f in fields:
        report[f] = scan_field(f)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSON} for {len(fields)} fields")
    for f in fields:
        print(f"  {f}: {len(report[f])} hits")


if __name__ == "__main__":
    main()
