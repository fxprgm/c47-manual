#!/usr/bin/env python3
"""Collect C47's existing documentation into whole PDFs with bookmarks.

    python3 bundle/bundle.py [--c43 PATH] [--out dist]

Writes, into --out (default dist/):

  C47-R47-Owners-Manual.pdf         the newest Owner's Manual the C47 team published, unchanged
  C47-R47-Application-Notes.pdf     every application note, newest edition of each, in one file
  C47-R47-Manual-and-Notes.pdf      both of the above in one file
  SOURCES.txt                       what went in (manual version, c43 commit, each note's file)
  fingerprint.txt                   one line that changes exactly when the inputs change

The manual comes from the c43 project's package registry on GitLab (package `c47-docs`, the build
the team publishes), the notes from docs/appnotes/ of c43's master (fetched with a sparse clone, PDFs
only, unless --c43 names a checkout). Everything is GFDL 1.3+; the bundles carry a single copy of the
licence at the end, as the licence's section 6 allows for a collection.

Needs Python 3.9+, `pip install -r requirements.txt` (typst, pypdf) and git.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import logging
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import typst
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

C43_GIT = "https://gitlab.com/rpncalculators/c43.git"
C43_API = "https://gitlab.com/api/v4/projects/14055190"
C43_BLOB = "https://gitlab.com/rpncalculators/c43/-/blob/{ref}/docs/appnotes/{name}"
REPO = "fxprgm/c47-manual"
RELEASE_TAG = "bundle"
LATEST = f"https://github.com/{REPO}/releases/download/{RELEASE_TAG}/"

MANUAL = "C47-R47-Owners-Manual.pdf"
NOTES = "C47-R47-Application-Notes.pdf"
BOTH = "C47-R47-Manual-and-Notes.pdf"

# File names: AN0012-2026-04-24-C47-R47-JM-TVM.pdf (number, date, platforms, author initials, title),
# older ones with spaces for hyphens, screen builds with "Crop" on the end. The initials are a known
# set, as in c43's docs/manual/tools/gen-appnote-list.py: an acronym opening a title (EQN, RPN, TVM,
# ELEC) has the same shape as a second author.
PLATFORMS = {"C47", "R47", "DM42", "C43", "WP43"}
INITIALS = {"NUK", "JM", "WGR", "DE", "DL", "DA", "BM", "SF"}
NAME_RE = re.compile(r"^AN(?P<num>\d{4})[-\s]+(?P<date>\d{4}-\d{2}-\d{2})[-\s]+(?P<rest>.+)$")


# Some notes have a damaged cross-reference table that pypdf repairs, with a warning per object.
logging.getLogger("pypdf").setLevel(logging.ERROR)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def latest_manual(work: Path):
    """The newest c47-docs package: (version, path of its full-page PDF)."""
    pkgs = get_json(f"{C43_API}/packages?package_name=c47-docs&order_by=created_at&sort=desc&per_page=5")
    pkg = pkgs[0]
    files = get_json(f"{C43_API}/packages/{pkg['id']}/package_files")
    names = [f["file_name"] for f in files]
    # Two builds per package: the A4 page and a "_Crop" copy cut to the ink for screens. The A4 one.
    pdf = next(n for n in names if n.endswith(".pdf") and "_Crop" not in n)
    dest = work / pdf
    log(f"manual: c47-docs {pkg['version']} ({pdf})")
    download(f"{C43_API}/packages/generic/c47-docs/{pkg['version']}/{pdf}", dest)
    return pkg["version"], dest


def fetch_appnotes(work: Path):
    """Sparse, blobless clone of c43 master holding only docs/appnotes/*.pdf. Returns (dir, commit)."""
    dest = work / "c43"
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                    C43_GIT, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", "--no-cone",
                    "/docs/appnotes/*.pdf"], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "-q"], check=True)
    return dest / "docs" / "appnotes", git_head(dest)


def git_head(repo: Path):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


def parse_note(path: Path):
    stem = re.sub(r"Crop$", "", path.stem)
    m = NAME_RE.match(stem)
    if not m:
        raise SystemExit(f"cannot parse application note name: {path.name}")
    tokens = re.split(r"[-\s]+", m.group("rest"))
    plats, by = [], []
    while tokens and tokens[0] in PLATFORMS:
        plats.append(tokens.pop(0))
    while len(tokens) > 1 and tokens[0] in INITIALS:
        by.append(tokens.pop(0))
    title = " ".join(tokens)
    return {"num": m.group("num"), "date": m.group("date"), "for": " ".join(plats),
            "by": " ".join(by), "title": title, "path": path}


def select_notes(appnote_dir: Path):
    """The newest edition of each note. A note is its number and its title, because one number can
    carry two notes (AN0007: the guide and the specification; AN0032: the template and the character
    set), while a revision can add an author (AN0023), which the title leaves out."""
    newest = {}
    for pdf in sorted(appnote_dir.glob("AN*.pdf")):
        if re.search(r"\bREDLINE\b", pdf.name, re.I):
            continue
        n = parse_note(pdf)
        key = (n["num"], n["title"].lower())
        if key not in newest or n["date"] > newest[key]["date"]:
            newest[key] = n
    return [newest[k] for k in sorted(newest)]


def typst_pdf(template: Path, data: dict | None, out: Path):
    if data is not None:
        (template.parent / "data.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    try:
        typst.compile(str(template), output=str(out), root=str(ROOT))
    finally:
        if data is not None:
            (template.parent / "data.json").unlink(missing_ok=True)
    return out


def build(out_pdf: Path, front: dict, parts, license_pdf: Path, work: Path):
    """front: cover data without entries. parts: [(entry dict, pdf path, bookmark title)].
    Pages are numbered i, ii, ... on the front pages and 1, 2, ... from the first document on, so the
    Owner's Manual's own page numbers hold in the bundle and the contents' numbers are the ones a
    viewer's page box takes. The front's length does not change those numbers; it is compiled once
    more only if the length changed, to put the cover's numbering right."""
    front_pages = 2
    for _ in range(4):
        entries, page = [], 1
        for entry, pdf, _title in parts:
            entries.append({**entry, "page": page})
            page += len(PdfReader(pdf).pages)
        cover = typst_pdf(HERE / "cover.typ", {**front, "entries": entries}, work / "cover.pdf")
        n = len(PdfReader(cover).pages)
        if n == front_pages:
            break
        front_pages = n

    w = PdfWriter()
    w.append(str(cover), outline_item=front["title"])
    for entry, pdf, title in parts:
        # The part's own bookmarks go under one bookmark of its title.
        w.append(str(pdf), outline_item=title, import_outline=True)
    w.append(str(license_pdf), outline_item="GNU Free Documentation License 1.3")
    w.set_page_label(0, front_pages - 1, style="/r")
    w.set_page_label(front_pages, len(w.pages) - 1, style="/D", start=1)
    w.add_metadata({"/Title": front["title"], "/Subject": front["subtitle"],
                    "/Author": "The C47/R47 development team and contributors"})
    w.page_mode = "/UseOutlines"
    with open(out_pdf, "wb") as f:
        w.write(f)
    log(f"wrote {out_pdf.name}: {len(w.pages)} pages, {out_pdf.stat().st_size / 1e6:.1f} MB")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--c43", type=Path, help="an existing c43 checkout to take docs/appnotes from")
    ap.add_argument("--manual", type=Path, help="a manual PDF to use instead of the newest package")
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        if args.manual:
            man_version, man_pdf = args.manual.stem, args.manual
        else:
            man_version, man_pdf = latest_manual(work)
        if args.c43:
            note_dir, commit = args.c43 / "docs" / "appnotes", git_head(args.c43)
        else:
            note_dir, commit = fetch_appnotes(work)
        notes = select_notes(note_dir)
        log(f"{len(notes)} application notes from c43 {commit[:10]}")

        today = dt.date.today().isoformat()
        man_entry = {"num": "", "title": "Owner's Manual", "by": "C47 team", "date": man_version[:10]}
        man_part = (man_entry, man_pdf, "Owner's Manual")
        note_parts = [({"num": f"AN{n['num']}", "title": n["title"], "by": n["by"], "date": n["date"]},
                       n["path"], f"AN{n['num']} {n['title']}") for n in notes]
        sources = [f"Owner's Manual: c47-docs package {man_version} (gitlab.com/rpncalculators/c43)",
                   f"Application notes: c43 master {commit[:10]}, docs/appnotes, newest edition of each"]
        about = ("The C47/R47 documentation is published as many separate files. This is the same "
                 "documentation gathered into one file, with bookmarks for every document and every "
                 "chapter, so it can be read, searched and printed in one piece.")

        license_pdf = typst_pdf(HERE / "license.typ", None, work / "license.pdf")

        shutil.copyfile(man_pdf, args.out / MANUAL)
        log(f"wrote {MANUAL}")
        build(args.out / NOTES,
              {"title": "C47 / R47 Application Notes", "built": today, "sources": sources[1:],
               "subtitle": f"All {len(notes)} application notes in one file", "about": about,
               "latest_url": LATEST + NOTES},
              note_parts, license_pdf, work)
        build(args.out / BOTH,
              {"title": "C47 / R47 Owner's Manual and Application Notes", "built": today,
               "sources": sources, "about": about, "latest_url": LATEST + BOTH,
               "subtitle": f"The Owner's Manual and all {len(notes)} application notes in one file"},
              [man_part] + note_parts, license_pdf, work)

        lines = [f"built {today}", sources[0], sources[1], ""]
        lines += [f"AN{n['num']}  {n['date']}  {n['path'].name}" for n in notes]
        (args.out / "SOURCES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

        h = hashlib.sha256()
        for n in notes:
            h.update(n["path"].name.encode())
            h.update(hashlib.sha256(n["path"].read_bytes()).digest())
        for f in (HERE / "bundle.py", HERE / "cover.typ", HERE / "license.typ"):
            h.update(f.read_bytes())
        fp = f"manual={man_version} notes={h.hexdigest()[:16]}"
        (args.out / "fingerprint.txt").write_text(fp + "\n")
        log(fp)


if __name__ == "__main__":
    main()
