#!/usr/bin/env python3
"""Run the screenshot scripts and store their screens as 1-bit PNGs.

    python3 shots/shoot.py              # every shots/scripts/*.keys -> shots/png/NAME.png
    python3 shots/shoot.py rpn quick    # only the scripts whose name contains one of these
    python3 shots/shoot.py --check      # write nothing; list the screens that would change,
                                        # exit 1 if any (after moving C47_VERSION, say)

A script is a fresh calculator, as it is after a reset, driven one line at a time:

    # a comment
    key 2 ENTER 3 +        press keys, by the R47's legends (below) or c47-cg's names
    key f SIN              f, then SIN: ASIN (the shift keys are keys like the others)
    wait 500               let half a second pass (keys are 160 ms apart already)
    shot rpn-add           the screen now -> shots/png/rpn-add.png
    menu / off             MENU (C47 saves and comes back) / switch off (f EXIT)

Key names: the primary legend of each R47 key (x² √ 1/x yˣ LOG LN STO RCL R↓ DRG f g ENTER x⇄y
CHS EEX ← XEQ 0-9 ÷ × - + ↑ ↓ EXIT . R/S), the softkeys F1..F6, and ASCII spellings of the
symbols (x2 sqrt 1/x y^x Rdn swap bsp / * up down rs). The engine's own names (c47-cg's
src/plat_host.c: X2, SQRT, INV, YX, RDN, SWAP, BSP, DIV, MUL, SUB, ADD, UP, DOWN, DOT, RS,
SHIFT_F, SHIFT_G) work too.

A screen is written only when its pixels change, so git shows exactly the screens a new C47
version changed. Needs the engine (shots/engine.py) and Pillow.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "shots" / "scripts"
PNG = ROOT / "shots" / "png"
ENGINE = ROOT / "build" / "engine" / "c47shot"

KEYS = {
    "x²": "X2", "x2": "X2", "√": "SQRT", "sqrt": "SQRT", "1/x": "INV", "yˣ": "YX", "y^x": "YX",
    "LOG": "LOG", "LN": "LN", "STO": "STO", "RCL": "RCL", "R↓": "RDN", "Rdn": "RDN", "DRG": "DRG",
    "f": "SHIFT_F", "g": "SHIFT_G", "ENTER": "ENTER", "x⇄y": "SWAP", "swap": "SWAP", "CHS": "CHS",
    "EEX": "EEX", "←": "BSP", "bsp": "BSP", "XEQ": "XEQ", "÷": "DIV", "/": "DIV", "×": "MUL",
    "*": "MUL", "-": "SUB", "+": "ADD", "↑": "UP", "up": "UP", "↓": "DOWN", "down": "DOWN",
    "EXIT": "EXIT", ".": "DOT", "R/S": "RS", "rs": "RS",
    **{str(d): str(d) for d in range(10)}, **{f"F{i}": f"F{i}" for i in range(1, 7)},
}
ENGINE_NAMES = {"X2", "SQRT", "INV", "YX", "RDN", "SWAP", "BSP", "DIV", "MUL", "SUB", "ADD", "UP",
                "DOWN", "DOT", "RS", "SHIFT_F", "SHIFT_G"}
BOOT_MS = 3000          # the engine's C47 is ready after this
SETTLE_MS = 300         # before each shot, so the last key's redraw is done


def translate(path: Path, outdir: Path):
    """The manual's script -> the engine's. Returns (engine script, [shot names])."""
    # The power-on screen names the build and its date, which changes with every build: a key
    # (EXIT, which does nothing on a fresh stack) puts it away, and a second one the "No backup data
    # found" note a fresh calculator shows next, before the script starts.
    lines, shots = [f"wait {BOOT_MS}", "key EXIT EXIT", f"wait {SETTLE_MS}"], []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        cmd, *args = line.split()
        if cmd == "key":
            codes = []
            for k in args:
                code = KEYS.get(k) or (k if k in ENGINE_NAMES else None)
                if code is None:
                    raise SystemExit(f"{path.name}:{n}: unknown key '{k}'")
                codes.append(code)
            lines.append("key " + " ".join(codes))
        elif cmd == "wait":
            lines.append(line)
        elif cmd == "shot":
            name = args[0]
            if name in shots:
                raise SystemExit(f"{path.name}:{n}: shot '{name}' twice")
            shots.append(name)
            lines += [f"wait {SETTLE_MS}", f"lcd {outdir / (name + '.pbm')}"]
        elif cmd in ("menu", "off"):
            lines.append(cmd)
        else:
            raise SystemExit(f"{path.name}:{n}: unknown command '{cmd}'")
    return "\n".join(lines) + "\n", shots


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("only", nargs="*")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not ENGINE.exists():
        raise SystemExit(f"no engine at {ENGINE}: run python3 shots/engine.py first")
    PNG.mkdir(parents=True, exist_ok=True)

    scripts = sorted(SCRIPTS.glob("*.keys"))
    if args.only:
        scripts = [s for s in scripts if any(o in s.stem for o in args.only)]
    changed, new, same, seen = [], [], 0, {}
    for script in scripts:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            text, shots = translate(script, tmp)
            for s in shots:
                if s in seen:
                    raise SystemExit(f"shot '{s}' in both {seen[s]} and {script.name}")
                seen[s] = script.name
            (tmp / "run.txt").write_text(text)
            r = subprocess.run([str(ENGINE), "run.txt", "files"], cwd=tmp, capture_output=True, text=True)
            if r.returncode:
                sys.stderr.write(r.stderr[-2000:])
                raise SystemExit(f"{script.name}: the engine stopped with {r.returncode}")
            for s in shots:
                img = Image.open(tmp / f"{s}.pbm").convert("1")
                dest = PNG / f"{s}.png"
                if dest.exists():
                    old = Image.open(dest).convert("1")
                    if old.size == img.size and ImageChops.difference(old, img).getbbox() is None:
                        same += 1
                        continue
                    changed.append(s)
                else:
                    new.append(s)
                if not args.check:
                    img.save(dest, optimize=True)
    print(f"{len(scripts)} scripts: {same} screens unchanged, {len(changed)} changed, {len(new)} new")
    for s in changed:
        print(f"  changed  {s}  ({seen[s]})")
    for s in new:
        print(f"  new      {s}  ({seen[s]})")
    if not args.only and not args.check:
        orphans = sorted(p.stem for p in PNG.glob("*.png") if p.stem not in seen)
        for o in orphans:
            print(f"  no script makes {o}.png any more")
        (PNG / "C47_VERSION").write_text((ROOT / "build" / "engine" / "VERSION").read_text())
    if args.check and (changed or new):
        sys.exit(1)


if __name__ == "__main__":
    main()
