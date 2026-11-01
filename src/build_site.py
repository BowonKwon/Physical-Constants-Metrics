# -*- coding: utf-8 -*-
"""Static site builder: data/derived/*.csv + registry -> site/ (ko + en).

  python src/build_site.py

No dependencies beyond the standard library and numpy. Charts are inline SVG.
"""
from __future__ import annotations

import csv
import html
import json
import math
import shutil
from pathlib import Path

import numpy as np
from scipy import stats

from registry import EDITIONS, LATEST, METRICS, SOURCES

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
OUT = ROOT / "site"
VERSION = "1.0"
BUILD_DATE = "2026-11-01"
REPO = "https://github.com/BowonKwon/Physical-Constants-Metrics"
PUBLIC_DATA = ["constants_long.csv", "quantity_map.csv", "m1_halflife.csv", "m2_pairs.csv", "m2_summary.csv",
               "m3_vs_latest.csv", "m3_summary.csv", "m4_tail.csv", "m5_funnel.csv", "m6_events.csv",
               "hf_repro.csv", "sens_all_rows.csv", "sens_candidates.csv", "handcheck_mapped.csv", "handcheck_early.csv"]
DATA_DESC = {
    "constants_long.csv": ("상수 × 판 긴 표: 값·표준불확도·상대 불확도·단위·정의값 여부·원 표기·원자료 위치", "Constant × edition long table: value, standard uncertainty, relative uncertainty, unit, exact flag, printed form, source location"),
    "quantity_map.csv": ("27개 양의 대응표: 기호·이름(한·영)·판별 원 이름·정의값 시점·층(핵심/표시)·한국어 이름 근거", "Map of the 27 quantities: symbol, names, source names by edition, exact-from edition, layer, basis of the Korean name"),
    "m1_halflife.csv": ("M1 상대 불확도 반감기", "M1 relative-uncertainty half-life"),
    "m2_pairs.csv": ("M2 연속 판 쌍 전부(z, z_옛)", "M2 every consecutive-edition pair (z, z_old)"),
    "m2_summary.csv": ("M2 초과율과 신뢰구간", "M2 exceedance rates and intervals"),
    "m3_vs_latest.csv": ("M3 (판, 상수)별 2022 판 대조", "M3 every (edition, constant) against 2022"),
    "m3_summary.csv": ("M3 판별·묶음별 놓침률, 사분위 지수, 놀람 지수", "M3 miss rates, interquartile and surprise indices by edition and group"),
    "m4_tail.csv": ("M4 Student-t 적합", "M4 Student-t fits"),
    "m5_funnel.csv": ("M5 수렴 그림 자료", "M5 convergence-plot data"),
    "m6_events.csv": ("M6 정의값 전환", "M6 exact-value transitions"),
    "hf_repro.csv": ("Henrion & Fischhoff 방식 재계산(상수 5개)", "Henrion & Fischhoff-style recalculation (five constants)"),
    "sens_candidates.csv": ("민감도: 핵심 17개에 같은 규칙의 후보 3개를 더한 20개로 M2·M3 재계산", "Sensitivity: M2 and M3 recomputed with three candidates meeting the same rule added (20 constants)"),
    "sens_all_rows.csv": ("민감도: 1998~2022 ASCII 표의 이름이 같은 모든 행", "Sensitivity: every 1998–2022 ASCII row with an unchanged name"),
    "handcheck_mapped.csv": ("대조: 이 사이트가 쓰는 1998~2022 행 전부를 NIST PDF 표와", "Check: every 1998–2022 row used here against NIST's PDF tables"),
    "handcheck_early.csv": ("대조: 1969·1973·1986 손 입력값 전부를 쪽 이미지·문자층과", "Check: every 1969/1973/1986 hand-entered value against page images and text layer"),
}

NOTE_KO = {
    "h": "2018 판부터 정의값(2019년 SI 개정).", "k": "2018 판부터 정의값(2019년 SI 개정).",
    "Ar_e": "NIST 표의 이름은 「electron mass in u」.", "Ar_p": "NIST 표의 이름은 「proton mass in u」.",
    "Ar_n": "NIST 표의 이름은 「neutron mass in u」.", "Ar_d": "NIST 표의 이름은 「deuteron mass in u」.",
    "Ar_alpha": "NIST 표의 이름은 「alpha particle mass in u」.",
    "a_e": "1969·1973 판은 g/2 = 1 + aₑ 로 적었다. 1을 뺀 값을 쓴다.", "a_mu": "1973 판은 g/2 = 1 + a_μ 로 적었다. 1을 뺀 값을 쓴다.",
    "mup_muN": "물속 양성자가 아닌 자유 양성자의 값.", "mun_muN": "관례상 음수.",
    "c": "1983년 미터 정의. 1986 판부터 정의값. 1969·1973 판은 측정값.",
    "e": "2019년 이전에는 √(2αh/μ₀c). 1998~2006 ASCII 표에는 기본 전하 행이 없어 같은 수치인 전자볼트(J) 행을 썼다(1 eV = {e} J).",
    "NA": "2019년 이전에는 몰 플랑크 상수를 통해 h 와 묶여 있었다. 2018 판부터 정의값.",
    "me": "= 2R∞h/(cα²). 핵심 상수들의 조합이라 통계에서 뺀다.", "mp_me": "= Ar(p)/Ar(e). 통계에서 뺀다.",
    "F": "= N_A e. 2018 판부터 정의값.", "R": "= N_A k. 2018 판부터 정의값.", "sigma": "= (π²/60)k⁴/ħ³c². 2018 판부터 정의값.",
    "mu0": "2014 판까지 정의값(4π×10⁻⁷), 2018 판부터 측정값.",
    "alpha_inv": "= 1/α. Henrion & Fischhoff(1986)와 1973 보고서가 α⁻¹ 로 비교하므로 함께 싣는다. 통계에는 α 만 쓴다.",
    "Ar_h": "민감도 후보. NIST 표의 이름은 「helion mass in u」.", "Ar_t": "민감도 후보. NIST 표의 이름은 「triton mass in u」(2006 판부터).",
    "mud_muN": "민감도 후보.", "Mu": "2014 판까지 정의값(1 g/mol), 2018 판부터 측정값.",
}

T = {
    "ko": dict(site="물리 상수 메트릭스", tagline="과학자들이 밝힌 오차 막대는 다음 판의 값을 얼마나 자주 놓쳤나 — CODATA 기본 물리 상수 1969~2022",
               home="홈", metrics="지표", constants="상수", reading="읽기", data="데이터", method="방법·한계", prior="선행 연구", lang_other="English",
               version="판", built="생성일", hub="공개 자료 전체", definition="정의", formula="공식", denominator="분모", howto="읽는 법", caveat="한계",
               download="CSV 내려받기", edition="판", value="값", u="표준불확도", urel="상대 불확도", exact="정의값", printed="원 표기", source="원자료 위치",
               z_prev="직전 판 대비 z", z_latest="z = (2022 판 − 이 판)/σ", core="핵심 상수", display="표시용 상수", cand="민감도 후보", layer="층", symbol="기호", unit="단위",
               name="이름", n_ed="판 수", halflife="반감기(년)", ci="95% 구간", yes="예", no="아니오", none="감소 없음", file="파일", desc="내용",
               normal="정규 기대", observed="관측", rate="비율", threshold="기준", pairs="판 쌍", quantities="상수", subset="묶음",
               basis="한국어 이름 근거"),
    "en": dict(site="Physical Constants Metrics", tagline="How often did the error bars scientists published miss the next edition's value? CODATA fundamental constants, 1969–2022",
               home="Home", metrics="Metrics", constants="Constants", reading="Reading", data="Data", method="Method & limits", prior="Prior work", lang_other="한국어",
               version="Version", built="Built", hub="All public materials", definition="Definition", formula="Formula", denominator="Denominator", howto="How to read it", caveat="Caveats",
               download="Download CSV", edition="Edition", value="Value", u="Std. uncertainty", urel="Rel. uncertainty", exact="Exact", printed="As printed", source="Source location",
               z_prev="z vs previous edition", z_latest="z = (2022 − this)/σ", core="core constant", display="display constant", cand="sensitivity candidate", layer="Layer", symbol="Symbol", unit="Unit",
               name="Name", n_ed="Editions", halflife="Half-life (y)", ci="95% interval", yes="yes", no="no", none="no decline", file="File", desc="Contents",
               normal="normal", observed="observed", rate="rate", threshold="threshold", pairs="pairs", quantities="constants", subset="Group",
               basis="Basis of Korean name"),
}

CSS = """
:root{color-scheme:light;
  --bg:#f7f7f5;--bg2:#ecede9;--card:#ffffff;--line:#d9dbd5;--line2:#e7e8e3;
  --fg:#1c1f22;--fg2:#575c62;--fg3:#868b90;
  --accent:#2d6b68;--accent2:#a5643c;
  --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--grid:#e4e5e0;--ref:#8f9398;
  --shadow:0 1px 2px rgba(30,34,38,.05),0 6px 18px rgba(30,34,38,.05);
  --display:"Noto Serif KR","Source Serif 4",Georgia,serif;
  --body:"Noto Sans KR",-apple-system,"Segoe UI","Apple SD Gothic Neo",Roboto,sans-serif}
@media(prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){color-scheme:dark;
  --bg:#1a1c1d;--bg2:#212425;--card:#222526;--line:#33383a;--line2:#2a2e30;
  --fg:#eaebe8;--fg2:#b2b5b2;--fg3:#7f8381;
  --accent:#73b3ad;--accent2:#d39467;
  --s1:#3987e5;--s2:#d95926;--s3:#199e70;--grid:#2c3032;--ref:#8a8e8c;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 20px rgba(0,0,0,.25)}}
:root[data-theme="dark"]{color-scheme:dark;
  --bg:#1a1c1d;--bg2:#212425;--card:#222526;--line:#33383a;--line2:#2a2e30;
  --fg:#eaebe8;--fg2:#b2b5b2;--fg3:#7f8381;
  --accent:#73b3ad;--accent2:#d39467;
  --s1:#3987e5;--s2:#d95926;--s3:#199e70;--grid:#2c3032;--ref:#8a8e8c;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 20px rgba(0,0,0,.25)}
*{box-sizing:border-box}html,body{max-width:100%;overflow-x:hidden}
body{margin:0;font:16px/1.7 var(--body);background:var(--bg);color:var(--fg);overflow-wrap:anywhere;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:3px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
header{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:.55rem 1.1rem;display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap}
header .brand{font-family:var(--display);font-weight:600;font-size:1.05rem;color:var(--fg)}
header nav{display:flex;gap:.9rem;flex-wrap:wrap}header nav a{color:var(--fg2);font-size:.92rem;padding:.2rem 0;border-bottom:2px solid transparent}
header nav a:hover{text-decoration:none;color:var(--fg)}header nav a.on{color:var(--fg);border-bottom-color:var(--accent2)}
header .right{margin-left:auto;display:flex;gap:.6rem;align-items:center}
header .lang{font-size:.88rem;color:var(--fg2);border:1px solid var(--line);border-radius:999px;padding:.15rem .7rem}header .lang:hover{text-decoration:none;color:var(--fg)}
.theme{border:1px solid var(--line);background:transparent;color:var(--fg2);border-radius:999px;width:30px;height:30px;cursor:pointer;font-size:.9rem;line-height:1;padding:0}
main{max-width:1060px;margin:0 auto;padding:1.6rem 1.1rem 4rem;min-width:0}
h1{font-family:var(--display);font-weight:600;font-size:clamp(1.6rem,3.2vw,2.2rem);line-height:1.25;margin:.3rem 0 .5rem;text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-size:1.3rem;line-height:1.3;margin:2.4rem 0 .8rem;padding-bottom:.35rem;border-bottom:1px solid var(--line)}
h3{font-size:1.02rem;margin:1.4rem 0 .4rem}
.tag{display:inline-block;font-size:.74rem;padding:.1rem .55rem;border-radius:999px;color:var(--fg2);background:var(--bg2);border:1px solid var(--line2);margin-right:.35rem}
.tag.k{color:var(--accent);border-color:color-mix(in srgb,var(--accent) 35%,transparent)}
.lead{color:var(--fg2);font-size:1.05rem;max-width:72ch;margin:0 0 1.2rem}
.hero{padding:.6rem 0 1.4rem;border-bottom:1px solid var(--line);margin-bottom:1.4rem}.hero h1{font-size:clamp(1.8rem,4vw,2.6rem)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.8rem;margin:1.2rem 0 1.6rem}
.stat{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.1rem;box-shadow:var(--shadow);color:var(--fg)}
.stat .n{font-family:var(--display);font-size:2rem;font-weight:600;line-height:1.1;font-variant-numeric:tabular-nums}
.stat .vs{font-size:.95rem;color:var(--fg2);margin-left:.3rem}
.stat small{display:block;color:var(--fg2);margin-top:.35rem;font-size:.86rem;line-height:1.45}a.stat:hover{text-decoration:none;border-color:var(--fg3)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.8rem;margin:.9rem 0 1.4rem}
.card{display:block;background:var(--card);border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:10px;padding:.85rem 1rem;box-shadow:var(--shadow);color:var(--fg)}
.card.d{border-top-color:var(--line)}a.card:hover{text-decoration:none;border-color:var(--fg3)}
.card b{display:block;margin-bottom:.25rem;color:var(--accent)}.card small{color:var(--fg2);font-size:.86rem;line-height:1.5;display:block}
.spec{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.2rem;margin:1rem 0 1.4rem;box-shadow:var(--shadow)}
dl{display:grid;grid-template-columns:max-content 1fr;gap:.55rem 1.4rem;margin:0}dt{color:var(--fg3);font-size:.82rem;padding-top:.15rem}dd{margin:0;min-width:0}
dd.formula{font-family:ui-monospace,Consolas,"Noto Sans KR",monospace;font-size:.9rem;background:var(--bg2);border-radius:6px;padding:.45rem .65rem}
@media(max-width:640px){dl{grid-template-columns:1fr}dt{margin-top:.5rem}}
table{border-collapse:collapse;width:100%;font-size:.88rem;margin:.6rem 0}
th,td{border-bottom:1px solid var(--line2);padding:.4rem .55rem;text-align:left;vertical-align:top;overflow-wrap:normal;word-break:keep-all}
.wrap table{min-width:560px}
thead th{color:var(--fg2);font-weight:600;font-size:.8rem;cursor:pointer;white-space:nowrap;border-bottom:1px solid var(--line)}
tbody tr:nth-child(even){background:color-mix(in srgb,var(--bg2) 55%,transparent)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card);padding:0 .3rem;margin:.6rem 0 1rem}.wrap table{margin:0}
figure{margin:1.2rem 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1rem .8rem;box-shadow:var(--shadow)}
figcaption{font-size:.86rem;color:var(--fg2);margin-top:.5rem;line-height:1.5}
svg{max-width:100%;height:auto;display:block}svg text{font-family:var(--body);fill:var(--fg2);font-size:12px}svg .grid{stroke:var(--grid)}svg .ref{stroke:var(--ref);stroke-dasharray:4 4}
svg .hit{fill:transparent}svg .hit:hover+.dot,svg .dot:hover{stroke:var(--fg);stroke-width:2}
.legend{display:flex;gap:1.1rem;font-size:.86rem;color:var(--fg2);flex-wrap:wrap;margin:.2rem 0 .4rem}.legend span::before{content:"";display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:.4rem;vertical-align:-1px;background:var(--c)}
.legend span.dash::before{height:0;border-top:2px dashed var(--c);border-radius:0;vertical-align:3px}
.takeaway{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent2);border-radius:10px;padding:.75rem 1.1rem .8rem;margin:.4rem 0 1.4rem;box-shadow:var(--shadow);max-width:80ch}
.takeaway b{display:block;font-size:.76rem;letter-spacing:.06em;color:var(--accent2);margin-bottom:.2rem}
.takeaway ul{margin:0;padding-left:1.1rem}.takeaway li{margin:.25rem 0}
.note{background:color-mix(in srgb,var(--accent) 7%,var(--card));border:1px solid color-mix(in srgb,var(--accent) 25%,var(--line));border-left:4px solid var(--accent);border-radius:8px;padding:.7rem 1rem;margin:1.2rem 0;font-size:.95rem}
.prose p,.prose ul,.prose ol{max-width:72ch}.prose p{margin:.8rem 0}.prose li{margin:.3rem 0}
.files a{display:inline-block;font-size:.85rem;background:var(--bg2);border:1px solid var(--line2);border-radius:6px;padding:.15rem .55rem;margin:.2rem .3rem .2rem 0;color:var(--fg2)}
footer{border-top:1px solid var(--line);color:var(--fg3);font-size:.82rem;padding:1.2rem;text-align:center}
.tip{position:fixed;pointer-events:none;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:.3rem .55rem;font-size:.82rem;box-shadow:var(--shadow);display:none;z-index:9;max-width:280px}
"""

JS = """
(function(){var k="pcm-theme",r=document.documentElement,b=document.getElementById("theme");function ap(v){if(v)r.setAttribute("data-theme",v);else r.removeAttribute("data-theme");if(b)b.textContent=v==="dark"?"\\u263E":v==="light"?"\\u2600":"\\u25D1"}var cur=localStorage.getItem(k)||"";ap(cur);if(b)b.addEventListener("click",function(){cur=cur===""?"light":cur==="light"?"dark":"";if(cur)localStorage.setItem(k,cur);else localStorage.removeItem(k);ap(cur)})})();
document.querySelectorAll('table.sort').forEach(function(t){t.querySelectorAll('th').forEach(function(th,i){th.addEventListener('click',function(){
 var rows=Array.from(t.tBodies[0].rows),asc=th.dataset.asc!=='1';th.dataset.asc=asc?'1':'0';
 rows.sort(function(a,b){var x=a.cells[i].dataset.v||a.cells[i].textContent,y=b.cells[i].dataset.v||b.cells[i].textContent;var nx=parseFloat(x),ny=parseFloat(y);
 if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;return asc?x.localeCompare(y):y.localeCompare(x)});rows.forEach(function(r){t.tBodies[0].appendChild(r)})})})});
(function(){var tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip);
document.querySelectorAll('svg [data-tip]').forEach(function(el){el.addEventListener('mousemove',function(e){tip.textContent=el.getAttribute('data-tip');tip.style.display='block';
 var x=e.clientX+14,y=e.clientY+14;if(x+tip.offsetWidth>innerWidth-8)x=e.clientX-tip.offsetWidth-10;tip.style.left=x+'px';tip.style.top=y+'px'});
 el.addEventListener('mouseleave',function(){tip.style.display='none'})})})();
"""


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def read(name):
    return list(csv.DictReader(open(DER / name, encoding="utf-8")))


def pct(x, d=1) -> str:
    return f"{float(x) * 100:.{d}f}"


def cip(s: str) -> str:
    """'[0.300, 0.900]' -> '30–90%'"""
    if not s:
        return ""
    lo, hi = s.strip("[]").split(",")
    return f"{float(lo) * 100:.0f}–{float(hi) * 100:.0f}%"


def ci_pct(lo, hi, d=1) -> str:
    return f"{float(lo) * 100:.{d}f}–{float(hi) * 100:.{d}f}%"


def page(lang, title, body, depth=1, active=""):
    t = T[lang]
    root = "../" * depth
    other = "en" if lang == "ko" else "ko"
    hub = "" if lang == "ko" else "en/"
    nav = [("home", "index.html", t["home"]), ("metrics", "metrics/index.html", t["metrics"]),
           ("constants", "constants/index.html", t["constants"]), ("reading", "reading.html", t["reading"]),
           ("prior", "prior.html", t["prior"]), ("method", "method.html", t["method"]), ("data", "data.html", t["data"])]
    navh = "".join(f'<a href="{root}{lang}/{h}"{" class=\"on\"" if k == active else ""}>{n}</a>' for k, h, n in nav)
    return f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — {t['site']}</title><meta name="description" content="{esc(t['tagline'])}">
<script>(function(){{var q=new URLSearchParams(location.search).get("theme");if(q==="light"||q==="dark"){{localStorage.setItem("pcm-theme",q)}}else if(q==="auto"){{localStorage.removeItem("pcm-theme")}}var v=localStorage.getItem("pcm-theme");if(v)document.documentElement.setAttribute("data-theme",v)}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><a class="brand" href="{root}{lang}/index.html">{t['site']}</a><nav>{navh}</nav>
<div class="right"><button id="theme" class="theme" type="button" aria-label="theme">◑</button><a class="lang" href="{root}{other}/index.html">{t['lang_other']}</a></div></header>
<main>{body}</main>
<footer>{t['site']} · {t['version']} {VERSION} · {t['built']} {BUILD_DATE} · <a href="{REPO}">GitHub</a> · {t['hub']} <a href="https://bowonkwon.github.io/{hub}">bowonkwon.github.io</a></footer>
<script>{JS}</script></body></html>"""


def table(headers, rows, num_cols=(), cls="sort"):
    th = "".join(f'<th class="num">{esc(h)}</th>' if i in num_cols else f"<th>{esc(h)}</th>" for i, h in enumerate(headers))
    body = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            if isinstance(c, tuple):  # (display html, sort value)
                tds.append(f'<td{" class=\"num\"" if i in num_cols else ""} data-v="{esc(c[1])}">{c[0]}</td>')
            else:
                tds.append(f'<td{" class=\"num\"" if i in num_cols else ""}>{c}</td>')
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div class="wrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


# ------------------------------------------------------------------ charts
def log_ticks(lo, hi):
    a, b = math.floor(math.log10(lo)), math.ceil(math.log10(hi))
    return [10.0 ** e for e in range(a, b + 1)]


def sup(e):
    return "10" + "".join("⁻⁰¹²³⁴⁵⁶⁷⁸⁹"[0] if ch == "-" else "⁰¹²³⁴⁵⁶⁷⁸⁹"[int(ch)] for ch in str(e))


def chart_uncertainty(qmap, long, lang, W=900, H=360):
    """G1: relative uncertainty by edition, one faint dot per core constant, median line."""
    L, R, Tp, B = 64, 20, 16, 40
    pts = [(int(r["edition"]), float(r["u_rel"]), r["qid"]) for r in long
           if qmap[r["qid"]]["layer"] == "K" and r["exact"] == "0" and float(r["u_rel"]) > 0]
    ys = [p[1] for p in pts]
    lo, hi = 10 ** math.floor(math.log10(min(ys))), 10 ** math.ceil(math.log10(max(ys)))
    x0, x1 = 1966, 2025

    def X(v): return L + (v - x0) / (x1 - x0) * (W - L - R)

    def Y(v): return Tp + (math.log10(hi) - math.log10(v)) / (math.log10(hi) - math.log10(lo)) * (H - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="relative uncertainty by edition">']
    for t in log_ticks(lo, hi):
        o.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{L-6}" y="{Y(t)+4:.1f}" text-anchor="end">{sup(int(round(math.log10(t))))}</text>')
    for e in EDITIONS:
        o.append(f'<text x="{X(e):.1f}" y="{H-14}" text-anchor="middle">{e}</text>')
    name = "name_ko" if lang == "ko" else "name_en"
    for e, v, q in pts:
        o.append(f'<circle class="dot" cx="{X(e):.1f}" cy="{Y(v):.1f}" r="4" fill="var(--s1)" fill-opacity=".28" stroke="var(--card)" stroke-width="1" data-tip="{esc(qmap[q][name])} · {e}: {v:.2e}"/>')
    med = []
    for e in EDITIONS:
        vs = [v for ee, v, _ in pts if ee == e]
        if vs:
            med.append((e, float(np.median(vs)), len(vs)))
    d = " ".join(f"{'M' if i == 0 else 'L'}{X(e):.1f},{Y(v):.1f}" for i, (e, v, _) in enumerate(med))
    o.append(f'<path d="{d}" fill="none" stroke="var(--s1)" stroke-width="2.5"/>')
    lab = "중앙값" if lang == "ko" else "median"
    for e, v, n in med:
        o.append(f'<circle class="dot" cx="{X(e):.1f}" cy="{Y(v):.1f}" r="5" fill="var(--s1)" stroke="var(--card)" stroke-width="2" data-tip="{e} {lab}: {v:.2e} (n={n})"/>')
    o.append("</svg>")
    return "".join(o), med


def chart_tail(pairs, nu, s, lang, W=900, H=360):
    """G2: P(|z|>t) observed vs normal vs fitted Student-t, log y."""
    L, R, Tp, B = 64, 120, 16, 40
    z = np.sort(np.abs([float(p["z"]) for p in pairs]))
    n = len(z)
    tmax = 7.0
    lo = 1e-4

    def X(v): return L + v / tmax * (W - L - R)

    def Y(v): return Tp + (0 - math.log10(max(v, lo))) / (0 - math.log10(lo)) * (H - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="tail plot">']
    for t in log_ticks(lo, 1):
        o.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{L-6}" y="{Y(t)+4:.1f}" text-anchor="end">{t:g}</text>')
    for t in range(0, 8):
        o.append(f'<text x="{X(t):.1f}" y="{H-18}" text-anchor="middle">{t}</text>')
    o.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H-2}" text-anchor="middle">|z|</text>')
    ts = np.linspace(0, tmax, 141)
    normal = [2 * stats.norm.sf(t) for t in ts]
    tfit = [2 * stats.t.sf(t / s, nu) for t in ts]
    for vals, ci, name in ((normal, 2, "정규분포" if lang == "ko" else "normal"),
                           (tfit, 3, (f"Student-t (ν={nu:.2f})"))):
        d = " ".join(f"{'M' if i == 0 else 'L'}{X(t):.1f},{Y(v):.1f}" for i, (t, v) in enumerate(zip(ts, vals)) if v >= lo)
        o.append(f'<path d="{d}" fill="none" stroke="var(--s{ci})" stroke-width="2"/>')
        last = [(t, v) for t, v in zip(ts, vals) if v >= lo][-1]
        o.append(f'<text x="{min(X(last[0]) + 6, W - R + 4):.1f}" y="{Y(last[1]) - 6:.1f}">{esc(name)}</text>')
    # observed survival (step)
    # empirical survival P(|z|>t): steps at each observed |z|; stops at the largest one (1/n)
    path, prev = [f"M{X(0):.1f},{Y(1):.1f}"], 1.0
    for i, t in enumerate(z[:-1], start=1):
        if t > tmax:
            break
        sv = (n - i) / n
        path.append(f"L{X(t):.1f},{Y(prev):.1f}L{X(t):.1f},{Y(sv):.1f}")
        prev = sv
    path.append(f"L{X(min(z[-1], tmax)):.1f},{Y(prev):.1f}")
    o.append(f'<path d="{"".join(path)}" fill="none" stroke="var(--s1)" stroke-width="2"/>')
    obs = "관측 (판 쌍)" if lang == "ko" else "observed (pairs)"
    t_lab = 4.2
    o.append(f'<text x="{X(t_lab):.1f}" y="{Y(float(np.mean(z > t_lab))) + 18:.1f}">{obs}</text>')
    for k in (1, 2, 3):
        r = float(np.mean(z > k))
        o.append(f'<circle class="dot" cx="{X(k):.1f}" cy="{Y(r):.1f}" r="5" fill="var(--s1)" stroke="var(--card)" stroke-width="2" data-tip="|z|>{k}: {r*100:.1f}% (n={n})"/>')
    o.append("</svg>")
    return "".join(o)


def chart_miss(s3, lang, W=900, H=340):
    """G3: miss rate by edition at 1σ and 2σ with CI whiskers and normal reference lines."""
    L, R, Tp, B = 56, 110, 16, 40
    eds = [r for r in s3 if r["subset"].isdigit()]

    def X(i): return L + (i + 0.5) / len(eds) * (W - L - R)

    def Y(v): return Tp + (1 - v) * (H - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="miss rate by edition">']
    for v in (0, .2, .4, .6, .8, 1.0):
        o.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{L-6}" y="{Y(v)+4:.1f}" text-anchor="end">{int(v*100)}%</text>')
    for v, lab in ((0.3173, "1σ 31.7%"), (0.0455, "2σ 4.6%")):
        o.append(f'<line class="ref" x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{W-R+6}" y="{Y(v)+4:.1f}">{("정규 " if lang == "ko" else "normal ") + lab}</text>')
    for i, r in enumerate(eds):
        o.append(f'<text x="{X(i):.1f}" y="{H-14}" text-anchor="middle">{r["subset"]}</text>')
        for col, key, off in ((1, "miss_1sigma", -7), (2, "miss_2sigma", 7)):
            v = float(r[key])
            ci = r[key + "_ci"].strip("[]").split(",")
            lo, hi = float(ci[0]), float(ci[1])
            x = X(i) + off
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(lo):.1f}" y2="{Y(hi):.1f}" stroke="var(--s{col})" stroke-width="2" stroke-opacity=".55"/>')
            tip = f'{r["subset"]} · {key.split("_")[1]}: {v*100:.0f}% [{lo*100:.0f}–{hi*100:.0f}%] n={r["n"]}'
            o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(v):.1f}" r="5" fill="var(--s{col})" stroke="var(--card)" stroke-width="2" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_halflife(m1, qmap, lang, W=900):
    rows = [r for r in m1 if qmap[r["qid"]]["layer"] == "K"]
    rows.sort(key=lambda r: float(r["halflife_years"]) if r["halflife_years"] != "inf" else 1e9)
    L, R, Tp, rh = 250, 30, 10, 26
    H = Tp + rh * len(rows) + 40
    xmax = 25.0

    def X(v): return L + min(v, xmax) / xmax * (W - L - R)
    name = "name_ko" if lang == "ko" else "name_en"
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="half-life by constant">']
    for v in range(0, 26, 5):
        o.append(f'<line class="grid" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{Tp}" y2="{H-34}"/><text x="{X(v):.1f}" y="{H-18}" text-anchor="middle">{v}</text>')
    o.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-2}" text-anchor="middle">{"년" if lang == "ko" else "years"}</text>')
    for i, r in enumerate(rows):
        y = Tp + rh * i + rh / 2
        o.append(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end">{esc(qmap[r["qid"]][name])}</text>')
        if r["halflife_years"] == "inf":
            o.append(f'<text x="{L+4}" y="{y+4:.1f}">{"감소 없음" if lang == "ko" else "no decline"}</text>')
            continue
        hl, lo = float(r["halflife_years"]), float(r["halflife_ci_low"])
        hi = float(r["halflife_ci_high"]) if r["halflife_ci_high"] != "inf" else xmax
        o.append(f'<line x1="{X(lo):.1f}" x2="{X(hi):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--s1)" stroke-width="2" stroke-opacity=".5"/>')
        if r["halflife_ci_high"] == "inf" or hi > xmax:
            o.append(f'<text x="{X(xmax)-2:.1f}" y="{y-4:.1f}" text-anchor="end">→</text>')
        tip = f'{qmap[r["qid"]][name]}: {hl:.1f} [{lo:.1f}–{r["halflife_ci_high"]}] n={r["n_editions"]}'
        o.append(f'<circle class="dot" cx="{X(hl):.1f}" cy="{y:.1f}" r="5" fill="var(--s1)" stroke="var(--card)" stroke-width="2" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_funnel(rows, lang, W=900, H=340):
    """G5: symmetric-log relative deviation from 2022 with ±1σ bars."""
    L, R, Tp, B = 70, 20, 16, 40
    meas = [r for r in rows if r["exact"] == "0" or float(r["rel_dev"]) != 0]
    vals = [abs(float(r["rel_dev"])) + float(r["rel_u"]) for r in meas] or [1e-9]
    small = [float(r["rel_u"]) for r in meas if float(r["rel_u"]) > 0] or [1e-12]
    lt = 10 ** math.floor(math.log10(min(small)))     # linear threshold
    top = 10 ** math.ceil(math.log10(max(vals + [lt * 10])))

    def f(v): return math.copysign(math.log10(1 + abs(v) / lt), v)
    fm = f(top)

    def X(e): return L + (EDITIONS.index(e) + 0.5) / len(EDITIONS) * (W - L - R)

    def Y(v): return Tp + (fm - f(v)) / (2 * fm) * (H - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="convergence plot">']
    e = int(round(math.log10(lt)))
    ticks = [0.0] + [s * 10.0 ** k for k in range(e + 1, int(round(math.log10(top))) + 1, max(1, (int(round(math.log10(top))) - e) // 4 or 1)) for s in (1, -1)]
    for t in sorted(set(ticks)):
        lab = "0" if t == 0 else ("−" if t < 0 else "+") + sup(int(round(math.log10(abs(t)))))
        o.append(f'<line class="{"ref" if t == 0 else "grid"}" x1="{L}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{L-6}" y="{Y(t)+4:.1f}" text-anchor="end">{lab}</text>')
    for ed in EDITIONS:
        o.append(f'<text x="{X(ed):.1f}" y="{H-14}" text-anchor="middle">{ed}</text>')
    for r in rows:
        ed = int(r["edition"])
        dv, uu = float(r["rel_dev"]), float(r["rel_u"])
        x = X(ed)
        if r["exact"] == "1":
            lab = "정의값" if lang == "ko" else "exact"
            o.append(f'<rect class="dot" x="{x-4:.1f}" y="{Y(dv)-4:.1f}" width="8" height="8" fill="var(--card)" stroke="var(--fg3)" stroke-width="1.5" data-tip="{ed}: {lab}"/>')
            continue
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(dv - uu):.1f}" y2="{Y(dv + uu):.1f}" stroke="var(--s1)" stroke-width="2"/>')
        miss = abs(dv) > uu
        tip = f"{ed}: {dv:+.2e} ± {uu:.2e}" + (" (1σ 밖)" if lang == "ko" and miss else " (outside 1σ)" if miss else "")
        o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(dv):.1f}" r="5" fill="{"var(--s1)" if not miss else "var(--card)"}" stroke="var(--s1)" stroke-width="2" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ numbers for the registry text
def numbers(qmap, m1, s2, s3, t4, summ):
    k1 = [r for r in m1 if qmap[r["qid"]]["layer"] == "K" and r["halflife_years"] != "inf"]
    k1s = sorted(k1, key=lambda r: float(r["halflife_years"]))
    core_all = {r["threshold"]: r for r in s2 if r["subset"].startswith("core: all") and r["measure"] == "z"}
    new = next(r for r in s2 if r["subset"].startswith("core: 1998") and r["measure"] == "z")
    old = next(r for r in s2 if r["subset"].startswith("core: 1969") and r["measure"] == "z")
    a3 = next(r for r in s3 if r["subset"] == "all")
    o3 = next(r for r in s3 if r["subset"] == "1969-1986")
    n3 = next(r for r in s3 if r["subset"] == "1998-2018")
    t_nz, t_new = t4[0], t4[1]
    k20 = {r["threshold"]: r for r in read("sens_candidates.csv")}

    def ci(s):
        lo, hi = s.strip("[]").split(",")
        return f"{float(lo)*100:.0f}–{float(hi)*100:.0f}%"
    return dict(
        m1_n_core=len([r for r in m1 if qmap[r["qid"]]["layer"] == "K"]), m1_n_all=len(m1),
        m1_median=f"{np.median([float(r['halflife_years']) for r in k1]):.1f}", m1_n_dec=len(k1),
        m1_median_all=f"{np.median([float(r['halflife_years']) if r['halflife_years'] != 'inf' else 1e12 for r in m1 if qmap[r['qid']]['layer'] == 'K']):.1f}",
        k20_r2=pct(k20["2"]["rate"]), k20_r3=pct(k20["3"]["rate"]), k20_m3=pct(k20["1/2 sigma"]["rate"].split("/")[1], 0),
        m1_min_name=qmap[k1s[0]["qid"]]["name_ko"], m1_min_name_en=qmap[k1s[0]["qid"]]["name_en"], m1_min=f"{float(k1s[0]['halflife_years']):.1f}",
        m1_max_name=qmap[k1s[-1]["qid"]]["name_ko"], m1_max_name_en=qmap[k1s[-1]["qid"]]["name_en"], m1_max=f"{float(k1s[-1]['halflife_years']):.1f}",
        m2_n=core_all["1"]["n_pairs"], m2_q=core_all["1"]["n_quantities"], m2_n_new=new["n_pairs"], m2_n_old=old["n_pairs"],
        m2_r1=pct(core_all["1"]["rate"]), m2_r1_ci=ci_pct(core_all["1"]["ci_low"], core_all["1"]["ci_high"]),
        m2_r2=pct(core_all["2"]["rate"]), m2_r2_ci=ci_pct(core_all["2"]["ci_low"], core_all["2"]["ci_high"]),
        m2_r3=pct(core_all["3"]["rate"]), m2_r3_ci=ci_pct(core_all["3"]["ci_low"], core_all["3"]["ci_high"]),
        m2_zero=summ["n_zero_change_pairs"],
        m2_x2=f"{float(core_all['2']['rate']) / 0.0455:.1f}", m2_x3=f"{float(core_all['3']['rate']) / 0.0027:.0f}",
        m2_1in2=f"{1 / float(core_all['2']['rate']):.0f}", m2_1in3=f"{1 / float(core_all['3']['rate']):.0f}",
        m3_m2_10=f"{float(next(r for r in s3 if r['subset'] == 'all')['miss_2sigma']) * 10:.0f}",
        m3_n=a3["n"], m3_q=a3["n_quantities"], m3_m1=pct(a3["miss_1sigma"], 0), m3_m1_ci=ci(a3["miss_1sigma_ci"]),
        m3_m2=pct(a3["miss_2sigma"], 0), m3_m2_ci=ci(a3["miss_2sigma_ci"]), m3_si=pct(a3["surprise"], 0), m3_si_ci=ci(a3["surprise_ci"]),
        m3_old_m2=pct(o3["miss_2sigma"], 0), m3_new_m2=pct(n3["miss_2sigma"], 0),
        m4_n=t_nz["n_pairs"], m4_nu=t_nz["nu"], m4_nu_ci=f"{t_nz['nu_ci_low']}–{t_nz['nu_ci_high']}", m4_s=t_nz["scale"],
        m4_s_ci=f"{t_nz['scale_ci_low']}–{t_nz['scale_ci_high']}", m4_new_nu=t_new["nu"], m4_new_nu_ci=f"{t_new['nu_ci_low']}–{t_new['nu_ci_high']}",
    )


GLOSS = {"ko": '<div class="note"><b>불확도(uncertainty)</b> — 측정값이 참값에서 벗어나 있을 수 있는 폭을 표준편차로 나타낸 값이다. 그림의 오차 막대(±1σ) 길이가 이것이다. 참값과의 실제 차이인 「오차(error)」와 달리, 불확도는 그 차이가 얼마쯤일지에 대한 추정이다. 계측 분야의 표준 용어로, 한국산업표준 KS Q ISO/IEC GUIDE 98-3 「측정불확도 표현 지침」이 이 말을 쓴다. 이 사이트가 재는 것은 그 추정한 폭이 판이 바뀔 때의 실제 이동을 담았는가이다.</div><div class="note"><b>판(edition)</b> — CODATA 기본상수 작업반이 그때까지 나온 측정과 이론 계산을 모두 모아 최소제곱 조정을 한 번 하고, 그 결과로 공표하는 권고값 한 벌이다. 판의 이름은 반영한 자료의 마감 연도다(예: 2022 판은 2022년 말까지의 자료로 만들어 2024년에 공표). 1973·1986 판 뒤 1998 판부터는 4년마다 나왔다. 1969 판은 CODATA 이전의 개인 연구진(Taylor·Parker·Langenberg) 조정값으로, 비교를 위해 함께 싣는다. 판이 바뀌면 같은 상수의 값과 불확도가 함께 바뀐다 — 이 사이트는 그 변화를 센다.</div>', "en": '<div class="note"><b>Uncertainty</b> — the width, expressed as a standard deviation, within which a measured value may differ from the true value; the length of the ±1σ error bars in the plots. Unlike the error, the actual difference from the true value, the uncertainty is an estimate of how large that difference may be. It is the standard term in metrology (ISO/IEC Guide 98-3, the Guide to the Expression of Uncertainty in Measurement). What this site measures is whether that estimated width covered the actual moves between editions.</div><div class="note"><b>Edition</b> — one set of recommended values published by the CODATA Task Group on Fundamental Constants after a least-squares adjustment of all the measurements and theoretical calculations available at the time. An edition is named after the closing year of its data (the 2022 edition uses data to the end of 2022 and was published in 2024). After the 1973 and 1986 editions, one has appeared every four years since 1998. The 1969 edition is the pre-CODATA adjustment by Taylor, Parker and Langenberg, included for comparison. With each new edition the values and uncertainties of the same constants change; this site counts those changes.</div>'}


def takeaway(lang, items):
    """The page's takeaway box: two or three sentences a reader should leave with."""
    items = [i for i in items if i]
    if not items:
        return ""
    lab = "핵심" if lang == "ko" else "Takeaway"
    return f'<div class="takeaway"><b>{lab}</b><ul>' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul></div>"


def spec_block(m, lang, N):
    t, d = T[lang], m[lang]
    return f"""<div class="spec"><dl>
<dt>{t['definition']}</dt><dd>{esc(d['definition'])}</dd>
<dt>{t['formula']}</dt><dd class="formula">{esc(d['formula'])}</dd>
<dt>{t['denominator']}</dt><dd>{esc(d['denominator'].format(**N))}</dd>
<dt>{t['howto']}</dt><dd>{esc(d['reading'].format(**N))}</dd>
<dt>{t['caveat']}</dt><dd>{esc(d['caveat'].format(**N))}</dd></dl></div>"""


def fmt_sci(v, sig=2) -> str:
    """6.8e-18 -> '6.8×10⁻¹⁸' (sig significant digits)."""
    x = float(v)
    if x == 0:
        return "0"
    m, e = f"{x:.{sig - 1}e}".split("e")
    return f"{m}×{sup(int(e))}"


def build():
    if OUT.exists():
        for child in OUT.iterdir():
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    OUT.mkdir(exist_ok=True)
    qmap = {r["qid"]: r for r in read("quantity_map.csv")}
    long = read("constants_long.csv")
    m1 = read("m1_halflife.csv")
    pairs = read("m2_pairs.csv")
    s2 = read("m2_summary.csv")
    m3r = read("m3_vs_latest.csv")
    s3 = read("m3_summary.csv")
    t4 = read("m4_tail.csv")
    m5 = read("m5_funnel.csv")
    m6 = read("m6_events.csv")
    hf = read("hf_repro.csv")
    sens = read("sens_all_rows.csv")
    summ = json.loads((DER / "summary.json").read_text(encoding="utf-8"))
    N = numbers(qmap, m1, s2, s3, t4, summ)
    kp = [p for p in pairs if p["layer"] == "K"]
    order = [q for q in qmap]  # map order: core first, then display

    (OUT / "data").mkdir()
    for f in PUBLIC_DATA:
        shutil.copy(DER / f, OUT / "data" / f)
    datapackage = dict(name="physical-constants-metrics", version=VERSION, created=BUILD_DATE,
                       licenses=[dict(name="CC-BY-4.0", path="https://creativecommons.org/licenses/by/4.0/")],
                       sources=[dict(title="CODATA recommended values (NIST)", path=SOURCES["codata"]["url"]),
                                dict(title="Taylor, Parker & Langenberg 1969", path=SOURCES["tpl1969"]["url"])],
                       resources=[dict(path=f"data/{f}", description=DATA_DESC[f][1], format="csv") for f in PUBLIC_DATA])
    shutil.copy(ROOT / "data" / "raw" / "manifest.json", OUT / "data" / "raw_manifest.json")
    (OUT / "data" / "datapackage.json").write_text(json.dumps(datapackage, indent=1, ensure_ascii=False), encoding="utf-8")

    for lang in ("ko", "en"):
        t = T[lang]
        name = "name_ko" if lang == "ko" else "name_en"
        base = OUT / lang
        (base / "metrics").mkdir(parents=True)
        (base / "constants").mkdir()

        # ---------- home
        g1, med = chart_uncertainty(qmap, long, lang)
        c2 = {r["threshold"]: r for r in s2 if r["subset"].startswith("core: all") and r["measure"] == "z"}
        a3 = next(r for r in s3 if r["subset"] == "all")
        if lang == "ko":
            hero = f"""<div class="hero"><h1>{t['site']}</h1><p class="lead">과학자들이 스스로 밝힌 오차 막대는 다음 판의 값을 얼마나 자주 놓쳤나. 국제과학위원회(ISC) 산하 과학기술데이터위원회(CODATA)가 1973년부터 내 온 기본 물리 상수 권고값 아홉 판과 그 직전의 1969년 조정값을 이어 붙여, 값과 불확도가 판마다 어떻게 바뀌었는지 센다.</p></div>"""
            stats_h = f"""<div class="stats">
<a class="stat" href="metrics/m2.html"><span class="n">{N['m2_r2']}%</span><span class="vs">기대 4.6%</span><small>연속한 두 판 사이 이동이 두 불확도의 2배를 넘은 비율 (판 쌍 {N['m2_n']}개, 핵심 상수 {N['m2_q']}개, 95% 구간 {N['m2_r2_ci']})</small></a>
<a class="stat" href="metrics/m2.html"><span class="n">{N['m2_r3']}%</span><span class="vs">기대 0.27%</span><small>같은 이동이 3배를 넘은 비율 (95% 구간 {N['m2_r3_ci']})</small></a>
<a class="stat" href="metrics/m3.html"><span class="n">{N['m3_m2']}%</span><span class="vs">기대 4.6%</span><small>옛 판의 ±2σ 막대가 2022 판 값을 담지 못한 비율 ({N['m3_n']}개 조합, 95% 구간 {N['m3_m2_ci']})</small></a>
<a class="stat" href="metrics/m1.html"><span class="n">{N['m1_median']}년</span><small>핵심 상수의 상대 불확도가 절반으로 줄어드는 데 걸린 햇수, 중앙값 (상수 {N['m1_n_core']}개 중 불확도가 줄어든 {N['m1_n_dec']}개)</small></a></div>"""
            g1cap = f"점 하나가 (판, 핵심 상수) 하나, 선은 판별 중앙값. 세로축은 로그. 중앙값은 1969 판 {fmt_sci(med[0][1])}(상수 {med[0][2]}개), 2022 판 {fmt_sci(med[-1][1])}({med[-1][2]}개). 판마다 들어간 상수가 달라(예: 양성자 전하 반지름은 2002 판부터) 중앙값이 판 사이에서 거꾸로 오르기도 한다."
            intro2 = """<div class="prose"><p>불확도는 반세기 동안 만 배 이상 줄었다. 그런데 판이 바뀔 때 값이 움직인 폭은 그 불확도로 설명되는 범위를 자주 넘었다. 이 사이트는 그 비율을 상수별·판별로 공개하고, 같은 질문을 먼저 던진 연구(Henrion & Fischhoff 1986, Bailey 2017)와 나란히 둔다. 수치마다 표본 수와 95% 구간을 붙였다. 「과학자가 과신했다」는 해석은 측정 설계를 들여다본 결과가 아니므로 지표 면에는 쓰지 않는다 — <a href="reading.html">읽기</a>에서 유보와 함께 다룬다.</p></div>"""
        else:
            hero = f"""<div class="hero"><h1>{t['site']}</h1><p class="lead">How often did the error bars that scientists published miss the next edition's value? This site joins the nine editions of the CODATA recommended values of the fundamental physical constants (1973–2022) and the 1969 adjustment that preceded them, and counts how values and uncertainties changed from edition to edition.</p></div>"""
            stats_h = f"""<div class="stats">
<a class="stat" href="metrics/m2.html"><span class="n">{N['m2_r2']}%</span><span class="vs">normal 4.6%</span><small>Moves between consecutive editions larger than twice the combined uncertainty ({N['m2_n']} pairs, {N['m2_q']} core constants, 95% interval {N['m2_r2_ci']})</small></a>
<a class="stat" href="metrics/m2.html"><span class="n">{N['m2_r3']}%</span><span class="vs">normal 0.27%</span><small>The same, larger than three times (95% interval {N['m2_r3_ci']})</small></a>
<a class="stat" href="metrics/m3.html"><span class="n">{N['m3_m2']}%</span><span class="vs">normal 4.6%</span><small>Earlier ±2σ error bars that do not contain the 2022 value ({N['m3_n']} combinations, 95% interval {N['m3_m2_ci']})</small></a>
<a class="stat" href="metrics/m1.html"><span class="n">{N['m1_median']} y</span><small>Median time for a core constant's relative uncertainty to halve (the {N['m1_n_dec']} of {N['m1_n_core']} core constants whose uncertainty declined)</small></a></div>"""
            g1cap = f"One dot per (edition, core constant); the line is the median per edition. Log scale. Median {fmt_sci(med[0][1])} in 1969 ({med[0][2]} constants), {fmt_sci(med[-1][1])} in 2022 ({med[-1][2]}). The set of constants changes between editions (the proton charge radius enters in 2002, for example), so the median can rise from one edition to the next."
            intro2 = """<div class="prose"><p>Uncertainties shrank by more than four orders of magnitude in half a century. Yet the moves between editions often exceeded what those uncertainties allow. This site publishes those rates by constant and by edition, next to the earlier studies that asked the same question (Henrion & Fischhoff 1986; Bailey 2017). Every number carries its sample size and a 95% interval. "Scientists were overconfident" is an interpretation that would require looking into the measurements themselves, so the metric pages do not use it; the <a href="reading.html">reading edition</a> takes it up with its qualifications.</p></div>"""
        cards = "".join(f'<a class="card" href="metrics/{m["id"]}.html"><b>{m["id"].upper()} · {esc(m[lang]["name"])}</b><small>{esc(m[lang]["short"])}</small></a>' for m in METRICS)
        cards += f'<a class="card" href="metrics/hf.html"><b>{"재계산" if lang == "ko" else "Recalculation"} · Henrion & Fischhoff</b><small>{"1986년 논문의 지표를 이 자료로 다시 계산" if lang == "ko" else "Their 1986 indices recomputed on these data"}</small></a>'
        hf22 = next(r for r in hf if r["reference"] == "2022" and r["qid"] == "ALL")
        if lang == "ko":
            tk = ["과학자들은 상수 값마다 「참값은 대략 이 범위 안에 있다」는 오차 막대를 함께 발표한다. 반세기 동안 이 막대는 만 배 넘게 좁아졌다.",
                  f"그런데 새 판이 나올 때 값이 막대 폭의 2배 넘게 움직인 경우가 약 {N['m2_1in2']}번에 1번이었다. 막대가 맞다면 22번에 1번이어야 한다. 3배 넘게 움직인 경우도 약 {N['m2_1in3']}번에 1번으로, 기대치(370번에 1번)보다 훨씬 잦았다.",
                  f"옛 판의 넉넉한 막대(±2σ)를 오늘의 값에 대 보면 10개 중 약 {N['m3_m2_10']}개가 빗나간다. 막대가 좁아진 최근 판도 이 비율은 줄지 않았다.",
                  "왜 그런지 — 과신인지, 몰랐던 오차인지, 값을 모으는 절차 탓인지 — 는 이 자료만으로는 가릴 수 없다."]
        else:
            tk = ["Scientists publish each constant with error bars that say the true value is probably inside this range. Over half a century these bars narrowed more than ten-thousand-fold.",
                  f"Yet when a new edition came out, a value moved by more than twice its bars about once in {N['m2_1in2']} times, where the bars imply once in 22; by more than three times about once in {N['m2_1in3']}, against an expected once in 370.",
                  f"Hold the generous bars (±2σ) of earlier editions against today's values and about {N['m3_m2_10']} in 10 miss. Recent editions, with far narrower bars, miss no less often.",
                  "Why — overconfidence, unknown errors, or the way values are combined — cannot be told from these data alone."]
        gloss = GLOSS[lang]
        body = hero + takeaway(lang, tk) + stats_h + f'<figure>{g1}<figcaption>{esc(g1cap)}</figcaption></figure>' + intro2 + gloss + f'<h2>{t["metrics"]}</h2><div class="cards">{cards}</div>'
        (base / "index.html").write_text(page(lang, t["home"], body, 1, "home"), encoding="utf-8")

        # ---------- metric pages
        lst = "".join(f'<a class="card" href="{m["id"]}.html"><b>{m["id"].upper()} · {esc(m[lang]["name"])}</b><small>{esc(m[lang]["short"])}</small></a>' for m in METRICS)
        lst += f'<a class="card" href="hf.html"><b>Henrion & Fischhoff</b><small>{"1986년 지표 재계산" if lang == "ko" else "1986 indices recomputed"}</small></a>'
        mtk = (["M1 은 불확도가 얼마나 빨리 줄었는지, M2~M4 는 그 불확도가 판간 이동을 얼마나 설명했는지, M5·M6 은 상수별 경과와 정의값 전환을 본다.", "모든 수치에 표본 수와 95% 구간이 붙어 있고, 정의·공식·분모·한계는 각 면에 있다."] if lang == "ko" else
               ["M1 shows how fast uncertainties fell; M2–M4 how well those uncertainties covered the moves between editions; M5 and M6 the history of each constant and the transitions to exact values.", "Every number carries its sample size and a 95% interval; definitions, formulas, denominators and caveats are on each page."])
        (base / "metrics" / "index.html").write_text(page(lang, t["metrics"], f"<h1>{t['metrics']}</h1>{takeaway(lang, mtk)}<div class='cards'>{lst}</div>", 2, "metrics"), encoding="utf-8")

        for m in METRICS:
            d = m[lang]
            parts = [f'<p><span class="tag k">{m["id"].upper()}</span></p><h1>{esc(d["name"])}</h1><p class="lead">{esc(d["short"])}</p>',
                     takeaway(lang, [x.format(**N) for x in m["takeaway"][lang]]), spec_block(m, lang, N)]
            if m["id"] == "m1":
                parts.append(f'<figure>{chart_halflife(m1, qmap, lang)}<figcaption>{"점은 반감기, 가로선은 95% 구간(화살표는 25년 넘게 열린 구간)." if lang == "ko" else "Dot = half-life; bar = 95% interval (arrow: open beyond 25 years)."}</figcaption></figure>')
                rows = []
                for r in sorted(m1, key=lambda r: (qmap[r["qid"]]["layer"], r["qid"])):
                    hl = r["halflife_years"]
                    rows.append([f'<a href="../constants/{r["qid"]}.html">{esc(qmap[r["qid"]][name])}</a>',
                                 {"K": t["core"], "D": t["display"], "S": t["cand"]}[qmap[r["qid"]]["layer"]], r["n_editions"], f'{r["first"]}–{r["last"]}',
                                 r["u_rel_first"], r["u_rel_last"],
                                 (t["none"] if hl == "inf" else hl, 1e9 if hl == "inf" else hl),
                                 "" if hl == "inf" else f'{r["halflife_ci_low"]}–{r["halflife_ci_high"]}', r["r2"]])
                parts.append(table([t["name"], t["layer"], t["n_ed"], t["edition"], f'{t["urel"]} ({"처음" if lang == "ko" else "first"})',
                                    f'{t["urel"]} ({"마지막" if lang == "ko" else "last"})', t["halflife"], t["ci"], "R²"], rows, num_cols=(2, 4, 5, 6, 7, 8)))
            if m["id"] == "m2":
                parts.append(f'<figure><div class="legend"><span style="--c:var(--s1)">{"관측" if lang == "ko" else "observed"}</span><span style="--c:var(--s2)">{"정규분포" if lang == "ko" else "normal"}</span><span style="--c:var(--s3)">Student-t ({"값이 바뀐 쌍에 맞춤" if lang == "ko" else "fitted to pairs with a change"})</span></div>{chart_tail(kp, float(t4[0]["nu"]), float(t4[0]["scale"]), lang)}<figcaption>{"|z| 가 가로축 값을 넘는 판 쌍의 비율(세로축 로그). 점은 |z|>1·2·3 의 관측 비율." if lang == "ko" else "Share of pairs with |z| above the horizontal value (log vertical axis). Dots: observed shares above 1, 2, 3."}</figcaption></figure>')
                lab = {"core: all consecutive pairs": ("전체 판 쌍", "all pairs"), "core: 1998-2022 (4-year gaps)": ("1998~2022 (4년 간격)", "1998–2022 (4-year gaps)"),
                       "core: 1969-1998 (4-13-year gaps)": ("1969~1998 (4~13년 간격)", "1969–1998 (4–13-year gaps)")}
                rows = [[lab[r["subset"]][0 if lang == "ko" else 1], "z" if r["measure"] == "z" else "z_old", f'|z|>{r["threshold"]}', r["n_pairs"], r["n_quantities"],
                         r["exceed"], pct(r["rate"]), ci_pct(r["ci_low"], r["ci_high"]), pct(r["normal"], 2)] for r in s2]
                parts.append(table([t["subset"], "z", t["threshold"], t["pairs"], t["quantities"], "n", t["rate"] + " %", t["ci"], t["normal"] + " %"], rows, num_cols=(3, 4, 5, 6, 8)))
                big = sorted(kp, key=lambda p: -abs(float(p["z"])))[:12]
                parts.append(f'<h3>{"이동이 컸던 판 쌍" if lang == "ko" else "Largest moves"}</h3>')
                parts.append(table([t["name"], t["edition"], "z", "z_old"], [[f'<a href="../constants/{p["qid"]}.html">{esc(qmap[p["qid"]][name])}</a>', f'{p["ed_from"]}→{p["ed_to"]}', p["z"], p["z_old"]] for p in big], num_cols=(2, 3)))
                s = sens
                parts.append(f'<div class="note">{"민감도 — 1998~2022 ASCII 표에서 이름이 바뀌지 않은 모든 행(서로 환산 관계인 행 포함)으로 같은 계산을 하면" if lang == "ko" else "Sensitivity — repeating the calculation over every 1998–2022 ASCII row whose name did not change (including rows that are conversions of one another):"} |z|>1 {pct(s[0]["rate"])}%, |z|>2 {pct(s[1]["rate"])}%, |z|>3 {pct(s[2]["rate"])}% ({s[0]["n_pairs"]} {t["pairs"]}). {"같은 이동이 여러 행에 중복해 세어지므로 표본 수는 부풀어 있다." if lang == "ko" else "The same move is counted in many rows, so the count is inflated."}</div>')
            if m["id"] == "m3":
                parts.append(f'<figure><div class="legend"><span style="--c:var(--s1)">±1σ {"밖" if lang == "ko" else "missed"}</span><span style="--c:var(--s2)">±2σ {"밖" if lang == "ko" else "missed"}</span><span class="dash" style="--c:var(--ref)">{"정규 기대" if lang == "ko" else "normal expectation"}</span></div>{chart_miss(s3, lang)}<figcaption>{"판별로 그 판과 2022 판에 모두 있는 핵심 상수 중 옛 오차 막대가 2022 판 값을 담지 못한 비율. 세로선은 상수 군집 부트스트랩 95% 구간." if lang == "ko" else "By edition, the share of core constants whose earlier error bar does not contain the 2022 value. Vertical bars: 95% cluster-bootstrap intervals."}</figcaption></figure>')
                sub = {"1969-1986": ("1969~1986 묶음", "1969–1986 pooled"), "1998-2018": ("1998~2018 묶음", "1998–2018 pooled"), "all": ("전체", "all")}
                rows = [[sub.get(r["subset"], (r["subset"], r["subset"]))[0 if lang == "ko" else 1], r["n"], r["n_quantities"], pct(r["miss_1sigma"], 0), cip(r["miss_1sigma_ci"]), pct(r["miss_2sigma"], 0), cip(r["miss_2sigma_ci"]),
                         pct(r["inside_iq"], 0), pct(r["surprise"], 0), r["median_abs_z"]] for r in s3]
                parts.append(table([t["edition"], "n", t["quantities"], "1σ %", t["ci"], "2σ %", t["ci"], "IQ %", "SI %", "median |z|"], rows, num_cols=(1, 2, 3, 5, 7, 8, 9)))
            if m["id"] == "m4":
                lab = {"core: pairs with a change": ("값이 바뀐 판 쌍", "pairs with a change"), "core: pairs with a change, 1998-2022": ("값이 바뀐 판 쌍, 1998~2022", "pairs with a change, 1998–2022")}
                rows = [[lab[r["subset"]][0 if lang == "ko" else 1], r["n_pairs"], r["n_quantities"], r["nu"], f'{r["nu_ci_low"]}–{r["nu_ci_high"]}', r["scale"], f'{r["scale_ci_low"]}–{r["scale_ci_high"]}'] for r in t4]
                rows.append(["Bailey 2017 (" + ("상수, 개별 측정 쌍" if lang == "ko" else "constants, pairs of individual measurements") + ")", "9,098", "7", "1.81 ± 0.15", "", "0.89 ± 0.06", ""])
                parts.append(table([t["subset"], t["pairs"], t["quantities"], "ν", t["ci"], "s", t["ci"]], rows, num_cols=(1, 2, 3, 5)))
            if m["id"] == "m5":
                parts.append('<div class="cards">' + "".join(f'<a class="card{"" if qmap[q]["layer"] == "K" else " d"}" href="../constants/{q}.html"><b>{esc(qmap[q]["symbol"])} · {esc(qmap[q][name])}</b></a>' for q in order) + "</div>")
            if m["id"] == "m6":
                dirl = {"measured->exact": ("측정값 → 정의값", "measured → exact"), "exact->measured": ("정의값 → 측정값", "exact → measured")}
                rows = [[f'<a href="../constants/{r["qid"]}.html">{esc(qmap[r["qid"]][name])}</a>', f'{r["ed_before"]}→{r["ed_after"]}', dirl[r["direction"]][0 if lang == "ko" else 1], r["u_rel_measured"]] for r in sorted(m6, key=lambda r: (r["ed_after"], r["qid"]))]
                parts.append(table([t["name"], t["edition"], "", t["urel"] + (" (측정값일 때)" if lang == "ko" else " (when measured)")], rows, num_cols=(3,)))
            parts.append(f'<p class="files"><a href="../../data/{m["file"]}">{t["download"]}: {m["file"]}</a></p>')
            (base / "metrics" / f'{m["id"]}.html').write_text(page(lang, d["name"], "".join(parts), 2, "metrics"), encoding="utf-8")

        # ---------- Henrion & Fischhoff page
        r73 = [r for r in hf if r["reference"] == "1973" and r["qid"] != "ALL"]
        all73 = next(r for r in hf if r["reference"] == "1973" and r["qid"] == "ALL")
        all22 = next(r for r in hf if r["reference"] == "2022" and r["qid"] == "ALL")
        if lang == "ko":
            hfb = f"""<h1>Henrion & Fischhoff (1986) 지표 재계산</h1><p class="lead">이들의 표 I 마지막 줄은 1929~1969년 권고값 여덟 개 검토의 상수 다섯 개(α⁻¹, e, h, mₑ, N_A)를 1973 판 값과 견주어 사분위 지수(IQ) 22%, 놀람 지수(SI) 57% 를 보고했다(정규 기대 50%, 2%). 1.0 은 1969 판까지만 갖고 있어 같은 계산의 일부를 다시 하고, 기준을 2022 판으로 옮긴 계산을 함께 싣는다. 그들과 1973 보고서 표 34.2 처럼 α 가 아닌 α⁻¹ 로 계산한다.</p>
<div class="prose"><ul><li>1969 판 → 1973 판 기준 (그들과 같은 기준, 상수 5개): {esc(all73['z_old'])}.</li><li>1969~2018 판 → 2022 판 기준 (상수 5개, 측정값이던 판만 {esc(all22['edition'])}): {esc(all22['z_old'])}.</li></ul>
<p>z = (기준 판 값 − 옛 값) / 옛 불확도. IQ 는 |z|<0.674, SI 는 |z|>2.326 인 비율, RMS 는 z 의 제곱평균제곱근이다. 1969→1973 의 e·h·mₑ·N_A 변화를 ppm 으로 바꾸면 −1.56·−3.02·−2.63·−20.6 으로, 1973 보고서 표 34.2 의 −1.6·−3.0·−2.6·−21 과 맞는다. α⁻¹ 는 +0.146 ppm(표 34.2: +0.15). 원 논문 표 I 의 22%·57% 는 공개 사본(OCR)에서 읽은 값이고 출판본과 대조하지 못했다. 1929~1963 판(Birge, DuMond–Cohen 등)은 1.1 이후에 넣는다.</p></div>"""
        else:
            hfb = f"""<h1>Henrion & Fischhoff (1986) indices, recomputed</h1><p class="lead">The last row of their table I compared five constants (α⁻¹, e, h, mₑ, N_A) in eight reviews from 1929 to 1969 with the 1973 values and reported an interquartile index of 22% and a surprise index of 57% (normal: 50% and 2%). Version 1.0 reaches back only to 1969, so it repeats part of that calculation and adds the same calculation against the 2022 edition. As in their paper and in table 34.2 of the 1973 report, α⁻¹ is used rather than α.</p>
<div class="prose"><ul><li>1969 edition against 1973 (their reference, five constants): {esc(all73['z_old'])}.</li><li>1969–2018 editions against 2022 (five constants, editions in which they were measured, {esc(all22['edition'])}): {esc(all22['z_old'])}.</li></ul>
<p>z = (reference value − earlier value) / earlier uncertainty. IQ is the share with |z| < 0.674, SI the share with |z| > 2.326, RMS the root mean square of z. The 1969→1973 changes of e, h, mₑ and N_A are −1.56, −3.02, −2.63 and −20.6 ppm, matching −1.6, −3.0, −2.6 and −21 in table 34.2 of the 1973 report; α⁻¹ changes by +0.146 ppm (table: +0.15). The 22% and 57% of their table I were read from a public OCR copy and have not been checked against the published version. The 1929–1963 reviews (Birge, DuMond–Cohen and others) are planned for 1.1 or later.</p></div>"""
        si22 = pct(all22["z_old"].split("SI=")[1].split()[0], 0)
        hftk = ([f"1969→1973 에서 다섯 상수 가운데 아보가드로 상수 하나가 옛 σ 의 3.1배를 움직였다. 나머지 넷은 0.5배 안이다.", f"2022 판을 기준으로 하면 1969~2018 판의 다섯 상수 {all22['edition'].split('=')[1]}건 중 {si22}% 가 98% 구간 밖이다(정규 기대 2%)."] if lang == "ko" else
                [f"From 1969 to 1973, one of the five constants, the Avogadro constant, moved by 3.1 old σ; the other four by less than 0.5.", f"Against the 2022 edition, {si22}% of {all22['edition'].split('=')[1]} values of the five constants in the 1969–2018 editions lie outside their 98% interval (normal: 2%)."])
        hfb = hfb.replace("</h1>", "</h1>" + takeaway(lang, hftk), 1)
        rows = [[esc(qmap[r["qid"]][name]), r["edition"], r["reference"], r["z_old"]] for r in hf if r["qid"] != "ALL"]
        hfb += table([t["name"], t["edition"], "ref", "z"], rows, num_cols=(3,)) + '<p class="files"><a href="../../data/hf_repro.csv">CSV: hf_repro.csv</a></p>'
        (base / "metrics" / "hf.html").write_text(page(lang, "Henrion & Fischhoff", hfb, 2, "metrics"), encoding="utf-8")

        # ---------- constants
        lst = []
        for layer, lab in (("K", t["core"]), ("D", t["display"]), ("S", t["cand"])):
            lst.append(f"<h2>{lab}</h2><div class='cards'>")
            for q in order:
                if qmap[q]["layer"] != layer:
                    continue
                lst.append(f'<a class="card{"" if layer == "K" else " d"}" href="{q}.html"><b>{esc(qmap[q]["symbol"])} · {esc(qmap[q][name])}</b><small>{esc(qmap[q]["name_en"] if lang == "ko" else qmap[q]["name_ko"])}</small></a>')
            lst.append("</div>")
        intro = ("<p class='lead'>핵심 상수 17개는 서로 정확한 환산 관계가 없도록 골랐고 M2~M4 의 분모다(M1·M3 은 판별로 측정값인 것만). 표시용 상수 11개는 널리 쓰이지만 핵심 상수의 조합이거나 정의값 전환(M6)을 보여 주려고 싣는다 — 통계에는 넣지 않는다. 민감도 후보 3개는 같은 선정 규칙에 맞아 민감도 계산에만 쓴다.</p>" if lang == "ko"
                 else "<p class='lead'>The 17 core constants were chosen so that none is an exact function of the others; they form the denominator of M2–M4 (M1 and M3 use those measured in the relevant editions). The 11 display constants are widely used but are combinations of core constants, or illustrate the exact-value transitions (M6); they are not in the statistics. The 3 sensitivity candidates meet the same selection rule and are used only in the sensitivity checks.</p>")
        ctk = (["상수마다 판별 값·불확도·원 표기·원자료 위치와 수렴 그림이 있다.", "핵심 상수 17개만 통계에 들어간다. 표시용 상수는 핵심 상수의 조합이거나 정의값 전환을 보여 준다."] if lang == "ko" else
               ["Each constant has its values, uncertainties, printed forms, source locations and a convergence plot by edition.", "Only the 17 core constants enter the statistics; display constants are combinations of them or illustrate the exact-value transitions."])
        (base / "constants" / "index.html").write_text(page(lang, t["constants"], f"<h1>{t['constants']}</h1>{takeaway(lang, ctk)}{intro}{''.join(lst)}", 2, "constants"), encoding="utf-8")

        prev_z = {(p["qid"], int(p["ed_to"])): p["z"] for p in pairs}
        lat = {(r["qid"], int(r["edition"])): r["z_old"] for r in m3r}
        for q in order:
            qm = qmap[q]
            rows = [r for r in long if r["qid"] == q]
            fr = [r for r in m5 if r["qid"] == q]
            tab = []
            for r in sorted(rows, key=lambda r: int(r["edition"])):
                e = int(r["edition"])
                tab.append([str(e), esc(r["value_text"]), fmt_sci(r["u"]) if r["exact"] == "0" else "", (fmt_sci(r["u_rel"]) if r["exact"] == "0" else "", r["u_rel"]),
                            t["yes"] if r["exact"] == "1" else "", prev_z.get((q, e), ""), lat.get((q, e), ""), esc(r["source"].replace("_allascii.txt", " ASCII"))])
            note = NOTE_KO.get(q, "") if lang == "ko" else qm["note_en"]
            hl = next((r for r in m1 if r["qid"] == q), None)
            hl_txt = ""
            if hl:
                hl_txt = (f'{t["halflife"]}: {t["none"] if hl["halflife_years"] == "inf" else hl["halflife_years"] + " (" + hl["halflife_ci_low"] + "–" + hl["halflife_ci_high"] + ")"}')
            ctk = constant_takeaway(lang, q, qm, rows, pairs, m3r, m6)
            basis = f'<dt>{t["basis"]}</dt><dd>{esc(qm["name_ko_basis"])}</dd>' if lang == "ko" else ""
            body = f"""<p><span class="tag{" k" if qm["layer"] == "K" else ""}">{ {"K": t["core"], "D": t["display"], "S": t["cand"]}[qm["layer"]] }</span></p>
<h1>{esc(qm["symbol"])} · {esc(qm[name])}</h1><p class="lead">{esc(qm["name_en"] if lang == "ko" else qm["name_ko"])}</p>
{takeaway(lang, ctk)}<div class="spec"><dl><dt>{t["unit"]}</dt><dd>{esc(qm["unit"]) if qm["unit"] != "1" else ("없음(무차원)" if lang == "ko" else "none (dimensionless)")}</dd>{basis}<dt>{"메모" if lang == "ko" else "Note"}</dt><dd>{esc(note) or "—"}</dd><dt>M1</dt><dd>{esc(hl_txt) or "—"}</dd></dl></div>
<figure><div class="legend"><span style="--c:var(--s1)">{"판별 값 ±1σ" if lang == "ko" else "value ±1σ by edition"}</span><span class="dash" style="--c:var(--ref)">2022</span></div>{chart_funnel(fr, lang)}
<figcaption>{"2022 판 값에서의 상대 편차(대칭 로그 축). 속이 빈 원은 오차 막대가 2022 판 값에 닿지 않은 판, 네모는 정의값." if lang == "ko" else "Relative deviation from the 2022 value (symmetric-log axis). Open circles: the error bar does not reach the 2022 value. Squares: exact."}</figcaption></figure>
{table([t["edition"], t["printed"], t["u"], t["urel"], t["exact"], t["z_prev"], t["z_latest"], t["source"]], tab, num_cols=(2, 3, 5, 6))}"""
            (base / "constants" / f"{q}.html").write_text(page(lang, qm[name], body, 2, "constants"), encoding="utf-8")

        # ---------- reading, prior, method, data
        (base / "reading.html").write_text(page(lang, t["reading"], reading_page(lang, N), 1, "reading"), encoding="utf-8")
        (base / "prior.html").write_text(page(lang, t["prior"], prior_page(lang), 1, "prior"), encoding="utf-8")
        (base / "method.html").write_text(page(lang, t["method"], method_page(lang, N), 1, "method"), encoding="utf-8")
        rows = [[f'<a href="../data/{f}">{f}</a>', esc(DATA_DESC[f][0 if lang == "ko" else 1])] for f in PUBLIC_DATA]
        lic = ("<p>파생 표(아래 CSV)는 CC BY 4.0. 원 수치는 NIST가 공개한 CODATA 권고값과 1969년 논문의 표에서 옮겼고, 각 행에 원자료 위치를 적었다. NIST의 원 파일(ASCII 표·PDF)은 이 저장소에 싣지 않는다 — NIST는 표준참조자료(SRD)의 복제에 사전 허락을 요구한다고 밝힌다. 원 파일의 주소·내려받은 날짜·SHA-256 은 <a href='../data/raw_manifest.json'>raw_manifest.json</a> 에 있다.</p>" if lang == "ko"
               else "<p>The derived tables below are CC BY 4.0. The underlying values were taken from the CODATA recommended values published by NIST and from the 1969 paper's table; every row records its source location. NIST's original files (ASCII tables, PDFs) are not included: NIST states that its Standard Reference Data may not be reproduced without prior permission. Their URLs, retrieval dates and SHA-256 hashes are in <a href='../data/raw_manifest.json'>raw_manifest.json</a>.</p>")
        dtk = (["파생 CSV 15개와 datapackage.json 을 내려받을 수 있다. 파생 데이터는 CC BY 4.0 이다.", "NIST 원 파일은 싣지 않는다. 주소·날짜·해시로 같은 파일을 다시 받을 수 있다."] if lang == "ko" else
               ["Fifteen derived CSV files and datapackage.json can be downloaded; the derived data are CC BY 4.0.", "NIST's original files are not included; their URLs, dates and hashes let anyone fetch the same files."])
        body = f"<h1>{t['data']}</h1>{takeaway(lang, dtk)}{lic}" + table([t["file"], t["desc"]], rows, cls="") + '<p class="files"><a href="../data/datapackage.json">datapackage.json</a></p>'
        (base / "data.html").write_text(page(lang, t["data"], body, 1, "data"), encoding="utf-8")

    (OUT / "index.html").write_text('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=ko/index.html"><link rel="canonical" href="ko/index.html"><title>Physical Constants Metrics</title><a href="ko/index.html">한국어</a> · <a href="en/index.html">English</a>', encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("pages:", sum(1 for _ in OUT.rglob("*.html")))


def constant_takeaway(lang, q, qm, rows, pairs, m3r, m6):
    rs = sorted(rows, key=lambda r: int(r["edition"]))
    meas = [r for r in rs if r["exact"] == "0" and float(r["u_rel"]) > 0]
    out = []
    if len(meas) >= 2:
        a, z = meas[0], meas[-1]
        fold = float(a["u_rel"]) / float(z["u_rel"])
        if fold >= 1.5:
            f = f"{fold:,.0f}" if fold >= 10 else f"{fold:.1f}"
            out.append(f"오차 막대가 {a['edition']} 판에서 {z['edition']} 판까지 약 {f}배 좁아졌다(상대 불확도 {fmt_sci(a['u_rel'])} → {fmt_sci(z['u_rel'])})." if lang == "ko"
                       else f"The error bars narrowed about {f}-fold from the {a['edition']} to the {z['edition']} edition (relative uncertainty {fmt_sci(a['u_rel'])} → {fmt_sci(z['u_rel'])}).")
        else:
            out.append(f"오차 막대가 {a['edition']} 판부터 {z['edition']} 판까지 거의 좁아지지 않았다(상대 불확도 {fmt_sci(a['u_rel'])} → {fmt_sci(z['u_rel'])})." if lang == "ko"
                       else f"The error bars barely narrowed from the {a['edition']} to the {z['edition']} edition (relative uncertainty {fmt_sci(a['u_rel'])} → {fmt_sci(z['u_rel'])}).")
    m = [r for r in m3r if r["qid"] == q]
    if m:
        n1 = sum(int(r["miss_1sigma"]) for r in m)
        n2 = sum(int(r["miss_2sigma"]) for r in m)
        ex = m[0]["ref_exact"] == "1"
        if n1 == 0:
            out.append(f"옛 판 {len(m)}개의 오차 막대가 모두 오늘의(2022 판) 값을 품었다{"(2022 판 값은 정의값)" if ex else ""}." if lang == "ko"
                       else f"The error bars of {'both' if len(m) == 2 else 'all ' + str(len(m))} earlier editions reach today's (2022) value{' (the 2022 value is exact)' if ex else ''}.")
        else:
            out.append(f"옛 판 {len(m)}개 중 {n1}개의 오차 막대(±1σ)가 오늘의(2022 판) 값을 품지 못했고, 막대를 두 배로 넓혀도 {n2}개가 빗나갔다. 막대가 맞다면 각각 3개 중 1개, 20개 중 1개 꼴이어야 한다{"(2022 판 값은 정의값)" if ex else ""}." if lang == "ko"
                       else f"Of {len(m)} earlier editions, {n1} had error bars (±1σ) that miss today's (2022) value, and {n2} still miss with the bars doubled. If the bars were right, that would be about 1 in 3 and 1 in 20{' (the 2022 value is exact)' if ex else ''}.")
    ps = [p for p in pairs if p["qid"] == q]
    if ps:
        big = max(ps, key=lambda p: abs(float(p["z"])))
        zb = abs(float(big["z"]))
        if zb < 0.1:
            out.append("판이 바뀔 때마다 값은 오차 막대 폭의 0.1배도 움직이지 않았다." if lang == "ko"
                       else "From edition to edition the value never moved by even a tenth of its error bars.")
        else:
            out.append(f"가장 크게 움직인 때는 {big['ed_from']}→{big['ed_to']} 판으로, 두 판의 오차 막대를 합친 폭의 {zb:.1f}배였다." if lang == "ko"
                   else f"The biggest jump was {big['ed_from']}→{big['ed_to']}, {zb:.1f} times the combined error bars of the two editions.")
    for e in m6:
        if e["qid"] == q:
            out.append((f"{e['ed_after']} 판부터는 재는 값이 아니라 약속으로 정한 값(정의값)이라 오차 막대가 없다." if e["direction"] == "measured->exact" else f"{e['ed_after']} 판부터는 약속으로 정한 값이 아니라 재는 값이 되었다.") if lang == "ko"
                       else (f"From the {e['ed_after']} edition it is fixed by definition, not measured, so it has no error bars." if e["direction"] == "measured->exact" else f"From the {e['ed_after']} edition it is measured rather than fixed by definition."))
    if not meas and not out:
        out.append("이 사이트가 다루는 판에서는 줄곧 정의값이다." if lang == "ko" else "Exact in every edition covered here.")
    return out[:4]


def reading_page(lang, N):
    if lang == "ko":
        return f"""<div class="prose"><h1>읽기 — 오차 막대와 그 다음 판</h1>
<p class="lead">지표 면의 숫자를 한 번에 읽는 글이다. 해석이 들어가는 대목에는 근거의 한계를 같이 적었다.</p>
<div class="takeaway"><b>핵심</b><ul><li>불확도는 꾸준히 줄었지만, 판이 바뀔 때 값은 그 불확도가 허용하는 것보다 자주 크게 움직였다.</li><li>공표된 불확도는 「이 범위 밖일 확률 5%」라는 약속보다, 이 분야 기록이 보여 주는 두꺼운 꼬리와 함께 읽는 것이 맞다.</li></ul></div>
<h2>무엇을 셌나</h2>
<p>CODATA 는 대략 4년마다 그동안의 측정과 이론 계산을 한데 모아 최소제곱 조정을 하고 기본 물리 상수의 권고값과 표준불확도를 낸다. 이 사이트는 1969년 조정(CODATA 이전)과 CODATA 아홉 판에서 서로 환산 관계가 없는 핵심 상수 17개를 골라, 판이 바뀔 때 값이 움직인 폭을 그 불확도와 견주었다.</p>
<h2>보이는 것</h2>
<p>불확도는 꾸준히 줄었다. 불확도가 줄어든 핵심 상수 {N['m1_n_dec']}개의 상대 불확도는 중앙값으로 {N['m1_median']}년마다 절반이 되었다. 그런데 이동의 크기는 불확도가 말하는 범위를 자주 넘었다. 연속한 두 판 사이에서 두 불확도를 합친 것의 2배를 넘은 이동이 {N['m2_r2']}%, 3배를 넘은 이동이 {N['m2_r3']}% 였다. 판이 독립이고 정규분포를 따른다면 각각 4.6%, 0.27% 여야 한다. 2022 판 값을 기준으로 보면 옛 판의 ±2σ 막대 중 {N['m3_m2']}% 가 그 값을 담지 못했다.</p>
<p>반대로 작은 이동은 기대보다 드물었다. |z|>1 인 판 쌍은 {N['m2_r1']}% 로 기대치 31.7% 보다 낮다. 판과 판이 같은 실험 자료를 상당 부분 공유하기 때문이다. 새 측정이 없으면 값은 거의 그대로 남고({N['m2_zero']}개 쌍은 한 자리도 바뀌지 않았다), 새 측정이나 이론 수정이 들어오면 한꺼번에 크게 움직인다. 2006→2010 판의 미세 구조 상수 이동(옛 σ 기준 6.4배)은 CODATA 2010 보고서가 주로 전자 자기 모멘트 이론의 8차 항 계산 오류를 바로잡은 결과로 설명한다. 2014→2018 판의 양성자 전하 반지름 이동(옛 σ 기준 5.5배)에는 뮤온 수소·중수소의 램 이동 측정이 처음 들어온 것과 수소·중수소 분광의 개선이 함께 작용했다.</p>
<h2>어디까지 말할 수 있나</h2>
<ul><li>이 숫자는 「보고된 불확도가 판간 이동을 설명하지 못한 비율」이다. 그 원인이 연구자의 과신인지, 알려지지 않은 계통 오차인지, 조정 절차(어떤 측정을 넣고 뺄지, 불확도를 얼마나 키울지)인지는 이 자료로 가릴 수 없다.</li>
<li>2022 판도 참값이 아니다. 기준을 바꾸면 놓침률도 바뀐다.</li>
<li>판은 서로 독립이 아니고 상수도 서로 상관되어 있다(공동 조정, α 와 aₑ 의 이론 관계, R∞ 와 핵 반지름의 분광 입력). 비율의 구간은 상수 단위 군집 부트스트랩으로 냈지만, 이것은 같은 상수 안의 의존만 다루고 상수 사이의 상관은 남는다. 표본은 상수 17개뿐이다.</li>
<li>Henrion & Fischhoff(1986)는 같은 경향을 1929~1973년 자료에서, Bailey(2017)는 개별 측정 4만여 건에서 보고했다. 이 사이트의 자료는 그보다 좁고(권고값, 핵심 상수) 길다(2022 판까지). 결과의 방향은 같다.</li></ul>
<p>실무에서 쓸 만한 교훈은 하나다. 공표된 불확도는 「이 범위 밖일 확률이 5%」라는 약속으로 읽기보다, 이 분야의 과거 기록이 보여 주는 꼬리를 함께 보고 읽어야 한다는 것이다. 그 꼬리의 크기가 이 사이트의 숫자다.</p></div>"""
    return f"""<div class="prose"><h1>Reading — error bars and the next edition</h1>
<p class="lead">An essay that reads the metric pages in one pass. Where interpretation enters, the limits of the evidence are stated alongside.</p>
<div class="takeaway"><b>Takeaway</b><ul><li>Uncertainties fell steadily, yet values moved between editions by more than those uncertainties allow, and more often than a normal distribution predicts.</li><li>A published uncertainty is better read together with the heavy tail the field's record shows than as a promise of a 5% chance of lying outside.</li></ul></div>
<h2>What was counted</h2>
<p>About every four years CODATA gathers the measurements and theoretical calculations of the period, performs a least-squares adjustment, and publishes recommended values and standard uncertainties for the fundamental physical constants. This site takes 17 core constants, none an exact function of the others, from the 1969 adjustment (pre-CODATA) and the nine CODATA editions, and compares each move between editions with the stated uncertainties.</p>
<h2>What it shows</h2>
<p>Uncertainties fell steadily: among the {N['m1_n_dec']} core constants whose uncertainty declined, the median halved its relative uncertainty every {N['m1_median']} years. Yet moves often exceeded what the uncertainties allowed. Between consecutive editions, {N['m2_r2']}% of moves exceeded twice the combined uncertainty and {N['m2_r3']}% exceeded three times, against 4.6% and 0.27% if editions were independent and normal. Against the 2022 values, {N['m3_m2']}% of earlier ±2σ error bars miss.</p>
<p>Small moves, on the other hand, were rarer than expected: |z| > 1 in {N['m2_r1']}% of pairs, below the 31.7% expected. Editions share much of their experimental input. Without new data a value stays put ({N['m2_zero']} pairs did not change in any printed digit); when a new measurement or a corrected calculation arrives, it moves a long way at once. The CODATA 2010 report attributes the 2006→2010 move of the fine-structure constant (6.4 old σ) mainly to the correction of an error in eighth-order terms of the theory of the electron magnetic moment. The 2014→2018 move of the proton charge radius (5.5 old σ) came with the first inclusion of the muonic hydrogen and deuterium Lamb-shift measurements, together with improved hydrogen and deuterium spectroscopy.</p>
<h2>How far this goes</h2>
<ul><li>These numbers are the share of moves that the reported uncertainties did not cover. Whether the cause is the researchers' overconfidence, unknown systematic errors, or the adjustment procedure (which data to keep, how far to expand uncertainties) cannot be told from these data.</li>
<li>The 2022 edition is not the true value either; another reference gives other miss rates.</li>
<li>Editions are not independent and constants are correlated (joint adjustment, the theoretical link between α and aₑ, spectroscopic input shared by R∞ and nuclear radii). Intervals for rates are cluster bootstraps over constants, which handle dependence within a constant but not correlation between constants; and there are only 17 constants.</li>
<li>Henrion & Fischhoff (1986) reported the same tendency for 1929–1973, and Bailey (2017) for some 41,000 individual measurements. The data here are narrower (recommended values, core constants) and longer (to 2022). The direction of the result is the same.</li></ul>
<p>One practical lesson follows. A published uncertainty is better read together with the tail that the field's record shows than as a promise that the truth lies outside the stated range only 5% of the time. The size of that tail is what this site measures.</p></div>"""


def prior_page(lang):
    if lang == "ko":
        return """<div class="prose"><h1>선행 연구</h1><p class="lead">같은 질문을 먼저 다룬 연구를 소개한다. 수치는 각 문헌에서 옮겼다.</p>
<div class="takeaway"><b>핵심</b><ul><li>보고된 불확도가 실제 이동이나 측정 간 차이보다 작다는 결과는 1986년(권고값·개별 측정)과 2017년(측정 약 41,000건) 연구에서 서로 다른 자료로 나왔다.</li><li>이 사이트는 권고값 판을 2022 판까지 이어 같은 질문을 다시 센다.</li></ul></div>
<h2>Henrion & Fischhoff (1986)</h2><p>M. Henrion, B. Fischhoff, "Assessing uncertainty in physical constants", <i>American Journal of Physics</i> 54(9), 791–798. 주관적 확률 판단의 보정(calibration)을 재는 심리학 지표 — 사분위 지수와 놀람 지수 — 를 빛의 속력·중력 상수 등의 개별 측정과 1929~1969년 권고값에 적용했다. 권고값 상수 다섯 개 × 검토 여덟 개를 1973 판 기준으로 보면 놀람 지수가 57% 였다(정규 기대 2%; 공개 사본에서 읽은 값으로 출판본 대조 전). 이 사이트는 같은 지표를 1969 판부터 2022 판까지 다시 계산한다(<a href="metrics/hf.html">재계산</a>).</p>
<h2>Bailey (2017)</h2><p>D. C. Bailey, "Not Normal: the uncertainties of scientific measurements", <i>Royal Society Open Science</i> 4, 160600. 의학·핵물리·입자물리·실험실 간 비교의 측정 약 41,000 건, 양 약 3,200 개에서 같은 양의 측정 쌍마다 z 를 구하고 Student-t 를 맞췄다. 기본 상수 부분(양 7개, 측정 320개, 쌍 9,098개)의 자유도는 ν = 1.81 ± 0.15 다. 개별 측정끼리의 비교라는 점에서 권고값 판끼리를 비교하는 이 사이트와 단위가 다르다. 자료는 Dryad(doi:10.5061/dryad.jb3mj, CC0)에 있다.</p>
<h2>Shlyakhter (1994)</h2><p>A. I. Shlyakhter, "Uncertainty estimates in scientific models: lessons from trends in physical measurements, population and energy projections", B. M. Ayyub, M. M. Gupta 편 <i>Uncertainty Modelling and Analysis: Theory and Applications</i>(Elsevier, 1994), 477쪽 이하. 같은 양의 연속 측정에서 정규화 편차의 분포를 지수분포로 맞추고, 과거 오차에서 불확도를 넓히는 계수를 정하자고 제안했다.</p>
<h2>Particle Data Group</h2><p>입자의 질량·수명 등에 대해 판별 평균값의 변천을 그린 그림(history plot)을 낸다. 이 사이트는 1.0 에서 PDG 자료를 다루지 않는다.</p>
<h2>CODATA 의 자기 점검</h2><p>CODATA 보고서는 판마다 직전 판과의 비교를 싣는다(예: 2022 보고서의 「Comparison of 2022 and 2018 CODATA recommended values」, 1973 보고서의 표 34.2 는 1963·1969 조정값과 비교). 1969년 Taylor–Parker–Langenberg 보고서도 1950년대 이후 α⁻¹ 의 변천을 그림으로 보이며 「어떤 상수 집합도 복음처럼 받아들여서는 안 된다」고 적었다.</p></div>"""
    return """<div class="prose"><h1>Prior work</h1><p class="lead">Earlier studies of the same question. Figures are taken from each publication.</p>
<div class="takeaway"><b>Takeaway</b><ul><li>That reported uncertainties are smaller than the actual moves or the differences between measurements was found in 1986 (recommended values and individual measurements) and in 2017 (some 41,000 measurements), on different data.</li><li>This site asks the same question again, following recommended values through the 2022 edition.</li></ul></div>
<h2>Henrion & Fischhoff (1986)</h2><p>M. Henrion and B. Fischhoff, "Assessing uncertainty in physical constants", <i>American Journal of Physics</i> 54(9), 791–798. They applied the calibration indices of the psychology of subjective probability — the interquartile index and the surprise index — to individual measurements of the speed of light, the gravitational constant and others, and to recommended values from 1929 to 1969. For five constants in eight reviews, against the 1973 values, the surprise index was 57% (normal: 2%; read from a public copy, not yet checked against the published version). This site recomputes the same indices from 1969 to 2022 (<a href="metrics/hf.html">recalculation</a>).</p>
<h2>Bailey (2017)</h2><p>D. C. Bailey, "Not Normal: the uncertainties of scientific measurements", <i>Royal Society Open Science</i> 4, 160600. About 41,000 measurements of some 3,200 quantities in medicine, nuclear and particle physics and interlaboratory comparisons; z for every pair of measurements of the same quantity, fitted with Student-t. For the fundamental constants (7 quantities, 320 measurements, 9,098 pairs) ν = 1.81 ± 0.15. Individual measurements are compared, whereas this site compares editions of recommended values. Data on Dryad (doi:10.5061/dryad.jb3mj, CC0).</p>
<h2>Shlyakhter (1994)</h2><p>A. I. Shlyakhter, "Uncertainty estimates in scientific models: lessons from trends in physical measurements, population and energy projections", in B. M. Ayyub and M. M. Gupta (eds.), <i>Uncertainty Modelling and Analysis: Theory and Applications</i> (Elsevier, 1994), pp. 477ff. Fitted an exponential distribution to normalised deviations of successive measurements and proposed widening uncertainties by factors drawn from past errors.</p>
<h2>Particle Data Group</h2><p>Publishes history plots of its averages for particle masses, lifetimes and other properties. Version 1.0 of this site does not use PDG data.</p>
<h2>CODATA's own comparisons</h2><p>Each CODATA report compares its values with the previous edition (for example, "Comparison of 2022 and 2018 CODATA recommended values" in the 2022 report; table 34.2 of the 1973 report compares with the 1963 and 1969 adjustments). The 1969 Taylor–Parker–Langenberg report plotted the history of α⁻¹ since the 1950s and wrote that no set of fundamental constants should be taken as Gospel truth.</p></div>"""


def method_page(lang, N):
    if lang == "ko":
        return f"""<div class="prose"><h1>방법·한계</h1>
<div class="takeaway"><b>핵심</b><ul><li>1969·1973·1986 판은 원 논문 쪽 이미지에서 손으로, 1998 판 이후는 NIST 표에서 옮겼고, 쓰는 값 전부를 별도 조판본과 대조했다.</li><li>대조 중 NIST 2002 판 ASCII 보관본의 오기 3행을 찾아 출판본 값으로 고쳤다.</li><li>판은 서로 독립이 아니고 2022 판도 참값이 아니다 — 모든 수치는 이 두 조건 아래에서 읽는다.</li></ul></div>
{GLOSS["ko"]}<h2>자료</h2><p>{esc(SOURCES['codata']['ko'])} {esc(SOURCES['tpl1969']['ko'])}</p>
<ul><li>1998~2022 판: NIST ASCII 표를 파싱했다. 1998~2006 판은 「값(불확도)」 괄호 표기(괄호 안 숫자는 마지막 자리 기준), 2010 판부터는 값과 불확도가 따로 적혀 있다. 「...」로 끝나는 값과 「(exact)」는 정의값이다.</li>
<li>1969·1973·1986 판: 이 사이트가 쓰는 양을 원 논문 표의 쪽 이미지에서 손으로 옮겼다. 66개(측정값 63, 정의값 3) 전부를 PDF 문자층과 자동 대조해 64개가 같았고, 나머지 2개는 문자층의 OCR 오류로 이미지 판독이 맞다. 이 판들의 불확도는 원문에 「표준편차」로 적혀 있다(1969: 표 XXXII 머리말, 1973: 표 33.1 각주 a, 1986: 미주 3).</li>
<li>1998~2022 판의 사용 행 213개 전부를 NIST 가 따로 조판한 「all values」 PDF 표와 대조했다. 판별 무작위 10행 표본도 같은 PDF 와 대조했다.</li></ul>
<h2>원자료 보정</h2><ul>
<li>2002 판 ASCII 보관본은 볼츠만 상수를 1.380 6504(24)×10⁻²³ 로 적었으나, 같은 판의 PDF 표와 출판된 보고서(Rev. Mod. Phys. 77, 1)는 1.380 6505(24)×10⁻²³ 다. 출판본 값을 쓴다. 같은 보관본의 전자 자기 모멘트와 양성자 비전하도 마지막 자리가 출판본과 달라 함께 보정했다(통계에는 쓰지 않는 행).</li>
<li>1998~2006 ASCII 표에는 기본 전하 행이 없다. 같은 수치인 전자볼트(J) 행을 썼다.</li>
<li>1998 판 ASCII 의 진공 투자율 행은 지수가 빠져 있어(정의값 4π×10⁻⁷) 복원했다.</li></ul>
<h2>상수 선정</h2><p>통계의 분모인 핵심 상수 17개는 서로 정확한 환산 관계가 없도록 골랐다. 예컨대 2019년 이전에는 e = √(2αh/μ₀c), mₑ = 2R∞h/(cα²) 이므로 α·h·R∞ 를 넣으면 e·mₑ 는 뺀다. 아보가드로 상수는 몰 플랑크 상수 관계로 h 와 묶여 있어 뺐다. 상대 원자 질량(전자·양성자·중성자·중양성자·알파 입자)을 넣고, 그 비인 양성자–전자 질량비는 뺐다. PDG 에서 받아 쓰는 양(타우 질량, 페르미 결합 상수, 약한 혼합각)은 넣지 않았다. 빛의 속력은 1969·1973 판에서 측정값이었으므로 그 두 판의 관계식에는 c 가 측정값으로 더 들어가지만, 측정값인 판이 둘뿐이라 핵심 상수에 넣지 않았다. μ₀·M_u 는 2014 판까지 정의값이었다.</p>
<p>17개는 설계 단계에서 고른 목록이다. 같은 규칙(정확한 관계 없음, 측정값인 판 4개 이상, PDG 채택값 아님)에 맞지만 넣지 않은 양이 더 있다 — 헬리온·삼중수소핵의 상대 원자 질량, 중양성자 자기 모멘트, 규소 격자 간격 등. 앞의 셋을 더한 20개로 다시 계산한 값을 M2·M3 면에 민감도로 적었다(<code>sens_candidates.csv</code>). 정확한 관계가 없다는 것이 통계적으로 독립이라는 뜻은 아니다.</p>
<h2>통계</h2><ul><li>비율(M2·M3)과 M4 의 신뢰구간: 상수를 통째로 다시 뽑는 군집 부트스트랩, 10,000회(M4 는 2,000회), 시드 2026, 백분위 95%. M1 의 구간은 회귀 기울기의 t(n−2) 구간이다.</li>
<li>M4 는 값이 한 자리도 바뀌지 않은 판 쌍(z = 0)을 빼고 맞춘다. 남기면 중심 0 Student-t 의 우도가 척도 0 쪽으로 무한대가 되어 최대우도 추정량이 없다.</li>
<li>판 연도는 판 이름의 연도(자료 마감 연도)다. 1998 판은 2000년에 출판되었다.</li>
<li>정의값인 판은 그 상수의 M1~M4 계산에서 뺀다.</li></ul>
<h2>한계</h2><ul><li>연속한 판은 같은 실험 자료를 공유해 독립이 아니다. 공유는 이동을 작게 만드는 쪽으로 작용한다.</li>
<li>최근 판은 서로 맞지 않는 입력 자료의 불확도를 키워서(확장 인자) 조정한다. 권고 불확도에 이미 그런 판단이 들어 있다.</li>
<li>2022 판은 참값이 아니다.</li>
<li>한국어 상수 이름 가운데 진공에서의 빛의 속력·플랑크 상수·기본 전하·볼츠만 상수·아보가드로 상수는 국가표준기본법 시행령 별표 1 의 표기다. 나머지는 관행 표기이며 대한물리학회 용어집과 대조하지 않았다.</li></ul>
<h2>재현</h2><p>모든 표는 저장소의 <code>src/</code> 에서 만든다: <code>fetch_raw.py</code>(원 파일 내려받기·해시) → <code>parse_codata.py</code>(파싱·보정·대응) → <code>handcheck.py</code>(대조) → <code>metrics.py</code>(지표) → <code>build_site.py</code>(사이트).</p></div>"""
    return f"""<div class="prose"><h1>Method & limits</h1>
<div class="takeaway"><b>Takeaway</b><ul><li>The 1969, 1973 and 1986 values were transcribed by hand from page images of the published tables, later editions from NIST's tables; every value used was checked against a separately typeset version.</li><li>The checks found three rows of NIST's archived 2002 ASCII table that differ from the published report; the published values are used.</li><li>Editions are not independent and the 2022 edition is not the true value; every number should be read with both in mind.</li></ul></div>
{GLOSS["en"]}<h2>Data</h2><p>{esc(SOURCES['codata']['en'])} {esc(SOURCES['tpl1969']['en'])}</p>
<ul><li>1998–2022: NIST ASCII tables, parsed. 1998–2006 use concise notation, value(uncertainty), the bracketed digits referring to the last digits; from 2010 value and uncertainty are in separate columns. Values ending in '...' and '(exact)' are exact.</li>
<li>1969, 1973, 1986: the quantities used here were transcribed by hand from page images of the published tables. All 66 values (63 measured, 3 exact) were compared automatically with the PDF text layer: 64 are identical, and the other two are OCR errors in the text layer, the image reading being correct. These editions state their uncertainties as standard deviations (1969: heading of table XXXII; 1973: table 33.1, note a; 1986: endnote 3).</li>
<li>All 213 rows used from 1998–2022 were checked against NIST's separately typeset 'all values' PDF tables, as was a random sample of 10 rows per edition.</li></ul>
<h2>Corrections to the sources</h2><ul>
<li>The archived 2002 ASCII table gives the Boltzmann constant as 1.380 6504(24)×10⁻²³; the 2002 PDF table and the published report (Rev. Mod. Phys. 77, 1) give 1.380 6505(24)×10⁻²³. The published value is used. Two other rows of the same file (electron magnetic moment, proton charge-to-mass quotient) differ from the publication in the last digit and were corrected too; neither enters the statistics.</li>
<li>The 1998–2006 ASCII tables have no elementary-charge row; the electron-volt row in joules carries the same number and is used.</li>
<li>The 1998 ASCII row for the vacuum magnetic permeability lacks its exponent; the exact value 4π×10⁻⁷ was restored.</li></ul>
<h2>Choice of constants</h2><p>The 17 core constants that form every denominator were chosen so that none is an exact function of the others. Before 2019, e = √(2αh/μ₀c) and mₑ = 2R∞h/(cα²); with α, h and R∞ in, e and mₑ are out. The Avogadro constant is tied to h through the molar Planck constant and is out. The relative atomic masses of the electron, proton, neutron, deuteron and alpha particle are in, and their ratio mₚ/mₑ is out. Quantities CODATA adopts from the PDG (tau mass, Fermi coupling constant, weak mixing angle) are not used. The speed of light was measured in the 1969 and 1973 editions, so in those two editions the relations above involve c as a further measured quantity; with only two measured editions it is not a core constant. μ₀ and M_u were exact up to 2014.</p>
<p>The 17 were chosen at the design stage. Other quantities meet the same rule (no exact relation, measured in at least four editions, not adopted from the PDG) but were not included: the helion and triton relative atomic masses, the deuteron magnetic moment, the silicon lattice spacing and others. The M2 and M3 pages give, as a sensitivity check, the values with the first three added (20 constants; <code>sens_candidates.csv</code>). The absence of exact relations does not make the constants statistically independent.</p>
<h2>Statistics</h2><ul><li>Intervals for the rates (M2, M3) and for M4: cluster bootstrap resampling whole constants, 10,000 resamples (2,000 for M4), seed 2026, 95% percentile. M1 intervals are t(n−2) intervals of the regression slope.</li>
<li>M4 is fitted without the pairs whose printed value did not change (z = 0); with them, the likelihood of a zero-centred Student-t is unbounded as the scale goes to zero and no maximum-likelihood estimate exists.</li>
<li>Edition year is the year in the edition's name (data cut-off); the 1998 edition was published in 2000.</li>
<li>Editions in which a constant is exact are left out of its M1–M4 calculations.</li></ul>
<h2>Limits</h2><ul><li>Consecutive editions share experimental data and are not independent; sharing pulls the moves toward zero.</li>
<li>Recent adjustments expand the uncertainties of mutually inconsistent input data (expansion factors), so recommended uncertainties already contain such judgements.</li>
<li>The 2022 edition is not the true value.</li>
<li>Korean names: the speed of light in vacuum, Planck constant, elementary charge, Boltzmann constant and Avogadro constant follow Table 1 of the Enforcement Decree of the Korean Framework Act on National Standards; the other Korean names follow common usage and have not been checked against the Korean Physical Society glossary.</li></ul>
<h2>Reproduction</h2><p>Every table is made by <code>src/</code> in the repository: <code>fetch_raw.py</code> (download and hash the source files) → <code>parse_codata.py</code> (parse, correct, map) → <code>handcheck.py</code> (checks) → <code>metrics.py</code> (metrics) → <code>build_site.py</code> (site).</p></div>"""


if __name__ == "__main__":
    build()
