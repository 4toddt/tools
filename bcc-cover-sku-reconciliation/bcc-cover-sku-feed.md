# Cover SKU: BCC repository vs catalog feed

Reference for reconciling **coverSku** items in Oracle Commerce BCC with external product/cover data and with the **`LZB_Catalog_covers.txt`** bulk feed.

Sources in this repo:

- Item descriptor `coverSku`: `atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml` (search for `name="coverSku"`).
- Feed column → property mapping: `atg/la-z-boy/modules/LB/Commerce/config/com/lzb/feed/product/LZBCatalogSourceDestinationMapping.properties` (`coverFileSrcDestMap`, `restrictedCoverPropertiesToUpdate`).
- Import pipeline: `LZBCatalogFeedProcessor` switches on `LZB_Catalog_covers.txt` → `LZBProductFileFeedService.importCoverSkuItemFromTokens`.

---

## 1. Cover SKU identity

- **Repository id** for the SKU is the cover identifier (used as first `|` field in the feed line after the header).
- **Sibling product** for cover merchandising is typically `prod` + cover id (see `importCoverSkuItemFromTokens` creating product id `prod{lCoverId}`).

---

## 2. Notable `coverSku` properties (auxiliary table `lzb_cover_sku`)

These are the main merchandising and display fields (not exhaustive—see XML for full list):

| Property (repository) | Notes |
|----------------------|--------|
| `id` | SKU id |
| `coverType` | Enumerated: `leather` / `fabric` |
| `collectionName` | |
| `grade` | |
| `patternName` | Feed mapping intentionally avoids overwriting from fabric feed—“updated in BCC” per comments in mapping file |
| `colorDescription` | |
| `capCode` | |
| `wearDatedId` | |
| `cleaningCode` | |
| `wearability` | |
| `productCategoryCode` | |
| `coverStatus` | Separate from SKU **`status`** (see note below). Merchandising code often references `LZBCatalogConstants.COVER_SKU_STATUS` → **`coverStatus`**. |
| `series` | |
| `coverColor` | |
| `faceContents` | |
| `prodCategoryDesc` | |
| `commodityCode` | |
| `performanceFabricFlag` | Boolean |
| `colorNumber` | |
| `hideForCA` | Boolean |
| `archCoverAvlb` | Boolean |
| `additionalDetails` | Big string |
| `isNew`, `mostPopular` | Booleans |
| `archwayID`, `sortOrder` | |
| `addedMaterialTypes` | Multi-valued set |
| `displayName` | Derived/custom property (`CoverDisplayName`); feed sets from **`colordescription`** column when present |

---

## 3. `LZB_Catalog_covers.txt` format

- Encoding: **ISO-8859-1** when read by `LZBCatalogFeedProcessor`.
- **First line**: header keys (pipe `|` separated).
- **Following lines**: values aligned to keys; **first value is cover id**.
- Parser: `importCoverSkuItemFromTokens` splits keys and values with `split("\\|", -1)`.

### Header keys → repository properties (`coverFileSrcDestMap`)

Lowercase keys on the left map to repository properties on the right:

| File column key | Property |
|-----------------|----------|
| `cover_type` | `coverType` |
| `collectionname` | `collectionName` |
| `covergrade` | `grade` |
| `colordescription` | `colorDescription` (also drives `displayName` when key is `colordescription`) |
| `capcode` | `capCode` |
| `cleaningcode` | `cleaningCode` |
| `productcategorycode` | `productCategoryCode` |
| `coverseries` | `series` |
| `facecontents` | `faceContents` |
| `coverdesc` | `description` |
| `performfabricflag` | `performanceFabricFlag` (`1` = true) |
| `colorNumber` | `colorNumber` |
| `wearability` | `wearability` |
| `status` | **`status`** (inherited SKU property on `sku` super-type—not the same XML block as `coverStatus` on `coverSku`). Overwrite guard in code: existing non-null **`status`** may be preserved—see `setCoverSkuPropertiesFromTokens`. **Confirm in BCC which column you edit** (`status` vs Cover Status / `coverStatus`) before mass updates. |
| `covercolor` | `coverColor` |

### Restricted properties

`restrictedCoverPropertiesToUpdate` = **`coverColor`**, **`colorFamliy`**, **`description`**: if the repository already has a non-blank value, the feed **does not** overwrite it (except as implemented in code—verify against current branch before relying on mass fix).

---

## 4. Status values (feed / merchandising)

From `LZBProductFeedService`: merchandising uses pending/active/discontinued style constants for cover SKU status; BCC enumerated options on `coverStatus` in XML include **A**, **P**, **O**. Align any import with what production BCC allows for that field.

**`status` vs `coverStatus`:** The pipe feed maps header `status` → repository property **`status`** (see `LZBCatalogSourceDestinationMapping.properties`). The `coverSku` descriptor also defines **`coverStatus`** (same DB column name in XML as `status` in one place—verify on your schema). When reconciling exports, check both columns if present; do not assume one feed column updates both.

---

## 5. Practical reconciliation

1. Normalize **join keys** (trim, consistent casing for fabric vs leather ids).
2. Compare attributes that are allowed to change via feed vs those **restricted**—restricted fields may need **direct BCC edit** or a one-time clear per business rules.
3. Emit either:
   - **Pipe file rows** matching `coverFileSrcDestMap` keys on the header line, or  
   - A **CSV of BCC field updates** if feed cannot touch restricted columns.

---

## 6. Code references

```1252:1323:atg/la-z-boy/modules/LB/Commerce/src/com/lzb/commerce/catalog/LZBCatalogTools.java
	public boolean setCoverSkuPropertiesFromTokens(String[] pKeys, String[] pValues, MutableRepositoryItem pCoverSkuItem) throws RepositoryException {
		// ... maps keys through getCoverFileSrcDestMap(), restrictedCoverPropertiesToUpdate,
		// performanceFabricFlag handling, colordescription → displayName, status overwrite guard ...
```

```68:99:atg/la-z-boy/modules/LB/Merchandising/src/com/lzb/feed/product/LZBProductFileFeedService.java
	public void importCoverSkuItemFromTokens(String pKeys, String pValues) throws RepositoryException  {
		// First token is cover ID; create/update coverSku; optional prod + cat_cover association ...
```
