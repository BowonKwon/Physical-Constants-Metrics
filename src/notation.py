# -*- coding: utf-8 -*-
"""Subscripts in constant symbols (1.3.4): one rule for every page.

The source strings (quantity_map.csv, prose in the page builders) write a subscript either as a Unicode
subscript letter (mₑ, μₚ, μ₀) or with an underscore (N_A, μ_N, a_μ), because Unicode has no subscript
capital letters, no subscript μ and no subscript d. The data files keep what they say; the pages apply
this rule when they are written:

  * HTML text (headings, cards, tables, lists, prose, formulas): <sub>, e.g. m<sub>e</sub>, N<sub>A</sub>,
    μ<sub>p</sub>/μ<sub>N</sub>, μ<sub>0</sub>.
  * SVG <text>: a <tspan> lowered by 0.3 of the font size and set at 75 %, which looks like <sub>.
  * Plain text with no markup (page <title>, tooltips in data-tip, aria-label, alt, title attributes):
    the underscore form for every subscript, e.g. m_e, N_A, μ_p/μ_N, μ_0. One fixed form, so no symbol
    mixes a Unicode subscript with an underscore.
  * Left as written: code, pre, data files (CSV, JSON), and formula variables named after CSV columns
    (x_old, u_x, z_old, R_B, …), which are not constant symbols.

Only the symbols listed in SYMBOLS are converted, so file names and page addresses such as Ar_d.html or
mup_muN.html are never touched.
"""
from __future__ import annotations

import re

# symbol as written in the sources -> (base, subscript)
SYMBOLS = {
    "mₑ": ("m", "e"), "aₑ": ("a", "e"), "mₚ": ("m", "p"), "μₚ": ("μ", "p"), "μₙ": ("μ", "n"), "rₚ": ("r", "p"),
    "μ₀": ("μ", "0"), "N₀": ("N", "0"),
    "N_A": ("N", "A"), "M_u": ("M", "u"), "a_μ": ("a", "μ"), "m_μ": ("m", "μ"), "r_d": ("r", "d"),
    "μ_N": ("μ", "N"), "μ_d": ("μ", "d"),
}
# Not preceded by a Latin or Greek letter, digit or underscore (Ar_d, mup_muN stay as they are). An underscore
# form must also not be followed by one; a Unicode subscript ends itself, so μ₀c (a product) is still converted.
# A Korean particle written right after the symbol (N_A가) is allowed.
_W = "A-Za-z0-9_Ͱ-Ͽ"   # Greek and Coptic block
_TOK = re.compile(r"(?<![" + _W + r"])(" + "|".join(
    re.escape(s) + ("" if "_" not in s else r"(?![" + _W + r"])") for s in sorted(SYMBOLS, key=len, reverse=True)) + r")")


def sym_html(text: str) -> str:
    return _TOK.sub(lambda m: "{0}<sub>{1}</sub>".format(*SYMBOLS[m.group(1)]), text)


def sym_plain(text: str) -> str:
    return _TOK.sub(lambda m: "{0}_{1}".format(*SYMBOLS[m.group(1)]), text)


def sym_svg(text: str) -> str:
    """Inside an SVG <text>: the subscript tspan is set at .75em and lowered by .4 of its own size (= .3 of
    the text size); a run that follows is raised back by .3em of the text size."""
    m = _TOK.search(text)
    if not m:
        return text
    base, sub = SYMBOLS[m.group(1)]
    head = text[:m.start()] + base + f'<tspan dy=".4em" font-size=".75em">{sub}</tspan>'
    rest = text[m.end():]
    return head + (f'<tspan dy="-.3em">{sym_svg(rest)}</tspan>' if rest else "")


_BLOCK = re.compile(r"(<script.*?</script>|<style.*?</style>|<code.*?</code>|<pre.*?</pre>|<math.*?</math>|<svg.*?</svg>|<title>.*?</title>)", re.S)
_TAG = re.compile(r"(<[^>]*>)")
_ATTR = re.compile(r'((?:data-tip|aria-label|alt|title)=")([^"]*)(")')


def _attrs(tag: str) -> str:
    return _ATTR.sub(lambda m: m.group(1) + sym_plain(m.group(2)) + m.group(3), tag)


def _svg(block: str) -> str:
    out, in_text = [], False
    for i, part in enumerate(_TAG.split(block)):
        if i % 2:
            if part.startswith("<text"):
                in_text = True
            elif part.startswith("</text"):
                in_text = False
            out.append(_attrs(part))
        else:
            out.append(sym_svg(part) if in_text else part)
    return "".join(out)


def apply(html: str) -> str:
    """Apply the rule to a page body: text nodes -> <sub>, SVG text -> tspan, the listed attributes and
    <title> -> underscore form. Code, pre, script, style and math are left alone."""
    out = []
    for i, chunk in enumerate(_BLOCK.split(html)):
        if i % 2:
            if chunk.startswith("<svg"):
                chunk = _svg(chunk)
            elif chunk.startswith("<title>"):
                chunk = sym_plain(chunk)
        else:
            chunk = "".join(_attrs(p) if j % 2 else sym_html(p) for j, p in enumerate(_TAG.split(chunk)))
        out.append(chunk)
    return "".join(out)
