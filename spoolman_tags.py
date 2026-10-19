#!/usr/bin/env python3
"""Tag <-> spool mapping helper for Spoolman (NTAG215, UID-only).

Spoolman stores the tag UID in the per-spool custom field `card_uids`
(one tag per spool). This tool lists/assigns/clears those mappings.

Usage:
  spoolman_tags.py list
  spoolman_tags.py lookup <UID>
  spoolman_tags.py assign <spool_id> <UID> [--force]
  spoolman_tags.py clear <spool_id>

Env: SPOOLMAN_URL (default http://spoolman.local:7912 — set it to your own).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("SPOOLMAN_URL", "http://spoolman.local:7912").rstrip("/") + "/api/v1"


def _req(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def get_spools():
    return _req("/spool?limit=10000") or []


def norm(uid):
    return uid.strip().replace(":", "").replace("-", "").replace(" ", "").upper()


def raw_extra(spool):
    # Spoolman stores extra-field values as JSON-encoded strings ("...")
    return dict(spool.get("extra") or {})


def uid_of(spool):
    v = raw_extra(spool).get("card_uids")
    if v is None:
        return ""
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except Exception:
            pass
    return norm(str(v))


def by_id(spools, sid):
    return next((s for s in spools if s["id"] == sid), None)


def by_uid(spools, uid):
    return next((s for s in spools if uid_of(s) == uid), None)


def cmd_list(_a):
    spools = get_spools()
    mapped = sum(1 for s in spools if uid_of(s))
    print(f"{'id':>3}  {'card_uids':<16} {'material':<9} {'name':<30} {'loc':<6} {'rem g':>6}")
    for s in sorted(spools, key=lambda x: x["id"]):
        f = s.get("filament") or {}
        print(f"{s['id']:>3}  {uid_of(s):<16} {str(f.get('material','')):<9} "
              f"{str(f.get('name',''))[:30]:<30} {str(s.get('location','')):<6} "
              f"{(s.get('remaining_weight') or 0):>6.0f}")
    print(f"\n{mapped}/{len(spools)} spools mapped.")


def cmd_lookup(a):
    s = by_uid(get_spools(), norm(a.uid))
    if not s:
        print("no spool with that UID"); return
    f = s.get("filament") or {}
    print(json.dumps({
        "spool_id": s["id"], "material": f.get("material"), "name": f.get("name"),
        "color_hex": f.get("color_hex"), "location": s.get("location"),
        "remaining_weight": s.get("remaining_weight"),
    }))


def cmd_assign(a):
    uid = norm(a.uid)
    spools = get_spools()
    target = by_id(spools, a.spool_id)
    if not target:
        sys.exit(f"spool {a.spool_id} not found")
    other = by_uid(spools, uid)
    if other and other["id"] != a.spool_id:
        msg = f"UID {uid} is currently on spool {other['id']}"
        if not a.force:
            sys.exit(msg + " — use --force to move it here")
        print("WARN: " + msg + " -> moving")
        oextra = raw_extra(other)
        oextra["card_uids"] = None
        _req(f"/spool/{other['id']}", method="PATCH", body={"extra": oextra})
    extra = raw_extra(target)
    extra["card_uids"] = json.dumps(uid)
    _req(f"/spool/{a.spool_id}", method="PATCH", body={"extra": extra})
    print(f"assigned {uid} -> spool {a.spool_id}")


def cmd_clear(a):
    spools = get_spools()
    target = by_id(spools, a.spool_id)
    if not target:
        sys.exit(f"spool {a.spool_id} not found")
    extra = raw_extra(target)
    extra["card_uids"] = None
    _req(f"/spool/{a.spool_id}", method="PATCH", body={"extra": extra})
    print(f"cleared card_uids on spool {a.spool_id}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    lp = sub.add_parser("lookup"); lp.add_argument("uid"); lp.set_defaults(fn=cmd_lookup)
    ap = sub.add_parser("assign"); ap.add_argument("spool_id", type=int); ap.add_argument("uid")
    ap.add_argument("--force", action="store_true"); ap.set_defaults(fn=cmd_assign)
    cp = sub.add_parser("clear"); cp.add_argument("spool_id", type=int); cp.set_defaults(fn=cmd_clear)
    a = p.parse_args()
    try:
        a.fn(a)
    except urllib.error.URLError as e:
        sys.exit(f"Spoolman unreachable at {BASE}: {e}")


if __name__ == "__main__":
    main()
