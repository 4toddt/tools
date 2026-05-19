# BCC coverSku export — field inventory

Ground-truth analysis of **260501161753export.csv** (repository path line 1: `SecureProductCatalog:coverSku`). Each column is cross-checked against **item-descriptor `sku` + `coverSku`** in [customCatalog.xml](atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml), **coverFileSrcDestMap** in [LZBCatalogSourceDestinationMapping.properties](atg/la-z-boy/modules/LB/Commerce/config/com/lzb/feed/product/LZBCatalogSourceDestinationMapping.properties), childSKUs index rules in [product-sku-output-config.xml](atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml), and **ripgrep** reference counts across `atg/la-z-boy/modules` (excluding the two `customCatalog.xml` descriptor files).

## Summary buckets
- **Rows in export:** 4159 cover SKU records; **Columns:** 100
- **Properties parsed from item-descriptor `sku` + `coverSku` in LZB customCatalog.xml:** 80 (remaining columns are usually ATG DCS stock-catalog fields merged via xml-combine).
- **Code hits:** `-2` means `ripgrep` (`rg`) was not found on PATH — reinstall this document after `brew install ripgrep` (or equivalent) for Java/JSP reference counts.
- **ACTIVE:** 39
- **DORMANT:** 37
- **LEGACY:** 10
- **ORPHAN:** 14

## Field clusters (skimmable)

### identity
`ID`

### pricing
`listPrice`, `salePrice`, `wholesalePrice`, `nonreturnable`, `discountable`, `onSale`

### dates_status
`startDate`, `endDate`, `status`, `creationDate`, `coverStatus`

### online_visibility
`showOnline`, `unsearchable`, `hideForTextSearch`, `hideForCA`, `onlineExclusive`, `onlineExclusiveText`, `onlineOnly`

### images_media
`largeImage`, `smallImage`, `thumbnailImage`, `pdpDefaultImage`, `cdpDefaultImage`, `cdpMouseOverImage`, `dimensionImage`, `altImages`, `colorFamilyImages`, `auxiliaryMedia`, `videos`, `belowFoldVideoMedia`, `belowFoldHowToMedia`, `wtbFeatureImg1`, `wtbFeatureImg1Alt`, `wtbFeatureImg1Caption`, `wtbFeatureImg2`, `wtbFeatureImg2Alt`, `wtbFeatureImg2Caption`, `wtbLeftImg`

### cover_core
`coverType`, `patternName`, `collectionName`, `colorDescription`, `coverColor`, `colorNumber`, `capCode`, `cleaningCode`, `wearability`, `wearDatedId`, `faceContents`, `grade`, `series`, `productCategoryCode`, `prodCategoryDesc`, `commodityCode`, `performanceFabricFlag`, `addedMaterialTypes`, `additionalDetails`, `description`

### pdp_below_fold
`atAGlanceContent`, `hideAGlance`, `perfectForInfo`, `romanceCopy`, `careFeatures`, `useCareInstructions`, `warrantyInfo`, `stillDecidingLinks`, `displayHeader`, `headerText`, `hideStillDeciding`, `linkDescription`, `skuDocUrl`

### commerce_sku_inherited
`bundleLinks`, `dynamicAttributes`, `fulfiller`, `fractionalQuantitiesAllowed`, `itemAcl`, `manufacturer_part_number`, `quantity`, `template`, `unitOfMeasure`, `fixedReplacementProducts`, `isPurchaseable`

## ORPHAN columns (export-only relative to this repo)

14 fields are **not** found under `<property name="…">` in scanned LZB module XML, and are **not** listed in `coverFileSrcDestMap` or the childSKUs index rule set used above. They are usually **ATG Commerce stock `sku` properties** (merged via xml-combine but defined outside this repo’s customCatalog fragment) or **BCC export artifacts**. Treat as policy decisions, not typos, until verified against the full DCS schema.

`auxiliaryMedia`, `bundleLinks`, `discountable`, `dynamicAttributes`, `fixedReplacementProducts`, `fractionalQuantitiesAllowed`, `fulfiller`, `itemAcl`, `largeImage`, `onlineOnly`, `smallImage`, `template`, `thumbnailImage`, `unitOfMeasure`

## How to read this document

Wide Markdown tables mix **many dimensions** (schema, wiring, stats, prose) into one row, so viewers stretch columns or wrap **Notes** into very tall rows. This file uses two layers: a **quick reference** table (one short line per field) and **[Fields by cluster (full detail)](#fields-by-cluster-full-detail)** with everything else, including long notes and full top-value samples. For machine use, run `scripts/analyze-bcc-fields.py` and add a JSON export later if you need one.

## Quick reference

One line per field. **Hits** = ripgrep count (`-1` = N/A for `ID`, `-2` = `rg` missing, `-3` = timeout). Long paths, types, DB columns, samples, and notes are under [full detail](#fields-by-cluster-full-detail).

| Field | Assessment | Cluster | LZB XML | Feed | Idx | Hits | % | Distinct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bundleLinks` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `dynamicAttributes` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `fixedReplacementProducts` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `fractionalQuantitiesAllowed` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 32.12 | 1 |
| `fulfiller` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `isPurchaseable` | ACTIVE | commerce_sku_inherited | yes | no | yes | -2 | 98.32 | 2 |
| `itemAcl` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `manufacturer_part_number` | ACTIVE | commerce_sku_inherited | no | no | yes | -2 | 0.0 | 0 |
| `quantity` | ACTIVE | commerce_sku_inherited | yes | no | yes | -2 | 0.0 | 0 |
| `template` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `unitOfMeasure` | ORPHAN | commerce_sku_inherited | no | no | no | -2 | 0.0 | 0 |
| `addedMaterialTypes` | ACTIVE | cover_core | yes | no | yes | -2 | 14.11 | 14 |
| `additionalDetails` | LEGACY | cover_core | yes | no | no | -2 | 22.53 | 6 |
| `capCode` | ACTIVE | cover_core | yes | yes | yes | -2 | 100.0 | 16 |
| `cleaningCode` | ACTIVE | cover_core | yes | yes | no | -2 | 99.98 | 8 |
| `collectionName` | ACTIVE | cover_core | yes | yes | yes | -2 | 100.0 | 13 |
| `colorDescription` | ACTIVE | cover_core | yes | yes | no | -2 | 100.0 | 785 |
| `colorNumber` | ACTIVE | cover_core | yes | yes | no | -2 | 65.06 | 99 |
| `commodityCode` | LEGACY | cover_core | yes | no | no | -2 | 44.67 | 6 |
| `coverColor` | ACTIVE | cover_core | yes | yes | yes | -2 | 83.58 | 103 |
| `coverType` | ACTIVE | cover_core | yes | yes | yes | -2 | 100.0 | 2 |
| `description` | ACTIVE | cover_core | yes | yes | yes | -2 | 84.52 | 602 |
| `faceContents` | ACTIVE | cover_core | yes | yes | no | -2 | 98.2 | 362 |
| `grade` | ACTIVE | cover_core | yes | yes | no | -2 | 100.0 | 36 |
| `patternName` | ACTIVE | cover_core | yes | no | yes | -2 | 68.0 | 312 |
| `performanceFabricFlag` | ACTIVE | cover_core | yes | yes | no | -2 | 100.0 | 2 |
| `prodCategoryDesc` | DORMANT | cover_core | yes | no | no | -2 | 0.0 | 0 |
| `productCategoryCode` | ACTIVE | cover_core | yes | yes | no | -2 | 99.81 | 12 |
| `series` | ACTIVE | cover_core | yes | yes | no | -2 | 100.0 | 1033 |
| `wearDatedId` | DORMANT | cover_core | yes | no | no | -2 | 0.0 | 0 |
| `wearability` | ACTIVE | cover_core | yes | yes | no | -2 | 99.93 | 26 |
| `coverStatus` | LEGACY | dates_status | yes | no | no | -2 | 99.93 | 3 |
| `endDate` | ACTIVE | dates_status | yes | no | yes | -2 | 0.0 | 0 |
| `startDate` | ACTIVE | dates_status | yes | no | yes | -2 | 0.0 | 0 |
| `status` | ACTIVE | dates_status | yes | yes | yes | -2 | 100.0 | 2 |
| `ID` | ACTIVE | identity | yes | no | no | -1 | 100.0 | 4159 |
| `altImages` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `auxiliaryMedia` | ORPHAN | images_media | no | no | no | -2 | 0.0 | 0 |
| `belowFoldHowToMedia` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `belowFoldVideoMedia` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `cdpDefaultImage` | ACTIVE | images_media | yes | no | yes | -2 | 0.0 | 0 |
| `cdpMouseOverImage` | ACTIVE | images_media | yes | no | yes | -2 | 0.0 | 0 |
| `colorFamilyImages` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `dimensionImage` | ACTIVE | images_media | yes | no | yes | -2 | 0.0 | 0 |
| `largeImage` | ORPHAN | images_media | no | no | no | -2 | 0.0 | 0 |
| `pdpDefaultImage` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `smallImage` | ORPHAN | images_media | no | no | no | -2 | 0.0 | 0 |
| `thumbnailImage` | ORPHAN | images_media | no | no | no | -2 | 0.0 | 0 |
| `videos` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg1` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg1Alt` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg1Caption` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg2` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg2Alt` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbFeatureImg2Caption` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `wtbLeftImg` | DORMANT | images_media | yes | no | no | -2 | 0.0 | 0 |
| `hideForCA` | ACTIVE | online_visibility | yes | no | yes | -2 | 100.0 | 1 |
| `hideForTextSearch` | ACTIVE | online_visibility | yes | no | yes | -2 | 100.0 | 1 |
| `onlineExclusive` | LEGACY | online_visibility | yes | no | no | -2 | 34.62 | 1 |
| `onlineExclusiveText` | DORMANT | online_visibility | yes | no | no | -2 | 0.0 | 0 |
| `onlineOnly` | ORPHAN | online_visibility | no | no | no | -2 | 100.0 | 1 |
| `showOnline` | ACTIVE | online_visibility | yes | no | yes | -2 | 100.0 | 2 |
| `unsearchable` | ACTIVE | online_visibility | yes | no | yes | -2 | 100.0 | 2 |
| `acaBadge` | ACTIVE | other | yes | no | yes | -2 | 100.0 | 1 |
| `ar_enabled` | LEGACY | other | yes | no | no | -2 | 43.62 | 1 |
| `archCoverAvlb` | ACTIVE | other | yes | no | yes | -2 | 100.0 | 2 |
| `archwayID` | ACTIVE | other | yes | no | yes | -2 | 30.56 | 1271 |
| `hasAdjustableHeadrest` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasAdjustableLumbar` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasHeatMassage` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasLiftFunction` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasPower` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasStorage` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `hasUsbChargingPort` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `isNew` | LEGACY | other | yes | no | no | -2 | 100.0 | 1 |
| `isPillowOptions` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `isSleeper` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `madeInUSABadge` | ACTIVE | other | yes | no | yes | -2 | 100.0 | 1 |
| `mostPopular` | LEGACY | other | yes | no | no | -2 | 100.0 | 1 |
| `numberOfCushions` | DORMANT | other | yes | no | no | -2 | 0.0 | 0 |
| `sortOrder` | ACTIVE | other | yes | no | yes | -2 | 15.6 | 649 |
| `atAGlanceContent` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `careFeatures` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `displayHeader` | LEGACY | pdp_below_fold | yes | no | no | -2 | 22.0 | 1 |
| `headerText` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `hideAGlance` | LEGACY | pdp_below_fold | yes | no | no | -2 | 22.0 | 1 |
| `hideStillDeciding` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `linkDescription` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `perfectForInfo` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `romanceCopy` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `skuDocUrl` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `stillDecidingLinks` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `useCareInstructions` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `warrantyInfo` | DORMANT | pdp_below_fold | yes | no | no | -2 | 0.0 | 0 |
| `discountable` | ORPHAN | pricing | no | no | no | -2 | 100.0 | 1 |
| `listPrice` | ACTIVE | pricing | no | no | yes | -2 | 0.0 | 0 |
| `nonreturnable` | LEGACY | pricing | no | no | no | -2 | 100.0 | 2 |
| `onSale` | ACTIVE | pricing | no | no | yes | -2 | 100.0 | 1 |
| `salePrice` | ACTIVE | pricing | no | no | yes | -2 | 0.0 | 0 |
| `wholesalePrice` | ACTIVE | pricing | yes | no | yes | -2 | 0.0 | 0 |

## Fields by cluster (full detail)

### identity

#### `ID`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -1
- **Export sample:** 100.0% non-empty, **4159** distinct values
- **Top values (up to 5):** D180086 (1); LB143687 (1); LB143677 (1); B143987 (1); J154672 (1)
- **Notes:**
  - Repository item id (primary key); not a `<property>` on the descriptor.


### pricing

#### `discountable`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** true (4159)
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `listPrice`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Commerce/config/com/lzb/repository/lzbExtract/lzbRepository.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `nonreturnable`

- **Assessment:** LEGACY
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** false (4107); true (52)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `onSale`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `salePrice`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wholesalePrice`

- **Assessment:** ACTIVE
- **Schema:** type `double`, DB column `wholesale_price`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### dates_status

#### `coverStatus`

- **Assessment:** LEGACY
- **Schema:** type `enumerated`, DB column `status`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 99.93% non-empty, **3** distinct values
- **Top values (up to 5):** P (1531); O (1354); A (1271)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `endDate`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `startDate`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `status`

- **Assessment:** ACTIVE
- **Schema:** type `enumerated`, DB column `status`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** D (3344); A (815)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### online_visibility

#### `hideForCA`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `hide_for_ca`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hideForTextSearch`

- **Assessment:** ACTIVE
- **Schema:** type `String`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** true (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `onlineExclusive`

- **Assessment:** LEGACY
- **Schema:** type `boolean`, DB column `online_exclusive`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 34.62% non-empty, **1** distinct values
- **Top values (up to 5):** false (1440)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `onlineExclusiveText`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `online_exclusive_text`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `onlineOnly`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `showOnline`

- **Assessment:** ACTIVE
- **Schema:** type `enumerated`, DB column `online_only_sku`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** false (3412); true (747)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `unsearchable`

- **Assessment:** ACTIVE
- **Schema:** type `enumerated`, DB column `unsearchable`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** true (3175); false (984)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### images_media

#### `altImages`

- **Assessment:** DORMANT
- **Schema:** type `list`, DB column `image_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `auxiliaryMedia`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `belowFoldHowToMedia`

- **Assessment:** DORMANT
- **Schema:** type `list`, DB column `bf_how_to_media`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `belowFoldVideoMedia`

- **Assessment:** DORMANT
- **Schema:** type `list`, DB column `bf_video_media`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `cdpDefaultImage`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `image_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `cdpMouseOverImage`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `mouse_over_image_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `colorFamilyImages`

- **Assessment:** DORMANT
- **Schema:** type `map`, DB column `imageURL`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `dimensionImage`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `dimension_image_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `largeImage`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `pdpDefaultImage`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `pdp_image_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `smallImage`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `thumbnailImage`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `videos`

- **Assessment:** DORMANT
- **Schema:** type `list`, DB column `media_id`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg1`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_1`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg1Alt`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_1_alt`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg1Caption`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_1_caption`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg2`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_2`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg2Alt`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_2_alt`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbFeatureImg2Caption`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_feature_img_2_caption`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wtbLeftImg`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wtb_left_img`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### cover_core

#### `addedMaterialTypes`

- **Assessment:** ACTIVE
- **Schema:** type `set`, DB column `material_type`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 14.11% non-empty, **14** distinct values
- **Top values (up to 5):** Performance (262); Performance,iClean (86); Pet Friendly,Performance,iClean (65); iClean (64); Conserve,iClean (26)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `additionalDetails`

- **Assessment:** LEGACY
- **Schema:** type `big string`, DB column `additional_details`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 22.53% non-empty, **6** distinct values
- **Top values (up to 5):** Normal Fabric (484); Performance Fabric (268); Authentic Leather (100); Performance Leather (66); Medium Fabric (17)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `capCode`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `cap_code`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **16** distinct values
- **Top values (up to 5):** DR (2071); UR (761); LM (276); LL (243); PS (185)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `cleaningCode`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `cleaning_code`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 99.98% non-empty, **8** distinct values
- **Top values (up to 5):** W (1191); WS (1085); S (817); L (567); UN (445)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `collectionName`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `collection_name`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **13** distinct values
- **Top values (up to 5):** Major Upholstery (3136); Chair (461); Promotion Cover (138); Joybird (121); Out-sourced Sets (96)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `colorDescription`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `color_description`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **785** distinct values
- **Top values (up to 5):** Charcoal (82); Chocolate (67); Navy (66); Stone (63); Mocha (49)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `colorNumber`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `color_number`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 65.06% non-empty, **99** distinct values
- **Top values (up to 5):** 78 (141); 86 (95); 79 (90); 32 (78); 08 (77)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `commodityCode`

- **Assessment:** LEGACY
- **Schema:** type `string`, DB column `commodity_code`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 44.67% non-empty, **6** distinct values
- **Top values (up to 5):** CL (1587); LH (209); RL (43); CS (11); CH (6)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `coverColor`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `cover_color`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 83.58% non-empty, **103** distinct values
- **Top values (up to 5):** 78 (159); 86 (131); 32 (121); 87 (107); 54 (103)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `coverType`

- **Assessment:** ACTIVE
- **Schema:** type `enumerated`, DB column `cover_type`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** fabric (3582); leather (577)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `description`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml`
- **Feed map:** yes · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 84.52% non-empty, **602** distinct values
- **Top values (up to 5):** Major Upholstery (639); Our wide range of leather options provide long-lasting, stylish versatility that develops even more  (152); Joybird (118); Promotion Cover (95); LZB Chair (89)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `faceContents`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `face_contents`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 98.2% non-empty, **362** distinct values
- **Top values (up to 5):** 100% Polyester (1777); null (427); 100% Leather (288); Leather/Vinyl (173); 100% Cotton (48)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `grade`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `grade`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **36** distinct values
- **Top values (up to 5):** D (979); C (656); E (391); J (283); B (268)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `patternName`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `pattern_name`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 68.0% non-empty, **312** distinct values
- **Top values (up to 5):** Solids (966); Secondary (171); Accents (128); Florals (113); Modern (88)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `performanceFabricFlag`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `per_fabric_flag`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** false (3281); true (878)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `prodCategoryDesc`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `prod_category_desc`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `productCategoryCode`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `product_category_code`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 99.81% non-empty, **12** distinct values
- **Top values (up to 5):** MU (3109); CH (496); PR (130); JO (121); OS (93)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `series`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `series`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1033** distinct values
- **Top values (up to 5):** 9810 (45); 9419 (31); 1534 (29); 6533 (21); 1639 (19)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wearDatedId`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `wear_dated_id`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `wearability`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `wearability`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** yes · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 99.93% non-empty, **26** distinct values
- **Top values (up to 5):** 2 (1999); ? (828); 7 (297); 10 (230); 8 (176)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### pdp_below_fold

#### `atAGlanceContent`

- **Assessment:** DORMANT
- **Schema:** type `big string`, DB column `at_a_glance_content`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `careFeatures`

- **Assessment:** DORMANT
- **Schema:** type `big string`, DB column `care_features`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `displayHeader`

- **Assessment:** LEGACY
- **Schema:** type `boolean`, DB column `pdp_still_deciding_show_header`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 22.0% non-empty, **1** distinct values
- **Top values (up to 5):** true (915)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `headerText`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `pdp_still_deciding_header_text`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hideAGlance`

- **Assessment:** LEGACY
- **Schema:** type `boolean`, DB column `hide_at_a_glance`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 22.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (915)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hideStillDeciding`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `pdp_hide_still_deciding`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `linkDescription`

- **Assessment:** DORMANT
- **Schema:** type `map`, DB column `link_description`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `perfectForInfo`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `perfect_for_info`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `romanceCopy`

- **Assessment:** DORMANT
- **Schema:** type `big string`, DB column `romance_copy`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `skuDocUrl`

- **Assessment:** DORMANT
- **Schema:** type `map`, DB column `doc_url`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `stillDecidingLinks`

- **Assessment:** DORMANT
- **Schema:** type `list`, DB column `still_deciding_link`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `useCareInstructions`

- **Assessment:** DORMANT
- **Schema:** type `big string`, DB column `use_care_instructions`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `warrantyInfo`

- **Assessment:** DORMANT
- **Schema:** type `string`, DB column `warranty_info`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


### commerce_sku_inherited

#### `bundleLinks`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `dynamicAttributes`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `fixedReplacementProducts`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `fractionalQuantitiesAllowed`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 32.12% non-empty, **1** distinct values
- **Top values (up to 5):** false (1336)
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `fulfiller`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `isPurchaseable`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `purchaseable`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 98.32% non-empty, **2** distinct values
- **Top values (up to 5):** false (3331); true (758)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `itemAcl`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `manufacturer_part_number`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `quantity`

- **Assessment:** ACTIVE
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `atg/la-z-boy/modules/LB/Commerce/config/atg/commerce/catalog/custom/customCatalog.xml`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `template`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).

#### `unitOfMeasure`

- **Assessment:** ORPHAN
- **Schema:** type `—`, DB column `—`, in LZB catalog XML: no
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - No `<property name="…">` match in scanned LZB config XML — typically inherited ATG Commerce sku field (see Oracle ATG reference) or rename mismatch.
  - Code hit count skipped (`rg` not on PATH).


### other

#### `acaBadge`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `aca_badge`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `ar_enabled`

- **Assessment:** LEGACY
- **Schema:** type `enumerated`, DB column `ar_enabled`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 43.62% non-empty, **1** distinct values
- **Top values (up to 5):** false (1814)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `archCoverAvlb`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `archway_cover_avlb`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **2** distinct values
- **Top values (up to 5):** false (3588); true (571)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `archwayID`

- **Assessment:** ACTIVE
- **Schema:** type `string`, DB column `archway_id`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 30.56% non-empty, **1271** distinct values
- **Top values (up to 5):** SM6ZB143987 (1); SM6ZC191079 (1); SM6ZH169165 (1); SM6ZC161055 (1); SL6LB160151 (1)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasAdjustableHeadrest`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_adjustable_headrest`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasAdjustableLumbar`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_adjustable_lumbar`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasHeatMassage`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_heat_massage`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasLiftFunction`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_lift_function`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasPower`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_power`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasStorage`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_storage`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `hasUsbChargingPort`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `has_usb_charge_port`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `isNew`

- **Assessment:** LEGACY
- **Schema:** type `boolean`, DB column `is_new`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `isPillowOptions`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `pillow_options`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `isSleeper`

- **Assessment:** DORMANT
- **Schema:** type `boolean`, DB column `is_sleeper`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `madeInUSABadge`

- **Assessment:** ACTIVE
- **Schema:** type `boolean`, DB column `made_in_usa_badge`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `mostPopular`

- **Assessment:** LEGACY
- **Schema:** type `boolean`, DB column `most_popular`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 100.0% non-empty, **1** distinct values
- **Top values (up to 5):** false (4159)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `numberOfCushions`

- **Assessment:** DORMANT
- **Schema:** type `int`, DB column `number_of_cushions`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** no
- **Code hits:** -2
- **Export sample:** 0.0% non-empty, **0** distinct values
- **Top values (up to 5):** —
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).

#### `sortOrder`

- **Assessment:** ACTIVE
- **Schema:** type `long`, DB column `sort_order`, in LZB catalog XML: yes
- **Other XML (`name="…"` match):** `—`
- **Feed map:** no · **Indexed (childSKUs rule set):** yes
- **Code hits:** -2
- **Export sample:** 15.6% non-empty, **649** distinct values
- **Top values (up to 5):** 4 (1); 170 (1); 485 (1); 72 (1); 570 (1)
- **Notes:**
  - Code hit count skipped (`rg` not on PATH).


## Assessment rule (deterministic)

- **ORPHAN:** Not in `coverFileSrcDestMap`, not in the childSKUs index set, and no `name="…"` match for the field in scanned LZB config XML (Commerce / Endeca / Merchandising / Base). Not `ID`. Typically ATG core sku properties absent from the repo fragment.
- **DORMANT:** In schema, **0%** non-empty in export, **0** code hits (after descriptor exclude), not in feed map, not in index config.
- **LEGACY:** **>0%** populated but no feed, no index, and **≤0** code hits — data exists in BCC but nothing in this repo reads it.
- **ACTIVE:** In feed map, or in index config, or **≥3** code hits, or field is `ID`.
- **UNCLEAR:** Mixed / low signal (e.g. 1–2 code hits only). Triaged manually if needed.
