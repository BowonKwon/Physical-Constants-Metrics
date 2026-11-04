# -*- coding: utf-8 -*-
"""Hubble-constant chapter pages (1.2). Called from build_site.build() once per language, like aw_site.build().
H is a dict of helpers from build_site (page, table, takeaway, esc, fmt_sci, sup, spec_block, N = the numbers of the
physical-constants chapter). Every number on these pages comes from data/h0_*.csv; nothing here reads data/raw/.

Huchra's list may be shown only in aggregate (h0_registry.H0_SOURCES["huchra"]): its figures draw yearly and decade
quantiles from data/h0_huchra_*.csv and never a row. Table A2 (CC BY 4.0) is shown row by row."""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import stats

from h0_registry import H0_METRICS, H0_SOURCES, H2_TEXT, REFS, TYPE_PRIMARY, TYPE_SECONDARY, UNVERIFIED

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PUBLIC = ["h0_faerber2020.csv", "h0_h3_rows_faerber.csv", "h0_h1_halflife.csv", "h0_h3_summary.csv", "h0_h4_tail.csv",
          "h0_huchra_yearly.csv", "h0_huchra_decades.csv", "h0_huchra_types.csv", "h0_huchra_codes.csv"]
DESC = {
    "h0_faerber2020.csv": ("Faerber & López-Corredoira (2020) 표 A2 전부: 연도·H0·오차(원 표기)·참고문헌(CC BY 4.0, 출처 표시)", "Every row of Table A2 of Faerber & López-Corredoira (2020): year, H0, error as printed, reference (CC BY 4.0, with attribution)"),
    "h0_h3_rows_faerber.csv": ("표 A2 행마다 두 기준값 대비 z(H3)", "z against both references for every Table A2 row (H3)"),
    "h0_h1_halflife.csv": ("H1 정밀도 반감기(계열·시작 연도·변형별)", "H1 precision half-life by series, start year and variant"),
    "h0_h3_summary.csv": ("H3 놓침률·사분위 지수·놀람 지수와 95% 구간(계열·기준값별)", "H3 miss rates, interquartile and surprise indices with 95% intervals, by series and reference"),
    "h0_h4_tail.csv": ("H4 Student-t 적합(계열·기준값별)", "H4 Student-t fits by series and reference"),
    "h0_huchra_yearly.csv": ("Huchra 목록 연도별 집계: 건수, H0 와 상대 오차의 사분위(3건 미만인 해는 건수만)", "Huchra's list by year: count, quartiles of H0 and of the relative error (years with fewer than three rows: count only)"),
    "h0_huchra_decades.csv": ("Huchra 목록 10년 단위 집계: 건수, H0 사분위", "Huchra's list by decade: count, quartiles of H0"),
    "h0_huchra_types.csv": ("Huchra 목록 10년 단위 × Type 부호 건수", "Huchra's list: rows per decade and type code"),
    "h0_huchra_codes.csv": ("Huchra 목록 Type 부호별 건수와 첫·마지막 연도", "Huchra's list: rows, first and last year per type code"),
}
HU, FA, MG = "huchra", "faerber", "merged"
SERIES_LABEL = {"ko": {HU: "Huchra 목록", FA: "표 A2", MG: "합친 계열(감도)"}, "en": {HU: "Huchra's list", FA: "Table A2", MG: "Merged (sensitivity)"}}
REF_COLOR = {"planck18": "var(--s3)", "riess22": "var(--s2)"}
MIN_N = 3

L = {
    "ko": dict(nav="허블 상수", title="허블 상수 장 — 발표된 H0 추정값과 그 오차, 1929~2019",
               lead="허블 상수 H0 는 우주의 팽창률이다. 1929년부터 발표된 H0 추정값은 500 을 넘는 값에서 70 안팎으로 내려왔고, 오차 막대는 그 사이 수백 배 짧아졌다. 이 장은 두 집성에서 인용된 오차가 뒤의 기준값과의 차이를 얼마나 자주 담았는지를 센다. 물리 상수 장과 같은 질문을, 판 대신 개별 측정의 기록에 던진다.",
               metrics="지표", pages="연대기·방법", timeline="연대기", method="방법·한계", glance="한눈에 보기", download="CSV 내려받기",
               year="연도", h0="H0", err="오차(원 표기)", author="저자(표 A2)", ref_h="참고문헌", z_p="z (Planck 2018)", z_r="z (Riess 외 2022)",
               series="계열", start="시작", variant="변형", nyears="해 수", span="기간", slope="기울기 log₂/년", hl="반감기(년)", ci="95% 구간", rows="행",
               ref="기준값", n="n", excl="제외", below="기준값보다 작은 값", m1="1σ 놓침 %", m2="2σ 놓침 %", iq="사분위 지수 %", si="놀람 지수 %", medz="중앙값 |z|",
               cluster="군집", nu="ν", scale="척도 s", unit="km s⁻¹ Mpc⁻¹", code="부호", meaning="뜻(파일 범례)", first="첫 연도", last="마지막 연도",
               median="해별 중앙값", frontier="정밀도 최전선", start1929="1929년부터", start1950="1950년부터", all="1976~2019"),
    "en": dict(nav="Hubble constant", title="Hubble constant — published H0 estimates and their errors, 1929–2019",
               lead="The Hubble constant H0 is the expansion rate of the universe. Published estimates have come down from above 500 in 1929 to about 70, and their error bars shortened a few hundredfold on the way. This chapter counts how often the errors quoted in two compilations covered the distance to a later reference value: the question of the physical-constants chapter, asked of individual measurements instead of editions.",
               metrics="Metrics", pages="Chronology and method", timeline="Chronology", method="Method and limits", glance="At a glance", download="Download CSV",
               year="Year", h0="H0", err="Error (as printed)", author="Authors (Table A2)", ref_h="Reference", z_p="z (Planck 2018)", z_r="z (Riess et al. 2022)",
               series="Series", start="Start", variant="Variant", nyears="Years (n)", span="Span", slope="Slope log₂/year", hl="Half-life (years)", ci="95% interval", rows="Rows",
               ref="Reference", n="n", excl="Left out", below="Values below the reference", m1="1σ miss %", m2="2σ miss %", iq="Interquartile %", si="Surprise %", medz="Median |z|",
               cluster="Cluster", nu="ν", scale="Scale s", unit="km s⁻¹ Mpc⁻¹", code="Code", meaning="Meaning (file legend)", first="First year", last="Last year",
               median="Yearly median", frontier="Precision frontier", start1929="from 1929", start1950="from 1950", all="1976–2019"),
}


# ------------------------------------------------------------------ data
def read(name):
    with open(DATA / name, encoding="utf-8", newline="") as fh:
        lines = [l for l in fh.read().splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def pct(x, d=1):
    return f"{float(x) * 100:.{d}f}"


def cip(s):
    lo, hi = s.strip("[]").split(",")
    return f"{float(lo) * 100:.0f}–{float(hi) * 100:.0f}%"


def load():
    h1 = {(r["series"], int(r["start"]), r["variant"]): r for r in read("h0_h1_halflife.csv")}
    h3 = {(r["series"], int(r["start"]), r["ref"], r["cluster"]): r for r in read("h0_h3_summary.csv")}
    h4 = {(r["series"], int(r["start"]), r["ref"]): r for r in read("h0_h4_tail.csv")}
    fz = {r["meas_id"]: r for r in read("h0_h3_rows_faerber.csv")}
    frows = []
    for r in read("h0_faerber2020.csv"):
        mid = f"FLC20-{int(r['row']):03d}"
        if mid not in fz:      # the repeated printed row (dropped by h0_faerber.load) has no z
            continue
        frows.append(dict(r, meas_id=mid, u_mean=fz[mid]["u_mean"], z_planck18=fz[mid]["z_planck18"], z_riess22=fz[mid]["z_riess22"]))
    return dict(h1=h1, h3=h3, h4=h4, frows=frows, yearly=read("h0_huchra_yearly.csv"), decades=read("h0_huchra_decades.csv"),
                types=read("h0_huchra_types.csv"), codes=read("h0_huchra_codes.csv"))


def numbers(D, N0):
    h1, h3, h4 = D["h1"], D["h3"], D["h4"]
    N = dict(m1_median=N0["m1_median"], m3_m2=N0["m3_m2"], m4_nu=N0["m4_nu"])

    def hl(s, start, var):
        r = h1[(s, start, var)]
        return f'{float(r["halflife_years"]):.1f}', f'{float(r["halflife_ci_low"]):.1f}–{float(r["halflife_ci_high"]):.1f}'
    for key, s, start in (("hu", HU, 1929), ("hu50", HU, 1950), ("fa", FA, 1929), ("mg", MG, 1929), ("mg50", MG, 1950)):
        med, med_ci = hl(s, start, "yearly_median")
        fr, fr_ci = hl(s, start, "frontier")
        N[f"h1_{key}_med"], N[f"h1_{key}_med_ci"], N[f"h1_{key}_fr"], N[f"h1_{key}_fr_ci"] = med, med_ci, fr, fr_ci
        N[f"h1_{key}_rows"], N[f"h1_{key}_years"] = h1[(s, start, "yearly_median")]["n_rows"], h1[(s, start, "yearly_median")]["n_points"]
    N["h1_hu_small"] = sum(1 for y in D["yearly"] if int(y["n"]) < MIN_N)
    for key, s, start in (("hu", HU, 1929), ("hu50", HU, 1950), ("fa", FA, 1929), ("mg", MG, 1929)):
        for rk, ref in (("p", "planck18"), ("r", "riess22")):
            r = h3[(s, start, ref, "year")]
            N[f"h3_{key}_{rk}_m1"], N[f"h3_{key}_{rk}_m2"] = pct(r["miss_1sigma"]), pct(r["miss_2sigma"])
            N[f"h3_{key}_{rk}_si"], N[f"h3_{key}_{rk}_iq"] = pct(r["surprise"]), pct(r["inside_iq"])
            N[f"h3_{key}_{rk}_m2_ci"], N[f"h3_{key}_{rk}_si_ci"] = cip(r["miss_2sigma_ci"]), cip(r["surprise_ci"])
            N[f"h3_{key}_n_{rk}"] = r["n"]
            t = h4[(s, start, ref)]
            N[f"h4_{key}_{rk}_nu"], N[f"h4_{key}_{rk}_ci"] = t["nu"], f'{t["nu_ci_low"]}–{t["nu_ci_high"]}'
    N["h3_hu_n"], N["h3_hu50_n"] = h3[(HU, 1929, "riess22", "year")]["n"], h3[(HU, 1950, "riess22", "year")]["n"]
    N["fa_rows"] = len(D["frows"])
    N["fa_asym"] = sum(1 for r in D["frows"] if r["err_plus"] != r["err_minus"])
    return N


# ------------------------------------------------------------------ chart helpers
def _svg(W, Hh, label):
    return [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="{label}">']


def _logy(lo, hi, Tp, B, Hh):
    def Y(v):
        return Tp + (math.log10(hi) - math.log10(max(v, lo))) / (math.log10(hi) - math.log10(lo)) * (Hh - Tp - B)
    return Y


def chart_urel_yearly(yearly, lang, H, W=900, Hh=340):
    """Huchra's list: per year the quartile bar (q1–q3) and median of the relative error; years with fewer than
    MIN_N rows show only a count mark. Log vertical axis. Aggregates only."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 20, 18, 44
    x0, x1, lo, hi = 1926, 2013, 0.005, 1.2

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)
    Y = _logy(lo, hi, Tp, B, Hh)
    o = _svg(W, Hh, "연도별 상대 오차 집계" if lang == "ko" else "Relative error by year, aggregated")
    for t, lab in ((0.01, "1%"), (0.03, "3%"), (0.1, "10%"), (0.3, "30%"), (1.0, "100%")):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{lab}</text>')
    for yv in range(1930, 2020, 10):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-16}" text-anchor="middle">{yv}</text>')
    small = "집계 생략(3건 미만)" if lang == "ko" else "count only (fewer than 3 rows)"
    for r in yearly:
        y, n = int(r["year"]), int(r["n"])
        x = X(y)
        if not r["urel_median"]:
            o.append(f'<path class="dot" d="M{x-3:.1f},{Hh-B-8} L{x+3:.1f},{Hh-B-2} M{x-3:.1f},{Hh-B-2} L{x+3:.1f},{Hh-B-8}" stroke="var(--fg3)" stroke-width="1.5" data-tip="{y}: n={n}, {small}"/>')
            continue
        q1, med, q3 = float(r["urel_q1"]), float(r["urel_median"]), float(r["urel_q3"])
        tip = f'{y}: n={n}, {"중앙값" if lang == "ko" else "median"} {med*100:.1f}%, {"사분위" if lang == "ko" else "quartiles"} {q1*100:.1f}–{q3*100:.1f}%'
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(q3):.1f}" y2="{Y(q1):.1f}" stroke="var(--fg3)" stroke-opacity=".45" stroke-width="5"/>')
        o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(med):.1f}" r="4" fill="var(--fg2)" stroke="var(--card)" stroke-width="1.5" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_urel_points(frows, lang, H, W=900, Hh=340):
    """Table A2: one dot per row, relative error by year (log vertical axis)."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 20, 18, 44
    x0, x1, lo, hi = 1974, 2021, 0.005, 1.2

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)
    Y = _logy(lo, hi, Tp, B, Hh)
    o = _svg(W, Hh, "표 A2 행별 상대 오차" if lang == "ko" else "Relative error of each Table A2 row")
    for t, lab in ((0.01, "1%"), (0.03, "3%"), (0.1, "10%"), (0.3, "30%"), (1.0, "100%")):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{lab}</text>')
    for yv in range(1975, 2021, 5):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-16}" text-anchor="middle">{yv}</text>')
    for r in frows:
        u = float(r["u_mean"]) / float(r["h0"])
        tip = f'{r["year"]}: {r["h0"]} ± {r["err_as_printed"]} ({r["ref_label"]})'
        o.append(f'<circle class="dot" cx="{X(int(r["year"])):.1f}" cy="{Y(u):.1f}" r="4" fill="var(--s1)" fill-opacity=".55" stroke="var(--card)" stroke-width="1" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_rates(h3, lang, H, W=900, Hh=360):
    """H3 shares with 95% intervals: four indices, within each the two compilations × two references; the normal
    expectation as a dashed segment."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 20, 18, 56
    idx = [("miss_1sigma", "1σ 놓침" if lang == "ko" else "1σ miss", 0.317), ("miss_2sigma", "2σ 놓침" if lang == "ko" else "2σ miss", 0.046),
           ("surprise", "놀람 지수" if lang == "ko" else "surprise", 0.020), ("inside_iq", "사분위 지수" if lang == "ko" else "interquartile", 0.500)]
    cells = [(HU, "planck18"), (HU, "riess22"), (FA, "planck18"), (FA, "riess22")]
    gw = (W - Lm - R) / len(idx)

    def Y(v): return Tp + (1 - v / 0.7) * (Hh - Tp - B)
    o = _svg(W, Hh, "H3 비율과 구간" if lang == "ko" else "H3 shares and intervals")
    for v in (0, .1, .2, .3, .4, .5, .6, .7):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{Lm-6}" y="{Y(v)+4:.1f}" text-anchor="end">{int(v*100)}%</text>')
    for gi, (col, lab, norm) in enumerate(idx):
        gx = Lm + gi * gw
        o.append(f'<line class="ref" x1="{gx+8:.1f}" x2="{gx+gw-8:.1f}" y1="{Y(norm):.1f}" y2="{Y(norm):.1f}"/>')
        o.append(f'<text x="{gx+gw/2:.1f}" y="{Hh-30}" text-anchor="middle">{esc(lab)}</text><text x="{gx+gw/2:.1f}" y="{Hh-14}" text-anchor="middle">{"정규 기대" if lang == "ko" else "normal"} {norm*100:g}%</text>')
        for ci, (s, ref) in enumerate(cells):
            r = h3[(s, 1929, ref, "year")]
            v = float(r[col])
            lo, hi = (float(x) for x in r[col + "_ci"].strip("[]").split(","))
            x = gx + gw * (ci + 1) / (len(cells) + 1)
            colr = REF_COLOR[ref]
            fill = colr if s == HU else "var(--card)"
            tip = f'{SERIES_LABEL[lang][s]} · {REFS[ref][lang]}: {v*100:.1f}% [{lo*100:.0f}–{hi*100:.0f}%], n={r["n"]}'
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(lo):.1f}" y2="{Y(hi):.1f}" stroke="{colr}" stroke-width="2" stroke-opacity=".6"/>')
            o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(v):.1f}" r="5.5" fill="{fill}" stroke="{colr}" stroke-width="2.5" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_z_panels(frows, lang, H, W=900, Hh=480):
    """Table A2: z against each reference by year, one panel per reference, clipped at ±8, dashed ±1 and ±2."""
    esc = H["esc"]
    Lm, R, Tp, B, gap = 56, 110, 22, 40, 60
    ph = (Hh - Tp - B - gap) / 2
    x0, x1, cap = 1974, 2021, 8.0

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)
    o = _svg(W, Hh, "기준값 대비 z" if lang == "ko" else "z against each reference")
    for pi, (ref, zcol) in enumerate((("planck18", "z_planck18"), ("riess22", "z_riess22"))):
        top = Tp + pi * (ph + gap)

        def Y(v, top=top): return top + (cap - max(-cap, min(cap, v))) / (2 * cap) * ph
        o.append(f'<text x="{Lm}" y="{top-10:.1f}" font-weight="600">{REFS[ref][lang]} ({REFS[ref]["value"]} ± {REFS[ref]["u"]})</text>')
        for v in (-8, -4, -2, -1, 0, 1, 2, 4, 8):
            cls = "ref" if abs(v) in (1, 2) else "grid"
            o.append(f'<line class="{cls}" x1="{Lm}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{Lm-6}" y="{Y(v)+4:.1f}" text-anchor="end">{v:+d}</text>'.replace(">+0<", ">0<"))
        for yv in range(1975, 2021, 5):
            o.append(f'<text x="{X(yv):.1f}" y="{top+ph+14:.1f}" text-anchor="middle">{yv}</text>')
        o.append(f'<text x="{W-R+8}" y="{Y(0)+4:.1f}">z = 0</text><text x="{W-R+8}" y="{Y(2)+4:.1f}">z = ±2</text>')
        for r in frows:
            if not r[zcol]:
                continue
            z = float(r[zcol])
            x, y = X(int(r["year"])), Y(z)
            tip = f'{r["year"]}: {r["h0"]} ± {r["err_as_printed"]} ({r["ref_label"]}), z = {z:.2f}'
            if abs(z) > cap:
                o.append(f'<path class="dot" d="M{x-5:.1f},{y + (6 if z < 0 else -6):.1f} L{x+5:.1f},{y + (6 if z < 0 else -6):.1f} L{x:.1f},{y:.1f} Z" fill="{REF_COLOR[ref]}" data-tip="{esc(tip)}"/>')
            else:
                o.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{REF_COLOR[ref]}" fill-opacity=".6" stroke="var(--card)" stroke-width="1" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_tail(frows, zcol, nu, s, ref, lang, H, W=900, Hh=340):
    """Table A2: P(|z| > t) observed against the normal and the fitted Student-t (log vertical axis)."""
    Lm, R, Tp, B = 64, 130, 16, 40
    z = np.sort(np.abs([float(r[zcol]) for r in frows if r[zcol]]))
    n = len(z)
    tmax, lo = 7.0, 1e-3

    def X(v): return Lm + v / tmax * (W - Lm - R)

    def Y(v): return Tp + (0 - math.log10(max(v, lo))) / (0 - math.log10(lo)) * (Hh - Tp - B)
    o = _svg(W, Hh, "꼬리 분포 그림" if lang == "ko" else "Tail plot")
    for t in (1e-3, 1e-2, 1e-1, 1):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{t:g}</text>')
    for t in range(0, 8):
        o.append(f'<text x="{X(t):.1f}" y="{Hh-18}" text-anchor="middle">{t}</text>')
    o.append(f'<text x="{(Lm + W - R) / 2:.0f}" y="{Hh-2}" text-anchor="middle">|z|</text>')
    ts = np.linspace(0, tmax, 141)
    for vals, colr, name in (([2 * stats.norm.sf(t) for t in ts], "var(--s1)", "정규분포" if lang == "ko" else "normal"),
                             ([2 * stats.t.sf(t / s, nu) for t in ts], REF_COLOR[ref], f"Student-t (ν={nu:.2f})")):
        pts = [(t, v) for t, v in zip(ts, vals) if v >= lo]
        d = " ".join(f"{'M' if i == 0 else 'L'}{X(t):.1f},{Y(v):.1f}" for i, (t, v) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="2" stroke-dasharray="{"5 4" if name.startswith("Student") else "none"}"/>')
        last = pts[-1]
        o.append(f'<text x="{min(X(last[0]) + 6, W - R + 4):.1f}" y="{Y(last[1]) - 6:.1f}">{name}</text>')
    path, prev = [f"M{X(0):.1f},{Y(1):.1f}"], 1.0
    for i, t in enumerate(z[:-1], start=1):
        if t > tmax:
            break
        sv = (n - i) / n
        path.append(f"L{X(t):.1f},{Y(prev):.1f}L{X(t):.1f},{Y(sv):.1f}")
        prev = sv
    path.append(f"L{X(min(z[-1], tmax)):.1f},{Y(prev):.1f}")
    o.append(f'<path d="{"".join(path)}" fill="none" stroke="var(--fg2)" stroke-width="2"/>')
    for k in (1, 2, 3):
        r = float(np.mean(z > k))
        o.append(f'<circle class="dot" cx="{X(k):.1f}" cy="{Y(r):.1f}" r="5" fill="var(--fg2)" stroke="var(--card)" stroke-width="2" data-tip="|z| > {k}: {r*100:.1f}% (n={n})"/>')
    o.append(f'<text x="{X(4.6):.1f}" y="{Y(max(float(np.mean(z > 4.6)), lo)) + 16:.1f}">{"관측(표 A2)" if lang == "ko" else "observed (Table A2)"}</text>')
    o.append("</svg>")
    return "".join(o)


EVENTS = [
    # (year or (from, to), label ko, label en, source ko, source en). Only events traceable in the data or the notes.
    (1929, "Hubble 1929", "Hubble 1929",
     "Huchra 목록 1929년의 유일한 행(1차 부호 A): Hubble 1929, PNAS 15, 168.", "The one 1929 row of Huchra's list (primary code A): Hubble 1929, PNAS 15, 168."),
    ((1960, 1997), "Sandage 외 대 de Vaucouleurs 외", "Sandage et al. vs. de Vaucouleurs et al.",
     "Huchra 목록의 설명문: 「1960년에는 Sandage 외 대 de Vaucouleurs 외의 긴 거리 척도 대 짧은 거리 척도 논쟁의 무대가 마련되어 있었다(H ~ 50 대 H ~ 100)」. 2차 부호 V(deVaucouleurs 또는 van den Bergh) 행 {nV}건은 {V0}~{V1}년, S(Sandage 또는 Tammann) 행 {nS}건은 {S0}~{S1}년에 있다. 띠는 V 부호 행의 기간이다.",
     "The explanatory text of Huchra's list: \"By 1960, the stage was set for the Sandage et al. versus deVaucouleurs et al. debate on the long versus short distance scale, H ~ 50 versus H ~ 100.\" The {nV} rows with secondary code V (deVaucouleurs or van den Bergh) span {V0}–{V1}, the {nS} rows with code S (Sandage and/or Tammann) {S0}–{S1}. The band spans the V rows."),
    ((1979, 2010), "HST Key Project (K)", "HST Key Project (K)",
     "2차 부호 K(Key Project 또는 그 팀원) 행 {nK}건, {K0}~{K1}년. 목록 자체가 Key Project 의 일부로 작성되었다.", "The {nK} rows with secondary code K (Key Project or a Key Project team member), {K0}–{K1}. The list itself was assembled as part of the Key Project."),
    (2001, "Key Project 최종", "Key Project final",
     "Freedman 외 2001, ApJ 553, 47–72 (arXiv astro-ph/0012376): 「H0 = 72 ± 8」(초록).", "Freedman et al. 2001, ApJ 553, 47–72 (arXiv astro-ph/0012376): \"H0 = 72 ± 8\" (abstract)."),
    (2013, "Planck 2013", "Planck 2013",
     "Planck 2013 결과 XVI, A&A 571, A16 (2014; arXiv 1303.5076): 「H0 = 67.3 ± 1.2」(초록).", "Planck 2013 results XVI, A&A 571, A16 (2014; arXiv 1303.5076): \"H0 = 67.3 ± 1.2\" (abstract)."),
    (2018, "Planck 2018", "Planck 2018",
     "기준값 67.36 ± 0.54 (Planck 2018 결과 VI, 표 2). 표 A2 의 2018년 행 「67.4 ± 0.5」는 그 반올림 값이다.", "Reference value 67.36 ± 0.54 (Planck 2018 results VI, Table 2). The 2018 row \"67.4 ± 0.5\" of Table A2 is its rounded value."),
    (2022, "SH0ES 2022", "SH0ES 2022",
     "기준값 73.04 ± 1.04 (Riess 외 2022, 초록).", "Reference value 73.04 ± 1.04 (Riess et al. 2022, abstract)."),
]


def event_facts(codes):
    c = {(r["kind"], r["code"]): r for r in codes}
    f = {}
    for k in "SVK":
        r = c[("secondary", k)]
        f[f"n{k}"], f[f"{k}0"], f[f"{k}1"] = r["n"], r["first_year"], r["last_year"]
    return f


def _bands(decades, X, Y, lang, esc, o, label_n=True):
    for d in decades:
        d0, n = int(d["decade"]), int(d["n"])
        xa, xb = X(d0) + 3, X(d0 + 10) - 3
        if d["h0_median"]:
            q1, med, q3 = float(d["h0_q1"]), float(d["h0_median"]), float(d["h0_q3"])
            tip = f'{d0}{"년대" if lang == "ko" else "s"}: n={n}, {"중앙값" if lang == "ko" else "median"} {med:g}, {"사분위" if lang == "ko" else "quartiles"} {q1:g}–{q3:g}'
            o.append(f'<rect class="dot" x="{xa:.1f}" y="{Y(q3):.1f}" width="{xb-xa:.1f}" height="{max(2, Y(q1)-Y(q3)):.1f}" rx="3" fill="var(--fg3)" fill-opacity=".22" stroke="none" data-tip="{esc(tip)}"/>')
            o.append(f'<line x1="{xa:.1f}" x2="{xb:.1f}" y1="{Y(med):.1f}" y2="{Y(med):.1f}" stroke="var(--fg2)" stroke-width="2"/>')
        if label_n:
            o.append(f'<text x="{(xa+xb)/2:.1f}" y="{label_n:.1f}" text-anchor="middle" font-size="10">n={n}</text>')


def chart_timeline(decades, frows, codes, lang, H, W=900, Hh=460):
    """The chronology: Table A2 rows as dots with error bars, Huchra's list as decade bands (quartiles, median),
    the two reference lines, and the events of EVENTS along the top. Log vertical axis."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 110, 92, 56
    x0, x1, lo, hi = 1925, 2025, 30, 800

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)
    Y = _logy(lo, hi, Tp, B, Hh)
    o = _svg(W, Hh, "H0 연대기 1929~2022" if lang == "ko" else "H0 chronology, 1929–2022")
    for t in (30, 50, 70, 100, 200, 300, 500):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{t}</text>')
    for yv in range(1930, 2030, 10):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-32}" text-anchor="middle">{yv}</text>')
    _bands(decades, X, Y, lang, esc, o, label_n=Hh - B + 12)
    for r in frows:
        x, v, u = X(int(r["year"])), float(r["h0"]), float(r["u_mean"])
        tip = f'{r["year"]}: {r["h0"]} ± {r["err_as_printed"]} ({r["ref_label"]})'
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(v+u):.1f}" y2="{Y(max(v-u, lo)):.1f}" stroke="var(--s1)" stroke-opacity=".45" stroke-width="1.5"/>')
        o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(v):.1f}" r="3.5" fill="var(--s1)" stroke="var(--card)" stroke-width="1" data-tip="{esc(tip)}"/>')
    for ref, dy in (("planck18", 12), ("riess22", -5)):
        v = float(REFS[ref]["value"])
        o.append(f'<line x1="{Lm}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{REF_COLOR[ref]}" stroke-width="2" stroke-dasharray="6 4"/>')
        o.append(f'<text x="{W-R+6}" y="{Y(v)+dy:.1f}" fill="{REF_COLOR[ref]}">{"Planck" if ref == "planck18" else "SH0ES"} {REFS[ref]["value"]}</text>')
    # events along the top, two rows
    rows_by_when = {1929: 0, (1960, 1997): 1, (1979, 2010): 0, 2001: 1, 2013: 2, 2018: 1, 2022: 0}
    for i, (when, lko, len_, _, _) in enumerate(EVENTS):
        row = rows_by_when.get(when, i % 2)
        yl = 16 + row * 30
        lab = lko if lang == "ko" else len_
        if isinstance(when, tuple):
            xa, xb = X(when[0]), X(when[1])
            o.append(f'<line x1="{xa:.1f}" x2="{xb:.1f}" y1="{yl+8}" y2="{yl+8}" stroke="var(--accent2)" stroke-width="3" stroke-opacity=".7"/>')
            o.append(f'<text x="{(xa+xb)/2:.1f}" y="{yl}" text-anchor="middle" font-size="11">{esc(lab)}</text>')
        else:
            x = X(when)
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{yl+4}" y2="{Tp-4}" stroke="var(--accent2)" stroke-width="1" stroke-dasharray="2 3"/>')
            o.append(f'<circle cx="{x:.1f}" cy="{yl+4}" r="3" fill="var(--accent2)"/>')
            anchor = "end" if when > 2010 else "middle"
            o.append(f'<text x="{x + (4 if anchor == "end" else 0):.1f}" y="{yl-2}" text-anchor="{anchor}" font-size="11">{esc(lab)}</text>')
    o.append("</svg>")
    return "".join(o)


def chart_zoom(decades, frows, lang, H, W=900, Hh=380):
    """The same elements from 1970 on a linear axis (40–110)."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 110, 26, 40
    x0, x1, lo, hi = 1970, 2024, 40, 110

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)

    def Y(v): return Tp + (hi - max(lo, min(hi, v))) / (hi - lo) * (Hh - Tp - B)
    o = _svg(W, Hh, "H0 연대기 1970~2022 확대" if lang == "ko" else "H0 chronology, 1970–2022, enlarged")
    for t in range(40, 111, 10):
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{t}</text>')
    for yv in range(1970, 2025, 5):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-14}" text-anchor="middle">{yv}</text>')
    _bands([d for d in decades if int(d["decade"]) >= 1970], X, Y, lang, esc, o, label_n=False)
    clipped = "집계 생략(3건 미만)" if lang == "ko" else "count only (fewer than 3 rows)"
    for r in frows:
        x, v, u = X(int(r["year"])), float(r["h0"]), float(r["u_mean"])
        tip = f'{r["year"]}: {r["h0"]} ± {r["err_as_printed"]} ({r["ref_label"]})'
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(v+u):.1f}" y2="{Y(v-u):.1f}" stroke="var(--s1)" stroke-opacity=".45" stroke-width="1.5"/>')
        if lo <= v <= hi:
            o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(v):.1f}" r="4" fill="var(--s1)" stroke="var(--card)" stroke-width="1" data-tip="{esc(tip)}"/>')
        else:
            o.append(f'<path class="dot" d="M{x-5:.1f},{Y(v) + (6 if v < lo else -6):.1f} L{x+5:.1f},{Y(v) + (6 if v < lo else -6):.1f} L{x:.1f},{Y(v):.1f} Z" fill="var(--s1)" data-tip="{esc(tip)}"/>')
    for ref, dy in (("planck18", 14), ("riess22", -5)):
        v = float(REFS[ref]["value"])
        o.append(f'<line x1="{Lm}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{REF_COLOR[ref]}" stroke-width="2" stroke-dasharray="6 4"/>')
        o.append(f'<text x="{W-R+6}" y="{Y(v)+dy:.1f}" fill="{REF_COLOR[ref]}">{"Planck" if ref == "planck18" else "SH0ES"} {REFS[ref]["value"]}</text>')
    del clipped
    o.append("</svg>")
    return "".join(o)


def chart_types(types, decades, lang, H, W=900):
    """Rows per decade and primary type code as a heat grid: one hue, darker = larger share of the decade's rows;
    the count printed in each cell. Codes with fewer than 10 rows in all are folded into 'other codes'."""
    esc = H["esc"]
    prim = [r for r in types if r["kind"] == "primary"]
    tot = {}
    for r in prim:
        tot[r["code"]] = tot.get(r["code"], 0) + int(r["n"])
    main = [c for c, n in sorted(tot.items(), key=lambda kv: (-kv[1], kv[0])) if n >= 10]
    rest = [c for c in tot if c not in main]
    decs = [int(d["decade"]) for d in decades]
    dn = {int(d["decade"]): int(d["n"]) for d in decades}
    cell = {}
    for r in prim:
        key = r["code"] if r["code"] in main else "other"
        cell[(int(r["decade"]), key)] = cell.get((int(r["decade"]), key), 0) + int(r["n"])
    rows = main + ["other"]
    Lm, Tp, rh = 190, 44, 26
    cw = (W - Lm - 10) / len(decs)
    Hh = Tp + rh * len(rows) + 10
    o = _svg(W, Hh, "10년 단위 방법 부호 건수" if lang == "ko" else "Rows per decade and method code")
    for j, d in enumerate(decs):
        x = Lm + (j + 0.5) * cw
        o.append(f'<text x="{x:.1f}" y="18" text-anchor="middle">{d}{"년대" if lang == "ko" else "s"}</text><text x="{x:.1f}" y="34" text-anchor="middle" font-size="10">n={dn[d]}</text>')
    other = "그 밖의 부호" if lang == "ko" else "other codes"
    for i, c in enumerate(rows):
        y = Tp + i * rh
        lab = f'{c} · {TYPE_PRIMARY.get(c, "?")}' if c != "other" else f'{other} ({", ".join(sorted(rest))})'
        o.append(f'<text x="{Lm-8}" y="{y+rh/2+4:.1f}" text-anchor="end">{esc(lab)}</text>')
        for j, d in enumerate(decs):
            k = cell.get((d, c), 0)
            share = k / dn[d] if dn[d] else 0
            x = Lm + j * cw
            tip = f'{d}{"년대" if lang == "ko" else "s"} · {lab}: {k} ({share*100:.0f}%)'
            o.append(f'<rect class="dot" x="{x+1:.1f}" y="{y+1}" width="{cw-2:.1f}" height="{rh-2}" rx="3" fill="var(--s1)" fill-opacity="{0.06 + 0.8 * share:.2f}" data-tip="{esc(tip)}"/>')
            if k:
                o.append(f'<text x="{x+cw/2:.1f}" y="{y+rh/2+4:.1f}" text-anchor="middle" fill="{"var(--card)" if share > 0.45 else "var(--fg)"}">{k}</text>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ pages
def credit(lang, H, which=("huchra", "faerber")):
    esc = H["esc"]
    lab = "자료 출처" if lang == "ko" else "Sources"
    return '<p class="src" style="margin-top:2rem;font-size:.82rem;color:var(--fg3)">' + f"{lab}: " + " · ".join(esc(H0_SOURCES[k]["credit"]) for k in which) + "</p>"


def sources_block(lang, H):
    esc = H["esc"]
    out = []
    for k in ("huchra", "faerber"):
        s = H0_SOURCES[k]
        out.append(f'<div class="note"><b>{esc(s["short_ko"] if lang == "ko" else s["short_en"])}</b> — {esc(s[lang])} <a href="{esc(s["url"])}">{esc(s["url"])}</a></div>')
    return "".join(out)


def leaf(lang, t, cur):
    return dict(crumbs=[(("홈" if lang == "ko" else "Home"), "../index.html"), (t["nav"], "index.html")], cur=cur,
                groups=[(t["metrics"], [(f'{m["id"].upper()} · {m[lang]["name"]}', f'{m["id"]}.html') for m in H0_METRICS]),
                        (t["pages"], [(t["timeline"], "timeline.html"), (t["method"], "method.html")])])


def h1_table(D, lang, t, table):
    rows = []
    for (s, start, var), r in D["h1"].items():
        rows.append([SERIES_LABEL[lang][s], t["all"] if s == FA else (t["start1929"] if start == 1929 else t["start1950"]), t["median"] if var == "yearly_median" else t["frontier"],
                     r["n_points"], f'{r["first"]}–{r["last"]}', f'{r["slope_log2_per_year"]} ({r["slope_se"]})', r["halflife_years"], f'{r["halflife_ci_low"]}–{r["halflife_ci_high"]}', r["r2"], r["n_rows"]])
    return table([t["series"], t["start"], t["variant"], t["nyears"], t["span"], t["slope"] + " (SE)", t["hl"], t["ci"], "R²", t["rows"]], rows, num_cols=(3, 5, 6, 7, 8, 9))


def h3_table(D, lang, t, table):
    rows = []
    for (s, start, ref, cl), r in D["h3"].items():
        lab = SERIES_LABEL[lang][s] + ("" if cl == "year" else (" — 군집 = Type 부호(감도)" if lang == "ko" else ", cluster = type code (sensitivity)"))
        rows.append([lab, t["all"] if s == FA else (t["start1929"] if start == 1929 else t["start1950"]), REFS[ref][lang], r["n"], r["n_excluded"], r["below_ref"],
                     f'{pct(r["miss_1sigma"])} [{cip(r["miss_1sigma_ci"])}]', f'{pct(r["miss_2sigma"])} [{cip(r["miss_2sigma_ci"])}]',
                     f'{pct(r["inside_iq"])} [{cip(r["inside_iq_ci"])}]', f'{pct(r["surprise"])} [{cip(r["surprise_ci"])}]', r["median_abs_z"]])
    return table([t["series"], t["start"], t["ref"], "n", t["excl"], t["below"], t["m1"], t["m2"], t["iq"], t["si"], t["medz"]], rows, num_cols=(3, 4, 5, 6, 7, 8, 9, 10))


def h4_table(D, lang, t, table):
    rows = []
    for (s, start, ref), r in D["h4"].items():
        rows.append([SERIES_LABEL[lang][s], t["all"] if s == FA else (t["start1929"] if start == 1929 else t["start1950"]), REFS[ref][lang], r["n"], r["n_excluded"],
                     r["nu"], f'{r["nu_ci_low"]}–{r["nu_ci_high"]}', r["scale"], f'{r["scale_ci_low"]}–{r["scale_ci_high"]}'])
    return table([t["series"], t["start"], t["ref"], "n", t["excl"], "ν", t["ci"], t["scale"], t["ci"]], rows, num_cols=(3, 4, 5, 6, 7, 8))


def a2_table(frows, lang, t, table, esc):
    rows = []
    for r in frows:
        note = ""
        if r["year"] == "2018" and r["h0"] == "67.4" and r["err_as_printed"] == "0.5":
            note = "Planck 2018 의 반올림 값 — Planck 기준에서 뺌" if lang == "ko" else "rounded Planck 2018 value, left out against Planck"
        rows.append([r["year"], r["h0"], esc(r["err_as_printed"]), esc(r["ref_label"]), r["z_planck18"] or "—", r["z_riess22"], esc(note)])
    return table([t["year"], t["h0"], t["err"], t["author"], t["z_p"], t["z_r"], ("비고" if lang == "ko" else "Note")], rows, num_cols=(1, 2, 4, 5))


def method_body(lang, N, D, t, H):
    esc, table = H["esc"], H["table"]
    codes = {(r["kind"], r["code"]): r for r in D["codes"]}
    prim = sorted([r for r in D["codes"] if r["kind"] == "primary"], key=lambda r: (-int(r["n"]), r["code"]))
    sec = sorted([r for r in D["codes"] if r["kind"] == "secondary"], key=lambda r: (-int(r["n"]), r["code"]))
    unv = "미확인(범례에 없음)" if lang == "ko" else "unverified (not in the legend)"
    ptab = table([t["code"], t["meaning"], t["rows"], t["first"], t["last"]],
                 [[r["code"], esc(TYPE_PRIMARY.get(r["code"], unv)), r["n"], r["first_year"], r["last_year"]] for r in prim], num_cols=(2, 3, 4))
    stab = table([t["code"], t["meaning"], t["rows"], t["first"], t["last"]],
                 [[r["code"], esc(TYPE_SECONDARY.get(r["code"], unv)), r["n"], r["first_year"], r["last_year"]] for r in sec], num_cols=(2, 3, 4))
    none_n = 1   # one row of the list carries no type code (stage 1, notes/1.2-hubble-sources.md 7.4)
    if lang == "ko":
        return f"""<div class="prose"><h1>허블 상수 장 — 방법·한계</h1>
<div class="takeaway"><b>핵심</b><ul><li>두 집성을 쓴다. Huchra 목록(1927~2010, 553건)은 재게시 허락 문장이 없어 집계만 싣고, Faerber & López-Corredoira(2020) 표 A2(1976~2019, 163건, CC BY 4.0)는 행 단위로 싣는다.</li><li>두 집성 모두 오차가 몇 σ 인지 적지 않아 「수준 미표기」계열로 다루고 1σ 로 바꿔 부르지 않는다.</li><li>지표는 H1·H3·H4 이고 H2 는 내지 않는다. 기준값은 Planck 2018 과 Riess 외 2022 를 나란히 둔다. 관찰 자료의 집계이며 원인을 말하지 않는다.</li></ul></div>
<h2>자료원과 이용 조건</h2>{sources_block(lang, H)}
<p>Huchra 목록에 대해서는 허락을 구하지 않았다(저자는 2010년에 작고했고, 사본의 관리자와 권리 승계는 확인되지 않았다). 표 A2 는 164행이 인쇄돼 있고 본문은 163건이라 한다. 「1998, 62 ± 6, Croft and Dailey」가 두 번 인쇄돼 있어 둘째 것을 뺐다. 그러면 Croft & Dailey 120 + 1976~1989년 8 + 2011~2019년 35 = 163 으로 논문이 적은 구성과 맞는다. 위·아래 오차가 다른 행은 {N['fa_asym']}개로, 원 표기를 CSV 의 err_as_printed 열에 남겼다.</p>
<h2>두 집성이 겹치는 기간(1976~2010)</h2>
<p>같은 측정으로 볼 수 있는 짝은 연도가 1년 이내, H0 차이 0.5 이내, 오차 차이가 0.5 또는 큰 쪽 오차의 10% 이내인 행으로 정했다(1976~1989년 행은 저자 이름도 Huchra 의 문헌 칸에 있어야 한다). 표 A2 의 128행 가운데 69행이 Huchra 목록과 짝이 되고(연도·값·오차가 모두 같은 것 42), 59행은 Huchra 목록에 없다. 1990~2010년의 120행 중 65행이 짝이 된다. 두 집성을 합친 계열(짝이 된 행은 한 번만 셈)은 감도 표에만 싣는다 — 값으로만 맞춘 짝이 있어 과잉 제거일 수 있다. Huchra 와 표 A2 를 짝지은 행 단위 대조표는 공개하지 않는다.</p>
<h2>오차의 수준</h2>
<p>두 집성 모두 오차가 몇 σ 인지 적지 않았다. Huchra 목록의 설명문은 「외부 오차가 있으면 그것을, 없으면 저자가 인용한 오차를 적당히 반올림해 쓴다」고 적고, 표 A2 의 논문은 표의 오차를 χ² 의 σ_i 로 쓰며 「주어진 오차 막대는 모든 통계적 효과를 포함한다」고 적는다. 둘 다 신뢰 수준의 진술은 아니다. 그래서 이 장의 오차는 「수준 미표기」계열로 다루고 1σ 로 바꿔 부르지 않는다. 위·아래 오차가 다른 행은 평균을 쓴다. 참고로 Chen, Gott & Ratra(2003)는 Huchra 목록의 위·아래 오차를 1 표준편차 오차 막대로 다뤘다 — 그 논문의 해석이지 집성의 진술은 아니다.</p>
<h2>지표와 결정</h2>
<ul><li><b>H1 정밀도 반감기.</b> 해마다 상대 오차(u/|x|)의 중앙값을 취해 log₂ 를 연도에 회귀한다(본값). 해마다 가장 작은 상대 오차만 쓰는 정밀도 최전선을 참고로 나란히 둔다. 구간은 기울기의 t 구간.</li>
<li><b>H2 — 내지 않음.</b> {esc(H2_TEXT["ko"])}</li>
<li><b>H3 기준값 대비 놀람 지수.</b> z = (기준값 − x)/u_x 로 |z| > 1, |z| > 2, |z| < 0.674(사분위 안), |z| > 2.326 의 비율. 기준값은 Planck 2018(67.36 ± 0.54 — {esc(REFS["planck18"]["cite_ko"])})과 Riess 외 2022(73.04 ± 1.04 — {esc(REFS["riess22"]["cite_ko"])})를 나란히 둔다. 기준값의 불확도는 z 에 들어가지 않는다. 구간은 출판 연도를 군집으로 한 부트스트랩 10,000회(시드 2026). Huchra 목록은 Type 부호를 군집으로 한 구간도 감도로 싣는다(더 넓다).</li>
<li><b>H4 t 분포 자유도.</b> H3 의 z 에 중심 0 Student-t 를 최대우도로 맞춘 ν(부트스트랩 2,000회).</li>
<li><b>표 A2 의 2018년 행 「67.4 ± 0.5」.</b> 논문 3절이 같은 수를 우주배경복사에서 얻은 값으로 인용하는 Planck 2018 의 반올림 값이다(표의 참고문헌 [96]은 표준 사이렌 전망 논문). 기준값 자체가 계열에 들어가지 않도록 Planck 기준 H3·H4 에서 이 행을 뺐다(표 A2 162건). Riess 기준에서는 163건 그대로다.</li>
<li><b>시작 연도.</b> 기본 계산은 1929년부터이고 1950년부터의 값을 병기한다. Huchra 목록의 1929년 이전 행 2개(1927년, 1928년 — 둘 다 1차 부호 O, 위 오차에 부호가 없는 형식)는 기본 계산에서 뺀다. 오차가 없는 행 3개(1978·1984·1986년)도 쓰지 않는다.</li>
<li><b>집계의 표시.</b> Huchra 목록의 연도별·10년별 집계는 건수와 H0·상대 오차의 사분위(선형 보간)만 싣고, 3건 미만인 해는 건수만 적는다 — 한두 건의 중앙값은 곧 그 행의 값이기 때문이다. 1929~2010년 51개 해 가운데 {N['h1_hu_small']}개 해가 그렇다. 1940년대에는 행이 없다.</li>
<li><b>번호.</b> 정의가 M1~M4 와 달라 H1~H4 로 새로 붙였다(원자량 장의 A1~A5 와 같은 방식).</li></ul>
<h2>방법 부호</h2>
<p>Huchra 목록의 Type 부호를 그대로 쓴다. 새 분류를 붙이지 않는다. 1차 부호(방법)와 2차 부호(저자군·조건)의 뜻은 파일의 범례 그대로이고, 범례에 없는 부호(1차 I·M, 2차 T)는 미확인으로 둔다. 부호가 없는 행이 {none_n}개 있다. 표 A2 에는 방법 열이 없다. 건수는 1929년 이후 오차 있는 행 기준이다.</p>
<h3>1차 부호</h3>{ptab}<h3>2차 부호</h3>{stab}
<h2>한계</h2>
<ul><li>두 집성은 각각 전수 조사가 아니다. 겹치는 기간에서도 표 A2 의 절반 가까이가 Huchra 목록에 없고, Huchra 목록의 대부분은 표 A2 에 없다.</li>
<li>오차의 뜻(통계만인지, 계통 포함인지, 몇 σ 인지)이 행마다 다를 수 있고 집성은 그것을 적지 않았다.</li>
<li>같은 해 측정이 여럿이라 H1 은 해별 요약에 기대며, 초기 연도는 점이 하나뿐인 해가 많다.</li>
<li>H3 는 기준값의 선택에 따라 어느 쪽이 「놀람」이 되는지가 바뀐다. 두 기준을 나란히 두는 이유다. 이 사이트는 긴장이 실재하는지, 어느 기준이 맞는지를 판정하지 않는다.</li>
<li>같은 보정자·같은 자료·같은 팀의 갱신은 독립 측정이 아니다. 연도 군집 부트스트랩은 그 의존의 일부만 다룬다.</li>
<li>표 A2 의 1990~2010년 행은 원 논문을 알 수 없어, 같은 논문의 값이 두 집성에 한 번씩 들어가는 것을 완전히 막지 못했다.</li>
<li>표 A2 의 출판본(MDPI)과 arXiv 판의 대조, Planck 2018·Riess 외 2022 원문의 쪽·표 재확인은 이 판에서 네트워크가 막혀 하지 못했다(1단계 기록을 따름).</li></ul>
<h2>재현</h2><p>표 A2 는 <code>h0_faerber.py</code> 가 arXiv PDF 의 문자층에서 읽어 <code>h0_faerber2020.csv</code> 로 쓴다. H1·H3·H4 는 <code>h0_stage1b.py</code> 가 <code>metrics.py</code> 의 공식을 어댑터(<code>h0_metrics.py</code>)로 불러 계산한다. Huchra 목록의 집계는 <code>h0_aggregate.py</code>, 면은 <code>h0_site.py</code>(정의 문장은 <code>h0_registry.py</code>)가 만든다. Huchra 목록 원 파일은 공개 저장소에 싣지 않는다.</p></div>"""
    return f"""<div class="prose"><h1>Hubble constant — method and limits</h1>
<div class="takeaway"><b>Takeaway</b><ul><li>Two compilations are used. Huchra's list (1927–2010, 553 rows) grants no right to republish and is shown only in aggregate; Table A2 of Faerber & López-Corredoira (2020) (1976–2019, 163 rows, CC BY 4.0) is shown row by row.</li><li>Neither compilation states the confidence level of its errors, so they are treated as an "unstated" series and not relabeled as 1σ.</li><li>The metrics are H1, H3 and H4; H2 is not produced. Two references, Planck 2018 and Riess et al. 2022, are shown side by side. The pages aggregate observed records and state no cause.</li></ul></div>
<h2>Sources and terms of use</h2>{sources_block(lang, H)}
<p>No permission was sought for Huchra's list (the author died in 2010; who maintains the copy and holds the rights could not be established). Table A2 prints 164 rows while the text counts 163: the row "1998, 62 ± 6, Croft and Dailey" is printed twice and the second copy is dropped. The remainder, 120 Croft & Dailey + 8 (1976–1989) + 35 (2011–2019), matches the paper's own breakdown. {N['fa_asym']} rows have different upper and lower errors; the printed form is kept in the err_as_printed column of the CSV.</p>
<h2>Where the two compilations overlap (1976–2010)</h2>
<p>Two rows are taken as the same estimate when their years are at most one apart, H0 differs by at most 0.5, and the errors differ by at most 0.5 or 10% of the larger one (for the named rows of 1976–1989 the surname must also appear in Huchra's reference text). Of the 128 Table A2 rows in this span, 69 pair with a Huchra row (42 with identical year, value and error) and 59 are absent from Huchra's list; 65 of the 120 Croft & Dailey rows pair. A merged series (paired rows counted once) appears only in the sensitivity tables, since pairs matched on values alone may remove too much. The row-level comparison of Huchra and Table A2 is not published.</p>
<h2>What the errors mean</h2>
<p>Neither compilation states the confidence level of its errors. The explanatory text of Huchra's list says that external errors are used when available and otherwise the errors quoted by the authors, appropriately rounded; the Table A2 paper uses the errors as σ_i in χ² and says that "the given error bars account for all statistical effects". Neither is a statement of a confidence level. The chapter therefore treats the errors as one "unstated" series and does not relabel them as 1σ. Asymmetric errors enter as the mean of the two. For the record, Chen, Gott & Ratra (2003) treated Huchra's upper and lower errors as one-standard-deviation error bars; that is the authors' reading, not a statement of the compilation.</p>
<h2>Metrics and decisions</h2>
<ul><li><b>H1 precision half-life.</b> The yearly median of the relative error (u/|x|), log₂-regressed on year (main value); the precision frontier (the smallest relative error of each year) as a reference. Interval: t interval of the slope.</li>
<li><b>H2, not produced.</b> {esc(H2_TEXT["en"])}</li>
<li><b>H3 surprise against a reference.</b> z = (reference − x)/u_x, with the shares |z| > 1, |z| > 2, |z| < 0.674 (inside the interquartile band) and |z| > 2.326. Two references side by side: Planck 2018 (67.36 ± 0.54; {esc(REFS["planck18"]["cite_en"])}) and Riess et al. 2022 (73.04 ± 1.04; {esc(REFS["riess22"]["cite_en"])}). The reference's uncertainty does not enter z. Intervals: cluster bootstrap by publication year (10,000 resamples, seed 2026). For Huchra's list, intervals with the type code as cluster are shown as a sensitivity check (they are wider).</li>
<li><b>H4 Student-t degrees of freedom.</b> ν of a zero-centered Student-t fitted by maximum likelihood to the H3 z (2,000 bootstrap resamples).</li>
<li><b>The 2018 row "67.4 ± 0.5" of Table A2.</b> It is the rounded Planck 2018 value, which section 3 of the paper quotes as the value derived from the cosmic microwave background (the table's reference [96] is a standard-siren forecast paper). So that the reference itself does not enter the series, the row is left out of H3 and H4 against Planck (162 rows); against Riess all 163 rows are used.</li>
<li><b>Start year.</b> The baseline starts in 1929; values from 1950 are shown alongside. The two rows before 1929 in Huchra's list (1927 and 1928, both primary code O, both with an unsigned upper error) are left out of the baseline, as are the three rows without an error (1978, 1984, 1986).</li>
<li><b>How aggregates are shown.</b> The yearly and decade aggregates of Huchra's list give only counts and the quartiles (linear interpolation) of H0 and of the relative error, and a year with fewer than three rows gives its count only, since the median of one or two rows is a printed value. {N['h1_hu_small']} of the 51 years from 1929 to 2010 are such years. The 1940s have no row.</li>
<li><b>Numbering.</b> The definitions differ from M1–M4, so the metrics are numbered H1–H4 (as A1–A5 in the atomic-weights chapter).</li></ul>
<h2>Method codes</h2>
<p>Huchra's type codes are used as printed; no new classification is added. The meanings of the primary codes (method) and secondary codes (authors, conditions) are the file legend's own words, and codes absent from the legend (primary I and M, secondary T) are left unverified. {none_n} row has no code. Table A2 has no method column. Counts are over the rows with an error from 1929 on.</p>
<h3>Primary codes</h3>{ptab}<h3>Secondary codes</h3>{stab}
<h2>Limits</h2>
<ul><li>Neither compilation is complete. Even in the overlapping years nearly half of Table A2 is absent from Huchra's list, and most of Huchra's list is absent from Table A2.</li>
<li>What an error means (statistical only or with systematics, and at what level) may differ from row to row; the compilations do not say.</li>
<li>Several estimates share a year, so H1 rests on a yearly summary; many early years have a single point.</li>
<li>Which side counts as "surprising" in H3 depends on the reference, which is why two are shown. The site does not decide whether the tension is real or which reference is right.</li>
<li>Estimates sharing a calibrator, the same data or the same team are not independent; the year-cluster bootstrap handles only part of that dependence.</li>
<li>The 1990–2010 rows of Table A2 cannot be traced to their papers, so the same paper may enter the two compilations once each.</li>
<li>The check of Table A2 against the published (MDPI) version, and a re-reading of the page and table numbers in Planck 2018 and Riess et al. 2022, could not be done in this version (network blocked); the stage-1 records were used.</li></ul>
<h2>Reproduction</h2><p>Table A2 is read from the text layer of the arXiv PDF by <code>h0_faerber.py</code> into <code>h0_faerber2020.csv</code>. H1, H3 and H4 are computed by <code>h0_stage1b.py</code>, which calls the formulas of <code>metrics.py</code> through the adapter <code>h0_metrics.py</code>. The aggregates of Huchra's list come from <code>h0_aggregate.py</code>; the pages from <code>h0_site.py</code> (definitions in <code>h0_registry.py</code>). The original file of Huchra's list is not included in the public repository.</p></div>"""


def build(lang, base, H, out_root):
    esc, page, table, takeaway, spec_block = H["esc"], H["page"], H["table"], H["takeaway"], H["spec_block"]
    t = L[lang]
    D = load()
    N = numbers(D, H["N"])
    d = base / "hubble"
    d.mkdir(parents=True, exist_ok=True)
    for f in PUBLIC:
        (out_root / "data" / f).write_bytes((DATA / f).read_bytes())
    ko = lang == "ko"

    # ---------- chapter index
    if ko:
        tk = [f"Huchra 목록(1929~2010, {N['h3_hu_n']}건)에서 해별 중앙값 상대 오차는 {N['h1_hu_med']}년마다 절반이 되었다. 표 A2(1976~2019, {N['fa_rows']}건)는 {N['h1_fa_med']}년이다.",
              f"Planck 2018 을 기준으로 하면 Huchra 목록의 {N['h3_hu_p_m2']}% 가 인용 오차의 2배 밖에 있고(정규 기대 4.6%), Riess 외 2022 를 기준으로 하면 {N['h3_hu_r_m2']}% 다. 표 A2 는 {N['h3_fa_p_m2']}% 와 {N['h3_fa_r_m2']}%. 어느 기준에서도 정규분포가 예상하는 것보다 자주 빗나간다.",
              f"z 에 맞춘 Student-t 의 자유도는 ν ≈ {N['h4_hu_p_nu']}~{N['h4_hu_r_nu']}(Huchra 목록)로 두꺼운 꼬리다. 물리 상수 장의 판 쌍 ν 는 {N['m4_nu']} 다.",
              "이 장은 긴장의 어느 편이 맞는지를 판정하지 않는다. 인용된 오차가 뒤의 기준값과의 차이를 담았는가를 셀 뿐이다."]
    else:
        tk = [f"In Huchra's list (1929–2010, {N['h3_hu_n']} rows) the yearly median relative error halved every {N['h1_hu_med']} years; in Table A2 (1976–2019, {N['fa_rows']} rows) every {N['h1_fa_med']} years.",
              f"Against Planck 2018, {N['h3_hu_p_m2']}% of Huchra's list lies beyond twice the quoted error (normal: 4.6%); against Riess et al. 2022, {N['h3_hu_r_m2']}%. Table A2: {N['h3_fa_p_m2']}% and {N['h3_fa_r_m2']}%. Under either reference the quoted errors miss more often than a normal distribution predicts.",
              f"A Student-t fitted to the z has ν ≈ {N['h4_hu_p_nu']}–{N['h4_hu_r_nu']} (Huchra's list): a heavy tail. The edition-pair ν of the physical-constants chapter is {N['m4_nu']}.",
              "The chapter does not decide which side of the tension is right; it counts whether quoted errors covered the distance to a later reference."]
    stats_h = f"""<div class="stats">
<a class="stat" href="h1.html"><span class="n">{N['h1_hu_med']}{"년" if ko else " years"}</span><small>{"H1 정밀도 반감기 — Huchra 목록 1929~2010 해별 중앙값(95% 구간 " if ko else "H1 precision half-life, Huchra's list 1929–2010, yearly median (95% interval "}{N['h1_hu_med_ci']}{"); 표 A2 는 " if ko else "); Table A2: "}{N['h1_fa_med']}{"년" if ko else " years"}</small></a>
<a class="stat" href="h3.html"><span class="n">{N['h3_hu_p_m2']}%</span><span class="vs">{"정규 기대 4.6%" if ko else "normal 4.6%"}</span><small>{"H3 — Planck 2018 기준으로 인용 오차의 2배 밖에 있는 Huchra 목록 추정값의 비율(95% 구간 " if ko else "H3: share of Huchra's list beyond twice the quoted error against Planck 2018 (95% interval "}{N['h3_hu_p_m2_ci']}{"); Riess 외 2022 기준 " if ko else "); against Riess et al. 2022 "}{N['h3_hu_r_m2']}%</small></a>
<a class="stat" href="h3.html"><span class="n">{N['h3_hu_p_si']}%</span><span class="vs">{"정규 기대 2%" if ko else "normal 2%"}</span><small>{"H3 놀람 지수(|z| > 2.326), Planck 기준; Riess 기준 " if ko else "H3 surprise index (|z| > 2.326) against Planck; against Riess "}{N['h3_hu_r_si']}%</small></a>
<a class="stat" href="h4.html"><span class="n">ν = {N['h4_hu_p_nu']}</span><small>{"H4 — Huchra 목록의 z 에 맞춘 Student-t 자유도, Planck 기준(95% 구간 " if ko else "H4: Student-t degrees of freedom fitted to the z of Huchra's list, against Planck (95% interval "}{N['h4_hu_p_ci']}{"); Riess 기준 " if ko else "); against Riess "}{N['h4_hu_r_nu']}</small></a></div>"""
    what = ("<h2>무엇을 재는가</h2><div class=\"prose\"><p>허블 상수 H0 는 은하의 후퇴 속도를 거리로 나눈 값으로, 단위는 km s⁻¹ Mpc⁻¹ 이다. CODATA 판과 달리 H0 에는 「다음 판」이 없다. 한 해에 여러 팀이 서로 다른 방법으로 값을 내고, 오늘날에도 초기 우주(우주배경복사)와 후기 우주(거리 사다리) 측정이 서로 다른 값을 낸다. 그래서 이 장은 각 추정값을 두 기준값과 나란히 견주고, 두 기준 모두에 대해 「인용된 오차가 기준값과의 차이를 담았는가」를 센다. 판 사이 이동(M2)에 대응하는 지표는 내지 않는다.</p></div>" if ko else
            "<h2>What is measured</h2><div class=\"prose\"><p>The Hubble constant H0 is the recession velocity of galaxies divided by their distance, in km s⁻¹ Mpc⁻¹. Unlike a CODATA edition, an H0 estimate has no \"next edition\": several teams publish values by different methods in the same year, and today early-universe (cosmic microwave background) and late-universe (distance ladder) measurements give different values. The chapter therefore sets every estimate against two reference values and counts, for both, whether the quoted error covered the distance to the reference. No analogue of the edition-to-edition move (M2) is published.</p></div>")
    h2line = (f'<div class="note"><b>H2 — 내지 않음.</b> 연속 측정 쌍의 |z| 초과 비율은 쌍을 어떻게 묶느냐에 따라 결론이 갈려 내지 않는다. <a href="h2.html">까닭</a>.</div>' if ko else
              f'<div class="note"><b>H2, not produced.</b> The exceedance rate of consecutive pairs changes its verdict with how the pairs are grouped, so no number is published. <a href="h2.html">Why</a>.</div>')
    cards = "".join(f'<a class="card{" d" if m["id"] == "h2" else ""}" href="{m["id"]}.html"><b>{m["id"].upper()} · {esc(m[lang]["name"])}</b><small>{esc(m[lang]["short"])}</small></a>' for m in H0_METRICS)
    pcards = (f'<a class="card" href="timeline.html"><b>{t["timeline"]}</b><small>{"1929~2022년 H0 값과 오차의 흐름, 방법 부호의 변화, 사건" if ko else "H0 values and errors from 1929 to 2022, the changing mix of methods, events"}</small></a>'
              f'<a class="card" href="method.html"><b>{t["method"]}</b><small>{"자료원·이용 조건·오차 수준·결정·부호 표·한계" if ko else "Sources, terms of use, error levels, decisions, code tables, limits"}</small></a>')
    ef = event_facts(D["codes"])
    cap_tl = ("파란 점은 표 A2 의 행(오차 막대는 ± 인용 오차, 비대칭이면 평균), 회색 띠는 Huchra 목록 10년 단위의 사분위 범위와 중앙값(건수 표시), 점선은 두 기준값. 세로축 로그. 위의 사건은 연대기 면에 근거를 적었다." if ko
              else "Blue dots: rows of Table A2 (bars: ± quoted error, the mean if asymmetric). Gray bands: quartile range and median of Huchra's list per decade (with counts). Dashed lines: the two references. Log vertical axis. The events along the top are documented on the chronology page.")
    body = (f'<h1>{esc(t["title"])}</h1><p class="lead">{esc(t["lead"])}</p>' + takeaway(lang, tk) + f'<h2>{t["glance"]}</h2>' + stats_h +
            f'<figure><div class="legend"><span style="--c:var(--s1)">{"표 A2 (행)" if ko else "Table A2 (rows)"}</span><span style="--c:var(--fg3)">{"Huchra 목록 (10년 단위 집계)" if ko else "Huchra (decade aggregates)"}</span><span class="dash" style="--c:var(--s3)">Planck 2018</span><span class="dash" style="--c:var(--s2)">{"Riess 외 2022" if ko else "Riess et al. 2022"}</span></div>{chart_timeline(D["decades"], D["frows"], D["codes"], lang, H)}<figcaption>{esc(cap_tl)}</figcaption></figure>' +
            what + f'<h2>{"두 자료원과 이용 조건" if ko else "The two sources and their terms"}</h2>' + sources_block(lang, H) + h2line +
            f'<h2>{t["metrics"]}</h2><div class="cards">{cards}</div><h2>{t["pages"]}</h2><div class="cards">{pcards}</div>' + credit(lang, H))
    (d / "index.html").write_text(page(lang, t["nav"], body, 2, "hubble"), encoding="utf-8")

    # ---------- metric pages
    for m in H0_METRICS:
        mid = m["id"]
        parts = [f'<p><span class="tag k">{mid.upper()}</span></p><h1>{esc(m[lang]["name"])}</h1><p class="lead">{esc(m[lang]["short"])}</p>']
        if mid == "h2":
            parts.append(f'<div class="prose"><p>{esc(H2_TEXT[lang])}</p><p>{"1단계 감도 표의 요지: Huchra 목록에서 연속 쌍의 |z| > 2 비율은 하나로 묶으면 정규 기대값(4.6%)보다 위였고, Type 부호로 묶으면 구간이 기대값과 겹쳤다. 결론이 묶는 방식에 달려 있어 수치를 싣지 않는다." if ko else "The gist of the stage-1 sensitivity tables: in Huchra\'s list the share of consecutive pairs with |z| > 2 lay above the normal expectation (4.6%) when the list was pooled, and its interval overlapped the expectation when pairs were grouped by type code. The conclusion depends on the grouping, so no number is published."}</p></div>')
        else:
            parts.append(takeaway(lang, [x.format(**N) for x in m["takeaway"][lang]]))
            parts.append(spec_block(m, lang, N))
        if mid == "h1":
            parts.append(f'<figure>{chart_urel_yearly(D["yearly"], lang, H)}<figcaption>{"Huchra 목록, 연도별 집계: 막대는 그해 상대 오차의 사분위 범위, 점은 중앙값. 3건 미만인 해는 × 표시만(건수는 툴팁). 세로축 로그." if ko else "Huchra’s list, aggregated by year: bar = quartile range of the relative error, dot = median. Years with fewer than three rows show only an × (count in the tooltip). Log vertical axis."}</figcaption></figure>')
            parts.append(f'<figure>{chart_urel_points(D["frows"], lang, H)}<figcaption>{"표 A2, 행마다 점 하나: 상대 오차(인용 오차 ÷ H0, 비대칭이면 평균). 세로축 로그." if ko else "Table A2, one dot per row: relative error (quoted error ÷ H0, the mean if asymmetric). Log vertical axis."}</figcaption></figure>')
            parts.append(h1_table(D, lang, t, table))
        if mid == "h3":
            parts.append(f'<figure><div class="legend"><span style="--c:var(--s3)">Planck 2018</span><span style="--c:var(--s2)">{"Riess 외 2022" if ko else "Riess et al. 2022"}</span><span class="dash" style="--c:var(--ref)">{"정규 기대" if ko else "Normal expectation"}</span></div>{chart_rates(D["h3"], lang, H)}<figcaption>{"채운 점은 Huchra 목록(1929~), 빈 점은 표 A2(1976~2019). 세로선은 연도 군집 부트스트랩 95% 구간." if ko else "Filled dots: Huchra’s list (from 1929); open dots: Table A2 (1976–2019). Vertical bars: 95% year-cluster bootstrap intervals."}</figcaption></figure>')
            parts.append(f'<figure>{chart_z_panels(D["frows"], lang, H)}<figcaption>{"표 A2 의 행마다 z = (기준값 − x)/u_x. 위: Planck 2018 기준(2018년의 반올림 Planck 값 행 제외), 아래: Riess 외 2022 기준. ±8 을 넘는 값은 세모로 잘랐다." if ko else "z = (reference − x)/u_x for each Table A2 row. Top: against Planck 2018 (the 2018 rounded-Planck row left out); bottom: against Riess et al. 2022. Triangles: clipped beyond ±8."}</figcaption></figure>')
            parts.append(h3_table(D, lang, t, table))
        if mid == "h4":
            for ref, zcol in (("planck18", "z_planck18"), ("riess22", "z_riess22")):
                r = D["h4"][(FA, 1929, ref)]
                parts.append(f'<figure><div class="legend"><span style="--c:var(--fg2)">{"관측(표 A2)" if ko else "Observed (Table A2)"}</span><span style="--c:var(--s1)">{"정규분포" if ko else "Normal"}</span><span class="dash" style="--c:{REF_COLOR[ref]}">Student-t</span></div>{chart_tail(D["frows"], zcol, float(r["nu"]), float(r["scale"]), ref, lang, H)}<figcaption>{"표 A2, " + REFS[ref]["ko"] + " 기준: |z| 가 가로축 값을 넘는 행의 비율(세로축 로그)과 맞춘 Student-t(ν = " + r["nu"] + ", s = " + r["scale"] + "). Huchra 목록은 집계만 싣는 자료라 그림을 그리지 않는다." if ko else "Table A2 against " + REFS[ref]["en"] + ": share of rows whose |z| exceeds the value on the horizontal axis (log vertical axis) and the fitted Student-t (ν = " + r["nu"] + ", s = " + r["scale"] + "). Huchra’s list is shown only in aggregate, so it has no such plot."}</figcaption></figure>')
            parts.append(h4_table(D, lang, t, table))
        if m["file"]:
            parts.append(f'<p class="files"><a href="../../data/{m["file"]}">{t["download"]}: {m["file"]}</a></p>')
        parts.append(credit(lang, H))
        (d / f"{mid}.html").write_text(page(lang, f'{mid.upper()} · {m[lang]["name"]}', "".join(parts), 2, "hubble", leaf=leaf(lang, t, f"{mid}.html")), encoding="utf-8")

    # ---------- chronology
    evrows = []
    for when, lko, len_, sko, sen in EVENTS:
        yr = f"{when[0]}~{when[1]}" if isinstance(when, tuple) and ko else (f"{when[0]}–{when[1]}" if isinstance(when, tuple) else str(when))
        evrows.append([yr, esc(lko if ko else len_), esc((sko if ko else sen).format(**ef))])
    dm = {x["decade"]: x["h0_median"] for x in D["decades"]}
    tl_tk = ([f"Huchra 목록의 10년 단위 중앙값은 1930년대 {dm['1930']}, 1950년대 {dm['1950']}, 1960년대 {dm['1960']}, 1970년대 {dm['1970']}, 1990년대 {dm['1990']}, 2000년대 {dm['2000']} 이다. 값은 1930년대의 500 안팎에서 1970년대 이후 50~100 사이로 내려왔다.",
              "1990년대 이후 Ia형 초신성(S)·렌즈(L)·Sunyaev-Zeldovich(Z) 부호의 행이 늘고, 2000년대에는 우주배경복사 맞춤(C)이 더해진다. 표 A2 의 2011~2019년 행은 Planck 2018 과 Riess 외 2022 의 두 기준값 사이와 그 바깥에 함께 놓인다.",
              "사건은 연대기 면의 「사건」 표에 근거와 함께 적었다."] if ko else
             [f"The decade medians of Huchra's list are {dm['1930']} in the 1930s, {dm['1950']} in the 1950s, {dm['1960']} in the 1960s, {dm['1970']} in the 1970s, {dm['1990']} in the 1990s and {dm['2000']} in the 2000s: values came down from about 500 in the 1930s to between 50 and 100 from the 1970s on.",
              "From the 1990s the rows coded SNe Ia (S), lenses (L) and Sunyaev-Zeldovich (Z) grow, and CMB fits (C) join in the 2000s. The 2011–2019 rows of Table A2 lie both between and outside the two references, Planck 2018 and Riess et al. 2022.",
              "Each event is listed with its source in the events table on this page."])
    tbody = (f'<h1>{"허블 상수 연대기 1929~2022" if ko else "Hubble constant chronology, 1929–2022"}</h1><p class="lead">{"두 집성의 H0 값과 오차의 흐름을 한 그림에 모으고, 측정 방법 부호의 분포가 10년마다 어떻게 바뀌었는지를 함께 본다." if ko else "The H0 values and errors of the two compilations in one picture, with the decade-by-decade mix of method codes alongside."}</p>' +
             takeaway(lang, tl_tk) +
             f'<figure><div class="legend"><span style="--c:var(--s1)">{"표 A2 (행)" if ko else "Table A2 (rows)"}</span><span style="--c:var(--fg3)">{"Huchra 목록 (10년 단위 집계)" if ko else "Huchra (decade aggregates)"}</span><span class="dash" style="--c:var(--s3)">Planck 2018</span><span class="dash" style="--c:var(--s2)">{"Riess 외 2022" if ko else "Riess et al. 2022"}</span></div>{chart_timeline(D["decades"], D["frows"], D["codes"], lang, H)}<figcaption>{esc(cap_tl)}</figcaption></figure>' +
             f'<figure>{chart_zoom(D["decades"], D["frows"], lang, H)}<figcaption>{"같은 요소를 1970년부터 선형 축(40~110)으로. 범위 밖 값은 세모." if ko else "The same elements from 1970 on a linear axis (40–110); triangles: outside the range."}</figcaption></figure>' +
             f'<h2>{"사건" if ko else "Events"}</h2>' + table([t["year"], ("사건" if ko else "Event"), ("근거" if ko else "Basis")], evrows, cls="") +
             f'<h2>{"측정 방법의 변화" if ko else "The changing mix of methods"}</h2><figure>{chart_types(D["types"], D["decades"], lang, H)}<figcaption>{"Huchra 목록, 10년 단위 × 1차 Type 부호(파일 범례 그대로). 칸의 색은 그 10년 행 가운데의 비율, 숫자는 건수. 10건 미만인 부호는 「그 밖의 부호」로 묶었다. 1929년 이후 오차 있는 행 기준." if ko else "Huchra’s list by decade and primary type code (file legend as printed). Shade: share of the decade’s rows; number: count. Codes with fewer than 10 rows are folded into “other codes”. Rows with an error from 1929 on."}</figcaption></figure>' +
             f'<h2>{"표 A2 전체" if ko else "Table A2 in full"}</h2>' + a2_table(D["frows"], lang, t, table, esc) +
             f'<p class="files"><a href="../../data/h0_faerber2020.csv">{t["download"]}: h0_faerber2020.csv</a> <a href="../../data/h0_h3_rows_faerber.csv">{t["download"]}: h0_h3_rows_faerber.csv</a> <a href="../../data/h0_huchra_decades.csv">{t["download"]}: h0_huchra_decades.csv</a> <a href="../../data/h0_huchra_types.csv">{t["download"]}: h0_huchra_types.csv</a></p>' + credit(lang, H))
    (d / "timeline.html").write_text(page(lang, t["timeline"], tbody, 2, "hubble", leaf=leaf(lang, t, "timeline.html")), encoding="utf-8")

    # ---------- method
    (d / "method.html").write_text(page(lang, t["method"], method_body(lang, N, D, t, H) + credit(lang, H), 2, "hubble", leaf=leaf(lang, t, "method.html")), encoding="utf-8")
    return N


def data_rows(lang, esc):
    return [[f'<a href="../data/{f}">{f}</a>', esc(DESC[f][0 if lang == "ko" else 1])] for f in PUBLIC]


def data_license(lang, esc):
    if lang == "ko":
        return ("<h2>허블 상수 장</h2><p>표 A2 의 값은 Faerber & López-Corredoira (2020), Universe 6, 114 의 부록 표에서 옮겼다(CC BY 4.0, arXiv 판 2008.04035v1 에서 읽음; 출판본 대조 전). 행 단위 CSV 에 출처를 적었다. Huchra 목록(hubble.plot.dat)은 저작권 표시와 인용 요청만 있고 재게시 허락 문장이 없어 집계(연도별·10년별 건수와 사분위, 부호별 건수, 지표)만 싣는다. 행 단위 값, 개별 추정을 찍은 그림, 두 집성을 짝지은 행 단위 대조표는 싣지 않으며 원 파일은 공개 저장소에 없다. 이 사이트의 CC BY 4.0 은 엮은이가 계산한 부분(z·집계·반감기·적합)에 미친다. 출처: "
                + esc(H0_SOURCES["huchra"]["credit"]) + " · " + esc(H0_SOURCES["faerber"]["credit"]) + "</p>")
    return ("<h2>Hubble-constant chapter</h2><p>The Table A2 values are taken from the appendix table of Faerber & López-Corredoira (2020), Universe 6, 114 (CC BY 4.0; read from arXiv:2008.04035v1, not yet checked against the published version); the row-level CSV carries the attribution. Huchra's list (hubble.plot.dat) carries a copyright line and a request for citation but no grant to republish, so only aggregates are published: counts and quartiles by year and decade, counts by code, and the metrics. No row values, no chart of individual estimates and no row-level pairing of the two compilations are published, and the original file is not in the public repository. The site's CC BY 4.0 covers the editor's computations (z, aggregates, half-lives, fits). Sources: "
            + esc(H0_SOURCES["huchra"]["credit"]) + " · " + esc(H0_SOURCES["faerber"]["credit"]) + "</p>")


def datapackage_resources():
    terms = (". Table A2 values © the authors, CC BY 4.0 (Faerber & López-Corredoira 2020, Universe 6, 114). Huchra's list (hubble.plot.dat) grants no right to republish: these files hold aggregates only (counts, quartiles, metrics), never a row of the list. CC BY 4.0 covers the editor's computations.")
    return [dict(path=f, description=DESC[f][1] + terms, format="csv") for f in PUBLIC]
