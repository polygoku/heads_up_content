# Builder Task — Upload 200+ Card Starter Library to Public OTA Content Repo

Public content repo:
https://github.com/polygoku/heads_up_content

Use this bundle as the source of truth.

## Goal

Replace/expand OTA content so every visible category starts with at least 200 cards.

Included packs:

- daily_life_cn: 242 cards, version 2.0.0
- food_cn: 257 cards, version 2.0.0
- animals_cn: 244 cards, version 2.0.0
- gen_z_phrases_en: 258 cards, version 2.0.0
- movies_cn: 273 cards, version 1.0.0
- idioms_cn: 233 cards, version 1.0.0

## Files to upload

Copy these bundle files into the root of `heads_up_content`:

```text
.gitattributes
manifest.json
Packs/daily_life_cn.json
Packs/food_cn.json
Packs/animals_cn.json
Packs/gen_z_phrases_en.json
Packs/movies_cn.json
Packs/idioms_cn.json
```

Keep line endings LF. Do not let Windows convert JSON to CRLF.

## Important app mapping

The app already maps:
```text
daily_life_cn -> DailyLifeGraphic
food_cn -> FoodBanner
animals_cn -> AnimalsBanner
gen_z_phrases_en -> GenZPhrasesBanner
```

If adding `movies_cn` and `idioms_cn` to live content, the app should also map:
```text
movies_cn -> MoviesBanner
idioms_cn -> IdiomsBanner
```

If the app build does not yet map Movies/Idioms, those packs may show generic cards until the mapping is added.

## Validation

From `heads_up_content` root after copying files:

```bash
python validate_public_packs.py
```

Or run this quick check:

```python
import hashlib, json
from pathlib import Path
m = json.loads(Path("manifest.json").read_text(encoding="utf-8"))
for e in m["packs"]:
    data = Path(e["path"]).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    print(e["pack_id"], len(json.loads(data)["cards"]), "OK" if actual == e["sha256"] else f"MISMATCH {actual}")
```

Expected:
```text
daily_life_cn >= 200 OK
food_cn >= 200 OK
animals_cn >= 200 OK
gen_z_phrases_en >= 200 OK
movies_cn >= 200 OK
idioms_cn >= 200 OK
```

## After push

On installed TestFlight build, tap `更新词包`.

Expected status:
```text
词包：已更新 6 个词包 · 2026.05.20.1
```
