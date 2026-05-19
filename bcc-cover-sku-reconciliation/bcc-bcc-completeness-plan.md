# BCC cover SKU completeness plan

**Goal:** Move **Oracle Commerce BCC** `coverSku` data toward parity with the **April 2026 cover workbook**, using **[data/cover-skus-by-color.csv](data/cover-skus-by-color.csv)** as the machine-readable **source of truth** derived from that workbook ([scripts/build-by-sku-csv.py](scripts/build-by-sku-csv.py)).

**Definition of “relevant”:** Fields classified **ACTIVE** in [bcc-field-inventory.md](bcc-field-inventory.md) with storefront/search behavior described in [bcc-field-display-trace.md](bcc-field-display-trace.md). Not every ACTIVE column appears in the CSV; some values are set only in BCC, by feed pipelines, or by pricing/index jobs—treat gaps as **out of workbook scope** until you explicitly extend the extract.

**Principles:** Small batches, **read-only comparisons before writes**, **UAT before prod**, and a **validation gate** after every step. Prefer **feed rows** where the mapping allows; use **direct BCC** (or one-time clear + feed) where [bcc-cover-sku-feed.md](bcc-cover-sku-feed.md) says properties are **restricted** or not feed-mapped.

**Related:** Data-only cleanup (e.g. `sortOrder`) lives in [bcc-data-cleanup-plan.md](bcc-data-cleanup-plan.md).

---

## Workbook ↔ CSV ↔ BCC mapping (starter)

Use this as a checklist; extend it as BCC export analysis adds columns.

| Reference CSV column | Typical BCC / feed touchpoint | Notes |
|----------------------|-------------------------------|--------|
| `skuId` | `id` (repository id) | Join key; must match exactly after trim/normalize. |
| `coverType` | `coverType` | Align enumerated values with BCC (e.g. `fabric` / `leather`). |
| `patternName` | `patternName` | Feed often avoids overwriting; may be **BCC-only** updates—confirm mapping comments in `LZBCatalogSourceDestinationMapping.properties`. |
| `colorName` / `colorCode` | `colorDescription`, `colorNumber`, `coverColor` | `coverColor` / `description` are **restricted** for feed overwrites when already set—see feed doc. |
| `description` | `description` | Restricted; may need BCC edit or controlled clear + re-import. |
| `cleaningCode` | `cleaningCode` | Feed-mappable (`cleaningcode` key). |
| `capCode` | `capCode` | Feed-mappable. |
| `faceContents` | `faceContents` | Feed-mappable. |
| `wearabilityCode` / `wearabilityDescription` | `wearability` | Feed key `wearability`; align encoding with feed expectations. |
| `dropStatus` / `issues` | (triage, not direct BCC fields) | Use for **eligibility** and data quality; do not blindly import `issues` text into BCC. |

Columns in the CSV with **no** direct BCC column in this table stay **workbook-only context** until you define a mapping.

---

## Phase 0 — Freeze and validate sources

**Step 0.1 — Workbook version**  
Record the exact workbook filename and **version/date** (e.g. `Copy of April 2026 Cover Information List FINAL (v.4.10.2026).xlsx`). Store the file where [scripts/build-by-sku-csv.py](scripts/build-by-sku-csv.py) expects it (see `WORKBOOK` in that script—typically under `data/`).

**Validation:** File opens; you can note the SHA-256 or last-modified time in your run log.

**Step 0.2 — Regenerate reference CSV**  
From the project folder:

```bash
cd docs/projects/bcc-cover-sku-reconciliation
.xlsx-venv/bin/python scripts/build-by-sku-csv.py
```

**Validation:** Script exits 0; note printed row count, `dropStatus` breakdown, and **`issues`** counts. If `issues` is non-trivial, **triage or fix the workbook** before using the CSV as authority for bulk BCC work.

**Step 0.3 — Freeze BCC export**  
Export `coverSku` from BCC to CSV (same process as for [scripts/analyze-bcc-fields.py](scripts/analyze-bcc-fields.py)); keep a **dated copy** under `data/`. Optionally re-run `analyze-bcc-fields.py` so [bcc-field-inventory.md](bcc-field-inventory.md) matches that export.

**Validation:** Export row count documented; `id` column unique; join key format matches `skuId` in reference (same casing rules).

**Execution log (2026-05-04):** [data/phase-0-freeze-log.md](data/phase-0-freeze-log.md) — workbook under `data/`, reference CSV regenerated, BCC export hashed and uniqueness-checked. Multi-row `skuId` and `issues` semantics are documented there (workbook-intentional splits, not export corruption).

**Phase 1 output:** [data/phase-1-coverage-summary.md](data/phase-1-coverage-summary.md) (regenerate with `scripts/phase1_cover_sku_coverage.py`).

---

## Phase 1 — Coverage (existence only, no edits)

**Step 1.1 — Build three ID sets**  
From frozen files: **(A)** all `skuId` in reference CSV where `dropStatus` is not `dropped` (or whatever rule you agree means “should exist in catalog”), **(B)** all cover ids in BCC export, **(C)** optional: dropped-only set for audit.

**Validation:**  
`|A|`, `|B|`, `|A∩B|`, `|A−B|`, `|B−A|` printed or in a small spreadsheet. No property comparisons yet.

**Execution (automated):** From repo root run  
`python3 docs/projects/bcc-cover-sku-reconciliation/scripts/phase1_cover_sku_coverage.py`  
→ writes [data/phase-1-coverage-summary.md](data/phase-1-coverage-summary.md), `data/phase1-only-in-reference.csv`, `data/phase1-only-in-bcc.csv`, and `data/phase1-reference-multi-row-skus.csv`. Re-run whenever the reference CSV or BCC export changes.

**Step 1.2 — Triage gaps**  
- **`A − B`:** Covers the business expects **live** but missing in BCC → backlog for **create** (feed/BCC) with owner.  
- **`B − A`:** In BCC but not in reference → backlog for **keep / retire / investigate** (do not delete in this phase).

**Validation:** Each gap list reviewed by merchandising/catalog owner; **no mass repository changes** until lists are signed off.

---

## Phase 2 — Relevance scope (what the workbook can fix)

**Step 2.1 — Lock the reconciliation field list**  
From [bcc-field-display-trace.md](bcc-field-display-trace.md), copy the **ACTIVE** `coverSku` / `sku` fields you intend to compare. Mark each as: **(i)** mappable from CSV, **(ii)** feed-only / BCC-only, **(iii)** out of scope (pricing, dates, images, etc.).

**Validation:** Short written list (even a table in a ticket) agreed by you + whoever owns catalog data.

**Step 2.2 — Restricted-field flag**  
For **`coverColor`**, **`colorFamliy`**, **`description`** (and any future restricted keys), mark them as **“compare only”** until you choose **manual BCC** vs **clear + feed** per [bcc-cover-sku-feed.md](bcc-cover-sku-feed.md).

**Validation:** No feed file has been applied to prod for those keys without that decision recorded.

---

## Phase 3 — Read-only field parity (diffs only)

**Step 3.1 — One property pilot**  
Pick **one** low-risk, feed-friendly field (e.g. `cleaningCode` or `capCode`) where reference and BCC export both have values. Produce a **diff report**: `skuId`, reference value, BCC value, match/mismatch.

**Validation:** Spot-check **10** mismatches in BCC UI + workbook source row (`sourceSheet` / `sourceRow` in CSV); confirm the reference is truly correct.

**Step 3.2 — Expand in small batches**  
Repeat 3.1 for additional properties in **groups of 1–3** at a time (never a large multi-column blind merge).

**Validation:** After each group, re-export BCC subset or full and confirm **only intended** columns moved for a **golden set** of 5–10 SKUs you track across runs.

---

## Phase 4 — Apply changes (conservative write paths)

**Step 4.1 — UAT feed slice**  
For fields allowed by **`LZB_Catalog_covers.txt`** / `coverFileSrcDestMap`, build a **small** pipe file (or official slice) with **only** header + rows for a **test set** of SKUs (e.g. 10–25). Import on **UAT** using the normal catalog feed process.

**Validation:** BCC item query + one **storefront or CDP** spot check per ACTIVE field changed; no regressions on sibling `prod{coverId}` if your process creates/updates those.

**Step 4.2 — Restricted or BCC-only fields**  
Apply updates **only** via BCC UI or approved bulk tool, in **small batches**, with the restricted-field strategy from Phase 2.2.

**Validation:** Re-export those rows; confirm values match reference **or** documented intentional override.

**Step 4.3 — Scale up**  
Increase batch size only after **two** successful UAT cycles with clean validation.

---

## Phase 5 — Post-change platform checks

**Step 5.1 — Index / search smoke**  
After BCC changes that affect indexed ACTIVE fields, run your standard **partial or full index** on UAT (per team practice). Spot-check **cover search**, **fabric selector**, and **free swatches** if `archCoverAvlb` / `archwayId` / visibility fields moved.

**Validation:** Checklist of URLs or SKUs passes; no new `unsearchable` / `showOnline` surprises on the golden set.

**Step 5.2 — Prod promotion**  
Repeat 4.x on prod only after UAT sign-off; keep **before** and **after** exports for the same date window.

**Validation:** Same golden-set spot checks in prod.

---

## Phase 6 — Ongoing drift control

**Step 6.1 — Workbook bump protocol**  
When the workbook gets a new version: rerun Phase **0.2**, archive the old CSV, rerun **`scripts/phase1_cover_sku_coverage.py`** at minimum.

**Validation:** Delta of `skuId` sets and `issues` column summarized in one paragraph for the release note.

---

## What this plan does *not* do

- It does **not** replace **pricing**, **inventory**, or **image** workflows—the reference CSV does not carry those; they stay governed by commerce ops and other feeds.  
- It does **not** mandate **deleting** BCC-only SKUs; orphan handling stays a **business** decision after Phase 1.2.

---

_Add new phases or split steps as BCC export analysis surfaces additional columns or risk areas._
