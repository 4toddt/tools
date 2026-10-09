# Store promos

The promo banner every open La-Z-Boy store shows today, from Yext: its Promo
Override (`c_promoOverride`) if set, otherwise its Promo Calendar (`c_promo`).

- **Live:** https://4toddt.github.io/tools/store-promos/
- **Views:** Text (one row per store) or Banners (each promo's desktop banner
  once, with its stores underneath; overrides tinted).
- **Filters:** ILS (Independent, Yext label 38347) or CLS (everything else),
  country, calendar vs override, promo, search. Filters are kept in the URL,
  e.g. `?type=ILS&source=override&view=banners`.

## Data

`data.json` holds only what store pages already show: store name, address,
type, and promo slugs, plus names for the promos in use today. No contact
details, and no promos that haven't started, because the page is public.

The page never sees a Yext key. `.github/workflows/store-promos.yml` runs
`build_data.py` hourly with the `YEXT_API_KEY` repo secret and commits
`data.json` only when a store's promo changes. To refresh by hand:

```bash
YEXT_API_KEY=... python3 store-promos/build_data.py
```

Future dates aren't shown: the Knowledge API can't read Scheduled Updates
(only the signed-in Yext web app can), and upcoming sales shouldn't be on a
public page anyway.
