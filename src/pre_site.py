# -*- coding: utf-8 -*-
"""1.3 chapter pages: recommended values before CODATA (1929-1963) and the Henrion & Fischhoff check.
Called from build_site.build() once per language, like h0_site.build(). Every number comes from
data/derived/pre_codata_values.csv, pre_codata_hf.csv and constants_long.csv (made by src/pre_codata.py)."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
TRANS = ROOT / "data" / "transcribed"
PUBLIC = ["pre_codata_reviews.csv", "pre_codata_values.csv", "pre_codata_hf.csv"]
PUBLIC_SRC = {"pre_codata_reviews.csv": TRANS, "pre_codata_values.csv": DER, "pre_codata_hf.csv": DER}
DESC = {
    "pre_codata_reviews.csv": ("CODATA 이전 권고값 전사: 1929·1941·1950·1952·1955·1963 검토의 α⁻¹·h·e·mₑ·N_A, 원 표기 값과 ±, ±의 뜻(확률오차·표준오차·표준편차), 원자량 척도, 원 논문 쪽",
                               "Recommended values before CODATA as transcribed: α⁻¹, h, e, mₑ, N_A in the 1929, 1941, 1950, 1952, 1955 and 1963 reviews, value and ± as printed, kind of ± (probable error, standard error, standard deviation), atomic-weight scale, page of the paper"),
    "pre_codata_values.csv": ("위 값을 SI·통합 척도·표준 불확도로 바꾼 값과 1973·2022 판 대비 z·ppm (1969 판 포함 35행)",
                              "The same values in SI units, on the unified scale and with standard uncertainties, with z and ppm against the 1973 and 2022 editions (35 rows with 1969)"),
    "pre_codata_hf.csv": ("Henrion & Fischhoff 방식 지수(R_B·IQ·SI): 본값·감도 변형, 1973·2022 기준, H&F 인쇄값",
                          "Henrion & Fischhoff indices (R_B, IQ, SI): main set and sensitivity variants, against 1973 and 2022, with H&F's printed row"),
}
QIDS = ["alpha_inv", "h", "e", "me", "NA"]
QNAME = {"ko": {"alpha_inv": "미세 구조 상수의 역수 α⁻¹", "h": "플랑크 상수 h", "e": "기본 전하 e", "me": "전자 질량 mₑ", "NA": "아보가드로 상수 N_A"},
         "en": {"alpha_inv": "Inverse fine-structure constant α⁻¹", "h": "Planck constant h", "e": "Elementary charge e", "me": "Electron mass mₑ", "NA": "Avogadro constant N_A"}}
KIND = {"ko": {"PE": "확률오차", "SE": "표준오차", "SD": "표준편차"}, "en": {"PE": "probable error", "SE": "standard error", "SD": "standard deviation"}}
SCALE = {"ko": {"chemical": "화학 척도", "physical": "물리 척도", "unified": "통합 척도"}, "en": {"chemical": "chemical scale", "physical": "physical scale", "unified": "unified scale"}}
REVIEWS = [  # year, short source, doi
    (1929, "Birge, Rev. Mod. Phys. 1, 1 (1929)", "10.1103/RevModPhys.1.1"),
    (1941, "Birge, Rep. Prog. Phys. 8, 90 (1941); same values in Rev. Mod. Phys. 13, 233 (1941)", "10.1088/0034-4885/8/1/307"),
    (1950, "DuMond & Cohen, Phys. Rev. 82, 555 (1951)", "10.1103/PhysRev.82.555.3"),
    (1952, "DuMond & Cohen, Rev. Mod. Phys. 25, 691 (1953)", "10.1103/RevModPhys.25.691"),
    (1955, "Cohen, DuMond, Layton & Rollett, Rev. Mod. Phys. 27, 363 (1955)", "10.1103/RevModPhys.27.363"),
    (1963, "Cohen & DuMond, Rev. Mod. Phys. 37, 537 (1965)", "10.1103/RevModPhys.37.537"),
    (1969, "Taylor, Parker & Langenberg, Rev. Mod. Phys. 41, 375 (1969) — the site's 1969 edition", "10.1103/RevModPhys.41.375"),
]
HF_CITE = "M. Henrion, B. Fischhoff, Am. J. Phys. 54, 791 (1986)"

T = {
    "ko": dict(nav="CODATA 이전", title="CODATA 이전 — 1929~1969년 권고값과 Henrion & Fischhoff 재계산",
               lead="CODATA 가 생기기 전에도 물리 상수의 권고값은 있었다. Birge(1929·1941)와 DuMond·Cohen(1950~1963)이 그때까지의 측정을 모아 값을 내고 오차를 붙였다. 이 장은 다섯 상수(α⁻¹·h·e·mₑ·N_A)의 그 값을 원 논문 표에서 옮겨, 1973 판과 2022 판에 비추어 오차가 뒤의 값을 담았는지 센다.",
               glance="한눈에 보기", fig="다섯 상수의 권고값, 1929~2022", values="옮긴 값", hf="Henrion & Fischhoff (1986) 재계산", method="방법·한계",
               review="검토", source="원 논문", page="쪽", const="상수", printed="원 표기", kind="±의 뜻", z73="z (1973 기준)", z22="z (2022 기준)", ppm22="2022 대비 ppm",
               variant="변형", ref="기준 판", n="n", rb="R_B (H&F 식 1)", rbsd="RMS", iq="IQ", si="SI", reviews="검토", download="CSV 내려받기"),
    "en": dict(nav="Before CODATA", title="Before CODATA — recommended values 1929–1969 and the Henrion & Fischhoff indices",
               lead="Recommended values of the physical constants existed before CODATA. Birge (1929, 1941) and DuMond and Cohen (1950–1963) gathered the measurements of their day into adopted values with stated errors. This chapter transcribes those values for five constants (α⁻¹, h, e, mₑ, N_A) from the original tables and counts, against the 1973 and 2022 editions, whether the stated errors covered the later values.",
               glance="At a glance", fig="Recommended values of five constants, 1929–2022", values="Transcribed values", hf="Henrion & Fischhoff (1986), recomputed", method="Method and limits",
               review="Review", source="Paper", page="Page", const="Constant", printed="As printed", kind="Kind of ±", z73="z (vs 1973)", z22="z (vs 2022)", ppm22="ppm vs 2022",
               variant="Variant", ref="Reference", n="n", rb="R_B (H&F eq. 1)", rbsd="RMS", iq="IQ", si="SI", reviews="Reviews", download="Download CSV"),
}
VARIANT_KO = {"main": "본값 — 보유한 검토 7개", "without 1950 (only reviews H&F cite)": "1950 제외(H&F 가 인용한 검토만)",
              "PE factor 1.48 (H&F)": "확률오차 환산 1.48(H&F)", "N_A not put on the unified scale": "N_A 척도 미환산",
              "probable errors not converted": "확률오차를 표준 불확도로 바꾸지 않음", "H&F printed": "H&F 표 I 인쇄값"}
VARIANT_EN = {"main": "Main — the seven reviews held"}


def read(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))


def load():
    vals = read(DER / "pre_codata_values.csv")
    hf = read(DER / "pre_codata_hf.csv")
    trans = read(TRANS / "pre_codata_reviews.csv")
    cl = {(r["qid"], int(r["edition"])): r for r in read(DER / "constants_long.csv") if r["qid"] in QIDS}
    return dict(vals=vals, hf=hf, trans=trans, cl=cl)


def hfrow(D, variant, ref):
    return next(r for r in D["hf"] if r["variant"] == variant and r["reference"] == str(ref))


def pct(x):
    return f"{float(x) * 100:.0f}"


def numbers(D):
    m73, m22 = hfrow(D, "main", 1973), hfrow(D, "main", 2022)
    pr = hfrow(D, "H&F printed", 1973)
    v = {(int(r["review"]), r["qid"]): r for r in D["vals"]}
    return dict(n=m73["n"], rb73=m73["rb_hf"], iq73=pct(m73["iq"]), si73=pct(m73["si"]), rb22=m22["rb_hf"], iq22=pct(m22["iq"]), si22=pct(m22["si"]),
                hf_n=pr["n"], hf_rb=pr["rb_hf"], hf_iq=pr["iq"].rstrip("%"), hf_si=pr["si"].rstrip("%"),
                h29=f"{float(v[(1929, 'h')]['ppm_vs_2022']) / 1e4:.1f}", e29=f"{float(v[(1929, 'e')]['ppm_vs_2022']) / 1e4:.1f}",
                zh29=f"{float(v[(1929, 'h')]['z_vs_2022']):.1f}", ze29=f"{float(v[(1929, 'e')]['z_vs_2022']):.1f}",
                rb_nf=hfrow(D, "N_A not put on the unified scale", 1973)["rb_hf"], rb_pe=hfrow(D, "probable errors not converted", 1973)["rb_hf"],
                rb_no50=hfrow(D, "without 1950 (only reviews H&F cite)", 1973)["rb_hf"])


# ------------------------------------------------------------------ figure
def _sl(v):
    return math.copysign(math.log10(1 + abs(v)), v)


def chart(D, lang, H, W=900, ph=150):
    """Five panels: deviation from the 2022 value in ppm on a symmetric log axis, pre-CODATA reviews (filled)
    and CODATA editions 1969-2018 (open), bars = ± one standard uncertainty."""
    esc = H["esc"]
    Lm, R, Tp, gap = 56, 20, 16, 30
    Hh = Tp + 5 * (ph + gap) + 20
    x0, x1 = 1925, 2025
    lim = _sl(30000)

    def X(y): return Lm + (y - x0) / (x1 - x0) * (W - Lm - R)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="{esc(T[lang]["fig"])}">']
    pre = {}
    for r in D["vals"]:
        pre.setdefault(r["qid"], []).append(r)
    for i, q in enumerate(QIDS):
        top = Tp + i * (ph + gap)

        def Y(v, top=top): return top + ph / 2 - _sl(v) / lim * (ph / 2)
        o.append(f'<text x="{Lm + 6}" y="{top + 4}" font-weight="600">{esc(QNAME[lang][q])}</text>')
        labs = {0: "0", 10: "+10", 100: "+100", 1000: "+10³", 10000: "+10⁴"}
        for t in (-10000, -1000, -100, -10, 0, 10, 100, 1000, 10000):
            lab = labs[abs(t)] if t >= 0 else labs[abs(t)].replace("+", "−")
            o.append(f'<line class="grid" x1="{Lm}" x2="{W-R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"{" stroke-width=\"1.4\"" if t == 0 else ""}/>'
                     f'<text x="{Lm-6}" y="{Y(t)+3.5:.1f}" text-anchor="end" font-size="9.5">{lab}</text>')
        x22 = float(D["cl"][(q, 2022)]["value"])
        pts = [(int(r["review"]), float(r["value_si"]), float(r["u_std_si"]), "pre" if int(r["review"]) < 1969 else "codata") for r in pre[q]]
        for ed in (1973, 1986, 1998, 2002, 2006, 2010, 2014, 2018):
            c = D["cl"].get((q, ed))
            if c and c["exact"] != "1":
                pts.append((ed, float(c["value"]), float(c["u"]), "codata"))
        for y, x, u, kind in pts:
            p, lo, hi = (x - x22) / x22 * 1e6, (x - u - x22) / x22 * 1e6, (x + u - x22) / x22 * 1e6
            col = "var(--s1)" if kind == "pre" else "var(--s3)"
            fill = col if kind == "pre" else "var(--card)"
            tip = f"{y}: {p:+,.1f} ppm (± {u / abs(x22) * 1e6:,.1f} ppm)".replace(",", " ").replace("-", "−")
            o.append(f'<line x1="{X(y):.1f}" x2="{X(y):.1f}" y1="{Y(lo):.1f}" y2="{Y(hi):.1f}" stroke="{col}" stroke-width="1.6"/>'
                     f'<circle class="dot" cx="{X(y):.1f}" cy="{Y(p):.1f}" r="4" fill="{fill}" stroke="{col}" stroke-width="1.6" data-tip="{esc(tip)}"/>')
    for yv in range(1930, 2030, 10):
        o.append(f'<text x="{X(yv):.1f}" y="{Hh - 6}" text-anchor="middle">{yv}</text>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ tables
def values_table(D, lang, t, table, esc):
    tr = {(r["review"], "e" if r["qid"].startswith("e_") else r["qid"]): r for r in D["trans"]}
    rows = []
    for r in D["vals"]:
        y, q = r["review"], r["qid"]
        s = tr.get((y, q))
        if s:
            sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
            unit = s["unit"].replace("^-1", "⁻¹")
            pw = "" if s["exp10"] == "0" else f' ×10{s["exp10"].translate(sup)}'
            printed = f'({s["printed_value"]} ± {s["printed_unc"]}){pw} {unit}'.strip() if pw else f'{s["printed_value"]} ± {s["printed_unc"]}'
            scale = f' ({SCALE[lang][s["atomic_scale"]]})' if s["atomic_scale"] else ""
            page = s["page"]
        else:
            printed, scale, page = ("사이트 1969 판" if lang == "ko" else "site's 1969 edition"), "", ""
        rows.append([y, esc(QNAME[lang][q]), esc(printed + scale), KIND[lang][r["printed_kind"]], page, r["z_vs_1973"], r["z_vs_2022"], r["ppm_vs_2022"]])
    return table([t["review"], t["const"], t["printed"], t["kind"], t["page"], t["z73"], t["z22"], t["ppm22"]], rows, num_cols=(5, 6, 7))


def hf_table(D, lang, t, table, esc):
    rows = []
    for r in D["hf"]:
        lab = VARIANT_KO.get(r["variant"], r["variant"]) if lang == "ko" else VARIANT_EN.get(r["variant"], r["variant"])
        if r["variant"] == "H&F printed":
            rows.append([esc(lab), r["reference"], r["n"], r["rb_hf"], "", r["iq"], r["si"]])
        else:
            rows.append([esc(lab), r["reference"], r["n"], r["rb_hf"], r["rb_rms"], pct(r["iq"]) + "%", pct(r["si"]) + "%"])
    return table([t["variant"], t["ref"], t["n"], t["rb"], t["rbsd"], t["iq"], t["si"]], rows, num_cols=(2, 3, 4, 5, 6))


def sources_list(lang, esc):
    items = "".join(f'<li>{y}: {esc(s)} — <a href="https://doi.org/{d}">doi:{d}</a></li>' for y, s, d in REVIEWS)
    return f'<ul>{items}</ul>'


def leaf(lang, t, cur):
    return dict(crumbs=[(("홈" if lang == "ko" else "Home"), "../index.html"), (t["nav"], "index.html")], cur=cur,
                groups=[(t["nav"], [(t["glance"], "index.html"), (t["method"], "method.html")])])


# ------------------------------------------------------------------ pages
def build(lang, base, H, out_root):
    esc, page, table, takeaway = H["esc"], H["page"], H["table"], H["takeaway"]
    t = T[lang]
    ko = lang == "ko"
    D = load()
    N = numbers(D)
    for f in PUBLIC:
        (out_root / "data" / f).write_bytes((PUBLIC_SRC[f] / f).read_bytes())
    d = base / "early"
    d.mkdir(parents=True, exist_ok=True)

    tk = ([f"1929~1963년 검토 6개와 1969 판의 다섯 상수 {N['n']}개 값을 1973 판에 비추면, 놀람 지수(|z| > 2.326)는 {N['si73']}%, 사분위 지수는 {N['iq73']}% 다(정규 기대 2%, 50%). Henrion & Fischhoff 표 I 은 {N['hf_n']}개에서 {N['hf_si']}%, {N['hf_iq']}% 였다.",
           f"기준을 2022 판으로 옮겨도 놀람 지수는 {N['si22']}%, 사분위 지수는 {N['iq22']}% 다. 뒤의 값이 인용 오차의 98% 구간 밖에 있는 경우가 절반을 넘는다는 결과는 기준 판을 바꿔도 남는다.",
           f"Birge 비 R_B(H&F 식 (1), R_B² = Σz²/(N−1))는 {N['rb73']} 로, 표 I 의 {N['hf_rb']} 와 다르다. H&F 는 검토 8개를 나열하지 않았고, 그 참고문헌 가운데 1957년 단행본을 이 사이트는 갖고 있지 않다. 그래서 같은 계산을 정확히 재현하지 못했고, 차이는 아래 감도 표에 그대로 둔다.",
           f"1929년 Birge 의 h 와 e 는 2022 판 값보다 각각 {N['h29'].lstrip('-')}%, {N['e29'].lstrip('-')}% 작았다. Birge 가 붙인 확률오차를 표준 불확도로 바꾸면 그 차이는 h 에서 {N['zh29']}배, e 에서 {N['ze29']}배다."] if ko else
          [f"Set against the 1973 edition, the {N['n']} values of the five constants in six reviews from 1929 to 1963 and the 1969 edition give a surprise index (|z| > 2.326) of {N['si73']}% and an interquartile index of {N['iq73']}% (normal: 2% and 50%). Henrion & Fischhoff's Table I reported {N['hf_si']}% and {N['hf_iq']}% for {N['hf_n']} values.",
           f"Against the 2022 edition the surprise index is {N['si22']}% and the interquartile index {N['iq22']}%. That more than half of the later values lie outside the stated 98% interval holds whichever edition is the reference.",
           f"The Birge ratio R_B (Henrion & Fischhoff's eq. (1), R_B² = Σz²/(N−1)) is {N['rb73']}, not the {N['hf_rb']} of Table I. Henrion & Fischhoff did not list their eight reviews, and the site does not hold one of the works they cite, a 1957 book. The calculation is therefore not reproduced exactly; the differences are left in the sensitivity table below.",
           f"Birge's 1929 h and e were {N['h29'].lstrip('-')}% and {N['e29'].lstrip('-')}% below the 2022 values: {N['zh29']} and {N['ze29']} times the standard uncertainty obtained from his probable errors."])
    cap = ("세로축은 2022 판 값에서의 편차(ppm)로, 0 근처는 선형이고 바깥은 로그인 대칭 로그 축이다. 채운 점은 CODATA 이전 검토(1929~1963), 빈 점은 1969~2018 판, 세로 막대는 ± 표준 불확도(확률오차는 1.4826 배). 2022 판에서 h·e·N_A 는 정의값이라 0 이다." if ko else
           "Vertical axis: deviation from the 2022 value in ppm, on a symmetric log scale (linear near zero, logarithmic beyond). Filled dots: reviews before CODATA (1929–1963); open dots: the 1969–2018 editions; bars: ± one standard uncertainty (probable errors × 1.4826). In 2022 h, e and N_A are exact, hence zero.")
    hf_lead = (f"<p>{esc(HF_CITE)} 의 표 I 「Recommended values」 줄(끝에서 두 번째, 794쪽)은 R_B {N['hf_rb']}, IQ {N['hf_iq']}%, SI {N['hf_si']}%(n = {N['hf_n']})를 보고했다. 본문(795쪽)에 따르면 다섯 상수를 「1929~1969년 검토 8개」에서 1973 값과 견주었다. 확률오차는 1.48 배해 표준편차로 바꿨다(797쪽 각주 21). 아래는 같은 정의로 다시 계산한 값과, 조건을 하나씩 바꾼 감도다. 감도 가운데 N_A 척도를 환산하지 않으면 R_B 가 {N['rb_nf']}, 확률오차를 바꾸지 않으면 {N['rb_pe']} 로 커지지만, 어느 조합도 표 I 과 정확히 맞지 않는다. 검토 목록이 정해지지 않은 상태에서 표 I 에 맞는 조건을 골라 쓰지 않았다.</p>" if ko else
               f"<p>The \"Recommended values\" row of Table I in {esc(HF_CITE)} (second to last, p. 794) reports R_B {N['hf_rb']}, IQ {N['hf_iq']}% and SI {N['hf_si']}% (n = {N['hf_n']}); the text (p. 795) says five constants in \"eight reviews from 1929 to 1969\" were set against the 1973 values. Probable errors were multiplied by 1.48 (p. 797, note 21). Below are the same indices recomputed with their definitions, and sensitivity variants that change one condition at a time. Leaving N_A on its original scale raises R_B to {N['rb_nf']}, and leaving probable errors unconverted to {N['rb_pe']}, but no combination reproduces Table I exactly. With the list of reviews unknown, no condition was picked to match it.</p>")
    body = (f'<h1>{esc(t["title"])}</h1><p class="lead">{esc(t["lead"])}</p>' + takeaway(lang, tk) +
            f'<h2>{t["fig"]}</h2><figure><div class="legend"><span style="--c:var(--s1)">{"CODATA 이전 검토" if ko else "Reviews before CODATA"}</span><span style="--c:var(--s3)">{"CODATA 판 1969~2018" if ko else "CODATA editions 1969–2018"}</span></div>{chart(D, lang, H)}<figcaption>{esc(cap)}</figcaption></figure>' +
            f'<h2>{t["hf"]}</h2><div class="prose">{hf_lead}</div>' + hf_table(D, lang, t, table, esc) +
            f'<h2>{t["values"]}</h2>' + values_table(D, lang, t, table, esc) +
            f'<h2>{"원 논문" if ko else "Papers"}</h2><div class="prose">{sources_list(lang, esc)}</div>' +
            '<p class="files">' + " ".join(f'<a href="../../data/{f}">{t["download"]}: {f}</a>' for f in PUBLIC) + '</p>' +
            f'<div class="cards"><a class="card" href="method.html"><b>{t["method"]}</b><small>{"±의 뜻·확률오차 환산·원자량 척도·단위·검증·한계" if ko else "Kinds of ±, probable errors, atomic-weight scales, units, checks, limits"}</small></a></div>')
    (d / "index.html").write_text(page(lang, t["nav"], body, 2, "early", leaf=leaf(lang, t, "index.html")), encoding="utf-8")
    (d / "method.html").write_text(page(lang, t["method"], method_body(lang, esc, takeaway), 2, "early", leaf=leaf(lang, t, "method.html")), encoding="utf-8")
    return N


def method_body(lang, esc, takeaway):
    if lang == "ko":
        tk = ["값은 원 논문 표의 쪽 이미지에서 손으로 옮겼고, 값을 모르는 독립 판독자가 같은 쪽을 다시 읽어 30개 모두 일치했다.",
              "±의 뜻은 판마다 다르다: 1929·1941·1950 은 확률오차, 1952·1955 는 표준오차, 1963 이후는 표준편차. 확률오차는 1.4826 배해 표준 불확도로 쓴다.",
              "아보가드로 상수는 원자량 척도가 화학 → 물리 → 통합(¹²C) 으로 바뀌어, Cohen & DuMond(1965)의 환산 계수로 통합 척도에 맞췄다."]
        return ("<div class=\"prose\"><h1>CODATA 이전 — 방법·한계</h1>" + takeaway("ko", tk) + """
<h2>무엇을 옮겼나</h2><p>Henrion & Fischhoff(1986) 표 I 「Recommended values」 줄의 다섯 상수 — α⁻¹, h, e, mₑ, N_A — 를, 원 논문이 그 조정의 결과로 내놓은 값(adopted value, least-squares adjusted output value)에서 옮겼다. 여러 판으로 실린 값(예: 1929년 분광·편향 두 전자 질량)은 그 논문이 다른 상수를 계산하는 데 쓴 쪽(분광)을 택했다. 줄 아래 작게 찍힌 보조 자릿수(guard digits)는 원문 설명대로 값의 일부로 쓴다.</p>
<h2>±의 뜻 — 원문 문장</h2><ul>
<li>1929 Birge: 「The real probable error in each constant is of course that indicated in the table」(61쪽).</li>
<li>1941 Birge: 표 c 각주가 「the probable error in a derived quantity」를 계산하는 법을 적는다(Rep. Prog. Phys. 129쪽, Rev. Mod. Phys. 237쪽). 전체에 대한 정의 문장은 찾지 못했다.</li>
<li>1950 DuMond & Cohen: 「the probable errors being all computed by the ellipsoid method」(555쪽).</li>
<li>1952 DuMond & Cohen: 「The quantity following each ± sign is the standard error by external consistency」(706쪽).</li>
<li>1955 Cohen 외: 「The quantity following each ± sign is the standard error」(378쪽 표 XIII).</li>
<li>1963 Cohen & DuMond: 「the standard deviation error in the final digits」(590쪽 표 XVII).</li></ul>
<p>확률오차는 정규분포의 사분위 반폭이므로 표준 불확도 = 확률오차 ÷ Φ⁻¹(0.75) ≈ 확률오차 ÷ 0.6745 다. 계산에는 1/Φ⁻¹(0.75) = 1.4826022 를 쓴다. H&F 는 1.48 을 썼고, 두 값의 차이는 지표를 거의 바꾸지 않는다(감도 표).</p>
<h2>단위와 원자량 척도</h2><ul>
<li>e 는 전자기 단위(emu) 값이 실린 경우 그것을 쓴다(1 emu = 10 C). esu 값은 그 시대의 빛의 속력에 따라 달라지기 때문이다. 1950 은 esu 만 실려 있어 같은 표의 c(299 790.2 km/s)로 바꿨다.</li>
<li>h 는 erg s → J s, mₑ 는 g → kg 로 바꿨다.</li>
<li>N_A: 1929·1941 은 옛 화학 척도(O = 16), 1950~1955 는 물리 척도(¹⁶O = 16), 1963 부터 통합 척도(¹²C = 12)다. Cohen & DuMond(1965) 547쪽의 「물리 척도 질량 ÷ 통합 척도 질량 = 1.000317917 ± 0.000000017」, 548쪽의 「옛 화학 척도 ÷ 통합 척도 = 1.000043 ± 0.000005」로 나눠 통합 척도에 맞췄다. 1929 의 N₀ 줄에는 척도가 적혀 있지 않아 표 a 의 원자량 정의(O = 16.0000)에서 화학 척도로 보았다. 1965 의 화학 척도 계수를 1929·1941 에 적용하는 것은 가정이다. 두 계수는 정확한 수로 쓰고 그 불확도(최대 5 ppm)는 전파하지 않았다. 전파해도 N_A 불확도는 0.02% 미만 커지고 지수는 소수 둘째 자리까지 같다.</li></ul>
<h2>지수</h2><p>z = (기준 판 값 − 옛 값) / 옛 표준 불확도. 기준 판의 불확도는 넣지 않는다(H&F 의 정의). 사분위 지수(IQ)는 |z| < 0.6745, 놀람 지수(SI)는 |z| > 2.326 인 비율이다(H&F 는 0.675·2.33 으로 적었다). Birge 비 R_B 는 H&F 식 (1)(792쪽)대로 R_B² = Σz²/(N−1) 이다. H&F 의 식은 집단 평균에 대한 잔차로 적혀 있으나, 권고값 줄은 1973 값에 대한 잔차로 계산했다고 적었으므로(795쪽) z 를 그대로 넣는다. 제곱평균제곱근 √(Σz²/N) 도 함께 싣는다. 1969 판 값은 이 사이트의 1969 판 자료를 쓴다.</p>
<h2>검증</h2><ul>
<li>값 30개(1929~1963 검토 6개 × 5)를 쪽 이미지에서 옮긴 뒤, 값을 모르는 독립 판독자가 같은 쪽을 그림으로 다시 읽었다. 값·±·지수·±의 뜻 모두 30/30 일치.</li>
<li>Birge 1941 의 두 판(Rep. Prog. Phys. 와 Rev. Mod. Phys.)에서 다섯 값이 같다.</li>
<li>연도별 ppm 편차는 H&F 그림 3(1952~1973)과 대체로 맞는다(예: 1952 h −147 ppm, N_A +126 ppm, 1973 기준).</li></ul>
<h2>한계</h2><ul>
<li>H&F 는 검토 8개를 나열하지 않았다. 표 I 의 참고문헌에서 특정되는 검토는 1929·1941·1952·1955·1957·1963·1969 의 7개이고, 1957 판(Cohen, Crowe & DuMond, <i>The Fundamental Constants of Physics</i>, Interscience)은 이 사이트에 없다. 1950 서한은 H&F 가 광속 그림에만 인용했다. 본값은 보유한 7개, 1950 을 뺀 6개는 감도다.</li>
<li>검토들은 같은 실험 자료를 이어 쓰므로 독립이 아니다. 1952 와 1955 는 같은 1952 자료를 다시 분석했다.</li>
<li>1973·2022 판도 참값이 아니다.</li>
<li>원 논문의 표는 학술지에 실린 것이다. 이 사이트는 값(숫자)과 쪽만 싣고 PDF 는 싣지 않는다.</li></ul>
<h2>재현</h2><p><code>data/transcribed/pre_codata_reviews.csv</code>(전사) → <code>src/pre_codata.py</code>(환산·지수) → <code>src/pre_site.py</code>(이 면).</p></div>""")
    tk = ["Values were transcribed by hand from page images of the original tables; an independent reader who did not know them read the same pages again, and all 30 agree.",
          "The ± means different things: probable error in 1929, 1941 and 1950, standard error in 1952 and 1955, standard deviation from 1963. Probable errors are multiplied by 1.4826 to give standard uncertainties.",
          "The atomic-weight scale behind the Avogadro constant moved from chemical to physical to unified (¹²C); values are put on the unified scale with the factors of Cohen & DuMond (1965)."]
    return ("<div class=\"prose\"><h1>Before CODATA — method and limits</h1>" + takeaway("en", tk) + """
<h2>What was transcribed</h2><p>The five constants of the "Recommended values" row of Henrion & Fischhoff's (1986) Table I — α⁻¹, h, e, mₑ, N_A — as each paper gave them as the result of its adjustment (adopted values, least-squares adjusted output values). Where a paper prints more than one version (in 1929 a spectroscopic and a deflection electron mass), the one the paper used to compute other constants (spectroscopic) is taken. Guard digits printed below the line are used as part of the value, as the papers explain.</p>
<h2>What the ± means, in the papers' words</h2><ul>
<li>1929, Birge: "The real probable error in each constant is of course that indicated in the table" (p. 61).</li>
<li>1941, Birge: the note to Table c explains how to compute "the probable error in a derived quantity" (Rep. Prog. Phys. p. 129; Rev. Mod. Phys. p. 237). No general defining sentence was found.</li>
<li>1950, DuMond & Cohen: "the probable errors being all computed by the ellipsoid method" (p. 555).</li>
<li>1952, DuMond & Cohen: "The quantity following each ± sign is the standard error by external consistency" (p. 706).</li>
<li>1955, Cohen et al.: "The quantity following each ± sign is the standard error" (p. 378, Table XIII).</li>
<li>1963, Cohen & DuMond: "the standard deviation error in the final digits" (p. 590, Table XVII).</li></ul>
<p>A probable error is the half-width of the central 50% of a normal distribution, so standard uncertainty = probable error ÷ Φ⁻¹(0.75) ≈ probable error ÷ 0.6745; the calculation uses 1/Φ⁻¹(0.75) = 1.4826022. Henrion & Fischhoff used 1.48; the difference hardly moves the indices (sensitivity table).</p>
<h2>Units and atomic-weight scales</h2><ul>
<li>For e the electromagnetic-unit (emu) figure is used where printed (1 emu = 10 C), because an esu figure depends on the speed of light of the day. 1950 prints esu only, converted with the same table's c (299 790.2 km/s).</li>
<li>h from erg s to J s, mₑ from g to kg.</li>
<li>N_A: the old chemical scale (O = 16) in 1929 and 1941, the physical scale (¹⁶O = 16) in 1950–1955, the unified scale (¹²C = 12) from 1963. Values are divided by "mass on physical scale / mass on unified scale = 1.000317917 ± 0.000000017" (Cohen & DuMond 1965, p. 547) and "old chemical scale / unified scale = 1.000043 ± 0.000005" (p. 548). The 1929 N₀ line states no scale; the chemical scale is inferred from the definition of atomic weights in Table a (O = 16.0000). Applying the 1965 chemical-scale factor to 1929 and 1941 is an assumption. Both factors are used as exact numbers and their uncertainty (at most 5 ppm) is not propagated; propagating it would enlarge the N_A uncertainties by less than 0.02% and leave the indices unchanged to two decimals.</li></ul>
<h2>Indices</h2><p>z = (reference value − earlier value) / earlier standard uncertainty; the reference's uncertainty is not included (Henrion & Fischhoff's definition). The interquartile index (IQ) is the share with |z| < 0.6745, the surprise index (SI) the share with |z| > 2.326 (written 0.675 and 2.33 by Henrion & Fischhoff). The Birge ratio follows Henrion & Fischhoff's eq. (1) (p. 792), R_B² = Σz²/(N−1). Their equation is written with residuals about the group mean, but for the recommended values they state that residuals were taken relative to the 1973 estimates (p. 795), so z is used as it is. The root mean square √(Σz²/N) is given too. The 1969 values are the site's 1969 edition.</p>
<h2>Checks</h2><ul>
<li>The 30 values (six reviews from 1929 to 1963 × 5) were transcribed from page images; an independent reader who did not know them read the same pages from images again. Values, ±, exponents and kinds of ± agree 30/30.</li>
<li>The two 1941 papers of Birge (Rep. Prog. Phys. and Rev. Mod. Phys.) give the same five values.</li>
<li>The ppm deviations by year broadly match Henrion & Fischhoff's Fig. 3 (1952–1973): for example 1952 h −147 ppm and N_A +126 ppm against 1973.</li></ul>
<h2>Limits</h2><ul>
<li>Henrion & Fischhoff did not list their eight reviews. The reviews identifiable from the references of Table I are seven, 1929, 1941, 1952, 1955, 1957, 1963 and 1969, and the 1957 one (Cohen, Crowe & DuMond, <i>The Fundamental Constants of Physics</i>, Interscience) is not held. They cite the 1950 letter only for their speed-of-light figure. The main set is the seven reviews held; the six without 1950 are a sensitivity check.</li>
<li>The reviews reuse the same experimental data and are not independent; 1952 and 1955 reanalyze the same 1952 data.</li>
<li>The 1973 and 2022 values are not the true values either.</li>
<li>The tables were published in journals; the site gives only the values (numbers) and pages, not the PDFs.</li></ul>
<h2>Reproduction</h2><p><code>data/transcribed/pre_codata_reviews.csv</code> (transcription) → <code>src/pre_codata.py</code> (conversions, indices) → <code>src/pre_site.py</code> (this page).</p></div>""")


def data_rows(lang, esc):
    return [[f'<a href="../data/{f}">{f}</a>', esc(DESC[f][0 if lang == "ko" else 1])] for f in PUBLIC]


def data_license(lang, esc):
    if lang == "ko":
        return "<h2>CODATA 이전 장</h2><p>1929~1963년 권고값은 원 논문(Rev. Mod. Phys., Rep. Prog. Phys., Phys. Rev.)의 표에서 값과 쪽만 옮겼다. 논문 PDF 는 싣지 않는다. 이 사이트의 CC BY 4.0 은 엮은이가 계산한 부분(환산·z·지수)에 미친다.</p>"
    return "<h2>Before-CODATA chapter</h2><p>The 1929–1963 recommended values were taken from the tables of the original papers (Rev. Mod. Phys., Rep. Prog. Phys., Phys. Rev.); only the values and pages are reproduced, not the PDFs. The site's CC BY 4.0 covers the editor's computations (conversions, z, indices).</p>"


def datapackage_resources():
    return [dict(path=f, description=DESC[f][1] + ". Values transcribed from the original papers (cited per row); CC BY 4.0 covers the editor's computations.", format="csv") for f in PUBLIC]
