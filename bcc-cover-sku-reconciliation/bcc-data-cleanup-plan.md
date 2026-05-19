# Cover SKU data cleanup plan

Working plan for **BCC catalog** changes on **`coverSku`** items. Steps are added as we finish analysis against the BCC export and related traces ([bcc-field-inventory.md](bcc-field-inventory.md), [bcc-field-display-trace.md](bcc-field-display-trace.md)). For **aligning BCC with the workbook-derived CSV** (existence, field parity, validation gates), use [bcc-bcc-completeness-plan.md](bcc-bcc-completeness-plan.md).

**Environment:** Run each change in the usual order (e.g. validate in **UAT** BCC before production). Record who ran the change and the approximate row count affected.

---

## Steps

### 1. Clear `sortOrder` on cover SKUs

**Action:** In BCC, for **`coverSku`** items, set **`sortOrder`** to empty / cleared for every row where it is currently populated (or use the bulk workflow your team uses for scalar property clears).

**Why:** The free swatches page queries with `ORDER BY id` and also passes `sortProperties="+sortOrder"` to `RQLQueryForEach`. With **`sortOrder` empty on all rows**, rendered swatch order on UAT has been observed to follow **cover id** (string) order. Keeping stale numeric `sortOrder` values overrides that and is easy to drift from source-of-truth ordering.

**Caveats:**

- `sortOrder` was added for the **free swatches** flow only (not a separate discovery pass needed before prod bulk clear). The property still exists on the item descriptor and is listed in the Endeca `coverSku` output config ([product-sku-output-config.xml](../../../atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml)); clearing values does not remove the attribute from the schema or index definition.
- If you only clear **some** rows, items with remaining numbers still sort ahead of/behind nulls per platform sort rules; **uniform clear** (or a JSP change to sort by `id` only) is what aligns behavior with id ordering.

---

## Future steps (placeholder)

_Additional cleanup steps will be listed here after further BCC export analysis._
