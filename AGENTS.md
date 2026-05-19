# Agent Context

Personal collection of small browser-based tools, published via GitHub Pages
at https://4toddt.github.io/tools/. Each tool is its own folder with a
self-contained `index.html`.

## Conventions
- Vanilla HTML/CSS/JS, system fonts, La-Z-Boy palette
  (navy `#003349`, rust `#BD472A`, cream `#F5F3EE`)
- No build step, no package manager
- External CDN deps avoided when possible; when used, pin with SRI hash
- Root `index.html` lists all tools

## Tools

### fiscal/
La-Z-Boy 5-4-4 (NRF retail) fiscal calendar viewer.

### cover-data/
XLSX → JSON extractor for the Cover Information List spreadsheet.
Vanilla JS + SheetJS Community 0.18.5 (jsdelivr CDN, SRI-pinned).

**Output `cover-families.json`** (schema v1.0.0) with a top-level `legends`
object decoding cryptic codes (wearability N/M/P, specialty I/C/PF/etc.,
product line MU/CH/SLR/etc., cleaning S/W/WS/L). Per-color drop status from
red+strikethrough text runs; per-family drop status from row fill colors
("Immediate Drop" / "Phase Out" / "New Phase Out" / "Market Drop"). Duplicate
leather rows merged by Series Number with per-color intro dates. Combo series
numbers (Grandview FL2026/LB2026) split into sibling records.

**Plus `extraction-report.json`** — counts, merges, unknown codes flagged
for follow-up with Merchandising.

**Test fixtures** in `cover-data/`:
- `April 2026 Cover Information List FINAL (v.5.01.2026).xlsx` — verified
- `April 2026 Cover Information List FINAL (v.5.15.2026).xlsx` — newer, untested

**Testing approach** (no committed harness): Node 22 + `xlsx` + `jsdom` to
provide DOMParser; pull the inline script from `index.html`, eval, call
`extractAll` against the workbook. Spot-check: Brink (Lentil dropped),
Samba (Clay/Marigold/Crimson dropped), Dean LB2063 (5 colors, 2 intro dates),
Grandview (split into FL2026+LB2026 siblings), Lota (familyStatus "Phase Out").
Expected counts on the v.5.01 workbook: 187 fabric, 38 leather, 6 dropped
colors, 4 merges, 2 unknown codes (W*S typo at rows 178 and 197).

## Open work — Phase 2: Oracle BCC export

Add a third export to `cover-data/` that produces a file importable into
Oracle BCC.

**Prerequisite**: the session must have `4toddt/lzb-docs` in scope (added via
the repo selector at claude.ai/code when starting). BCC format spec lives there.

**Investigation plan** (once unblocked):
1. Discover the BCC import format. Search lzb-docs for "BCC", "import",
   "cover", "fabric", "leather", "swatch", and likely extensions
   (`.csv`, `.xml`). Read any sample import files and existing converter scripts.
2. Map BCC fields ↔ extractor JSON. Note gaps (SKU IDs, prices, status codes
   BCC needs but the workbook doesn't provide).
3. Look for existing BCC-import tooling in lzb-docs — preserve compatibility.
4. Report back: format summary + field-mapping table + open questions.

**Open product questions** (deferred until investigation completes):
- Import scope: full data, or filtered (active only / drops only / delta)?
- UI flow: third download button alongside JSON + report, or its own step?
- Cadence: one-shot per market, or recurring sync?
