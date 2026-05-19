#!/usr/bin/env python3
"""
Phase 1 — cover SKU existence only (reference CSV vs BCC export).

Reads the frozen artifacts under data/:
  - cover-skus-by-color.csv (DictReader, utf-8)
  - 260501161753export.csv (ATG export: row 0 metadata, row 1 = headers, row 2+ = data)

Writes:
  - data/phase-1-coverage-summary.md
  - data/phase1-only-in-reference.csv
  - data/phase1-only-in-bcc.csv
  - data/phase1-reference-multi-row-skus.csv  (skuId with >1 non-dropped reference row)

Run from repo root:
  python3 docs/projects/bcc-cover-sku-reconciliation/scripts/phase1_cover_sku_coverage.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REF_CSV = PROJECT / "data" / "cover-skus-by-color.csv"
BCC_CSV = PROJECT / "data" / "260501161753export.csv"
OUT_MD = PROJECT / "data" / "phase-1-coverage-summary.md"
OUT_ONLY_REF = PROJECT / "data" / "phase1-only-in-reference.csv"
OUT_ONLY_BCC = PROJECT / "data" / "phase1-only-in-bcc.csv"
OUT_MULTI = PROJECT / "data" / "phase1-reference-multi-row-skus.csv"


def load_bcc_ids(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    headers = rows[1]
    try:
        ix = headers.index("ID")
    except ValueError as e:
        raise SystemExit("BCC export: no ID column in row 2 headers") from e
    out: set[str] = set()
    for row in rows[2:]:
        if ix >= len(row):
            continue
        v = (row[ix] or "").strip()
        if v:
            out.add(v)
    return out


def main() -> None:
    if not REF_CSV.is_file():
        print("Missing:", REF_CSV, file=sys.stderr)
        sys.exit(1)
    if not BCC_CSV.is_file():
        print("Missing:", BCC_CSV, file=sys.stderr)
        sys.exit(1)

    bcc_ids = load_bcc_ids(BCC_CSV)

    # Non-dropped reference rows: dropStatus != 'dropped' (empty = active)
    ref_rows_active: list[dict[str, str]] = []
    ref_rows_dropped: list[dict[str, str]] = []
    with REF_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ds = (row.get("dropStatus") or "").strip().lower()
            if ds == "dropped":
                ref_rows_dropped.append(row)
            else:
                ref_rows_active.append(row)

    # Existence set A = unique skuId among active (highest confidence for BCC join key parity)
    active_by_sku: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ref_rows_active:
        sid = (row.get("skuId") or "").strip()
        if sid:
            active_by_sku[sid].append(row)

    set_a = frozenset(active_by_sku.keys())
    set_b = frozenset(bcc_ids)
    inter = set_a & set_b
    only_ref = sorted(set_a - set_b)
    only_bcc = sorted(set_b - set_a)

    multi_skus = [(sid, rows) for sid, rows in active_by_sku.items() if len(rows) > 1]
    multi_skus.sort(key=lambda x: x[0])

    iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = []
    lines.append("# Phase 1 — cover SKU coverage (existence only)")
    lines.append("")
    lines.append(f"**Generated (UTC):** `{iso}`")
    lines.append("")
    lines.append("**Inputs:**")
    lines.append(f"- Reference: `{REF_CSV.relative_to(PROJECT.parent)}`")
    lines.append(f"- BCC export: `{BCC_CSV.relative_to(PROJECT.parent)}`")
    lines.append("")
    lines.append("## Definitions (high confidence)")
    lines.append("")
    lines.append(
        "- **Set A:** unique `skuId` from the reference CSV where `dropStatus` ≠ `dropped` "
        "(empty `dropStatus` = active in workbook). One id appears once in **A** even if "
        "the CSV has multiple rows for that id (see multi-row report)."
    )
    lines.append("- **Set B:** unique `ID` from the BCC `coverSku` export.")
    lines.append("- **Set C (audit):** `skuId` rows marked `dropped` in the reference (not used in A/B math).")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------:|")
    lines.append(f"| Reference rows, non-dropped | {len(ref_rows_active)} |")
    lines.append(f"| Reference rows, dropped | {len(ref_rows_dropped)} |")
    lines.append(f"| **\\|A\\|** (unique active `skuId`) | {len(set_a)} |")
    lines.append(f"| **\\|B\\|** (unique BCC `ID`) | {len(set_b)} |")
    lines.append(f"| **\\|A ∩ B\\|** | {len(inter)} |")
    lines.append(f"| **\\|A − B\\|** (in reference, not in BCC) | {len(only_ref)} |")
    lines.append(f"| **\\|B − A\\|** (in BCC, not in reference active set) | {len(only_bcc)} |")
    lines.append(f"| Active `skuId` with **>1** reference row | {len(multi_skus)} |")
    lines.append("")
    lines.append("## Output files (triage)")
    lines.append("")
    lines.append(f"- **`{OUT_ONLY_REF.name}`** — one row per id in **A − B** (plus context columns).")
    lines.append(f"- **`{OUT_ONLY_BCC.name}`** — one row per id in **B − A** (`id` only).")
    lines.append(
        f"- **`{OUT_MULTI.name}`** — ids in **A** with multiple non-dropped reference rows "
        "(workbook split / married-style rows; not a data quality failure)."
    )
    lines.append("")
    lines.append("## Phase 1.2 (human)")
    lines.append("")
    lines.append(
        "Review the two gap CSVs with merchandising / catalog owners: **create** backlog for "
        "**A − B**; **keep / retire / investigate** for **B − A**. No repository writes in Phase 1."
    )
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    # only-in-reference: one row per sku; aggregate source rows
    with OUT_ONLY_REF.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "skuId",
                "ref_row_count",
                "source_rows",
                "issues_union",
                "patternName",
                "colorName",
                "coverType",
            ]
        )
        for sid in only_ref:
            rows = active_by_sku[sid]
            src = ";".join(f"{r.get('sourceSheet')}:{r.get('sourceRow')}" for r in rows)
            issues = "|".join(
                sorted({t for r in rows for t in (r.get("issues") or "").split("|") if t})
            )
            r0 = rows[0]
            w.writerow(
                [
                    sid,
                    len(rows),
                    src,
                    issues,
                    r0.get("patternName", ""),
                    r0.get("colorName", ""),
                    r0.get("coverType", ""),
                ]
            )

    with OUT_ONLY_BCC.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id"])
        for sid in only_bcc:
            w.writerow([sid])

    with OUT_MULTI.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "skuId",
                "ref_row_count",
                "source_rows",
                "issues_union",
                "patternName_sample",
                "colorName_sample",
            ]
        )
        for sid, rows in multi_skus:
            src = ";".join(f"{r.get('sourceSheet')}:{r.get('sourceRow')}" for r in rows)
            issues = "|".join(
                sorted({t for r in rows for t in (r.get("issues") or "").split("|") if t})
            )
            r0 = rows[0]
            w.writerow(
                [
                    sid,
                    len(rows),
                    src,
                    issues,
                    r0.get("patternName", ""),
                    r0.get("colorName", ""),
                ]
            )

    print("Wrote", OUT_MD.relative_to(PROJECT.parent))
    print("Wrote", OUT_ONLY_REF.relative_to(PROJECT.parent), f"({len(only_ref)} rows)")
    print("Wrote", OUT_ONLY_BCC.relative_to(PROJECT.parent), f"({len(only_bcc)} rows)")
    print("Wrote", OUT_MULTI.relative_to(PROJECT.parent), f"({len(multi_skus)} rows)")
    print(f"|A|={len(set_a)} |B|={len(set_b)} |A∩B|={len(inter)} |A-B|={len(only_ref)} |B-A|={len(only_bcc)}")


if __name__ == "__main__":
    main()
