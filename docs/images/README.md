# Images and video

Media for the **SpoolmanNFC** reader and its Home Assistant side.

Nothing is committed here yet — add your own files and update the tables below,
then reference them from the main [`README.md`](../../README.md). Keep the
layout of the companion repo ([`sovol-sh03-dryer/docs/images`](https://github.com/speed007/sovol-sh03-dryer/tree/main/docs/images)):
one folder per subject, a row per file, captions in a table.

Suggested shots (in rough priority order):

## Reader hardware

| File | Shows |
|---|---|
| `hardware/reader.jpg` | The finished reader in its printed case, red LED lit |
| `hardware/reader-inside.jpg` | Inside the case — PN532 **V3** (Elechouse), ESP32-C3 and the I²C wiring |
| `hardware/spool-tag.jpg` | An NTAG215 in its holder, fitted to a spool |
| `hardware/dryer-loaded.jpg` | The dryer loaded with spools |
| `hardware/dryer-slot-tags.jpg` | The slot tags on the dryer — `4` / `3` / `UNLOAD` / `2` / `1` |

## Home Assistant

| File | Shows |
|---|---|
| `home-assistant/tag-map.png` | The tag map — `input_text.spool_slot_tags`, the UID → action JSON |
| `home-assistant/slot-helper.png` | The armed helper — `input_select.spool_slot` (`None` / `1`–`4` / `Unload` / `SV08`) |
| `home-assistant/automation-trace.png` | A trace of `nfc_spool_tag_scanned`, with the resolved variables |

## Spoolman

| File | Shows |
|---|---|
| `spoolman/spool.png` | A spool's page — `location` (bag), `slot` (dryer) and `card_uids` (tag) |

## Spoolman in Fluidd

| File | Shows |
|---|---|
| `fluidd/spool-selection.png` | Fluidd's **Spool Selection** dialog, populated straight from Spoolman |
| `fluidd/spool-cards.png` | Spool cards with Spoolman images and the loaded lane |

## Tagging demo

| File | Shows |
|---|---|
| _to add_ | Tap a slot tag, then a spool tag — the spool's `slot` appears in Spoolman |
| _to add_ | Tap the unload tag, then the spool tag — the Telegram bag reminder |

## Video

| File | Shows |
|---|---|
| _to add_ | **Working demo** — a full multicolour print following the active toolhead |

> If a file is third-party (a stock photo, a screenshot with someone else's UI),
> note it in [`NOTICE`](../../NOTICE) — it isn't covered by the MIT licence.
