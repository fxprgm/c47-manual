#!/usr/bin/env python3
"""The R47 keyboard's legends, from C47's own RefDB47 tables, for the guide's keyboard drawing.

    python3 tools/gen_keyboard.py [KEYBOARD_TSV]   # -> guide/data/keyboard-r47.json

KEYBOARD_TSV defaults to the engine's C47 checkout (build/engine/c47-cg/upstream/docs/refdb47/
data/keyboard.utf8.tsv, there after shots/engine.py). Layout R47f_g: the R47 with its two shift
keys f and g. Only legends painted on the keyboard are kept.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TSV = ROOT / "build/engine/c47-cg/upstream/docs/refdb47/data/keyboard.utf8.tsv"
LAYOUT = "R47f_g"


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else TSV
    lines = [l for l in src.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    keys = {}
    for r in rows:
        if r["layout"] != LAYOUT or r["layer"] not in ("primary", "f_shifted", "g_shifted"):
            continue
        k = keys.setdefault((int(r["row"]), int(r["col"])), {"row": int(r["row"]), "col": int(r["col"])})
        k[{"primary": "key", "f_shifted": "f", "g_shifted": "g"}[r["layer"]]] = \
            r["legend"] if r["painted"] == "1" else ""
    out = []
    for row in sorted({r for r, _ in keys}):
        out.append([keys[(row, c)] for c in sorted(c for r, c in keys if r == row)])
    for k in out[2]:      # the ENTER row: ENTER is two keys wide
        k["wide"] = k["key"] == "ENTER"
    dest = ROOT / "guide/data/keyboard-r47.json"
    dest.write_text(json.dumps({"layout": LAYOUT, "source": "RefDB47 keyboard.utf8.tsv (C47 repository, GPL-3.0)",
                                "rows": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{dest.relative_to(ROOT)}: {sum(map(len, out))} keys in {len(out)} rows")


if __name__ == "__main__":
    main()
