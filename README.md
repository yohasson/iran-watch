# Iran strike-risk watch

Personal dashboard: **https://yohasson.github.io/iran-watch/**

A static page (no build step) that shows the latest Iran strike-risk check and a flight-risk check. It can be installed as an app (manifest + service worker) and can show device notifications.

- `index.html` – the page. It loads `data.json` from the main branch (GitHub API → raw → local copy), re-reads live Polymarket prices, and recalculates the market part, the 7-day figure and the flight risk.
- `data.json` – written by the hourly watch run to **both** the `main` and `gh-pages` branches. Times are UTC; the page shows Israel time.
- Personal flight details (number, departure time) are never published; they are entered in the page's Settings and kept on the device only.

## `data.json` fields (keep names and structure)

| Field | Meaning |
|---|---|
| `updated_utc` | Time of the check |
| `summary` | One plain-English line on what changed |
| `message_sent` | `none`, `alert`, `flight alert`, `all clear` or `flight OK` |
| `major` | `F` main estimate %, `prev_F`, `E` news-based %, `M` market-based %, `F7` 7-day % (rough), `threshold` 7 |
| `limited` | `L` any-strike %, `prev_L` |
| `alert` | `active`, `last_alerted_pct`, `last_alert_utc`, `hard_triggers` [{`time_utc`,`source`,`text`}] |
| `flight` | `active`, `label` (generic, no flight number or date), `R` %, `prev_R`, `baseline` 17, `alert_at` 25, `C1`, `C2`, `W`, `triggers`, `status_note` (no flight number) |
| `model` | `E` %, `P_iran_nov30`, `P_iran_dec31`, `P_il_nov30` (fractions), `W` %, `F_floor`, `R_floor` |
| `markets` | List of {`label`,`now` %,`prev` %,`url`}. Item 0 must be "Iran full airspace closure by 30 Nov" |
| `brent` | `usd`, `prev_usd`, `change_pct_day`, `read_utc` |
| `items` | Up to 6 notable items from the latest check: {`time_utc`,`source`,`text`,`link`,`effect`} |
| `events` | All notable items from all checks, newest first, last 200 kept (same fields as `items`) |
| `checklist` | Warning signs: {`key`,`label`,`status` green/amber/red,`note`,`time_utc`} |
| `open_items` | Up to 5 short lines |
| `history` | One entry per check {`utc`,`F`,`E`,`M`,`L`,`R`,`F7`}, last 168 kept |

Estimates only, not predictions or advice.
