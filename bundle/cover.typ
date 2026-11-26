// Front pages of a bundle: title, what is inside and where it came from, contents.
// bundle.py writes data.json beside this file and compiles it; nothing here is edited per run.
#let d = json("data.json")

#set document(title: d.title, author: "The C47/R47 development team and contributors")
#set page(paper: "a4", margin: (x: 2.2cm, top: 2.4cm, bottom: 2.2cm),
  footer: context align(center, text(8pt, fill: luma(110), counter(page).display("i"))))
#set text(font: ("Libertinus Serif", "New Computer Modern"), size: 10.5pt)
#set par(justify: false)

#v(3.2cm)
#text(30pt, weight: "bold", d.title)
#v(0.2cm)
#text(14pt, fill: luma(70), d.subtitle)
#v(0.8cm)
#line(length: 100%, stroke: 0.6pt + luma(160))
#v(0.4cm)
#text(10pt)[
  *Built:* #d.built \
  #for s in d.sources [ #s \ ]
]
#v(1fr)
#block(width: 100%, inset: 10pt, fill: luma(245), radius: 3pt, text(9pt)[
  #d.about

  Every document in this file is unchanged from its published form, and each is Copyright its
  authors or the C47/R47 development team, under the GNU Free Documentation License, Version 1.3 or any
  later version, with no Invariant Sections, no Front-Cover Texts and no Back-Cover Texts. As the licence's
  section 6 allows for a collection, the single copy of the licence at the end of this file stands for the
  copies the documents refer to. These front pages and the bookmarks are under the same licence.

  Collected by #link("https://github.com/fxprgm/c47-manual")[github.com/fxprgm/c47-manual], which rebuilds
  this file whenever the sources change. Its newest copy:
  #link(d.latest_url)[#raw(d.latest_url)]
])

#pagebreak()
#text(16pt, weight: "bold")[Contents]
#v(0.3cm)
#set text(9.5pt)
#table(
  columns: (auto, 1fr, auto, auto, auto),
  stroke: none,
  inset: (x: 4pt, y: 3.2pt),
  table.header(..([*No.*], [*Title*], [*By*], [*Date*], [*Page*]).map(x => text(fill: luma(60), x))),
  table.hline(stroke: 0.5pt + luma(150)),
  ..d.entries.map(e => (
    e.num,
    e.title,
    text(fill: luma(80), e.by),
    text(fill: luma(80), e.date),
    align(right, str(e.page)),
  )).flatten()
)
