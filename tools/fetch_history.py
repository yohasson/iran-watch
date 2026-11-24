"""Fetch the official Polymarket price history for every bet the Iran watch tracks.
Runs on GitHub Actions (no user interaction). Writes history.json at the repo root."""
import json, time, urllib.request, urllib.parse, datetime
SLUGS = ["iran-full-airspace-closure-byptptpt-20260625195253028", "israeli-airspace-closed-by",
         "israel-x-iran-ceasefire-continues-throughptptpt-20260716224448963",
         "us-x-iran-effective-ceasefire-begins-by-2-week-pause-20261108",
         "major-airlines-suspend-ben-gurion-flights-byptptpt", "saudi-airspace-closed-byptptpt",
         "will-the-us-invade-iran-before-2027"]
try:
    extra = json.load(open("data.json")).get("predictions", [])
    for p in extra:
        if p.get("slug") and p["slug"] not in SLUGS: SLUGS.append(p["slug"])
except Exception: pass
UA = {"User-Agent": "iran-watch-history/1.0", "Accept": "application/json"}
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.loads(r.read())
        except Exception as e:
            err = str(e); time.sleep(2 + 3 * i)
    raise RuntimeError(err)
out = {"generated_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "Polymarket gamma-api (markets) + clob prices-history (interval=max, fidelity=60)", "events": {}, "errors": []}
for slug in SLUGS:
    try:
        ev = get("https://gamma-api.polymarket.com/events?slug=" + urllib.parse.quote(slug))
        ev = ev[0] if isinstance(ev, list) and ev else ev
        rows = []
        for m in (ev or {}).get("markets", []):
            try: tok = json.loads(m.get("clobTokenIds") or "[]")[0]
            except Exception: tok = None
            item = {"outcome": m.get("groupItemTitle") or m.get("question"), "question": m.get("question"), "closed": m.get("closed"),
                    "end_date": m.get("endDate"), "final_prices": m.get("outcomePrices"), "volume": m.get("volume"), "token": tok, "pts": []}
            if tok:
                try:
                    h = get("https://clob.polymarket.com/prices-history?interval=max&fidelity=60&market=" + tok).get("history", [])
                    item["pts"] = [[int(x["t"]), round(float(x["p"]) * 100, 2)] for x in h]
                except Exception as e: out["errors"].append(f"{slug} / {item['outcome']}: {e}")
                time.sleep(0.4)
            rows.append(item)
        out["events"][slug] = {"title": (ev or {}).get("title"), "markets": rows}
    except Exception as e: out["errors"].append(f"{slug}: {e}")
json.dump(out, open("history.json", "w"), separators=(",", ":"))
n = sum(len(m["pts"]) for e in out["events"].values() for m in e["markets"])
print("series:", sum(len(e["markets"]) for e in out["events"].values()), "points:", n, "errors:", len(out["errors"]))
