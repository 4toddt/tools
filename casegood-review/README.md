# Hammary casegood review

Static browser tool for reviewing Hammary casegood BCC import records.

- **Live:** https://4toddt.github.io/tools/casegood-review/ (after push)
- **Local:** open `index.html` (loads `data.js`) or serve the folder

## What’s on each product card

1. **Images** — primary CDN shot + clickable alt thumbs  
2. **Import fields** — product + casegoodSku values destined for BCC  
3. **Copy** — romance / long description / at a glance / care / resources  
   - Unchanged fields: import HTML only  
   - When import ≠ live BCC: side-by-side + simple word diff (`del`/`ins`)  
   - **Policy:** updates keep existing BCC wording (formatting-only lane); Wendy rewrite is for creates  

**Images:** `_alt1` omitted — byte-identical to primary on CDN (verified).

## Filters

| Control | Options / purpose |
|---------|-------------------|
| Search | SKU, name, series, category, features, delta field names |
| View | **All fields** · **Copy** (new/changed merch only) · **Features** (image + feature context; live feature Δ or creates with tags) |
| Product set | **All** · **New (create)** · **Live — has changes** · **Live — no changes** · **All live** |
| showOnline | all / true / false |
| **New copy** | Hides field table; products with create copy or live copy added/changed |
| Page size | 12–100 or All |

**Live — has changes** = in BCC export with at least one field delta (green).  
**Live — no changes** = in BCC, compared fields match (should not look like an “update”).

Green rows / chips: field value differs from existing BCC (`was: …`).

Deep links: `?sku=C11.0086.00BE`, `?kind=update&online=true`, `?newCopy=1`

## Regenerate data

From the lzb-workspace monorepo (paths relative to workspace root):

```bash
python3 docs/projects/casegood-loading/scripts/export_casegood_review.py
```

If that script is missing, re-run the export block used to build `data.json`
from:

- `docs/projects/casegood-loading/data/round2/records-all.json`
- `docs/projects/casegood-loading/data/round2/agent-facts.json`

Output:

- `tools/casegood-review/data.json`
- `tools/casegood-review/data.js`  (`window.CASEGOOD_REVIEW_DATA = …`)

`data.js` is preferred so `file://` open works without a server.

## Conventions

Matches sibling tools: vanilla HTML/CSS/JS, La-Z-Boy palette, no build step.
