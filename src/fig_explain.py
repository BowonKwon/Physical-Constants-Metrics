# -*- coding: utf-8 -*-
"""1.3.9: the explanation that goes with every chart — a one-line introduction above it and named paragraphs below
(In short / How the chart works / Reading one value / The numbers / Easy to misread / Terms), Korean and English.
Every number in these sentences is computed from the data by the caller; no number is typed in here except the
fixed expectations of the normal distribution (31.7%, 4.55%, 0.27%, 50%, 2%) and the fixed conversion 1.4826."""
from __future__ import annotations

import html
import math

LAB = {"ko": dict(glance="한눈에", how="그림 보는 법", one="숫자 하나 읽어 보기", nums="수로 보면", mis="잘못 읽기 쉬운 것", terms="낱말 풀이"),
       "en": dict(glance="In short", how="How the chart works", one="Reading one value", nums="The numbers", mis="Easy to misread", terms="Terms")}

CSS = (" .fi{font-size:.95rem;color:var(--fg);margin:0 0 .5rem;line-height:1.55}.fi b{font-weight:600}"
       " figcaption .cp{margin:.45rem 0 0;max-width:80ch}figcaption .cp>b:first-child{color:var(--fg);font-weight:600;margin-right:.4rem}"
       " :lang(ko) .fi,:lang(ko) figcaption .cp{word-break:keep-all;overflow-wrap:anywhere}"
       " .legend span.mk::before{display:none}.legend span.mk svg{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:.35rem;overflow:visible}")

# Legend swatches drawn with the same marks as the charts (circle filled / open, square, ×, diamond, triangle, dashed line).
_MK = {
    "dot": '<circle cx="7" cy="7" r="4.5" fill="{c}" stroke="{c}" stroke-width="1.5"/>',
    "open": '<circle cx="7" cy="7" r="4.5" fill="var(--card)" stroke="{c}" stroke-width="2"/>',
    "square": '<rect x="3" y="3" width="8" height="8" fill="var(--card)" stroke="{c}" stroke-width="1.5"/>',
    "cross": '<path d="M3.5,3.5 L10.5,10.5 M3.5,10.5 L10.5,3.5" stroke="{c}" stroke-width="1.8"/>',
    "diamond": '<path d="M7,1.5 L12.5,7 L7,12.5 L1.5,7 Z" fill="{c}" stroke="{c}" stroke-width="1"/>',
    "tri": '<path d="M2,11 L12,11 L7,3 Z" fill="{c}"/>',
    "box": '<rect x="4" y="1" width="6" height="12" fill="none" stroke="{c}" stroke-width="2"/>',
    "bar": '<line x1="7" y1="1" x2="7" y2="13" stroke="{c}" stroke-width="2"/><circle cx="7" cy="7" r="3.5" fill="{c}"/>',
    "line": '<line x1="0" y1="7" x2="14" y2="7" stroke="{c}" stroke-width="2.5"/>',
    "dash": '<line x1="0" y1="7" x2="14" y2="7" stroke="{c}" stroke-width="2" stroke-dasharray="4 3"/>',
    "band": '<rect x="0" y="3" width="14" height="8" rx="2" fill="{c}" fill-opacity=".3"/>',
}


def legend(items):
    """items: [(mark, colour, label)] -> the legend row above a chart, with the chart's own marks."""
    out = []
    for mk, col, lab in items:
        out.append(f'<span class="mk"><svg viewBox="0 0 14 14" aria-hidden="true">{_MK[mk].format(c=col)}</svg>{html.escape(lab, quote=False)}</span>')
    return '<div class="legend">' + "".join(out) + "</div>"


def figure(lang, title, intro, chart, paras, leg=""):
    """<figure> with the introduction line (title in bold), the legend, the chart and the named paragraphs."""
    lab = LAB[lang]
    sep = " — " if lang == "en" else " — "
    cap = "".join(f'<p class="cp"><b>{lab[k]}</b> {html.escape(t, quote=False)}</p>' for k, t in paras if t)
    return (f'<figure><p class="fi"><b>{html.escape(title, quote=False)}</b>{sep}{html.escape(intro, quote=False)}</p>{leg}{chart}'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------------------------ number words
_KO_POW = {2: "100", 3: "1,000", 4: "1만", 5: "10만", 6: "100만", 7: "1,000만", 8: "1억", 9: "10억", 10: "100억", 11: "1,000억",
           12: "1조", 13: "10조", 14: "100조", 15: "1,000조"}
_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(x, sig=2):
    """2.9e-10 -> '2.9×10⁻¹⁰' (sig significant digits)."""
    x = float(x)
    if x == 0:
        return "0"
    m, e = f"{x:.{sig - 1}e}".split("e")
    return f"{m}×10{str(int(e)).translate(_SUP)}"


def frac(x, lang, sig=2):
    """A small positive fraction in words: 2.9e-10 -> '100억분의 2.9' / '2.9 parts in 10¹⁰'; 0.012 -> '1.2%'.
    Returns (text, rounded) — rounded tells whether the words are rounded from the value."""
    x = abs(float(x))
    if x == 0:
        return ("0", False)
    if x >= 0.01:
        s = f"{x * 100:.{sig}g}"
        return (s + "%", float(s) / 100 != x)
    k = -int(math.floor(math.log10(x)))
    m = x * 10 ** k
    ms = f"{m:.{sig - 1}f}"
    if float(ms) >= 10:   # 9.96 -> 10.0
        k -= 1
        ms = f"{x * 10 ** k:.{sig - 1}f}"
    rounded = abs(float(ms) / 10 ** k - x) > 1e-9 * x
    if not rounded and ms.endswith(".0"):
        ms = ms[:-2]
    if lang == "ko":
        return (f"{_KO_POW.get(k, '10' + str(k).translate(_SUP))}분의 {ms}", rounded)
    return (f"{ms} part{'s' if ms != '1' else ''} in 10{str(k).translate(_SUP)}", rounded)


def num(x, fmt=".2f"):
    """a signed number with a true minus sign (−2.50)."""
    return format(float(x), fmt).replace("-", "−")


def about(lang, rounded):
    return ("약 " if lang == "ko" else "about ") if rounded else ""


def lt_words(lt, lang):
    """the linear range of a symmetric-log axis, in words."""
    w, _ = frac(lt, lang)
    return w


def symlog_sentence(lang, lt_txt):
    """One definition of the symmetric-log axis, used by every chart that has one (constant, element and before-CODATA pages)."""
    if lang == "ko":
        return (f"세로축은 대칭 로그 축(symmetric log scale)이다. 0 근처, 곧 ±{lt_txt} 안쪽은 거의 고른 간격으로 그리고, "
                "그 바깥으로 갈수록 눈금 한 칸이 10배에 가까워진다(둘 사이에 뚜렷한 경계는 없다). 0을 사이에 두고 위(+)와 아래(−)에 같은 모양의 눈금이 있다.")
    return (f"The vertical axis is a symmetric-log axis: near zero, within ±{lt_txt}, it is almost evenly spaced, and further out each step "
            "comes close to a factor of ten (with no sharp boundary between the two). The steps above (+) and below (−) zero mirror each other.")


def symlog_misread(lang):
    if lang == "ko":
        return ("대칭 로그 축에서는 0을 가로지르는 막대의 위아래 길이가 달라 보이고, 바깥쪽 눈금에서는 같은 길이의 막대라도 나타내는 폭이 10배씩 다르다. "
                "그래서 막대 길이를 눈으로 견주지 말고 수는 표와 점 위 말풍선(커서를 대면 보이는 글)에서 읽는다.")
    return ("On a symmetric-log axis a bar that crosses zero looks uneven above and below, and in the outer steps bars of the same drawn length "
            "can stand for widths that differ tenfold. Do not compare bar lengths by eye; read the numbers in the table and in the tooltips (shown when the pointer rests on a mark).")


def symlog_term(lang):
    return ("대칭 로그 축 = 0 근처는 고른 간격, 바깥은 로그 눈금(한 칸이 10배)인 축. 0과 음수를 함께 그릴 수 있어서, 아주 작은 차이와 큰 차이를 한 그림에 담을 때 쓴다." if lang == "ko"
            else "Symmetric-log axis: evenly spaced near zero and logarithmic (one step per factor of ten) further out; it can show zero and negative values, so very small and large differences fit in one chart.")
