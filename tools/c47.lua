--[==[
The guide's own markup, for Pandoc. tools/build.py runs every chapter through this filter, for
Typst (the PDF) and for HTML (the web pages and the EPUB).

  [ENTER]{.key}  [ASIN]{.f}  [CPX]{.g}  [RECT]{.soft}
      a key, an f-shifted or g-shifted legend, a softkey label. build.py writes them from the
      shorthand [[ENTER]], [[f ASIN]], [[g CPX]], [[s RECT]]; [[f]] and [[g]] are the shift keys.
  ![caption](screen:NAME)
      the screenshot shots/png/NAME.png (shots/scripts/*.keys make them), as a figure.
  1. a numbered list whose items hold screenshots
      a procedure: each step's text on the left, its screen on the right (on a narrow page,
      under it).
  ::: note / ::: tip / ::: caution / ::: example {title="..."}
      a callout box.
  ::: keyboard
      the R47 keyboard, drawn from guide/data/keyboard-r47.json.
]==]

local typst = FORMAT:match("typst") ~= nil
local html = FORMAT:match("html") ~= nil or FORMAT:match("epub") ~= nil

local function tq(s)  -- a Typst string literal
  return '"' .. s:gsub('\\', '\\\\'):gsub('"', '\\"') .. '"'
end

local function esc(s)  -- HTML text
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local KINDS = { key = "key", f = "f", g = "g", soft = "soft", fshift = "fshift", gshift = "gshift" }

function Span(el)
  for _, c in ipairs(el.classes) do
    local kind = KINDS[c]
    if kind then
      local label = pandoc.utils.stringify(el.content)
      if typst then
        return pandoc.RawInline("typst", "#key(" .. tq(label) .. ", kind: " .. tq(kind) .. ")")
      elseif html then
        return pandoc.RawInline("html", '<kbd class="k ' .. kind .. '">' .. esc(label) .. "</kbd>")
      else
        return pandoc.Str("[" .. label .. "]")
      end
    end
  end
end

local function screen_name(img)
  return img.src:match("^screen:(.+)$")
end

local function screen_html(name, alt, cls)
  return '<img class="' .. cls .. '" src="shots/png/' .. name .. '.png" alt="' .. esc(alt) ..
      '" width="400" height="240">'
end

-- A paragraph that is a screenshot alone becomes a figure.
local function screen_figure(name, caption)
  if typst then
    local cap = caption ~= "" and (", caption: [" .. (caption:gsub("([%[%]#\\])", "\\%1")) .. "]") or ""
    return pandoc.RawBlock("typst", "#screen(" .. tq(name) .. cap .. ")")
  elseif html then
    local cap = caption ~= "" and ("<figcaption>" .. esc(caption) .. "</figcaption>") or ""
    return pandoc.RawBlock("html", '<figure class="screen">' .. screen_html(name, caption, "screen") ..
        cap .. "</figure>")
  end
end

function Para(el)
  if #el.content == 1 and el.content[1].t == "Image" then
    local name = screen_name(el.content[1])
    if name then
      return screen_figure(name, pandoc.utils.stringify(el.content[1].caption))
    end
  end
end

Figure = function(el)
  -- Pandoc makes an implicit figure of an image with a caption alone in its paragraph.
  local img
  pandoc.walk_block(el, { Image = function(i) img = img or i end })
  if img and screen_name(img) then
    return screen_figure(screen_name(img), pandoc.utils.stringify(el.caption.long))
  end
end

-- Take the screenshots out of a list item: returns the item's blocks without them, and their names.
local function split_screens(blocks)
  local names, rest = {}, {}
  for _, b in ipairs(blocks) do
    local only_screens = (b.t == "Para" or b.t == "Plain")
    if only_screens then
      local found = {}
      for _, i in ipairs(b.content) do
        if i.t == "Image" and screen_name(i) then
          table.insert(found, screen_name(i))
        elseif not (i.t == "Space" or i.t == "SoftBreak") then
          only_screens = false
        end
      end
      if only_screens and #found > 0 then
        for _, n in ipairs(found) do table.insert(names, n) end
        goto continue
      end
    end
    table.insert(rest, b)
    ::continue::
  end
  return rest, names
end

function OrderedList(el)
  local any = false
  local items = {}
  for _, item in ipairs(el.content) do
    local rest, names = split_screens(item)
    if #names > 0 then any = true end
    table.insert(items, { rest = rest, names = names })
  end
  if not any then return nil end
  local out = {}
  if typst then
    table.insert(out, pandoc.RawBlock("typst", "#steps(start: " .. el.start .. ", ("))
    for _, it in ipairs(items) do
      local names = {}
      for _, n in ipairs(it.names) do table.insert(names, tq(n)) end
      table.insert(out, pandoc.RawBlock("typst", "(screens: (" .. table.concat(names, ", ") ..
          (#names == 1 and "," or "") .. "), body: ["))
      for _, b in ipairs(it.rest) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("typst", "]),"))
    end
    table.insert(out, pandoc.RawBlock("typst", "))"))
  elseif html then
    table.insert(out, pandoc.RawBlock("html", '<ol class="steps" start="' .. el.start .. '">'))
    for _, it in ipairs(items) do
      table.insert(out, pandoc.RawBlock("html", '<li><div class="step-text">'))
      for _, b in ipairs(it.rest) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("html", "</div>"))
      for _, n in ipairs(it.names) do
        table.insert(out, pandoc.RawBlock("html", '<div class="step-screen">' .. screen_html(n, "", "screen") ..
            "</div>"))
      end
      table.insert(out, pandoc.RawBlock("html", "</li>"))
    end
    table.insert(out, pandoc.RawBlock("html", "</ol>"))
  else
    return nil
  end
  return out
end

local CALLOUTS = { note = "Note", tip = "Tip", caution = "Caution", example = "Example" }

function Div(el)
  if el.classes:includes("keyboard") then
    if typst then return pandoc.RawBlock("typst", "#keyboard()") end
    if html then
      return pandoc.RawBlock("html", '<figure class="keyboard"><img src="build/guide/keyboard-r47.svg" ' ..
                'alt="The R47 keyboard"><figcaption>The R47 keyboard: the legend on each key, its ' ..
      '<span style="color:var(--f)">f-shifted</span> and <span style="color:var(--g)">g-shifted</span> ' ..
      'functions above it. The six softkeys under the screen are not drawn.</figcaption></figure>')
    end
    return {}
  end
  for kind, default in pairs(CALLOUTS) do
    if el.classes:includes(kind) then
      local title = el.attributes.title or default
      local blocks = {}
      if typst then
        table.insert(blocks, pandoc.RawBlock("typst", "#callout(" .. tq(kind) .. ", " .. tq(title) .. ")["))
        for _, b in ipairs(el.content) do table.insert(blocks, b) end
        table.insert(blocks, pandoc.RawBlock("typst", "]"))
      elseif html then
        table.insert(blocks, pandoc.RawBlock("html", '<aside class="callout ' .. kind ..
            '"><p class="callout-title">' .. esc(title) .. "</p>"))
        for _, b in ipairs(el.content) do table.insert(blocks, b) end
        table.insert(blocks, pandoc.RawBlock("html", "</aside>"))
      else
        return nil
      end
      return blocks
    end
  end
end

-- Any other format (DOCX, say): a screenshot is an ordinary image.
local function Image(img)
  local name = screen_name(img)
  if name then
    img.src = "shots/png/" .. name .. ".png"
    return img
  end
end

-- Order matters: lists before paragraphs (a list's screens are taken out before Para sees them).
if typst or html then
  return {
    { Span = Span },
    { OrderedList = OrderedList },
    { Figure = Figure, Para = Para, Div = Div },
  }
end
return { { Span = Span, Image = Image, Div = Div } }
