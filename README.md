# Iran strike-risk watch

Personal dashboard: **https://yohasson.github.io/iran-watch/**

A static page (no build step) that shows the latest hourly Iran strike-risk check and the 27 Nov flight-risk check.

- `index.html` – the page. It reloads `data.json` every 5 minutes and re-reads live Polymarket prices every hour. **Update now** does both at once and recalculates the market part of the main estimate and the flight risk.
- `data.json` – written by the hourly watch run. Times are UTC; the page shows Israel time.

## `data.json` fields (keep names and structure)

| Field | Meaning |
|---|---|
| `updated_utc` | Time of the hourly check |
| `summary` | One plain-English line on what changed |
| `message_sent` | `none`, `alert`, `flight alert`, `all clear` or `flight OK` |
| `major` | `F` main estimate %, `prev_F`, `E` news-based %, `M` market-based %, `threshold` 7 |
| `limited` | `L` any-strike %, `prev_L` |
| `alert` | `active`, `last_alerted_pct`, `last_alert_utc`, `hard_triggers` [{`time_utc`,`source`,`text`}] |
| `flight` | `active`, `label`, `R` %, `prev_R`, `baseline` 17, `alert_at` 25, `C1`, `C2`, `W`, `triggers`, `status_note` |
| `model` | Inputs for the live refresh: `E` %, `P_iran_nov30`, `P_iran_dec31`, `P_il_nov30` (fractions), `W` %, `F_floor`, `R_floor` (% or null) |
| `markets` | List of {`label`,`now` %,`prev` %,`url`}. Item 0 must be "Iran full airspace closure by 30 Nov" |
| `brent` | `usd`, `prev_usd`, `change_pct_day`, `read_utc` |
| `items` | Up to 6 notable items: {`time_utc`,`source`,`text`,`link`,`effect`} |
| `open_items` | Up to 5 short lines |
| `history` | One entry per check {`utc`,`F`,`E`,`M`,`L`,`R`}, last 168 kept |

Estimates only, not predictions or advice.
