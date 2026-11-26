#!/usr/bin/env python3
"""Build the screenshot engine: C47, headless, at the commit in C47_VERSION.

    python3 shots/engine.py [--c47cg PATH]      # -> build/engine/c47shot

The engine is fxprgm/c47-cg's PC test build (C47 with a DMCP layer, driven by a script on a
simulated clock, so a run gives the same pixels every time), built *without* c47-cg's CG50 layout
patch, so the screen is the R47's own 400x240. Its `lcd FILE` command writes that screen as a 1-bit
PBM. shots/shoot.py runs it.

--c47cg PATH takes a local c47-cg working tree (uncommitted changes included) instead of cloning
the ref in C47_VERSION.

Needs, as c47-cg does for its PC build (its tools/setup_env.py installs them on Debian/Ubuntu):
gcc, git, meson, ninja, pkg-config, freetype2, gmp, gtk+-3.0 dev headers and xlsxio_xlsx2csv.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "build" / "engine"
SRC = WORK / "c47-cg"
OUT = WORK / "c47shot"
C47CG_GIT = "https://github.com/fxprgm/c47-cg.git"


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def pins():
    vals = {}
    for line in (ROOT / "C47_VERSION").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip()
    return vals


def get_c47cg(local, ref):
    if local:
        if SRC.exists():
            shutil.rmtree(SRC)
        shutil.copytree(local, SRC, ignore=shutil.ignore_patterns(".git", "build", "upstream"))
        return
    if not (SRC / ".git").exists():
        if SRC.exists():
            shutil.rmtree(SRC)
        run(["git", "clone", "-q", C47CG_GIT, SRC])
    run(["git", "-C", SRC, "fetch", "-q", "origin", ref])
    run(["git", "-C", SRC, "checkout", "-q", "--force", "FETCH_HEAD"])
    run(["git", "-C", SRC, "clean", "-q", "-fdx", "-e", "upstream", "-e", "build"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--c47cg", type=Path, help="a local fxprgm/c47-cg working tree")
    args = ap.parse_args()
    p = pins()
    WORK.mkdir(parents=True, exist_ok=True)
    get_c47cg(args.c47cg, p["c47cg"])

    # The R47's screen, not the CG50's: drop the 396x224 layout patch. The others stay (byte
    # order, which is neutral on a little-endian PC; the test suite's buffer size).
    for patch in (SRC / "patches").glob("*layout*.patch"):
        print(f"without {patch.name}")
        patch.unlink()
    up = (SRC / "UPSTREAM").read_text().splitlines()
    (SRC / "UPSTREAM").write_text("\n".join(
        f"commit={p['c47']}" if l.startswith("commit=") else l for l in up) + "\n")

    run([sys.executable, "tools/sync_upstream.py"], cwd=SRC)
    run([sys.executable, "tools/build_host.py"], cwd=SRC)
    shutil.copyfile(SRC / "build" / "c47cg_host", OUT)
    os.chmod(OUT, 0o755)
    (WORK / "VERSION").write_text(f"c47={p['c47']}\nc47cg={p['c47cg']}\n")
    print(f"engine: {OUT}")


if __name__ == "__main__":
    main()
