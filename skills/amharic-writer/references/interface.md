# Interface strings

Read this when writing app or site strings.

- Markdown, HTML tags, `{placeholders}`, `%s` and `%d`, variable names, JSON keys and links pass through untranslated. Only their position in the sentence may change.
- Buttons and actions: the polite imperative (**ያስቀምጡ, ይሰርዙ, ይቀጥሉ, ይሞክሩ**), or a short noun where that reads better (**ፍለጋ**, **ቅንብሮች**). Use one pattern across the set.
- "Cancel" and "Delete" need different verbs in Amharic: **ይቅር** (cancel the action) and **ይሰርዙ** (delete).
- Placeholders may move: `Delete {name}?` → `{name}ን መሰረዝ ይፈልጋሉ?`. The object marker **‑ን** attaches to a placeholder that ends up as the object.
- Counts: `{count} files` → `{count} ፋይሎች`. A noun after a number can also stay singular (5 ፋይል); pick one and keep it.
- Error messages: say what happened and what to do, politely and plainly: **መገናኘት አልተቻለም። የኢንተርኔት ግንኙነትዎን ያረጋግጡና እንደገና ይሞክሩ።**
- Fidel glyphs are wider than Latin letters. Flag strings that may overflow a narrow button.
