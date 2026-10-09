#!/usr/bin/env python3
"""Write data.json: the promo every open La-Z-Boy store shows today, from Yext.

Needs YEXT_API_KEY in the environment (read access to the Knowledge API is
enough). Standard library only, so it runs in a bare GitHub Action.

    YEXT_API_KEY=... python3 build_data.py

data.json is published on a public page, so it holds only what the store
pages already show: name, address, and the promo slugs.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.yext.com/v2/accounts/me/entities"
VERSION = "20240401"
INDEPENDENT_LABEL = "38347"
OUT = Path(__file__).with_name("data.json")


def entities(key: str, entity_type: str, fields: str):
    params = {"api_key": key, "v": VERSION, "entityTypes": entity_type, "fields": fields, "limit": 50}
    while True:
        url = f"{API}?{urllib.parse.urlencode(params)}"
        try:
            with urllib.request.urlopen(url, timeout=60) as res:
                page = json.load(res)["response"]
        except urllib.error.HTTPError as exc:
            sys.exit(f"Yext {entity_type}: HTTP {exc.code}")  # the URL carries the key; never print it
        yield from page.get("entities", [])
        if not page.get("pageToken"):
            return
        params["pageToken"] = page["pageToken"]


def store(e: dict) -> dict:
    a, meta = e.get("address") or {}, e.get("meta") or {}
    city = a.get("city", "")
    # Some store names are Yext templates ("La-Z-Boy [[address.city]]").
    name = re.sub(r"\s+", " ", (e.get("name") or "").replace("[[address.city]]", city)).strip()
    promo = lambda field: (e.get(field) or [None])[0]
    return {
        "id": meta.get("id", ""),
        "name": name,
        "address": a.get("line1", ""),
        "city": city,
        "region": a.get("region", ""),
        "country": a.get("countryCode", ""),
        "type": "ILS" if INDEPENDENT_LABEL in (meta.get("labels") or []) else "CLS",
        "calendar": promo("c_promo"),
        "override": promo("c_promoOverride"),
    }


def main() -> None:
    key = os.environ.get("YEXT_API_KEY")
    if not key:
        sys.exit("Set YEXT_API_KEY.")
    promos = {e["meta"]["id"]: e.get("name", "") for e in entities(key, "ce_promotion", "name")}
    stores = [store(e) for e in entities(key, "location", "name,address,closed,c_promo,c_promoOverride")
              if not e.get("closed")]
    stores.sort(key=lambda s: (s["country"], s["region"], s["city"], s["name"]))
    # Names for today's promos only; the full list would name sales that haven't started.
    in_use = {s[f] for s in stores for f in ("calendar", "override") if s[f]}
    promos = {slug: name for slug, name in promos.items() if slug in in_use}
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    if previous.get("promos") == promos and previous.get("stores") == stores:
        print(f"{OUT.name}: unchanged since {previous.get('changedAt')}")
        return
    # Only real changes rewrite the file, so the hourly Action commits only then.
    data = {
        "changedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "promos": promos,
        "stores": stores,
    }
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{OUT.name}: {len(stores)} open stores, {len(promos)} promotions")


if __name__ == "__main__":
    main()
