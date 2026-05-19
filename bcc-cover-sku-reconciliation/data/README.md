# Data inputs and outputs

Place **local** artifacts here so the project root stays readable:

| File | Role |
|------|------|
| `260501161753export.csv` | Example BCC `coverSku` export used by `scripts/analyze-bcc-fields.py` (replace with your dated export; keep the filename or update `EXPORT_CSV` in that script). |
| `Copy of April 2026 Cover Information List FINAL (v.4.10.2026).xlsx` | Source workbook for `scripts/build-by-sku-csv.py` (path is fixed in the script—rename the script constant if your filename differs). |
| `cover-skus-by-color.csv` | **Output** of `build-by-sku-csv.py`: one row per cover SKU. |
| `phase-0-freeze-log.md` | **Phase 0** run record (workbook hash, CSV + BCC export validation). |
| `phase-1-coverage-summary.md` | **Phase 1** set counts; regenerate with `scripts/phase1_cover_sku_coverage.py`. |
| `phase1-only-in-reference.csv` | Workbook-active SKUs **not** in frozen BCC export (**A − B**). |
| `phase1-only-in-bcc.csv` | BCC ids **not** in workbook active set (**B − A**). |
| `phase1-reference-multi-row-skus.csv` | Active `skuId` with **>1** reference row (same id, multiple source rows). |
| `trace-active-field-hits.json` | **Output** of `scripts/trace-active-field-hits.py` for the display-trace doc. |

Nothing in this folder is required for a fresh clone except what you generate or drop in for analysis.
