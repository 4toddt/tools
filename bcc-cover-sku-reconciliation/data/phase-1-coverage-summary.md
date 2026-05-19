# Phase 1 — cover SKU coverage (existence only)

**Generated (UTC):** `2026-05-04T21:14:07Z`

**Inputs:**
- Reference: `bcc-cover-sku-reconciliation/data/cover-skus-by-color.csv`
- BCC export: `bcc-cover-sku-reconciliation/data/260501161753export.csv`

## Definitions (high confidence)

- **Set A:** unique `skuId` from the reference CSV where `dropStatus` ≠ `dropped` (empty `dropStatus` = active in workbook). One id appears once in **A** even if the CSV has multiple rows for that id (see multi-row report).
- **Set B:** unique `ID` from the BCC `coverSku` export.
- **Set C (audit):** `skuId` rows marked `dropped` in the reference (not used in A/B math).

## Counts

| Metric | Value |
|--------|-------:|
| Reference rows, non-dropped | 823 |
| Reference rows, dropped | 6 |
| **\|A\|** (unique active `skuId`) | 822 |
| **\|B\|** (unique BCC `ID`) | 4159 |
| **\|A ∩ B\|** | 804 |
| **\|A − B\|** (in reference, not in BCC) | 18 |
| **\|B − A\|** (in BCC, not in reference active set) | 3355 |
| Active `skuId` with **>1** reference row | 1 |

## Output files (triage)

- **`phase1-only-in-reference.csv`** — one row per id in **A − B** (plus context columns).
- **`phase1-only-in-bcc.csv`** — one row per id in **B − A** (`id` only).
- **`phase1-reference-multi-row-skus.csv`** — ids in **A** with multiple non-dropped reference rows (workbook split / married-style rows; not a data quality failure).

## Phase 1.2 (human)

Review the two gap CSVs with merchandising / catalog owners: **create** backlog for **A − B**; **keep / retire / investigate** for **B − A**. No repository writes in Phase 1.
