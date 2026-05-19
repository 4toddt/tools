# BCC coverSku — ACTIVE field behavior (display trace)

Companion to [bcc-field-inventory.md](bcc-field-inventory.md). For each column classified **ACTIVE** there, this document states **how it affects the shopper-facing experience** (or internal commerce flows) based on evidence in `atg/la-z-boy/modules/LB/Storefront`, `LB/Commerce`, and (where noted) `LB/Endeca`.

**Evidence helper:** [scripts/trace-active-field-hits.py](scripts/trace-active-field-hits.py) scans Storefront + Commerce for `sku.<field>` / `coverSku.<field>` substrings and writes [data/trace-active-field-hits.json](data/trace-active-field-hits.json). Manual greps extended that (e.g. `P_LowestPrice`, RQL, assembler filters).

## Vocabulary

| Label | Meaning |
| --- | --- |
| **Renders** | Value is emitted to HTML, JSON for the browser, or email in a way a shopper can see or hear (text, image URL, badge). |
| **Search / CDP** | Value appears on Endeca/Unbxd **records** (`element.attributes[...]`, `productRecord[...]`) or drives **navigation / typeahead** filters—not always visible text. |
| **Control** | Gates behavior (sort, RQL filter, `c:if`, discontinued logic) without necessarily printing the field as copy. |
| **Feed / catalog** | Wired in [LZBCatalogSourceDestinationMapping.properties](atg/la-z-boy/modules/LB/Commerce/config/com/lzb/feed/product/LZBCatalogSourceDestinationMapping.properties) or updated in [LZBCatalogTools.java](atg/la-z-boy/modules/LB/Commerce/src/com/lzb/commerce/catalog/LZBCatalogTools.java); may not surface as a literal `sku.*` string in JSP. |
| **Indexed only (here)** | Listed in [product-sku-output-config.xml](atg/la-z-boy/modules/LB/Endeca/config/atg/commerce/endeca/index/product-sku-output-config.xml) but no Storefront/Commerce hit in this pass beyond index/assembler code paths. |

**Inventory flags** (from Phase 1 quick reference): **Feed** = in `coverFileSrcDestMap`; **Idx** = childSKUs index rule includes the property.

---

## identity

### `ID`

- **Inventory:** Feed=no · Idx=no (ACTIVE as repository primary key).
- **Renders / Control:** Cover repository id is passed everywhere as `coverId`, used in URLs, modals, wishlist/cart payloads, and `addedItemInfo.coverSku.id` in JSON (e.g. [cart/json/cartSuccessJson.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/json/cartSuccessJson.jsp), [rwd.war/sitewide/json/addToCart.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/sitewide/json/addToCart.jsp)).
- **Search / CDP:** `sku.repositoryId` / `defaultCoverSku` on Endeca records for tiles and deep links (e.g. [cartridges/CoverResultsList/CoverResultsList.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/CoverResultsList/CoverResultsList.jsp)).

---

## pricing

### `listPrice`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** Storefront price tiles overwhelmingly use Endeca-derived keys such as `P_LowestPrice` / `P_LowestSalePrice` (e.g. [cdp/resultsListGrid.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cdp/resultsListGrid.jsp), [modals/quickviewmodal.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/modals/quickviewmodal.jsp)), not literal `sku.listPrice` text in CDP JSPs.
- **Renders:** [cart/gadgets/cartItems.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/gadgets/cartItems.jsp) reads `sku.listPrice` / `sku.salePrice` for line-item display paths (configurable SKU context).

### `salePrice`

- **Inventory:** Feed=no · Idx=yes.
- **Renders:** Same cart gadget path as `listPrice` (`sku.salePrice` alongside `sku.listPrice` in [cart/gadgets/cartItems.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/gadgets/cartItems.jsp)).
- **Search / CDP:** Shoppers see computed sale amounts via `P_LowestSalePrice` and related record attributes on listings/PDP, not raw `sku.salePrice` strings in the same files as `listPrice`.

### `onSale`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** CDP / recently viewed use record attribute **`onSale`** (e.g. [cdp/resultsListGrid.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cdp/resultsListGrid.jsp), [cartridges/RecentlyViewedProducts/RecentlyViewedProducts.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/RecentlyViewedProducts/RecentlyViewedProducts.jsp)) for sale badges—key name may differ from `sku.onSale` depending on assembler mapping.
- **Renders:** Sectional / simple PDP paths expose JSON or markup with an `onSale` flag derived from `hasSalePrice` (e.g. [browse/pdp/sectional_pdp_price.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/pdp/sectional_pdp_price.jsp)).

### `wholesalePrice`

- **Inventory:** Feed=yes · Idx=yes.
- **Control / internal:** Used heavily in **Commerce reporting and order** code (`getPropertyValue("wholesalePrice")`, [LZBCommerceItem.java](atg/la-z-boy/modules/LB/Commerce/src/com/lzb/commerce/order/LZBCommerceItem.java), licensee report generators)—**not** a typical consumer PDP string.
- **Indexed only (here):** No `sku.wholesalePrice` / `coverSku.wholesalePrice` hits in Storefront JSP scan; treat indexed output as supporting B2B / analytics / downstream consumers.

---

## dates_status

### `startDate` / `endDate`

- **Inventory:** Feed=no · Idx=yes (both).
- **Search / CDP:** Indexed for record-level merchandising / price validity; storefront **sale end** UI reads **`endDate`** as a **page/droplet param** (e.g. [browse/pdp/productTitleBar.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/pdp/productTitleBar.jsp), [rwd.war/browse/json/productPrice.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/browse/json/productPrice.jsp))—not always the same code path as `sku.endDate` literal in JSP.
- **Renders:** JSON price endpoints emit `endDate` for client scripts.

### `status`

- **Inventory:** Feed=yes · Idx=yes.
- **Control:** `sku.status` / `productRecord['sku.status']` gates **active vs discontinued** presentation on PDP, quick view, wishlist fragments (e.g. [cartridges/ProductDetail/ProductDetail.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/ProductDetail/ProductDetail.jsp), [modals/quickviewmodal.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/modals/quickviewmodal.jsp), [includes/pdpComponentData.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/includes/pdpComponentData.jsp)).

---

## online_visibility

### `hideForCA`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** [LZBCanadianFilterBuilder.java](atg/la-z-boy/modules/LB/Endeca/src/com/lzb/endeca/assembler/navigation/filter/LZBCanadianFilterBuilder.java) builds a constraint on **`sku.hideForCA`**—**navigation / result shaping** for Canada, not a visible string.

### `hideForTextSearch`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** [TypeAheadResultAdaptor.java](atg/la-z-boy/modules/LB/Endeca/src/com/lzb/endeca/typeahead/TypeAheadResultAdaptor.java) reads attribute **`sku.hideForTextSearch`**; index accessors default it on configurable SKUs ([LZBConfigurableSKUPropertyAccessor.java](atg/la-z-boy/modules/LB/Endeca/src/com/lzb/endeca/index/accessor/LZBConfigurableSKUPropertyAccessor.java)).

### `unsearchable`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** [LZBUnsearchableSkuFilterBuilder.java](atg/la-z-boy/modules/LB/Endeca/src/com/lzb/endeca/assembler/navigation/filter/LZBUnsearchableSkuFilterBuilder.java) applies **`sku.unsearchable`** filter to navigation.

### `showOnline`

- **Inventory:** Feed=no · Idx=yes.
- **Control:** Endeca **dimension / option** assembly reads `showOnline` from repository items to decide which SKUs/options surface ([LZBConfigurableSKUDimensionAccessor.java](atg/la-z-boy/modules/LB/Endeca/src/com/lzb/endeca/index/accessor/LZBConfigurableSKUDimensionAccessor.java)). Storefront JSPs also mention `showOnline` on **config options** (different item type)—do not conflate with cover-only lines without verifying runtime item.
- **Search / CDP:** Indexed flag participates in which SKUs appear in experience-driven lists.

---

## images_media

### `cdpDefaultImage`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** **`sku.cdpDefaultImage`** on Endeca records drives CDP / carousel imagery (e.g. [cdp/resultsListGrid.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cdp/resultsListGrid.jsp) `element.attributes['sku.cdpDefaultImage']`).

### `cdpMouseOverImage`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** Same pattern as `cdpDefaultImage` using **`sku.cdpMouseOverImage`** on records (multiple CDP JSP hits in trace JSON).

### `dimensionImage`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** At least one storefront reference to **`sku.dimensionImage`** for record-driven imagery (see [data/trace-active-field-hits.json](data/trace-active-field-hits.json)); treat like other `sku.*` image URLs on listings/PDP.

---

## cover_core

### `addedMaterialTypes`

- **Inventory:** Feed=no · Idx=yes.
- **Renders / Search:** [FabricSelectorResultsList.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/FabricSelectorResultsList/FabricSelectorResultsList.jsp) reads `sku.addedMaterialTypes` into JSON for fabric-selector UI.

### `capCode`

- **Inventory:** Feed=yes · Idx=yes.
- **Feed / catalog:** Import-side handling of property name **`capCode`** in [LZBCatalogTools.java](atg/la-z-boy/modules/LB/Commerce/src/com/lzb/commerce/catalog/LZBCatalogTools.java).
- **Control:** PDP cover selector exposes **`data-cover-cap-code`** from parsed in-stock cover tokens (`coverArr[7]`, lowercased)—client behavior for swatch / fabric flows ([browse/pdp/pdpCoverSelector.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/pdp/pdpCoverSelector.jsp)).

### `cleaningCode` / `wearability`

- **Inventory:** Feed=yes · Idx=no (both).
- **Renders (related UX):** [browse/coverCare.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/coverCare.jsp) renders **cleaning** and **wearability** lists from **`coverCare.*`** structures (care content model), not necessarily `dsp:valueof` of `coverSku.cleaningCode` / `wearability`—treat as **shopper-facing care** tied to cover selection flows.
- **Feed / catalog:** Values are feed-mapped for merchandising and downstream systems.

### `collectionName`

- **Inventory:** Feed=yes · Idx=yes.
- **Feed / catalog:** Strong feed + index wiring; no `sku.collectionName` / `coverSku.collectionName` hits in Storefront scan. Likely consumed in search records or non-`LB/Storefront` surfaces—**Search / CDP** until a specific cartridge reference is found outside this grep slice.

### `colorDescription`

- **Inventory:** Feed=yes · Idx=no.
- **Renders:** Cart / add-to-cart JSON emits **`addedItemInfo.coverSku.colorDescription`** ([cart/json/cartSuccessJson.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/json/cartSuccessJson.jsp), [rwd.war/sitewide/json/addToCart.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/sitewide/json/addToCart.jsp)).

### `colorNumber`

- **Inventory:** Feed=yes · Idx=no (ACTIVE via **feed** in Phase 1 rules).
- **Feed / catalog:** Feed-mapped; no `sku.colorNumber` / `coverSku.colorNumber` in Storefront scan. Shoppers more often see **`coverColor`** (param + modal) and image URLs keyed by cover id than this numeric column in JSPs.

### `coverColor`

- **Inventory:** Feed=yes · Idx=yes.
- **Renders:** Passed as **request param** and shown in cover modals (`${coverColor}`, [modals/viewCoverDetailsModal.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/modals/viewCoverDetailsModal.jsp), [rwd.war/browse/ajax/viewCoverDetailsModal.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/browse/ajax/viewCoverDetailsModal.jsp)); PDP cover loops use `param="coverColor"` across multiple `browse/pdp` JSPs.

### `coverType`

- **Inventory:** Feed=yes · Idx=yes.
- **Search / CDP:** Cover search refinements test **`coverSku.coverType`** ([CoverSearchRefinementContainer.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/CoverSearchRefinementContainer/CoverSearchRefinementContainer.jsp)).
- **Renders:** Add-to-cart JSON includes **`addedItemInfo.coverSku.coverType`** ([rwd.war/sitewide/json/addToCart.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/sitewide/json/addToCart.jsp)).

### `description`

- **Inventory:** Feed=yes · Idx=yes.
- **Search / CDP:** Indexed for search / SEO payloads; direct `coverSku.description` / `sku.description` strings are sparse in Storefront grep—copy often merged at **product** level or rendered via cartridges outside the narrow `sku.description` pattern.

### `faceContents`

- **Inventory:** Feed=yes · Idx=no.
- **Feed / catalog:** Feed-mapped; no `sku.faceContents` / `coverSku.faceContents` hit in Storefront/Commerce scan—likely **merchandising / downstream** or rendered via content paths not matching this substring pass.

### `grade`

- **Inventory:** Feed=yes · Idx=no.
- **Renders:** Legacy cart / configurator JSPs display **`configOptionCover.sku.grade`** in pricing include flows ([cart/atgProductDetail.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/atgProductDetail.jsp)).

### `patternName`

- **Inventory:** Feed=no · Idx=yes.
- **Search / CDP:** **`coverSku.patternName`** on records for link `title` and refinement dimensions ([CoverResultsList.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/CoverResultsList/CoverResultsList.jsp), [CoverSearchRefinementContainer.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/CoverSearchRefinementContainer/CoverSearchRefinementContainer.jsp)).

### `performanceFabricFlag`

- **Inventory:** Feed=yes · Idx=no.
- **Renders:** Cart success / add-to-cart JSON exposes **`addedItemInfo.coverSku.performanceFabricFlag`** ([cart/json/cartSuccessJson.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cart/json/cartSuccessJson.jsp), [rwd.war/sitewide/json/addToCart.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/sitewide/json/addToCart.jsp)).

### `productCategoryCode`

- **Inventory:** Feed=yes · Idx=no.
- **Feed / catalog:** Feed pipeline; no Storefront `sku.productCategoryCode` hit in scan—likely **merchandising / reporting** or category routing outside literal JSP substring.

### `series`

- **Inventory:** Feed=yes · Idx=no.
- **Feed / catalog:** Same as `productCategoryCode` for this repo slice—no `sku.series` / `coverSku.series` in Storefront grep.

---

## commerce_sku_inherited

### `isPurchaseable`

- **Inventory:** Feed=no · Idx=yes.
- **Control:** **`sku.isPurchaseable`** on Endeca records and `productRecord['sku.isPurchaseable']` gates discontinued / sellable presentation (e.g. [cdp/resultsListGrid.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cdp/resultsListGrid.jsp), [browse/gadgets/productTile.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/gadgets/productTile.jsp), [rwd.war/cartridges/ProductDetailsPage/ProductDetailsPage.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/cartridges/ProductDetailsPage/ProductDetailsPage.jsp)).

### `manufacturer_part_number`

- **Inventory:** Feed=no · Idx=yes.
- **Indexed only (here):** No `sku.manufacturer_part_number` Storefront hit; related **MPN** XML types exist under Merchandising / BazaarVoice feed packages—assume **integrations / syndication**, not PDP copy in this slice.

### `quantity`

- **Inventory:** Feed=no · Idx=yes.
- **Indexed only (here) for cover SKU:** Storefront **`quantity`** matches overwhelmingly refer to **commerce item line quantity**, not `coverSku.quantity`—do not equate cart quantity inputs with cover SKU repository `quantity` without item-type verification.

---

## other

### `acaBadge` / `madeInUSABadge`

- **Inventory:** Feed=no · Idx=yes (both).
- **Renders:** PDP info tests **`productRecord['sku.acaBadge']`** and **`productRecord['sku.madeInUSABadge']`** to emit USA / ACA imagery ([browse/pdp/pdpInfo.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/browse/pdp/pdpInfo.jsp)); constants in [LZBCatalogConstants.java](atg/la-z-boy/modules/LB/Base/src/com/lzb/common/LZBCatalogConstants.java).

### `archCoverAvlb`

- **Inventory:** Feed=no · Idx=yes.
- **Control:** Repository **RQL** on cover SKUs: `archCoverAvlb = true AND NOT archwayId IS NULL` for free swatches ([rwd.war/contactus/free-swatches.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/contactus/free-swatches.jsp)).

### `archwayID`

- **Inventory:** Feed=no · Idx=yes.
- **Control / Renders:** Same swatches flow: RQL references **`archwayId`**; result rows read **`element.archwayId`** into request vars for downstream display ([rwd.war/contactus/free-swatches.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/contactus/free-swatches.jsp)).

### `sortOrder`

- **Inventory:** Feed=no · Idx=yes.
- **Control:** Swatches repository queries sort by **`+sortOrder`** ([store.war/contactus/free-swatches.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/contactus/free-swatches.jsp), [rwd.war/contactus/free-swatches.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/contactus/free-swatches.jsp)).

---

## Spot-check (plan validation)

| Field | Expected pattern | Verified in |
| --- | --- | --- |
| `archCoverAvlb` | RQL control on cover repository | [rwd.war/contactus/free-swatches.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/rwd.war/contactus/free-swatches.jsp) |
| `patternName` | `coverSku.patternName` on CDP records | [CoverResultsList.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cartridges/CoverResultsList/CoverResultsList.jsp) |
| `cdpDefaultImage` | `sku.cdpDefaultImage` on records | [cdp/resultsListGrid.jsp](atg/la-z-boy/modules/LB/Storefront/j2ee/store.war/cdp/resultsListGrid.jsp) |

---

## Limitations

- Scope was **LB/Storefront + LB/Commerce** plus cited **LB/Endeca** assemblers/accessors—not Experience Manager, mobile apps, or off-repo services.
- **Indexed-only** does not mean “unused”; it means no literal property reference appeared in those trees in this pass.
- Typos in legacy record keys (e.g. **`colorFamliy`**) still drive behavior; align BCC field names to index `output-name` when tracing regressions.
