#!/usr/bin/env python3
"""Build the C47/R47 User's Guide from guide/*.md.

    python3 tools/build.py                 # every format, into dist/
    python3 tools/build.py pdf html        # only these: pdf, split, html, site, epub, docx
    python3 tools/build.py --list          # the chapters, in order

    pdf    dist/C47-R47-Users-Guide.pdf            the whole guide, A4
    split  dist/chapters/NN-name.pdf               each chapter alone, with the same page numbers
    html   dist/C47-R47-Users-Guide.html           one self-contained page (images and fonts inside)
    site   dist/site/                              a small website, a page per section
    epub   dist/C47-R47-Users-Guide.epub           for e-readers
    docx   dist/C47-R47-Users-Guide.docx           for word processors (plain styling)

Needs Python 3.11+ and `pip install -r requirements.txt` (Typst, Pandoc, Pillow), nothing else:
the screenshots are committed (shots/png), so the engine is only needed to remake them.

Writing: guide/README.md (the markup) and guide/book.toml (the chapter order).
"""
import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pypandoc
import typst

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "guide"
BUILD = ROOT / "build" / "guide"
DIST = ROOT / "dist"
FONTS = [str(ROOT / "fonts")]
FILTER = str(ROOT / "tools" / "c47.lua")
NAME = "C47-R47-Users-Guide"
FORMATS = ["pdf", "split", "html", "site", "epub", "docx"]

# [[ENTER]] a key, [[f ASIN]] / [[g CPX]] a shifted function, [[f]] / [[g]] the shift keys,
# [[s RECT]] a softkey label.
SHORT = re.compile(r"\[\[(?:(f|g|s) )?([^\]\n]+?)\]\]")


def shorthand(md: str) -> str:
    def rep(m):
        kind, label = m.group(1), m.group(2)
        if kind is None and label in ("f", "g"):
            return f"[{label}]{{.{label}shift}}"
        cls = {"f": "f", "g": "g", "s": "soft", None: "key"}[kind]
        label = label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("*", "\\*")
        return f"[{label}]{{.{cls}}}"
    return SHORT.sub(rep, md)


def book():
    with open(GUIDE / "book.toml", "rb") as f:
        b = tomllib.load(f)
    c47 = dict(l.split("=", 1) for l in (ROOT / "C47_VERSION").read_text().splitlines()
               if "=" in l and not l.startswith("#"))
    b["c47"] = c47["c47"].strip()
    return b


def chapter_md(name):
    return shorthand((GUIDE / name).read_text(encoding="utf-8"))


def pandoc(md, to, out=None, extra=()):
    args = ["--lua-filter", FILTER, "--resource-path", str(ROOT), *extra]
    if out:
        return pypandoc.convert_text(md, to, format="markdown", outputfile=str(out), extra_args=args)
    return pypandoc.convert_text(md, to, format="markdown", extra_args=args)


def typst_main(b, body, **opts):
    def lit(v):
        return "true" if v is True else "false" if v is False else str(v) if isinstance(v, int) \
            else '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'
    params = {"title": b["title"], "subtitle": b["subtitle"], "edition": b["edition"], "c47": b["c47"], **opts}
    head = '#import "/guide/template/lib.typ": *\n#show: book.with(' + \
        ", ".join(f"{k.replace('_', '-')}: {lit(v)}" for k, v in params.items()) + ")\n\n"
    return head + body


def compile_typst(src: str, out: Path, fmt="pdf"):
    BUILD.mkdir(parents=True, exist_ok=True)
    main = BUILD / ("main.typ" if fmt == "pdf" else "fig.typ")
    main.write_text(src, encoding="utf-8")
    typst.compile(str(main), output=str(out), root=str(ROOT), font_paths=FONTS, format=fmt)


def build_pdf(b):
    body = pandoc("\n\n".join(chapter_md(c) for c in b["chapters"]), "typst")
    out = DIST / f"{NAME}.pdf"
    compile_typst(typst_main(b, body), out)
    return out


def build_split(b):
    (DIST / "chapters").mkdir(parents=True, exist_ok=True)
    outs = []
    for i, c in enumerate(b["chapters"], 1):
        body = pandoc(chapter_md(c), "typst")
        out = DIST / "chapters" / (Path(c).stem + ".pdf")
        compile_typst(typst_main(b, body, cover=False, contents=False, first_chapter=i), out)
        outs.append(out)
    return outs


def keyboard_svg():
    """The keyboard drawing for the HTML formats: Typst's own, as an SVG (glyphs as outlines)."""
    out = BUILD / "keyboard-r47.svg"
    src = '#import "/guide/template/lib.typ": *\n#set page(width: auto, height: auto, margin: 4pt)\n' \
          '#set text(font: sans)\n#keyboard(caption: none)\n'
    compile_typst(src, out, fmt="svg")
    return out


def css(fonts_url: str) -> Path:
    """guide.css with its font URLs made right for where it will sit (they are written relative
    to guide/template/, as the single-page HTML reads it)."""
    out = BUILD / f"guide-{abs(hash(fonts_url)) % 10**6}.css"
    BUILD.mkdir(parents=True, exist_ok=True)
    out.write_text((GUIDE / "template" / "guide.css").read_text().replace("../../fonts/", fonts_url))
    return out


def html_args(b, css_file=None):
    return ["--css", str(css_file or GUIDE / "template" / "guide.css"), "--number-sections", "--toc", "--toc-depth=2",
            "--metadata", f"title={b['title']}", "--metadata", f"subtitle={b['subtitle']}",
            "--metadata", "lang=en-GB", "--section-divs"]


def build_html(b):
    keyboard_svg()
    out = DIST / f"{NAME}.html"
    md = "\n\n".join(chapter_md(c) for c in b["chapters"])
    pandoc(md, "html5", out, ["--standalone", "--embed-resources", *html_args(b)])
    return out


def build_site(b):
    keyboard_svg()
    out = DIST / "site"
    if out.exists():
        shutil.rmtree(out)
    md = "\n\n".join(chapter_md(c) for c in b["chapters"])
    pandoc(md, "chunkedhtml", out, ["--split-level=2", *html_args(b, Path("guide.css"))])
    # The pages' images (written as raw HTML by tools/c47.lua), stylesheet and fonts beside them.
    shutil.copyfile(css("fonts/"), out / "guide.css")
    shutil.copytree(ROOT / "fonts", out / "fonts", ignore=shutil.ignore_patterns("*.md"))
    shutil.copytree(ROOT / "shots" / "png", out / "shots" / "png", ignore=shutil.ignore_patterns("C47_VERSION"))
    (out / "build" / "guide").mkdir(parents=True)
    shutil.copyfile(BUILD / "keyboard-r47.svg", out / "build" / "guide" / "keyboard-r47.svg")
    return out


def build_epub(b):
    keyboard_svg()
    out = DIST / f"{NAME}.epub"
    md = "\n\n".join(chapter_md(c) for c in b["chapters"])
    pandoc(md, "epub3", out, ["--css", str(css("../fonts/")), "--number-sections",
                              "--toc-depth=2", "--split-level=1",
                              "--metadata", f"title={b['title']}", "--metadata", "lang=en-GB"]
           + [a for f in sorted((ROOT / "fonts").glob("C47__*.ttf")) for a in ("--epub-embed-font", str(f))]
           + [a for f in sorted((ROOT / "fonts").glob("SourceSans3-*.ttf")) for a in ("--epub-embed-font", str(f))])
    return out


def build_docx(b):
    out = DIST / f"{NAME}.docx"
    md = "\n\n".join(chapter_md(c) for c in b["chapters"])
    pandoc(md, "docx", out, ["--number-sections", "--toc", "--metadata", f"title={b['title']}"])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("formats", nargs="*", metavar="FORMAT", help=" ".join(FORMATS))
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    bad = [f for f in args.formats if f not in FORMATS]
    if bad:
        ap.error(f"unknown format(s) {' '.join(bad)}; known: {' '.join(FORMATS)}")
    b = book()
    if args.list:
        for i, c in enumerate(b["chapters"], 1):
            print(f"{i:2}  {c}")
        return
    DIST.mkdir(exist_ok=True)
    for fmt in args.formats or FORMATS:
        res = globals()["build_" + fmt](b)
        for r in res if isinstance(res, list) else [res]:
            size = sum(f.stat().st_size for f in r.rglob("*")) if r.is_dir() else r.stat().st_size
            print(f"{fmt:6} {r.relative_to(ROOT)}  ({size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
