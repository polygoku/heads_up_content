import hashlib
import json
from pathlib import Path

root = Path(".")
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
ok = True

seen_pack_ids = set()
seen_global_card_ids = set()

if manifest.get("schema_version") != 1:
    print("ERROR manifest schema_version must be 1")
    ok = False

for entry in manifest["packs"]:
    pack_id = entry["pack_id"]
    if pack_id in seen_pack_ids:
        print("ERROR duplicate pack_id", pack_id)
        ok = False
    seen_pack_ids.add(pack_id)

    path = root / entry["path"]
    if not path.exists():
        print("ERROR missing", path)
        ok = False
        continue

    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    expected = entry["sha256"].lower()
    pack = json.loads(data)

    if actual != expected:
        print("ERROR hash mismatch", pack_id, actual, "expected", expected)
        ok = False

    if pack["pack_id"] != pack_id:
        print("ERROR pack_id mismatch", pack_id, pack["pack_id"])
        ok = False

    if pack["version"] != entry["version"]:
        print("ERROR version mismatch", pack_id, pack["version"], entry["version"])
        ok = False

    cards = pack.get("cards", [])
    if len(cards) < 200:
        print("ERROR too few cards", pack_id, len(cards))
        ok = False

    answers = set()
    card_ids = set()
    for card in cards:
        cid = card["card_id"]
        ans = card["answer"].strip()
        if not ans:
            print("ERROR empty answer", pack_id, cid)
            ok = False
        if cid in card_ids:
            print("ERROR duplicate card_id in pack", pack_id, cid)
            ok = False
        card_ids.add(cid)
        if cid in seen_global_card_ids:
            print("ERROR duplicate global card_id", cid)
            ok = False
        seen_global_card_ids.add(cid)
        if ans in answers:
            print("ERROR duplicate answer in pack", pack_id, ans)
            ok = False
        answers.add(ans)
        if ans not in card.get("banned_tokens", []):
            print("ERROR answer missing from banned_tokens", pack_id, cid, ans)
            ok = False

    print(pack_id, len(cards), "OK" if ok else "checked")

raise SystemExit(0 if ok else 1)
