// The look of the guide's PDF. tools/build.py writes build/guide/main.typ: an import of this file,
// `#show: book.with(...)`, and the chapters as Pandoc converted them (tools/c47.lua makes the
// #key, #screen, #steps and #callout calls).

#let ink = rgb("#1a1a1a")
#let accent = rgb("#2b4c7e")        // headings and rules
#let forange = rgb("#e8891c")       // the R47's f legends
#let gblue = rgb("#3d8fd1")         // the R47's g legends
#let paper = rgb("#f4f6f8")
#let calc-font = ("C47__StandardFont", "C47__ManualFont", "Source Sans 3", "New Computer Modern Math", "DejaVu Sans")
#let sans = ("Source Sans 3", "C47__StandardFont", "New Computer Modern Math", "DejaVu Sans")

// ---- keys ------------------------------------------------------------------------------------
// kind: "key" a key by its primary legend; "f" / "g" a function by its shifted legend;
// "fshift" / "gshift" the shift keys themselves; "soft" a softkey label as the screen shows it.
#let key(label, kind: "key") = {
  let (fill, fg, stroke, font) = if kind == "f" {
    (forange.lighten(75%), ink, 0.6pt + forange, calc-font)
  } else if kind == "g" {
    (gblue.lighten(78%), ink, 0.6pt + gblue, calc-font)
  } else if kind == "fshift" {
    (forange, ink, none, calc-font)
  } else if kind == "gshift" {
    (gblue, white, none, calc-font)
  } else if kind == "soft" {
    (white, ink, 0.6pt + ink, calc-font)
  } else {
    (ink.lighten(12%), white, none, calc-font)
  }
  box(baseline: 22%, inset: (x: 3.2pt, y: 1.6pt), radius: if kind == "soft" { 0pt } else { 2.2pt },
    fill: fill, stroke: stroke,
    text(font: font, size: 0.86em, fill: fg, weight: "regular", label))
}

// ---- screens -----------------------------------------------------------------------------------
// The calculator's 400x240 screen at 1:1 pixel aspect, pixels kept square and sharp.
#let screen-image(name, width: 6.2cm) = box(
  stroke: 0.7pt + luma(150), radius: 2pt, inset: 3pt, fill: white,
  image("/shots/png/" + name + ".png", width: width, scaling: "pixelated"))

#let screen(name, caption: none, width: 7.2cm) = figure(
  screen-image(name, width: width), caption: caption, kind: "screen", supplement: [Screen])

// A procedure: numbered steps, each step's screen(s) to its right.
#let steps(start: 1, items) = {
  let n = start
  for it in items {
    block(breakable: false, above: 0.9em, below: 0.9em,
      grid(columns: (1.3em, 1fr, auto), column-gutter: 0.7em,
        text(weight: "bold", fill: accent, str(n) + "."),
        it.body,
        if it.screens.len() > 0 { stack(spacing: 4pt, ..it.screens.map(s => screen-image(s, width: 5.4cm))) }
      ))
    n += 1
  }
}

// ---- callouts ----------------------------------------------------------------------------------
#let callout(kind, title, body) = {
  let c = (note: accent, tip: rgb("#2e7d4f"), caution: rgb("#b3261e"), example: rgb("#6a4c93")).at(kind)
  block(width: 100%, breakable: true, above: 1em, below: 1em, inset: (left: 10pt, rest: 8pt),
    fill: c.lighten(93%), stroke: (left: 2.5pt + c),
    [#text(font: sans, weight: "bold", fill: c, title) \ #body])
}

// ---- the keyboard ------------------------------------------------------------------------------
#let keyboard(width: 13cm, caption: auto) = {
  let kb = json("/guide/data/keyboard-r47.json")
  let u = width / 6.6                    // a key's pitch in the six-key rows
  let legend(s, c) = text(font: calc-font, size: 6.6pt, fill: c, s)
  let cap(k, w) = box(width: w, {
    align(center, box(height: 9pt, legend(k.f, forange) + h(0.35em) + legend(k.g, gblue)))
    v(-3pt)
    align(center, box(width: w - 6pt, height: 0.42 * u, radius: 3pt,
      fill: if k.key == "f" { forange } else if k.key == "g" { gblue } else { ink.lighten(12%) },
      align(center + horizon, text(font: calc-font, size: 9pt,
        fill: if k.key == "f" { ink } else { white }, k.key))))
  })
  let rows = kb.rows.map(r => {
    // Six units to a row: six keys, or five with the double-width ENTER; the five-key rows
    // below are spread over the same width.
    let units = r.map(k => if k.at("wide", default: false) { 2 } else { 1 }).sum()
    let pitch = if units == 6 { u } else { width / 5.4 }
    let keys = r.map(k => cap(k, if k.at("wide", default: false) { 2 * pitch } else { pitch }))
    align(center, stack(dir: ltr, ..keys))
  })
  let board = block(fill: luma(235), radius: 6pt, inset: (x: 8pt, y: 10pt), width: width + 16pt,
    stack(spacing: 7pt, ..rows))
  if caption == none { return board }
  figure(board,
    caption: [The R47 keyboard: the legend on each key, its #text(fill: forange.darken(15%))[f-shifted]
      and #text(fill: gblue.darken(15%))[g-shifted] functions above it. The six softkeys under the
      screen are not drawn.],
    kind: "screen", supplement: [Figure])
}

// ---- the book ----------------------------------------------------------------------------------
#let chapter-title = state("chapter-title", none)

#let book(title: none, subtitle: none, edition: none, c47: none, cover: true, contents: true,
  first-chapter: 1, body) = {
  set document(title: title, author: "fxprgm/c47-manual contributors")
  set text(font: sans, size: 10.5pt, fill: ink, lang: "en", region: "gb")
  set par(justify: true, leading: 0.62em, spacing: 0.9em)
  show raw: set text(font: ("DejaVu Sans Mono", "C47__StandardFont"), size: 0.92em)
  set heading(numbering: "1.1")
  set figure(gap: 6pt)
  show figure.caption: set text(size: 9pt, fill: luma(70))
  set list(indent: 0.4em)
  set enum(indent: 0.4em)
  set table(stroke: 0.5pt + luma(170), inset: 5pt)
  show table.cell: set align(left)
  show table.cell.where(y: 0): set text(weight: "bold")
  show link: set text(fill: accent)

  // Pages are numbered by chapter, "2-5", so a chapter printed or bound alone keeps its numbers.
  set page(paper: "a4", margin: (inside: 2.3cm, outside: 2cm, top: 2.3cm, bottom: 2.2cm),
    header: context {
      let t = chapter-title.get()
      // Not on a chapter's first page (its heading is there; the title state still has the
      // previous chapter's name when the header is laid out).
      let opener = query(heading.where(level: 1)).any(h => h.location().page() == here().page())
      if t != none and not opener {
        set text(size: 8.5pt, fill: luma(100))
        h(1fr); t
        v(-6pt); line(length: 100%, stroke: 0.4pt + luma(190))
      }
    },
    footer: context {
      set text(size: 8.5pt, fill: luma(90))
      let ch = counter(heading).get().first()
      align(center, if ch > 0 { str(ch) + "-" + str(counter(page).get().first()) } else { counter(page).display("i") })
    })

  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    counter(page).update(1)
    chapter-title.update(it.body)
    v(1.2cm)
    grid(columns: (auto, 1fr), column-gutter: 14pt, align: horizon,
      box(fill: accent, inset: (x: 12pt, y: 8pt), radius: 3pt,
        text(28pt, weight: "bold", fill: white, counter(heading).display("1"))),
      text(24pt, weight: "bold", fill: accent, it.body))
    v(0.4cm)
    line(length: 100%, stroke: 1pt + accent)
    // What is in this chapter: its sections.
    context {
      let here-ch = counter(heading).get().first()
      let secs = query(heading.where(level: 2)).filter(h =>
        counter(heading).at(h.location()).first() == here-ch)
      if secs.len() > 0 {
        block(above: 0.5cm, below: 0.8cm, inset: (left: 4pt), {
          set text(size: 9.5pt)
          for s in secs {
            link(s.location(), [#numbering("1.1", ..counter(heading).at(s.location())) #h(0.6em) #s.body])
            h(1fr)
            text(fill: luma(110), str(here-ch) + "-" + str(counter(page).at(s.location()).first()))
            linebreak()
          }
        })
      }
    }
  }
  show heading.where(level: 2): it => block(above: 1.6em, below: 0.8em, breakable: false, {
    text(13.5pt, weight: "bold", fill: accent, [#counter(heading).display("1.1") #h(0.5em) #it.body])
    v(-7pt)
    line(length: 100%, stroke: 0.6pt + accent.lighten(40%))
  })
  show heading.where(level: 3): it => block(above: 1.3em, below: 0.6em,
    text(11pt, weight: "bold", it.body))

  // A part printed alone (build.py --split) starts at its own chapter number.
  counter(heading).update(first-chapter - 1)

  // Title page
  if cover { page(header: none, footer: none, {
    v(4cm)
    text(32pt, weight: "bold", fill: accent, title)
    v(0.3cm)
    text(15pt, fill: luma(60), subtitle)
    v(1fr)
    set text(9pt, fill: luma(80))
    [#edition \ Describes C47 #raw(c47.slice(0, 10)), whose screens it shows.]
    v(0.4cm)
    block(width: 100%, inset: 8pt, fill: paper, radius: 3pt, text(8.5pt)[
      Copyright © 2026 the fxprgm/c47-manual contributors. Permission is granted to copy, distribute
      and/or modify this document under the terms of the GNU Free Documentation License, Version 1.3
      or any later version published by the Free Software Foundation; with no Invariant Sections, no
      Front-Cover Texts, and no Back-Cover Texts. A copy of the licence is in the file LICENSE at
      #link("https://github.com/fxprgm/c47-manual")[github.com/fxprgm/c47-manual]. The screens are
      C47's own, made by its firmware (GPL-3.0); the key legends come from its RefDB47 tables.
    ])
  }) }
  // Contents, with the chapter-page numbers the pages carry.
  if contents {
    page(header: none, footer: none, {
      text(20pt, weight: "bold", fill: accent)[Contents]
      v(0.5cm)
      context for hd in query(heading.where(level: 1).or(heading.where(level: 2))) {
        let loc = hd.location()
        let nums = counter(heading).at(loc)
        // A chapter's heading sits just before its page counter goes back to 1.
        let pg = str(nums.first()) + "-" + if hd.level == 1 { "1" } else { str(counter(page).at(loc).first()) }
        if hd.level == 1 {
          v(8pt)
          link(loc, text(weight: "bold", [#nums.first() #h(0.8em) #hd.body]))
          h(1fr); text(weight: "bold", pg)
        } else {
          h(1.6em)
          link(loc, [#numbering("1.1", ..nums) #h(0.6em) #hd.body])
          box(width: 1fr, repeat(text(fill: luma(170))[.#h(3pt)]))
          text(fill: luma(90), pg)
        }
        linebreak()
      }
    })
  }
  body
}
