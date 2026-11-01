# -*- coding: utf-8 -*-
"""Atomic-weights chapter pages (1.1). Called from build_site.build() once per language.
H is a dict of helpers from build_site (page, table, takeaway, esc, fmt_sci, sup, spec_block)."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from aw_registry import AW_METRICS, AW_SOURCE

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
PUBLIC = ["aw_long.csv", "aw_a1_elements.csv", "aw_a1_eras.csv", "aw_a2_pairs.csv", "aw_a5_intervals.csv"]
DESC = {
    "aw_long.csv": ("원자량 개정 기록 전부(파싱 결과, 1961년 이전 값의 ¹²C 환산값 포함)", "Every atomic-weight revision, parsed (with pre-1961 values converted to the ¹²C scale)"),
    "aw_a1_elements.csv": ("원소별 개정 횟수·첫/마지막 개정·평균 간격(A1·A4)", "Revisions, first/last year and mean spacing per element (A1, A4)"),
    "aw_a1_eras.csv": ("시대별 개정 빈도(A1)", "Revisions per era (A1)"),
    "aw_a2_pairs.csv": ("직전 불확도가 있었던 개정 전부: 범위 밖 여부·범위 겹침·z(A2·A3)", "Every revision whose predecessor had an uncertainty: outside range, overlap, z (A2, A3)"),
    "aw_a5_intervals.csv": ("구간 표기 전환(A5)", "Switches to interval notation (A5)"),
}
# Korean element names (common usage following the Korean Chemical Society's spelling; not checked line by line)
KO = dict(H="수소", He="헬륨", Li="리튬", Be="베릴륨", B="붕소", C="탄소", N="질소", O="산소", F="플루오린", Ne="네온", Na="소듐", Mg="마그네슘",
          Al="알루미늄", Si="규소", P="인", S="황", Cl="염소", Ar="아르곤", K="포타슘", Ca="칼슘", Sc="스칸듐", Ti="타이타늄", V="바나듐", Cr="크로뮴",
          Mn="망가니즈", Fe="철", Co="코발트", Ni="니켈", Cu="구리", Zn="아연", Ga="갈륨", Ge="저마늄", As="비소", Se="셀레늄", Br="브로민", Kr="크립톤",
          Rb="루비듐", Sr="스트론튬", Y="이트륨", Zr="지르코늄", Nb="나이오븀", Mo="몰리브데넘", Tc="테크네튬", Ru="루테늄", Rh="로듐", Pd="팔라듐",
          Ag="은", Cd="카드뮴", In="인듐", Sn="주석", Sb="안티모니", Te="텔루륨", I="아이오딘", Xe="제논", Cs="세슘", Ba="바륨", La="란타넘",
          Ce="세륨", Pr="프라세오디뮴", Nd="네오디뮴", Pm="프로메튬", Sm="사마륨", Eu="유로퓸", Gd="가돌리늄", Tb="터븀", Dy="디스프로슘",
          Ho="홀뮴", Er="어븀", Tm="툴륨", Yb="이터븀", Lu="루테튬", Hf="하프늄", Ta="탄탈럼", W="텅스텐", Re="레늄", Os="오스뮴", Ir="이리듐",
          Pt="백금", Au="금", Hg="수은", Tl="탈륨", Pb="납", Bi="비스무트", Po="폴로늄", Rn="라돈", Ra="라듐", Ac="악티늄", Th="토륨",
          Pa="프로트악티늄", U="우라늄", Np="넵투늄")

# periodic order (atomic number 1-93) for listing
ZORDER = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd "
          "In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np").split()
Z = {sym: i + 1 for i, sym in enumerate(ZORDER)}

L = {
    "ko": dict(nav="원자량", title="원자량 장 — 표준 원자량의 개정 기록", lead="CIAAW 가 1902년부터 권고해 온 표준 원자량이 어떻게 바뀌었는지, 그리고 새 값이 직전 권고의 불확도 범위 안에 있었는지를 센다. 물리 상수 장과 같은 질문을, 불확도를 다르게 정의하는 기록에 던진다.",
               metrics="지표", elements="원소", year="연도", value="값(원 표기)", kind="표기", scale="척도", v12="¹²C 기준 값", zprev="직전 대비 z", doi="원 보고서",
               kinds={"unc": "값(불확도)", "interval": "구간", "none": "불확도 없음", "exact": "기준(정확)", "withdrawn": "철회"},
               credit_h="자료 출처", outside="직전 범위 밖", no_saw="표준 원자량 없음(방사성)", sym="기호", name="이름", nrev="개정", last="마지막 개정",
               cur="현재 값", download="CSV 내려받기"),
    "en": dict(nav="Atomic weights", title="Atomic weights — the revision record of standard atomic weights", lead="How the standard atomic weights recommended by CIAAW since 1902 changed, and whether each new value lay within the previous recommendation's uncertainty range. The question of the physical-constants chapter, asked of a record that defines its uncertainties differently.",
               metrics="Metrics", elements="Elements", year="Year", value="Value (as published)", kind="Notation", scale="Scale", v12="Value, ¹²C scale", zprev="z vs previous", doi="Report",
               kinds={"unc": "value(uncertainty)", "interval": "interval", "none": "no uncertainty", "exact": "reference (exact)", "withdrawn": "withdrawn"},
               credit_h="Source", outside="outside previous range", no_saw="no standard atomic weight (radioactive)", sym="Symbol", name="Name", nrev="Revisions", last="Latest revision",
               cur="Current value", download="Download CSV"),
}

GLOSS = {
    "ko": ('<div class="note"><b>표준 원자량(standard atomic weight)</b> — 지구의 정상 물질에서 그 원소 원자들의 평균 질량을 ¹²C 원자 질량의 1/12 로 나눈 값. 동위원소가 섞인 비율의 평균이라, 물리 상수와 달리 시료에 따라 실제로 조금씩 다르다.</div>'
           '<div class="note"><b>CIAAW 의 불확도 = 확장 범위</b> — CIAAW 가 원자량 뒤에 붙이는 불확도(예: 65.38(2) 의 0.02)는 표준불확도(1σ)가 아니다. 정상 물질의 원자량이 「매우 확실하게」 그 범위 안에 들어갈 것으로 기대되는 넓은 범위다(포함인자나 신뢰수준이 정해진 확장불확도와도 같지 않다). 그래서 물리 상수 장의 ±1σ 와 같은 눈금으로 읽지 않는다.</div>'
           '<div class="note"><b>구간(interval)</b> — 2009년부터 동위원소 조성의 자연 변동이 큰 원소는 하나의 값 대신 [하한, 상한] 으로 적는다(예: 수소 [1.007 84, 1.008 11]). 구간은 불확도가 아니라 실제로 나타나는 값의 범위다.</div>'),
    "en": ('<div class="note"><b>Standard atomic weight</b> — the mean mass of an element\'s atoms in normal terrestrial material, relative to 1/12 of the mass of a ¹²C atom. Because it averages over isotopic mixtures, unlike a physical constant it genuinely varies a little from sample to sample.</div>'
           '<div class="note"><b>CIAAW uncertainty = expanded range</b> — the uncertainty CIAAW attaches to an atomic weight (the 0.02 in 65.38(2)) is not a standard uncertainty (1σ) but a wide range within which the atomic weight of normal materials is expected to lie "with great certitude" (nor is it an expanded uncertainty with a stated coverage factor or confidence level). It is not read on the same scale as the ±1σ of the physical-constants chapter.</div>'
           '<div class="note"><b>Interval</b> — since 2009, elements whose isotopic composition varies widely in nature are given as [lower, upper] rather than a single value (hydrogen: [1.007 84, 1.008 11]). An interval is not an uncertainty but the range of values actually found.</div>'),
}


def read(name):
    return list(csv.DictReader(open(DER / name, encoding="utf-8")))


def numbers():
    s = json.loads((DER / "aw_summary.json").read_text(encoding="utf-8"))
    eras = {e["era"]: e for e in s["eras"]}
    els = read("aw_a1_elements.csv")
    saw = [e for e in els if e["has_standard_atomic_weight"] == "1"]
    pairs = read("aw_a2_pairs.csv")
    iv = read("aw_a5_intervals.csv")
    ratios = sorted(float(i["width_ratio"]) for i in iv if i["width_ratio"])
    dis = [p for p in pairs if p["ranges_disjoint"] == "1"]
    return dict(
        aw_rows=s["rows"], aw_elements=s["elements"], aw_saw=s["elements_with_saw"], aw_report_years=s["report_years"],
        aw_rev_mean=f"{s['revisions_mean']:.1f}", aw_rev_median=f"{s['revisions_median']:g}", aw_rev_max=s["revisions_max"],
        aw_era1=eras["1902-1960"]["revisions_per_year"], aw_era2=eras["1961-2008"]["revisions_per_year"], aw_era3=eras["2009-2024"]["revisions_per_year"],
        aw_a2_n=s["a2_pairs"], aw_a2_out=s["a2_outside"], aw_a2_out_pct=f"{100 * s['a2_outside'] / s['a2_pairs']:.1f}",
        aw_a2_dis=len(dis), aw_a2_dis_list=", ".join(f"{p['symbol']} {p['year_new']}" for p in dis),
        aw_a2_out_early=sum(1 for p in pairs if p["outside_prev_range"] == "1" and 1961 <= int(p["year_prev"]) <= 1969),
        aw_a3_med=f"{s['a3_median_abs_z']:.2f}", aw_a3_half=f"{100 * s['a3_share_le_half']:.0f}",
        aw_a4_n=len(s["a4_unchanged_since_1969"]), aw_a4_list="·".join(s["a4_unchanged_since_1969"]),
        aw_a4_2000=sum(1 for e in saw if int(e["last"]) >= 2000),
        aw_a5_n=len(iv), aw_a5_ratio=f"{s['a5_ratio_median']:.1f}", aw_a5_max=f"{s['a5_ratio_max']:.1f}",
    )


# ------------------------------------------------------------------ charts
def chart_z(pairs, lang, H, W=900, Hh=340):
    """Revision z_prev by year, clipped at ±8, dashed lines at ±1 (edge of the previous range)."""
    esc = H["esc"]
    Lm, R, Tp, B = 56, 150, 16, 40
    x0, x1, cap = 1950, 2026, 8.0

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)

    def Y(v): return Tp + (cap - max(-cap, min(cap, v))) / (2 * cap) * (Hh - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="revision z by year">']
    for v in (-8, -4, -1, 0, 1, 4, 8):
        cls = "ref" if abs(v) == 1 else "grid"
        o.append(f'<line class="{cls}" x1="{Lm}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{Lm-6}" y="{Y(v)+4:.1f}" text-anchor="end">{v:+d}</text>'.replace(">+0<", ">0<"))
    l1, l2 = (("직전 범위 경계", "(z = ±1)") if lang == "ko" else ("edge of previous", "range (z = ±1)"))
    # one two-line label between the dashed lines at +1 and -1
    o.append(f'<text x="{W-R+6}" y="{Y(0)-3:.1f}"><tspan x="{W-R+6}">{l1}</tspan><tspan x="{W-R+6}" dy="1.15em">{l2}</tspan></text>')
    for yv in range(1950, 2030, 10):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-14}" text-anchor="middle">{yv}</text>')
    for p in pairs:
        z = float(p["z_prev"])
        x, y = X(int(p["year_new"])), Y(z)
        out = p["outside_prev_range"] == "1"
        tip = f'{p["symbol"]} {p["year_prev"]}→{p["year_new"]}: {p["prev"]} → {p["new"]}, z = {z:.2f}'
        if abs(z) > cap:
            o.append(f'<path class="dot" d="M{x-5:.1f},{y + (6 if z < 0 else -6):.1f} L{x+5:.1f},{y + (6 if z < 0 else -6):.1f} L{x:.1f},{y:.1f} Z" fill="var(--s2)" data-tip="{esc(tip)}"/>')
            o.append(f'<text x="{x+7:.1f}" y="{y + (4 if z < 0 else 10):.1f}">{p["symbol"]} {z:.0f}</text>')
        else:
            o.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{5 if out else 3.5}" fill="{"var(--s2)" if out else "var(--s1)"}" fill-opacity="{1 if out else .45}" stroke="var(--card)" stroke-width="1" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


def chart_bars(items, H, W=900, Hh=260, unit=""):
    esc = H["esc"]
    Lm, R, Tp, B = 46, 16, 16, 40
    vmax = max(v for _, v in items) or 1
    bw = (W - Lm - R) / len(items)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="bar chart">']
    step = max(1, int(math.ceil(vmax / 5 / 5) * 5))
    for v in range(0, int(vmax) + step, step):
        y = Tp + (1 - v / (vmax * 1.05)) * (Hh - Tp - B)
        o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}"/><text x="{Lm-6}" y="{y+4:.1f}" text-anchor="end">{v}</text>')
    for i, (lab, v) in enumerate(items):
        h = v / (vmax * 1.05) * (Hh - Tp - B)
        x = Lm + i * bw + 2
        o.append(f'<rect class="dot" x="{x:.1f}" y="{Hh-B-h:.1f}" width="{bw-4:.1f}" height="{h:.1f}" rx="3" fill="var(--s1)" data-tip="{esc(lab)}: {v}{unit}"/>')
        o.append(f'<text x="{x + (bw-4)/2:.1f}" y="{Hh-22}" text-anchor="middle">{esc(lab)}</text>')
    o.append("</svg>")
    return "".join(o)


def chart_element(rows, lang, H, W=900, Hh=320):
    """Relative deviation (¹²C scale) from the current value, symmetric-log axis; intervals as hollow bars."""
    esc, sup = H["esc"], H["sup"]
    cur = rows[-1]
    if cur["kind"] == "withdrawn":
        cur = next(r for r in reversed(rows) if r["kind"] != "withdrawn")
    ref = float(cur["value_12C"])
    pts = []
    for r in rows:
        if r["kind"] == "withdrawn" or not r["value_12C"]:
            continue
        v = float(r["value_12C"])
        f = float(r["value_12C"]) / float(r["value"]) if r["value"] else 1
        if r["kind"] == "interval":
            lo, hi = float(r["lo"]) * f, float(r["hi"]) * f
            pts.append((int(r["year"]), (v - ref) / ref, (lo - ref) / ref, (hi - ref) / ref, "interval", r))
        else:
            u = float(r["u"]) * f if r["u"] else 0.0
            pts.append((int(r["year"]), (v - ref) / ref, (v - u - ref) / ref, (v + u - ref) / ref, r["kind"], r))
    mags = [abs(x) for p in pts for x in p[1:4] if x != 0]
    lt = 10 ** math.floor(math.log10(min(mags))) if mags else 1e-6
    top = 10 ** math.ceil(math.log10(max(mags + [lt * 10])))

    def fz(v): return math.copysign(math.log10(1 + abs(v) / lt), v)
    fm = fz(top)
    Lm, R, Tp, B = 70, 20, 16, 40
    x0, x1 = 1898, 2028

    def X(v): return Lm + (v - x0) / (x1 - x0) * (W - Lm - R)

    def Y(v): return Tp + (fm - fz(v)) / (2 * fm) * (Hh - Tp - B)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="atomic weight history">']
    e = int(round(math.log10(lt)))
    te = int(round(math.log10(top)))
    for t in [0.0] + [sgn * 10.0 ** k for k in range(e + 1, te + 1, max(1, (te - e) // 3 or 1)) for sgn in (1, -1)]:
        lab = "0" if t == 0 else ("−" if t < 0 else "+") + sup(int(round(math.log10(abs(t)))))
        o.append(f'<line class="{"ref" if t == 0 else "grid"}" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/><text x="{Lm-6}" y="{Y(t)+4:.1f}" text-anchor="end">{lab}</text>')
    for yv in range(1900, 2030, 20):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh-14}" text-anchor="middle">{yv}</text>')
    o.append(f'<line class="grid" x1="{X(1961):.1f}" x2="{X(1961):.1f}" y1="{Tp}" y2="{Hh-B}" stroke-dasharray="2 4"/><text x="{X(1961)+4:.1f}" y="{Tp+10}">{"1961 기준 변경" if lang == "ko" else "1961 scale change"}</text>')
    for yr, dv, lo, hi, kind, r in pts:
        x = X(yr)
        tip = f'{yr}: {r["value_text"]}'
        if kind == "interval":
            o.append(f'<rect class="dot" x="{x-4:.1f}" y="{Y(hi):.1f}" width="8" height="{max(2, Y(lo)-Y(hi)):.1f}" fill="none" stroke="var(--s2)" stroke-width="2" data-tip="{esc(tip)}"/>')
            continue
        if hi != lo:
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(lo):.1f}" y2="{Y(hi):.1f}" stroke="var(--s1)" stroke-width="2"/>')
        o.append(f'<circle class="dot" cx="{x:.1f}" cy="{Y(dv):.1f}" r="4.5" fill="{"var(--s1)" if kind in ("unc", "exact") else "var(--card)"}" stroke="var(--s1)" stroke-width="2" data-tip="{esc(tip)}"/>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ pages
def element_takeaway(lang, sym, rows, pairs, el):
    ko = lang == "ko"
    out = []
    ys = [int(r["year"]) for r in rows]
    out.append(f"1902~2024년에 {len(rows)}번 권고·개정되었다(첫 기록 {ys[0]}년, 마지막 개정 {ys[-1]}년)." if ko
               else f"Recommended or revised {len(rows)} times between 1902 and 2024 (first record {ys[0]}, latest revision {ys[-1]}).")
    ps = [p for p in pairs if p["symbol"] == sym]
    if ps:
        n_out = sum(int(p["outside_prev_range"]) for p in ps)
        if n_out:
            lst = ", ".join(p["year_new"] for p in ps if p["outside_prev_range"] == "1")
            out.append(f"직전 권고에 불확도가 있었던 개정 {len(ps)}건 중 {n_out}건({lst})에서 새 값이 직전 범위(확장 범위) 밖에 놓였다." if ko
                       else f"Of {len(ps)} revisions whose previous recommendation had an uncertainty, {n_out} ({lst}) put the new value outside the previous (expanded) range.")
        else:
            out.append(f"직전 권고에 불확도가 있었던 개정 {len(ps)}건 모두 새 값이 직전 범위(확장 범위) 안에 있었다." if ko
                       else f"All {len(ps)} revisions whose previous recommendation had an uncertainty kept the new value inside the previous (expanded) range.")
    last = rows[-1]
    if el["has_standard_atomic_weight"] != "1":
        out.append("현재 표준 원자량이 없다 — 방사성 원소로, 지구 물질에 일정한 동위원소 조성이 없다." if ko
                   else "It has no standard atomic weight today: a radioactive element without a characteristic terrestrial isotopic composition.")
    elif last["kind"] == "interval":
        out.append(f"{last['year']}년부터 하나의 값 대신 구간 {last['value_text']} 으로 표기한다(구간: 정상 물질에서 실제로 나타나는 범위)." if ko
                   else f"Since {last['year']} it is given as the interval {last['value_text']} rather than a single value (the range found in normal materials).")
    else:
        out.append(f"현재 표준 원자량은 {last['value_text']} 이다({last['year']}년 권고)." if ko else f"The current standard atomic weight is {last['value_text']} (recommended in {last['year']}).")
    return out


def credit(lang, H):
    esc = H["esc"]
    lab = "자료 출처" if lang == "ko" else "Source"
    return f'<p class="src" style="margin-top:2rem;font-size:.82rem;color:var(--fg3)">{lab}: {esc(AW_SOURCE["credit"])}</p>'


def build(lang, base, H, out_root):
    esc, page, table, takeaway, spec_block, fmt_sci = H["esc"], H["page"], H["table"], H["takeaway"], H["spec_block"], H["fmt_sci"]
    t = L[lang]
    N = numbers()
    long = read("aw_long.csv")
    els = {e["symbol"]: e for e in read("aw_a1_elements.csv")}
    pairs = read("aw_a2_pairs.csv")
    eras = read("aw_a1_eras.csv")
    iv = read("aw_a5_intervals.csv")
    d = base / "atomic"
    (d / "el").mkdir(parents=True, exist_ok=True)
    name = (lambda s: f"{KO.get(s, '')}") if lang == "ko" else (lambda s: els[s]["element"])

    # data files (shared by both languages)
    for f in PUBLIC:
        (out_root / "data" / f).write_bytes((DER / f).read_bytes())

    # chapter index
    if lang == "ko":
        tk = [f"CIAAW 는 1902년부터 표준 원자량을 {N['aw_rows']}번 권고·개정했다. 표준 원자량이 있는 원소 {N['aw_saw']}개는 평균 {N['aw_rev_mean']}회 바뀌었다.",
              f"CIAAW 의 불확도는 표준불확도(1σ)가 아니라 확장 범위(정상 물질이 매우 확실하게 들어갈 넓은 범위)다. 그래서 새 값이 직전 범위 밖에 놓인 개정은 {N['aw_a2_n']}건 중 {N['aw_a2_out']}건({N['aw_a2_out_pct']}%), 두 범위가 아예 겹치지 않은 개정은 {N['aw_a2_dis']}건({N['aw_a2_dis_list']})이다.",
              f"2009년부터 {N['aw_a5_n']}개 원소는 하나의 값 대신 구간(interval)으로 표기한다. {N['aw_a5_n']}개 모두 새 구간이 직전 값을 포함했다.",
              "물리 상수(표준불확도 기준)와 원자량(확장 범위 기준)은 불확도의 정의가 달라 놓침률을 같은 눈금으로 견주지 않는다 — 두 장을 나란히 두는 까닭이 그 차이에 있다."]
    else:
        tk = [f"CIAAW has recommended or revised standard atomic weights {N['aw_rows']} times since 1902; the {N['aw_saw']} elements with a standard atomic weight changed {N['aw_rev_mean']} times on average.",
              f"CIAAW uncertainties are not standard uncertainties (1σ) but expanded ranges (wide ranges that normal materials fall in with great certitude). So {N['aw_a2_out']} of {N['aw_a2_n']} revisions ({N['aw_a2_out_pct']}%) put the new value outside the previous range, and {N['aw_a2_dis']} had ranges that do not overlap at all ({N['aw_a2_dis_list']}).",
              f"Since 2009, {N['aw_a5_n']} elements are given as an interval rather than a single value; in all {N['aw_a5_n']} the new interval contains the previous value.",
              "Physical constants (standard uncertainties) and atomic weights (expanded ranges) define uncertainty differently, so their miss rates are not read on one scale; that difference is why the two chapters sit side by side."]
    stats = f"""<div class="stats">
<a class="stat" href="a2.html"><span class="n">{N['aw_a2_out']}<span class="vs">/ {N['aw_a2_n']}</span></span><small>{"직전 권고 범위 밖에 새 값이 놓인 개정(기준 ①)" if lang == "ko" else "revisions with the new value outside the previous range (criterion 1)"}</small></a>
<a class="stat" href="a2.html"><span class="n">{N['aw_a2_dis']}</span><small>{"두 범위가 아예 겹치지 않은 개정(기준 ②): " if lang == "ko" else "revisions whose ranges do not overlap (criterion 2): "}{N['aw_a2_dis_list']}</small></a>
<a class="stat" href="a1.html"><span class="n">{N['aw_rev_mean']}</span><small>{"원소당 평균 개정 횟수(표준 원자량이 있는 " if lang == "ko" else "mean revisions per element (the "}{N['aw_saw']}{"개)" if lang == "ko" else " with a standard atomic weight)"}</small></a>
<a class="stat" href="a5.html"><span class="n">{N['aw_a5_n']}</span><small>{"구간(interval) 표기로 바뀐 원소" if lang == "ko" else "elements switched to an interval"}</small></a></div>"""
    cards = "".join(f'<a class="card" href="{m["id"]}.html"><b>{m["id"].upper()} · {esc(m[lang]["name"])}</b><small>{esc(m[lang]["short"])}</small></a>' for m in AW_METRICS)
    elcards = "".join(f'<a class="card{"" if els[s]["has_standard_atomic_weight"] == "1" else " d"}" href="el/{s}.html"><b>{s} · {esc(name(s))}</b><small>Z={Z.get(s, "")} · {els[s]["n_revisions"]}{"회" if lang == "ko" else "×"} · {esc(els[s]["current"]) if els[s]["current"] != "n/a" else t["kinds"]["withdrawn"]}</small></a>'
                      for s in sorted(els, key=lambda s: Z.get(s, 999)))
    cap = ("점 하나가 개정 하나(직전 권고에 불확도가 있었던 것). 주황 점은 새 값이 직전 범위 밖에 놓인 개정, 세모는 ±8 을 넘어 잘린 값." if lang == "ko"
           else "One dot per revision whose previous recommendation had an uncertainty. Orange: new value outside the previous range; triangles: clipped beyond ±8.")
    body = (f'<h1>{esc(t["title"])}</h1><p class="lead">{esc(t["lead"])}</p>' + takeaway(lang, tk) + stats +
            f'<figure>{chart_z(pairs, lang, H)}<figcaption>{esc(cap)}</figcaption></figure>' + GLOSS[lang] +
            f'<h2>{t["metrics"]}</h2><div class="cards">{cards}</div><h2>{t["elements"]}</h2><div class="cards">{elcards}</div>' + credit(lang, H))
    (d / "index.html").write_text(page(lang, t["nav"], body, 2, "atomic"), encoding="utf-8")

    # metric pages
    for m in AW_METRICS:
        parts = [f'<p><span class="tag k">{m["id"].upper()}</span></p><h1>{esc(m[lang]["name"])}</h1><p class="lead">{esc(m[lang]["short"])}</p>',
                 takeaway(lang, [x.format(**N) for x in m["takeaway"][lang]]), spec_block(m, lang, N)]
        if m["id"] == "a1":
            dec = {}
            for r in long:
                dec[int(r["year"]) // 10 * 10] = dec.get(int(r["year"]) // 10 * 10, 0) + 1
            items = [(f"{k}s" if lang == "en" else f"{k}년대", dec.get(k, 0)) for k in range(1900, 2030, 10)]
            parts.append(f'<figure>{chart_bars([(a[:-1] if lang == "ko" else a[:-1], v) for a, v in items], H)}<figcaption>{"10년 단위 개정 건수." if lang == "ko" else "Revisions per decade."}</figcaption></figure>')
            parts.append(table([("시대" if lang == "ko" else "Era"), ("개정" if lang == "ko" else "Revisions"), ("보고 연도" if lang == "ko" else "Report years"), ("한 해 평균" if lang == "ko" else "Per year")],
                               [[e["era"], e["revisions"], e["report_years"], e["revisions_per_year"]] for e in eras], num_cols=(1, 2, 3)))
            top = sorted([e for e in els.values() if e["has_standard_atomic_weight"] == "1"], key=lambda e: (-int(e["n_revisions"]), e["symbol"]))[:15]
            parts.append(table([t["sym"], t["name"], t["nrev"], t["last"], ("평균 간격(년)" if lang == "ko" else "Mean gap (y)")],
                               [[f'<a href="el/{e["symbol"]}.html">{e["symbol"]}</a>', esc(name(e["symbol"])), e["n_revisions"], e["last"], e["mean_gap"]] for e in top], num_cols=(2, 3, 4)))
        if m["id"] in ("a2", "a3"):
            parts.append(f'<figure>{chart_z(pairs, lang, H)}<figcaption>{esc(cap)}</figcaption></figure>')
            sel = [p for p in pairs if p["outside_prev_range"] == "1"] if m["id"] == "a2" else sorted(pairs, key=lambda p: -abs(float(p["z_prev"])))[:20]
            parts.append(table([t["sym"], ("직전 권고" if lang == "ko" else "Previous"), ("새 권고" if lang == "ko" else "New"), ("z_옛" if lang == "ko" else "z_old"), ("범위 겹치지 않음" if lang == "ko" else "Ranges disjoint")],
                               [[f'<a href="el/{p["symbol"]}.html">{p["symbol"]}</a>', f'{p["year_prev"]}: {esc(p["prev"])}', f'{p["year_new"]}: {esc(p["new"])}', p["z_prev"], ("예" if lang == "ko" else "yes") if p["ranges_disjoint"] == "1" else ""] for p in sel],
                               num_cols=(3,)))
        if m["id"] == "a4":
            saw = [e for e in els.values() if e["has_standard_atomic_weight"] == "1"]
            dec = {}
            for e in saw:
                dec[int(e["last"]) // 10 * 10] = dec.get(int(e["last"]) // 10 * 10, 0) + 1
            parts.append(f'<figure>{chart_bars([(str(k), dec.get(k, 0)) for k in range(1960, 2030, 10)], H)}<figcaption>{"마지막 개정 연도(10년 단위)별 원소 수." if lang == "ko" else "Elements by decade of latest revision."}</figcaption></figure>')
            old = sorted([e for e in saw if int(e["last"]) <= 1969], key=lambda e: e["last"])
            parts.append(table([t["sym"], t["name"], t["last"], t["cur"]], [[f'<a href="el/{e["symbol"]}.html">{e["symbol"]}</a>', esc(name(e["symbol"])), e["last"], esc(e["current"])] for e in old], num_cols=(2,)))
        if m["id"] == "a5":
            parts.append(table([t["sym"], ("직전 권고" if lang == "ko" else "Previous"), ("구간" if lang == "ko" else "Interval"), ("폭의 비" if lang == "ko" else "Width ratio"), ("직전 값 포함" if lang == "ko" else "Contains previous")],
                               [[f'<a href="el/{i["symbol"]}.html">{i["symbol"]}</a>', f'{i["year_prev"]}: {esc(i["prev"])}', f'{i["year_interval"]}: {esc(i["interval"])}', i["width_ratio"], ("예" if lang == "ko" else "yes") if i["interval_contains_prev_value"] == "1" else ("아니오" if lang == "ko" else "no")] for i in iv],
                               num_cols=(3,)))
        parts.append(f'<p class="files"><a href="../../data/{m["file"]}">{t["download"]}: {m["file"]}</a></p>' + credit(lang, H))
        (d / f'{m["id"]}.html').write_text(page(lang, m[lang]["name"], "".join(parts), 2, "atomic"), encoding="utf-8")

    # element pages
    head = {"ko": [("연도", "권고·개정한 해"), ("값(원 표기)", "CIAAW 가 발표한 그대로. 괄호 안은 마지막 자리의 불확도(확장 범위)"), ("표기", "값(불확도)·구간·불확도 없음"),
                   ("척도", "1961년 이전은 산소 = 16, 이후는 ¹²C = 12"), ("¹²C 기준 값", "1961년 이전 값에 15.9994/16 을 곱한 값"), ("직전 대비 z", "(새 값 − 직전 값) ÷ 직전 불확도"), ("원 보고서", "CIAAW 보고서 DOI")],
            "en": [("Year", "year of the recommendation"), ("Value (as published)", "as published by CIAAW; digits in brackets are the uncertainty (expanded range) in the last digits"), ("Notation", "value(uncertainty), interval or no uncertainty"),
                   ("Scale", "before 1961 oxygen = 16, from 1961 ¹²C = 12"), ("Value, ¹²C scale", "pre-1961 values multiplied by 15.9994/16"), ("z vs previous", "(new − previous) ÷ previous uncertainty"), ("Report", "DOI of the CIAAW report")]}
    zmap = {(p["symbol"], p["year_new"]): p["z_prev"] for p in pairs}
    for s in els:
        rs = [r for r in long if r["symbol"] == s]
        el = els[s]
        corr = {(c["symbol"], c["year"]): c for c in csv.DictReader(open(ROOT / "data" / "transcribed" / "aw_corrections.csv", encoding="utf-8"))}

        def vt(r):
            c = corr.get((s, r["year"]))
            if not c:
                return esc(r["value_text"])
            return esc(r["value_text"]) + (f' <small>(보정 — 원 CSV {esc(c["csv_value"])}; 데이터 면 보정표)</small>' if lang == "ko" else f' <small>(corrected; source CSV {esc(c["csv_value"])}; see corrections file)</small>')

        def v12(r):
            if not r["value_12C"]:
                return ""
            x = r["value_12C"].rstrip("0").rstrip(".")
            return x + (" <small>(구간 중점, 계산용)</small>" if lang == "ko" else " <small>(interval midpoint, for calculation)</small>") if r["kind"] == "interval" else x

        def doi(r):
            if not r["doi"] or r["doi"] == "n/a":
                return "DOI 미제공" if lang == "ko" else "no DOI yet"
            return f'<a href="https://doi.org/{esc(r["doi"])}">{esc(r["doi"])}</a>'
        tab = [[r["year"], vt(r), t["kinds"][r["kind"]], r["scale"], v12(r), zmap.get((s, r["year"]), ""), doi(r)] for r in rs]
        tag = "" if el["has_standard_atomic_weight"] == "1" else f'<span class="tag">{t["no_saw"]}</span>'
        cap2 = ("현재 값(또는 마지막 값)에서의 상대 편차, 대칭 로그 축. 막대는 불확도(확장 범위), 빈 원은 불확도 없는 값, 주황 사각은 구간." if lang == "ko"
                else "Relative deviation from the current (or last) value, symmetric-log axis. Bars: uncertainty (expanded range); open circles: no uncertainty; orange boxes: intervals.")
        body = (f'<p><span class="tag k">{"원자량" if lang == "ko" else "Atomic weight"}</span>{tag}</p><h1>{s} · {esc(name(s))}</h1><p class="lead">{esc(el["element"] if lang == "ko" else KO.get(s, ""))}</p>' +
                takeaway(lang, element_takeaway(lang, s, rs, pairs, el)) +
                (f'<figure>{chart_element(rs, lang, H)}<figcaption>{esc(cap2)}</figcaption></figure>' if len([r for r in rs if r["value_12C"]]) >= 2 else "") +
                table(head[lang], tab, num_cols=(4, 5)) + credit(lang, H))
        (d / "el" / f"{s}.html").write_text(page(lang, f"{s} · {name(s)}", body, 3, "atomic"), encoding="utf-8")
    return N


def data_rows(lang, esc):
    return [[f'<a href="../data/{f}">{f}</a>', esc(DESC[f][0 if lang == "ko" else 1])] for f in PUBLIC]
