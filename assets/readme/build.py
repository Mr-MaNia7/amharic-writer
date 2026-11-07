#!/usr/bin/env python3
"""Build the README's animated SVGs: hero.svg, demo.svg and compare.svg.

    python3 assets/readme/build.py [FONT_DIR]

FONT_DIR must hold NotoSerifEthiopic-Regular.ttf, NotoSerifEthiopic-SemiBold.ttf,
NotoSansEthiopic.woff2 (variable), Literata-Regular.ttf, Literata-SemiBold.ttf and
SourceCodePro-Regular.ttf. All are SIL Open Font License fonts. Each SVG embeds a
subset holding only the characters it uses, because GitHub shows SVGs as images,
and images can't load web fonts.

Needs fonttools and brotli (pip install fonttools brotli).
"""
import base64
import io
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parent
FONT_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else OUT / "fonts")

FONTS = {
    "eth-serif": ("NotoSerifEthiopic-Regular.ttf", None),
    "eth-serif-sb": ("NotoSerifEthiopic-SemiBold.ttf", None),
    "eth-sans": ("NotoSansEthiopic.woff2", 400),
    "lat-serif": ("Literata-Regular.ttf", None),
    "lat-serif-sb": ("Literata-SemiBold.ttf", None),
    "mono": ("SourceCodePro-Regular.ttf", None),
}
# Font stacks: the Ethiopic face first, the Latin face for everything it lacks.
STACK = {
    "serif": ("eth-serif", "lat-serif"),
    "serif-sb": ("eth-serif-sb", "lat-serif-sb"),
    "mono": ("eth-sans", "mono"),
}

INK, PAPER, RED, MUTED, RULE = "#1F1B16", "#F6F1E7", "#A8231B", "#6E6355", "#E2D8C6"
TERM, TERM_TEXT, TERM_MUTED = "#1E1A16", "#EFE7D8", "#9A8F80"

_loaded = {}


def font(key):
    if key not in _loaded:
        name, wght = FONTS[key]
        f = TTFont(FONT_DIR / name)
        if wght and "fvar" in f:
            f = instancer.instantiateVariableFont(f, {"wght": wght})
        _loaded[key] = f
    return _loaded[key]


def face_for(stack, ch):
    for key in STACK[stack]:
        if ord(ch) in font(key).getBestCmap():
            return key
    raise SystemExit(f"no font in {stack} has {ch!r} (U+{ord(ch):04X})")


def width(text, stack, size, spacing=0.0):
    total = 0.0
    for ch in text:
        f = font(face_for(stack, ch))
        glyph = f.getBestCmap()[ord(ch)]
        total += f["hmtx"][glyph][0] / f["head"].unitsPerEm * size + spacing
    return total


def font_css(text):
    """@font-face rules embedding a subset of each font for the characters in text."""
    chars = set(text) | {" "}
    rules = []
    for stack, keys in STACK.items():
        for key in keys:
            have = font(key).getBestCmap()
            used = "".join(sorted(c for c in chars if ord(c) in have))
            if not used.strip():
                continue
            f = TTFont(io.BytesIO(_font_bytes(key)))
            opts = ftsubset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["*"]
            opts.name_IDs = []
            opts.notdef_outline = True
            sub = ftsubset.Subsetter(opts)
            sub.populate(text=used)
            sub.subset(f)
            buf = io.BytesIO()
            f.flavor = "woff2"
            f.save(buf)
            data = base64.b64encode(buf.getvalue()).decode()
            rules.append(f"@font-face{{font-family:'{key}';src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(dict.fromkeys(rules))


def _font_bytes(key):
    buf = io.BytesIO()
    f = font(key)
    f.flavor = None
    f.save(buf)
    return buf.getvalue()


def family(stack):
    return ",".join(f"'{k}'" for k in STACK[stack])


def text_el(x, y, s, stack, size, fill, extra="", spacing=0.0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family(stack)}" font-size="{size}" fill="{fill}"{ls}{extra}>{escape(s)}</text>'


def pct(t, total):
    return f"{max(0.0, min(100.0, t / total * 100)):.3f}%"


def svg_doc(w, h, label, css, body, all_text):
    style = (
        font_css(all_text)
        + css
        + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title><style>{style}</style>{body}</svg>\n"
    )


# ---------------------------------------------------------------- hero.svg

def hero():
    W, H = 1200, 420
    body, css, texts = [], [], []
    body.append(f'<rect width="{W}" height="{H}" rx="20" fill="{PAPER}"/>')
    body.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{RULE}"/>')

    # A Fidel chart (seven orders of eight consonants) that reads itself cell by cell.
    bases = [0x1200, 0x1208, 0x1210, 0x1218, 0x1220, 0x1228, 0x1230, 0x1238]
    cell, x0, y0 = 62, 742, 78
    loop = 16.0
    css.append(
        f"@keyframes read{{0%{{fill:{RULE}}}1.2%{{fill:{RED}}}5%{{fill:{RULE}}}100%{{fill:{RULE}}}}}"
        f".c{{fill:{RULE};animation:read {loop}s linear infinite}}"
    )
    i = 0
    for r, base in enumerate(bases):
        for o in range(7):
            ch = chr(base + o)
            texts.append(ch)
            x, y = x0 + o * cell, y0 + r * 40
            body.append(
                f'<text class="c" style="animation-delay:{i * 0.25:.2f}s" x="{x}" y="{y + 18}" text-anchor="middle" '
                f'font-family="{family("serif")}" font-size="30">{ch}</text>'
            )
            i += 1
    body.append(
        '<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="%s" stop-opacity="1"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs>' % (PAPER, PAPER)
    )
    body.append(f'<rect x="690" y="40" width="90" height="{H-80}" fill="url(#fade)"/>')

    # Left: label, title, tagline.
    x = 72
    label = "AGENT SKILL"
    body.append(text_el(x, 104, label, "serif-sb", 15, RED, spacing=3))
    lw = width(label, "serif-sb", 15, 3)
    body.append(text_el(x + lw + 10, 104, "· አማርኛ", "serif-sb", 15, MUTED))
    body.append(text_el(x, 176, "amharic-writer", "serif-sb", 66, INK))
    body.append(text_el(x, 222, "Amharic that reads as Amharic,", "serif", 25, "#4A4238"))
    body.append(text_el(x, 254, "not as translated English.", "serif", 25, "#4A4238"))
    texts += [label, "· አማርኛ", "amharic-writer", "Amharic that reads as Amharic,", "not as translated English."]

    # English phrases, each followed by its Amharic, written out left to right.
    pairs = [
        ("Call the office.", "ወደ ቢሮ ይደውሉ", "።"),
        ("Thank you for your patience.", "ስለ ትዕግስትዎ እናመሰግናለን", "።"),
        ("Monday, 9:00 a.m.", "ሰኞ ከጠዋቱ 3:00 ሰዓት", ""),
    ]
    slot = 5.0
    total = slot * len(pairs)
    css.append(
        f"@keyframes slot{{0%{{opacity:0}}3%{{opacity:1}}31%{{opacity:1}}33.3%{{opacity:0}}100%{{opacity:0}}}}"
        f".p{{opacity:0;animation:slot {total}s linear infinite}}.p0{{opacity:1}}"
        f"@keyframes wipe{{0%{{transform:scaleX(1)}}5%{{transform:scaleX(1)}}17%{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}}}"
        f".w{{transform:scaleX(0);transform-box:fill-box;transform-origin:right;animation:wipe {total}s linear infinite}}"
    )
    body.append(f'<line x1="{x}" y1="292" x2="{x + 560}" y2="292" stroke="{RULE}"/>')
    for k, (en, am, stop) in enumerate(pairs):
        d = f"animation-delay:{k * slot:.1f}s"
        g = [f'<g class="p p{k}" style="{d}">']
        g.append(text_el(x, 326, en, "mono", 18, MUTED))
        ew = width(en, "mono", 18)
        ax = x + ew + 16
        g.append(f'<path d="M{ax:.1f} 320h22m-7-6 7 6-7 6" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
        g.append(
            f'<text x="{x}" y="378" font-family="{family("serif-sb")}" font-size="38" fill="{INK}">{escape(am)}'
            + (f'<tspan fill="{RED}">{stop}</tspan>' if stop else "")
            + "</text>"
        )
        aw = width(am + stop, "serif-sb", 38)
        g.append(f'<rect class="w" style="{d}" x="{x - 2}" y="340" width="{aw + 8:.1f}" height="52" fill="{PAPER}"/>')
        g.append("</g>")
        body += g
        texts += [en, am, stop]

    return svg_doc(
        W, H,
        "amharic-writer: an agent skill for Amharic that reads as Amharic, not as translated English.",
        "".join(css), "".join(body), "".join(texts),
    )


# ---------------------------------------------------------------- demo.svg

def demo():
    W, H = 1200, 660
    T = 17.0
    END = 15.6
    body, css, texts = [], [], []
    body.append(f'<rect width="{W}" height="{H}" rx="20" fill="{PAPER}"/>')
    body.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{RULE}"/>')
    body.append(f'<rect x="40" y="36" width="1120" height="588" rx="14" fill="{TERM}"/>')
    for i in range(3):
        body.append(f'<circle cx="{68 + i * 20}" cy="62" r="5.5" fill="#3A332C"/>')
    body.append(text_el(600, 67, "claude", "mono", 15, TERM_MUTED, ' text-anchor="middle"'))
    body.append(f'<line x1="40" y1="88" x2="1160" y2="88" stroke="#2E2822"/>')
    texts.append("claude")

    n = [0]

    def appear(t):
        n[0] += 1
        name = f"a{n[0]}"
        css.append(
            f"@keyframes {name}{{0%{{opacity:0}}{pct(t, T)}{{opacity:0}}{pct(t + 0.35, T)}{{opacity:1}}"
            f"{pct(END, T)}{{opacity:1}}{pct(END + 0.5, T)}{{opacity:0}}100%{{opacity:0}}}}"
            f".{name}{{animation:{name} {T}s linear infinite}}"
        )
        return name

    def typed(t0, t1, steps):
        n[0] += 1
        name = f"t{n[0]}"
        css.append(
            f"@keyframes {name}{{0%{{transform:scaleX(1)}}{pct(t0, T)}{{transform:scaleX(1);animation-timing-function:steps({steps},end)}}"
            f"{pct(t1, T)}{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}}}"
            f".{name}{{transform:scaleX(0);transform-box:fill-box;transform-origin:right;animation:{name} {T}s linear infinite}}"
        )
        return name

    x, y = 76, 132
    # Prompt, typed.
    prompt = [
        "translate this for our community center's telegram channel.",
        "members are mostly in addis, a lot of older folks too.",
    ]
    t = 0.4
    fade = appear(0.0)
    for i, line in enumerate(prompt):
        yy = y + i * 32
        dur = len(line) * 0.028
        g = f'<g class="{fade}">'
        if i == 0:
            g += text_el(x, yy, ">", "mono", 19, RED)
        g += text_el(x + 24, yy, line, "mono", 19, TERM_TEXT)
        lw = width(line, "mono", 19)
        g += f'<rect class="{typed(t, t + dur, len(line))}" x="{x + 22}" y="{yy - 20}" width="{lw + 6:.1f}" height="28" fill="{TERM}"/>'
        g += "</g>"
        body.append(g)
        texts.append(line)
        t += dur + 0.15
    texts.append(">")

    # Tool steps.
    y = 222
    steps = [
        ("Skill", "amharic-writer", True),
        ("Read", "references/dates-numbers.md", False),
        ("Bash", "2025-11-07", False),
        ("Write", "notice-am.md", False),
    ]
    t += 0.5
    for i, (tool, arg, lead) in enumerate(steps):
        yy = y + i * 32
        cls = appear(t)
        dot = RED if lead else TERM_MUTED
        g = f'<g class="{cls}"><circle cx="{x + 6}" cy="{yy - 6}" r="5" fill="{dot}"/>'
        g += text_el(x + 24, yy, tool, "mono", 18, TERM_TEXT)
        tw = width(tool + "  ", "mono", 18)
        g += text_el(x + 24 + tw, yy, arg, "mono", 18, TERM_MUTED)
        if tool == "Bash":
            aw = width(arg + " ", "mono", 18)
            ax = x + 24 + tw + aw
            g += f'<path d="M{ax:.1f} {yy - 6}h20m-6-5 6 5-6 5" fill="none" stroke="{TERM_MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
            g += text_el(ax + 30, yy, "ዓርብ፣ ጥቅምት 28 2018", "mono", 18, TERM_TEXT)
            texts.append("ዓርብ፣ ጥቅምት 28 2018")
        g += "</g>"
        body.append(g)
        texts += [tool, arg]
        t += 0.6

    # The notice the run wrote.
    out = [
        "ውድ አባሎቻችን፣",
        "ቢሮአችን ለጥገና ስራ ዓርብ ጥቅምት 28 ቀን 2018 ዓ.ም. (እ.ኤ.አ. ኖቬምበር 7 ቀን 2025) ዝግ ይሆናል።",
        "አገልግሎት የሚጀምረው ሰኞ ከጠዋቱ 3:00 ሰዓት (9:00 a.m.) ነው።",
        "አስቸኳይ ጉዳይ ካለዎት ወደ 0911 234 567 ይደውሉ።",
        "ስለ ትዕግስትዎ እናመሰግናለን።",
    ]
    y = 372
    t += 0.3
    bar = appear(t)
    body.append(f'<rect class="{bar}" x="{x}" y="{y - 24}" width="3" height="{len(out) * 36 - 6}" rx="1.5" fill="{RED}"/>')
    for i, line in enumerate(out):
        cls = appear(t + i * 0.35)
        yy = y + i * 36
        body.append(f'<g class="{cls}">' + text_el(x + 24, yy, line, "mono", 21, TERM_TEXT) + "</g>")
        texts.append(line)
        if width(line, "mono", 21) > 1040:
            raise SystemExit(f"demo line too wide: {line}")
    t += len(out) * 0.35 + 0.4

    # What the checks confirmed.
    chips = ["Ethiopian date, computed", "Ethiopian clock", "Polite to older readers"]
    cx, cy = x, 576
    for i, c in enumerate(chips):
        cls = appear(t + i * 0.3)
        cw = width(c, "mono", 16) + 52
        g = f'<g class="{cls}"><rect x="{cx}" y="{cy - 22}" width="{cw:.1f}" height="34" rx="17" fill="none" stroke="#4A4036"/>'
        g += f'<path d="M{cx + 16} {cy - 5}l5 5 9-10" fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        g += text_el(cx + 38, cy, c, "mono", 16, TERM_TEXT) + "</g>"
        body.append(g)
        texts.append(c)
        cx += cw + 14

    return svg_doc(
        W, H,
        "A Claude Code session: a request to translate a closure notice for older members in Addis Ababa. The skill loads, "
        "converts the date to the Ethiopian calendar, and writes a polite Amharic notice with the Ethiopian date and clock.",
        "".join(css), "".join(body), "".join(texts),
    )


# ---------------------------------------------------------------- compare.svg

def layout(segments, stack, size, maxw):
    """Wrap styled segments into lines of (x, text, style) runs."""
    words = []
    for s, style in segments:
        parts = s.split(" ")
        for j, p in enumerate(parts):
            if p:
                words.append([p, style, j < len(parts) - 1])
            elif j < len(parts) - 1 and words:
                words[-1][2] = True
    lines, cur, cx = [], [], 0.0
    sp = width(" ", stack, size)
    for w, style, space_after in words:
        ww = width(w, stack, size)
        if cur and cx + ww > maxw:
            lines.append(cur)
            cur, cx = [], 0.0
        cur.append((cx, w, style))
        cx += ww + (sp if space_after else 0)
    if cur:
        lines.append(cur)
    return lines


def compare():
    W, H = 1200, 470
    slides = [
        (
            "Website notice",
            "“For more information, call the office.”",
            [("ለተጨማሪ መረጃ እባክዎ ", "n"), ("ቢሮውን", "bad"), (" ይደውሉ።", "n")],
            [("ለበለጠ መረጃ ", "n"), ("ወደ ቢሮ", "good"), (" ይደውሉ።", "n")],
            "On a public website the reader doesn’t know which office, so no -ው.",
        ),
        (
            "Health newsletter",
            "“The doctor told the patients to drink more water.”",
            [("ዶክተሩ ", "n"), ("ታካሚዎቹ", "bad"), (" ብዙ ውሃ እንዲጠጡ ነገራቸው።", "n")],
            [("ሐኪሙ ", "n"), ("ታካሚዎቹን", "good"), (" ተጨማሪ ውሃ እንዲጠጡ ነገራቸው።", "n")],
            "The patients are the object, so they take -ን. Without it, they read as a second subject.",
        ),
        (
            "Event flyer",
            "quoting Article 25 of the Constitution",
            [("አንቀጽ 25 እንዲህ ይላል፦ ", "n"), ("\"ሰዎች ሁሉ በሕግ ፊት እኩል ናቸው፤ ያለ ምንም ልዩነትም በሕግ እኩል ጥበቃ ይደረግላቸዋል።\"", "bad")],
            [("አንቀጽ 25 እንዲህ ይላል፦ ", "n"), ("[እዚህ ላይ የታተመ የአማርኛ ትርጉም ይገባል።]", "good")],
            "Without the skill, the model writes its own version of the law. With it, it leaves a place for the published text.",
        ),
    ]
    slot = 7.0
    total = slot * len(slides)
    a = 2.5 / total * 100  # fade length as a share of the loop
    span = 100 / len(slides)
    css = [
        f"@keyframes slot{{0%{{opacity:0}}{a:.2f}%{{opacity:1}}{span - a:.2f}%{{opacity:1}}{span:.2f}%{{opacity:0}}100%{{opacity:0}}}}"
        f".s{{opacity:0;animation:slot {total}s linear infinite}}.s0{{opacity:1}}"
        f"@keyframes dot{{0%{{fill:{RED}}}{span - 0.01:.2f}%{{fill:{RED}}}{span:.2f}%{{fill:{RULE}}}100%{{fill:{RULE}}}}}"
        f".d{{fill:{RULE};animation:dot {total}s step-end infinite}}.d0{{fill:{RED}}}"
    ]
    body, texts = [], []
    body.append(f'<rect width="{W}" height="{H}" rx="20" fill="{PAPER}"/>')
    body.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{RULE}"/>')

    colx = [56, 616]
    cw, top, ch = 528, 120, 236
    body.append(text_el(colx[0], 106, "WITHOUT THE SKILL", "serif-sb", 14, MUTED, spacing=2.5))
    body.append(text_el(colx[1], 106, "WITH THE SKILL", "serif-sb", 14, RED, spacing=2.5))
    body.append(f'<rect x="{colx[0]}" y="{top}" width="{cw}" height="{ch}" rx="12" fill="#EEE6D7"/>')
    body.append(f'<rect x="{colx[1]}" y="{top}" width="{cw}" height="{ch}" rx="12" fill="#FCFAF5" stroke="{RULE}"/>')
    body.append(f'<rect x="{colx[1]}" y="{top + 18}" width="4" height="{ch - 36}" rx="2" fill="{RED}"/>')
    texts += ["WITHOUT THE SKILL", "WITH THE SKILL"]

    size, lh, pad = 27, 46, 32
    for k, (case, en, bad, good, why) in enumerate(slides):
        d = f"animation-delay:{k * slot:.1f}s"
        g = [f'<g class="s s{k}" style="{d}">']
        g.append(text_el(56, 66, case, "serif-sb", 24, INK))
        g.append(text_el(56 + width(case + "  ", "serif-sb", 24), 66, en, "serif", 22, "#4A4238"))
        texts += [case, en]
        for col, segs in ((0, bad), (1, good)):
            lines = layout(segs, "serif", size, cw - 2 * pad)
            y0 = top + pad + 26 + (ch - 2 * pad - 26 - lh * (len(lines) - 1)) / 2 - 18
            for li, line in enumerate(lines):
                yy = y0 + li * lh
                # One <text> per line, so the browser spaces the words itself;
                # marked words are tspans with an underline in their own colour.
                runs = []
                for _, w, style in line:
                    if runs and runs[-1][1] == style:
                        runs[-1][0] += " " + w
                    else:
                        runs.append([(" " if runs else "") + w, style])
                    texts.append(w)
                spans = ""
                for s, style in runs:
                    lead = " " if s.startswith(" ") else ""
                    s = s.lstrip(" ")
                    if style == "n":
                        spans += escape(lead + s)
                    else:
                        fill = "#7A3A22" if style == "bad" else RED
                        spans += escape(lead) + f'<tspan fill="{fill}" text-decoration="underline">{escape(s)}</tspan>'
                g.append(
                    f'<text x="{colx[col] + pad}" y="{yy:.1f}" font-family="{family("serif")}" font-size="{size}" '
                    f'fill="{INK}" xml:space="preserve">{spans}</text>'
                )
        g.append(text_el(56, 404, why, "serif", 20, "#4A4238"))
        texts.append(why)
        if width(why, "serif", 20) > 1088:
            raise SystemExit(f"caption too wide: {why}")
        g.append("</g>")
        body += g

    for k in range(len(slides)):
        body.append(f'<circle class="d d{k}" style="animation-delay:{k * slot:.1f}s" cx="{600 - 16 + k * 16}" cy="440" r="4"/>')

    return svg_doc(
        W, H,
        "Three outputs without and with the skill: no ‑ው on “the office” for a website, ‑ን on the patients as the object, "
        "and a placeholder instead of an invented translation of the Constitution.",
        "".join(css), "".join(body), "".join(texts),
    )


if __name__ == "__main__":
    for name, fn in (("hero", hero), ("demo", demo), ("compare", compare)):
        svg = fn()
        (OUT / f"{name}.svg").write_text(svg, encoding="utf8")
        print(f"{name}.svg  {len(svg.encode()) / 1024:.0f} KB")
