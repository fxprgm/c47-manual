# Fonts

| File | From | Licence |
|---|---|---|
| `C47__StandardFont.ttf` | the C47 repository, `res/fonts/` (gitlab.com/rpncalculators/c43): the calculator's own screen font | GPL-3.0 |
| `C47__ManualFont.ttf`, `C47__KeysFont.ttf` | the same: the faces C47's own manual draws keys and softkeys with | GPL-3.0 |
| `SourceSans3-*.ttf` | [Adobe Source Sans 3](https://github.com/adobe-fonts/source-sans), release 3.052R | SIL OFL 1.1 (`SourceSans3-LICENSE.md`) |

The C47 fonts map some of the calculator's own symbols to unusual code points (`√Ϳ`, `ⅈ`),
as the key legends in `guide/data/keyboard-r47.json` use them: keep them first in the font list.
To refresh them, copy them from the engine's checkout after `shots/engine.py`
(`build/engine/c47-cg/upstream/res/fonts/`).
