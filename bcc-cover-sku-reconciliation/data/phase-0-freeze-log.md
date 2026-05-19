# Phase 0 freeze log — cover SKU reconciliation

**Run date:** 2026-05-04 (local). **Executor:** automated + repo paths below.

This log satisfies [Phase 0 — Freeze and validate sources](../bcc-bcc-completeness-plan.md#phase-0--freeze-and-validate-sources) in `bcc-bcc-completeness-plan.md`.

---

## Step 0.1 — Workbook version

| Field | Value |
|--------|--------|
| **Path** | `data/Copy of April 2026 Cover Information List FINAL (v.4.10.2026).xlsx` |
| **Size** | 549,700 bytes |
| **mtime** | 2026-05-01 15:40:41 (local) |
| **SHA-256** | `38039bf1220171797a562dc120e58d979baa052ec28ef336cf6884a4e49bf7a3` |

**Note:** The workbook was moved from the project root into `data/` so it matches `WORKBOOK` in `scripts/build-by-sku-csv.py`.

---

## Step 0.2 — Regenerate reference CSV

| Field | Value |
|--------|--------|
| **Command** | `cd docs/projects/bcc-cover-sku-reconciliation && .xlsx-venv/bin/python scripts/build-by-sku-csv.py` |
| **Exit code** | 0 |
| **Output file** | `data/cover-skus-by-color.csv` |
| **Rows written** | 829 |
| **Dropped (workbook)** | 6 (see script stdout for SKU list) |
| **`issues` breakdown** | `duplicate-series`: 20 rows; `hyphen-separator`: 2 rows |
| **Rows with any non-empty `issues`** | 22 |

### Reference CSV integrity checks

| Check | Result |
|--------|--------|
| **Row-level `skuId`** | 829 data rows; **828** distinct `skuId` values. **`LB164879`** appears on **two** rows (`MASTER LEATHER` rows 47 and 48): same series + color code (**79 Chocolate**), different `marriedStyles` / `notes`. That matches the **workbook** (two merchandising rows for one catalog cover id)—not a corrupt file. |
| **`issues` column** | Populated only by the extractor for triage: e.g. `duplicate-series` means “this **series** code appears on more than one workbook row” (see `scripts/build-by-sku-csv.py`); `hyphen-separator` means a color line used `-` instead of `=`. **Not** “missing data” or “bad xlsx.” |
| **Set operations vs BCC** | For **existence / coverage** (Phase 1), use **unique** `skuId` as the join key to BCC `id` (one workbook-derived id → one BCC item). For **row-level** attribute diffs when multiple rows share an id, disambiguate with `sourceSheet` + `sourceRow` or a merch rule—see `data/phase1-reference-multi-row-skus.csv` after Phase 1. |
| **`dropStatus`** | 823 empty (active in workbook sense), **6** `dropped` |
| **Spot-check** | `B153808` matches script stdout (fabric / Seamount / Burgundy, etc.) |

---

## Step 0.3 — Freeze BCC export

| Field | Value |
|--------|--------|
| **Artifact** | `data/260501161753export.csv` |
| **SHA-256** | `fe5dbf8c3e449b07e6f7aa185af5351720f5ec288120616bcf40ca6ca0d876ad` |
| **Data rows** | 4,159 |
| **`ID` non-empty** | 4,159 |
| **`ID` unique** | **Pass** — 4,159 unique (no duplicate repository ids) |
| **Join key shape** | Reference `skuId` samples (`B153808`, …) match BCC `ID` style (same casing; no case-only mismatches detected in a set overlap sanity check). |

**Optional inventory refresh:** Ran `python3 docs/projects/bcc-cover-sku-reconciliation/scripts/analyze-bcc-fields.py` from repo root → regenerated [bcc-field-inventory.md](../bcc-field-inventory.md) (bucket counts unchanged for this export: ACTIVE 39, LEGACY 10, DORMANT 37, ORPHAN 14).

---

## Before row-level attribute merges (not blocking Phase 1)

- **Multi-row `skuId`:** When the same `skuId` appears on more than one reference row, do **not** assume the CSV is a strict 1:1 row map to BCC without `sourceRow` (or a merch merge rule). **Phase 1 coverage** uses **unique ids** only.
- **`issues` flags:** Use them for triage; they do not block Phase 1 existence math.

When you replace the BCC export with a newer pull, add a new section to this file (or a new `phase-0-freeze-log--YYYY-MM-DD.md`) and update `EXPORT_CSV` in `scripts/analyze-bcc-fields.py` if the filename changes.

---

## Phase 1 (same frozen inputs)

Re-run coverage after any workbook or export refresh:

`python3 docs/projects/bcc-cover-sku-reconciliation/scripts/phase1_cover_sku_coverage.py`

Latest output: [phase-1-coverage-summary.md](phase-1-coverage-summary.md) (2026-05-04 run).
