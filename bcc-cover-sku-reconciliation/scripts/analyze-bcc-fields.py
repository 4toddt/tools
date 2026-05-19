#!/usr/bin/env python3
"""
Analyze BCC coverSku CSV export against ATG schema, feed mapping, Endeca index
config, codebase references, and population statistics. Emits bcc-field-inventory.md.

Run from repo root:

    python3 docs/projects/bcc-cover-sku-reconciliation/scripts/analyze-bcc-fields.py

Or from ``scripts/``:

    python3 analyze-bcc-fields.py
"""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

# .../bcc-cover-sku-reconciliation (parent of scripts/)
PROJECT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT.parent.parent.parent  # .../lzb-workspace
EXPORT_CSV = PROJECT / "data" / "260501161753export.csv"
COMMERCE_CATALOG = (
    WORKSPACE
    / "atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml"
)
FEED_PROPS = (
    WORKSPACE
    / "atg/la-z-boy/modules/LB/Commerce/config/com/lzb/feed/product/LZBCatalogSourceDestinationMapping.properties"
)
INDEX_CONFIG = (
    WORKSPACE
    / "atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml"
)
ATG_MODULES = WORKSPACE / "atg/la-z-boy/modules"
OUTPUT_MD = PROJECT / "bcc-field-inventory.md"

DESCRIPTOR_EXCLUDE_GLOBS = [
    "!**/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml",
    "!**/LB/Merchandising/config/atg/commerce/catalog/custom/customCatalog.xml",
]


def parse_item_descriptor_properties(xml_path: Path, descriptor_name: str) -> dict[str, dict]:
    """Return map property_name -> {data_type, column_name, default, display_name, table_hint}."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    desc = None
    for el in root.iter("item-descriptor"):
        if el.get("name") == descriptor_name:
            desc = el
            break
    if desc is None:
        return {}
    out: dict[str, dict] = {}
    for prop in desc.iter("property"):
        name = prop.get("name")
        if not name:
            continue
        column_name = prop.get("column-name") or ""
        out[name] = {
            "data_type": prop.get("data-type") or prop.get("component-data-type") or "",
            "column_name": column_name,
            "default": prop.get("default") or "",
            "display_name": prop.get("display-name") or prop.get("display-name-resource") or "",
            "descriptor": descriptor_name,
            "source_file": str(xml_path.relative_to(WORKSPACE)),
        }
    return out


def parse_cover_sku_schema() -> dict[str, dict]:
    """Merge `sku` + `coverSku` property definitions from customCatalog.xml."""
    sku_props = parse_item_descriptor_properties(COMMERCE_CATALOG, "sku")
    cover_props = parse_item_descriptor_properties(COMMERCE_CATALOG, "coverSku")
    merged = {**sku_props, **cover_props}
    return merged


def _pick_preferred_xml_path(paths: list[str]) -> str | None:
    """Prefer `customCatalog.xml` when the same property appears in multiple XML files."""
    if not paths:
        return None
    for p in paths:
        if "customCatalog.xml" in p:
            return p
    return paths[0]


def _find_property_xml_fallback(java_property: str) -> str | None:
    """Scan config XML when ripgrep is unavailable (slow; cached per field)."""
    needle = f'name="{java_property}"'
    scan_roots = [
        ATG_MODULES / "LB/Commerce/config",
        ATG_MODULES / "LB/Endeca/config",
        ATG_MODULES / "LB/Merchandising/config",
        ATG_MODULES / "LB/Base/config",
    ]
    matches: list[str] = []
    for root in scan_roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.xml"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if needle in text:
                try:
                    matches.append(str(path.relative_to(WORKSPACE)))
                except ValueError:
                    matches.append(str(path))
    return _pick_preferred_xml_path(matches)


def find_property_xml_repo_wide(java_property: str) -> str | None:
    """First XML file under modules defining name=\"java_property\" on a property element."""
    if java_property == "ID":
        return None
    if shutil.which("rg"):
        try:
            r = subprocess.run(
                [
                    "rg",
                    "-l",
                    "--glob",
                    "*.xml",
                    f'name="{java_property}"',
                    str(ATG_MODULES),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            return _find_property_xml_fallback(java_property)
        if r.returncode == 0 and r.stdout.strip():
            rels: list[str] = []
            for line in r.stdout.strip().splitlines():
                pth = line.strip()
                if not pth:
                    continue
                try:
                    rels.append(str(Path(pth).relative_to(WORKSPACE)))
                except ValueError:
                    rels.append(pth)
            dedup = list(dict.fromkeys(rels))
            picked = _pick_preferred_xml_path(dedup)
            if picked:
                return picked
    return _find_property_xml_fallback(java_property)


def parse_feed_cover_properties() -> set[str]:
    """Right-hand side Java property names from coverFileSrcDestMap only."""
    text = FEED_PROPS.read_text(encoding="utf-8", errors="replace")
    props: set[str] = set()
    in_cover_file = False
    for line in text.splitlines():
        if line.strip().startswith("coverFileSrcDestMap="):
            in_cover_file = True
            continue
        if in_cover_file:
            if line.strip().startswith("productFileSrcDestMap"):
                break
            chunk = line.strip().rstrip("\\").strip()
            if not chunk or chunk.startswith("#"):
                continue
            for part in chunk.split(","):
                part = part.strip()
                if "=" in part:
                    _, rhs = part.split("=", 1)
                    props.add(rhs.strip())
    return props


def parse_indexed_for_cover_sku() -> set[str]:
    tree = ET.parse(INDEX_CONFIG)
    root = tree.getroot()
    container = None
    for item in root.iter("item"):
        if item.get("property-name") == "childSKUs":
            container = item
            break
    if container is None:
        return set()
    indexed: set[str] = set()
    for prop in container.iter("property"):
        name = prop.get("name")
        if not name or name.startswith("$"):
            continue
        st = prop.get("subtype")
        if st is None or st == "coverSku":
            indexed.add(name)
    return indexed


def rg_code_hits(java_property: str) -> int:
    """Count matches in Java/JSP/properties (excluding repository descriptors)."""
    if java_property == "ID":
        return -1
    args = [
        "rg",
        "--count-matches",
        "-w",
        java_property,
        str(ATG_MODULES),
        "--glob",
        "*.java",
        "--glob",
        "*.jsp",
        "--glob",
        "*.jspf",
        "--glob",
        "*.properties",
        "--glob",
        "*.xml",
    ]
    for g in DESCRIPTOR_EXCLUDE_GLOBS:
        args.extend(["--glob", g])
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        # fallback: no ripgrep
        return -2
    except subprocess.TimeoutExpired:
        return -3
    if r.returncode not in (0, 1):
        return 0
    total = 0
    for line in r.stdout.splitlines():
        if ":" in line:
            try:
                total += int(line.split(":")[-1])
            except ValueError:
                pass
    return total


def column_stats(
    path: Path, headers: list[str]
) -> tuple[dict[str, float], dict[str, int], dict[str, list[str]]]:
    """non_null_pct, distinct_count, top_values (max 5)."""
    non_empty = Counter()
    distinct_sets: dict[str, set[str]] = {h: set() for h in headers}
    total = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    data_rows = rows[2:]
    for row in data_rows:
        if len(row) < len(headers):
            continue
        total += 1
        for i, h in enumerate(headers):
            v = row[i] if i < len(row) else ""
            s = (v or "").strip()
            if s != "":
                non_empty[h] += 1
            if s != "":
                distinct_sets[h].add(s[:200])
    pct = {h: (non_empty[h] / total * 100.0) if total else 0.0 for h in headers}
    dcount = {h: len(distinct_sets[h]) for h in headers}
    idx_map = {h: i for i, h in enumerate(headers)}
    top: dict[str, list[str]] = {}
    for h in headers:
        c = Counter()
        ix = idx_map[h]
        for row in data_rows:
            if ix >= len(row):
                continue
            v = (row[ix] or "").strip()
            if v:
                c[v[:100]] += 1
        top[h] = [f"{x} ({n})" for x, n in c.most_common(5)]
    return pct, dcount, top


def classify(
    field: str,
    schema_known: bool,
    in_feed: bool,
    in_index: bool,
    code_hits: int,
    non_null_pct: float,
) -> str:
    """schema_known = property found in customCatalog sku/coverSku OR elsewhere in *.xml OR ID."""
    if field == "ID":
        return "ACTIVE"
    # Feed / index define wire-active columns even when property is not in LZB customCatalog.xml
    # (e.g. ATG stock sku pricing fields merged via xml-combine).
    if in_feed or in_index:
        return "ACTIVE"
    if not schema_known:
        return "ORPHAN"
    # ripgrep missing (-2) or timeout (-3): treat hit count as 0 for population-based buckets
    hits = 0 if code_hits in (-2, -3) else (code_hits if code_hits >= 0 else 0)
    if non_null_pct == 0.0 and hits == 0:
        return "DORMANT"
    if non_null_pct > 0 and hits == 0:
        return "LEGACY"
    if hits >= 3:
        return "ACTIVE"
    return "UNCLEAR"


CLUSTER_MAP = {
    "identity": ["ID"],
    "pricing": [
        "listPrice",
        "salePrice",
        "wholesalePrice",
        "nonreturnable",
        "discountable",
        "onSale",
    ],
    "dates_status": ["startDate", "endDate", "status", "creationDate", "coverStatus"],
    "online_visibility": [
        "showOnline",
        "unsearchable",
        "hideForTextSearch",
        "hideForCA",
        "onlineExclusive",
        "onlineExclusiveText",
        "onlineOnly",
    ],
    "images_media": [
        "largeImage",
        "smallImage",
        "thumbnailImage",
        "pdpDefaultImage",
        "cdpDefaultImage",
        "cdpMouseOverImage",
        "dimensionImage",
        "altImages",
        "colorFamilyImages",
        "auxiliaryMedia",
        "videos",
        "belowFoldVideoMedia",
        "belowFoldHowToMedia",
        "wtbFeatureImg1",
        "wtbFeatureImg1Alt",
        "wtbFeatureImg1Caption",
        "wtbFeatureImg2",
        "wtbFeatureImg2Alt",
        "wtbFeatureImg2Caption",
        "wtbLeftImg",
    ],
    "cover_core": [
        "coverType",
        "patternName",
        "collectionName",
        "colorDescription",
        "coverColor",
        "colorNumber",
        "capCode",
        "cleaningCode",
        "wearability",
        "wearDatedId",
        "faceContents",
        "grade",
        "series",
        "productCategoryCode",
        "prodCategoryDesc",
        "commodityCode",
        "performanceFabricFlag",
        "addedMaterialTypes",
        "additionalDetails",
        "description",
    ],
    "pdp_below_fold": [
        "atAGlanceContent",
        "hideAGlance",
        "perfectForInfo",
        "romanceCopy",
        "careFeatures",
        "useCareInstructions",
        "warrantyInfo",
        "stillDecidingLinks",
        "displayHeader",
        "headerText",
        "hideStillDeciding",
        "linkDescription",
        "skuDocUrl",
    ],
    "commerce_sku_inherited": [
        "bundleLinks",
        "dynamicAttributes",
        "fulfiller",
        "fractionalQuantitiesAllowed",
        "itemAcl",
        "manufacturer_part_number",
        "quantity",
        "template",
        "unitOfMeasure",
        "fixedReplacementProducts",
        "isPurchaseable",
    ],
}


def cluster_for(field: str) -> str:
    for name, members in CLUSTER_MAP.items():
        if field in members:
            return name
    return "other"


CLUSTER_ORDER: list[str] = list(CLUSTER_MAP.keys()) + ["other"]


def notes_for_row(h: str, r: dict) -> list[str]:
    """Human-readable notes (shown in per-field detail blocks, not in the quick table)."""
    notes: list[str] = []
    if h == "ID":
        notes.append(
            "Repository item id (primary key); not a `<property>` on the descriptor."
        )
    if not r["in_custom_catalog"] and not r["xml_other"] and h != "ID":
        notes.append(
            "No `<property name=\"…\">` match in scanned LZB config XML — typically inherited ATG Commerce "
            "sku field (see Oracle ATG reference) or rename mismatch."
        )
    if r["code_hits"] == -2:
        notes.append("Code hit count skipped (`rg` not on PATH).")
    if r["code_hits"] == -3:
        notes.append("ripgrep timed out")
    return notes


def main() -> None:
    if not EXPORT_CSV.is_file():
        print("Missing export CSV:", EXPORT_CSV, file=sys.stderr)
        sys.exit(1)

    schema = parse_cover_sku_schema()
    feed_props = parse_feed_cover_properties()
    indexed = parse_indexed_for_cover_sku()

    with EXPORT_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    headers = rows[1]
    pct, dcount, topv = column_stats(EXPORT_CSV, headers)

    lines: list[str] = []
    lines.append("# BCC coverSku export — field inventory")
    lines.append("")
    lines.append(
        "Ground-truth analysis of **260501161753export.csv** (repository path line 1: "
        "`SecureProductCatalog:coverSku`). "
        "Each column is cross-checked against **item-descriptor `sku` + `coverSku`** in "
        "[customCatalog.xml](atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml), "
        "**coverFileSrcDestMap** in "
        "[LZBCatalogSourceDestinationMapping.properties](atg/la-z-boy/modules/LB/Commerce/config/com/lzb/feed/product/LZBCatalogSourceDestinationMapping.properties), "
        "childSKUs index rules in "
        "[product-sku-output-config.xml](atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml), "
        "and **ripgrep** reference counts across `atg/la-z-boy/modules` (excluding the two `customCatalog.xml` descriptor files)."
    )
    lines.append("")
    lines.append("## Summary buckets")
    assessments: list[str] = []
    rows_out: list[dict] = []

    for h in headers:
        in_custom = h in schema or h == "ID"
        xml_else = None if in_custom else find_property_xml_repo_wide(h)
        schema_known = in_custom or bool(xml_else)
        in_feed = h in feed_props
        in_index = h in indexed
        chits = rg_code_hits(h)
        if (
            h in schema
            and schema[h].get("column_name")
            and chits >= 0
            and chits < 3
        ):
            col = schema[h]["column_name"]
            if col and col != h:
                chits = max(chits, rg_code_hits(col))

        ass = classify(h, schema_known, in_feed, in_index, chits, pct.get(h, 0))

        assessments.append(ass)
        in_cat = (h in schema or h == "ID") or (
            xml_else and "customCatalog.xml" in xml_else
        )
        rows_out.append(
            {
                "field": h,
                "assessment": ass,
                "cluster": cluster_for(h),
                "in_custom_catalog": in_cat,
                "xml_other": xml_else or "",
                "type": schema.get(h, {}).get("data_type", ""),
                "column": schema.get(h, {}).get("column_name", ""),
                "feed": in_feed,
                "index": in_index,
                "code_hits": chits,
                "non_null_pct": round(pct.get(h, 0), 2),
                "distinct": dcount.get(h, 0),
                "top": topv.get(h, []),
            }
        )

    bucket_counts = Counter(assessments)
    lines.append(
        f"- **Rows in export:** {len(rows) - 2} cover SKU records; **Columns:** {len(headers)}"
    )
    lines.append(
        f"- **Properties parsed from item-descriptor `sku` + `coverSku` in LZB customCatalog.xml:** "
        f"{len(schema)} (remaining columns are usually ATG DCS stock-catalog fields merged via xml-combine)."
    )
    lines.append(
        "- **Code hits:** `-2` means `ripgrep` (`rg`) was not found on PATH — reinstall this document after "
        "`brew install ripgrep` (or equivalent) for Java/JSP reference counts."
    )
    for k in sorted(bucket_counts.keys()):
        lines.append(f"- **{k}:** {bucket_counts[k]}")
    lines.append("")
    lines.append("## Field clusters (skimmable)")
    lines.append("")
    for cname, members in CLUSTER_MAP.items():
        lines.append(f"### {cname}")
        lines.append(", ".join(f"`{m}`" for m in members))
        lines.append("")

    orphans = sorted(r["field"] for r in rows_out if r["assessment"] == "ORPHAN")
    lines.append("## ORPHAN columns (export-only relative to this repo)")
    lines.append("")
    lines.append(
        f"{len(orphans)} fields are **not** found under `<property name=\"…\">` in scanned LZB module XML, "
        "and are **not** listed in `coverFileSrcDestMap` or the childSKUs index rule set used above. "
        "They are usually **ATG Commerce stock `sku` properties** (merged via xml-combine but defined outside "
        "this repo’s customCatalog fragment) or **BCC export artifacts**. Treat as policy decisions, not typos, "
        "until verified against the full DCS schema."
    )
    lines.append("")
    lines.append(", ".join(f"`{x}`" for x in orphans) if orphans else "—")
    lines.append("")

    lines.append("## How to read this document")
    lines.append("")
    lines.append(
        "Wide Markdown tables mix **many dimensions** (schema, wiring, stats, prose) into one row, so viewers "
        "stretch columns or wrap **Notes** into very tall rows. This file uses two layers: a **quick reference** "
        "table (one short line per field) and **[Fields by cluster (full detail)](#fields-by-cluster-full-detail)** "
        "with everything else, including long notes and full top-value samples. For machine use, run "
        "`scripts/analyze-bcc-fields.py` and add a JSON export later if you need one."
    )
    lines.append("")

    lines.append("## Quick reference")
    lines.append("")
    lines.append(
        "One line per field. **Hits** = ripgrep count (`-1` = N/A for `ID`, `-2` = `rg` missing, `-3` = timeout). "
        "Long paths, types, DB columns, samples, and notes are under [full detail](#fields-by-cluster-full-detail)."
    )
    lines.append("")
    lines.append(
        "| Field | Assessment | Cluster | LZB XML | Feed | Idx | Hits | % | Distinct |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")

    for r in sorted(rows_out, key=lambda x: (x["cluster"], x["field"])):
        h = r["field"]
        lines.append(
            "| `{field}` | {ass} | {cl} | {lz} | {fd} | {ix} | {ch} | {pct} | {dst} |".format(
                field=h,
                ass=r["assessment"],
                cl=r["cluster"],
                lz="yes" if r["in_custom_catalog"] else "no",
                fd="yes" if r["feed"] else "no",
                ix="yes" if r["index"] else "no",
                ch=r["code_hits"],
                pct=r["non_null_pct"],
                dst=r["distinct"],
            )
        )

    lines.append("")
    lines.append("## Fields by cluster (full detail)")
    lines.append("")
    by_cluster: dict[str, list[dict]] = {c: [] for c in CLUSTER_ORDER}
    for r in rows_out:
        c = r["cluster"]
        if c not in by_cluster:
            by_cluster[c] = []
        by_cluster[c].append(r)
    for cname in CLUSTER_ORDER:
        members = sorted(by_cluster.get(cname, []), key=lambda x: x["field"])
        if not members:
            continue
        lines.append(f"### {cname}")
        lines.append("")
        for r in members:
            h = r["field"]
            lines.append(f"#### `{h}`")
            lines.append("")
            lines.append(f"- **Assessment:** {r['assessment']}")
            ox = r["xml_other"] or "—"
            typ = r["type"] or "—"
            col = r["column"] or "—"
            lines.append(
                f"- **Schema:** type `{typ}`, DB column `{col}`, in LZB catalog XML: "
                f"{'yes' if r['in_custom_catalog'] else 'no'}"
            )
            lines.append(f"- **Other XML (`name=\"…\"` match):** `{ox}`")
            lines.append(
                f"- **Feed map:** {'yes' if r['feed'] else 'no'} · **Indexed (childSKUs rule set):** "
                f"{'yes' if r['index'] else 'no'}"
            )
            lines.append(f"- **Code hits:** {r['code_hits']}")
            lines.append(
                f"- **Export sample:** {r['non_null_pct']}% non-empty, **{r['distinct']}** distinct values"
            )
            top_full = "; ".join(r["top"]) if r["top"] else "—"
            lines.append(f"- **Top values (up to 5):** {top_full}")
            note_lines = notes_for_row(h, r)
            if note_lines:
                lines.append("- **Notes:**")
                for nl in note_lines:
                    lines.append(f"  - {nl}")
            else:
                lines.append("- **Notes:** —")
            lines.append("")
        lines.append("")

    lines.append("## Assessment rule (deterministic)")
    lines.append("")
    lines.append(
        "- **ORPHAN:** Not in `coverFileSrcDestMap`, not in the childSKUs index set, and no `name=\"…\"` match for "
        "the field in scanned LZB config XML (Commerce / Endeca / Merchandising / Base). Not `ID`. Typically ATG "
        "core sku properties absent from the repo fragment."
    )
    lines.append(
        "- **DORMANT:** In schema, **0%** non-empty in export, **0** code hits (after descriptor exclude), not in feed map, not in index config."
    )
    lines.append(
        "- **LEGACY:** **>0%** populated but no feed, no index, and **≤0** code hits — data exists in BCC but nothing in this repo reads it."
    )
    lines.append(
        "- **ACTIVE:** In feed map, or in index config, or **≥3** code hits, or field is `ID`."
    )
    lines.append(
        "- **UNCLEAR:** Mixed / low signal (e.g. 1–2 code hits only). Triaged manually if needed."
    )
    lines.append("")

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")
    print("Bucket counts:", dict(bucket_counts))


if __name__ == "__main__":
    main()
