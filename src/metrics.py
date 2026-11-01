# -*- coding: utf-8 -*-
"""Compute every published metric from data/derived/constants_long.csv.

Outputs (data/derived/)
  m1_halflife.csv          relative-uncertainty half-life per quantity
  m2_pairs.csv             every consecutive-edition pair (z with both uncertainties, z_old)
  m2_summary.csv           exceedance rates |z|>1,2,3 vs normal, with cluster-bootstrap CIs
  m3_vs_latest.csv         every (edition, quantity) compared with the 2022 edition
  m3_summary.csv           miss rates by edition and pooled, interquartile and surprise indices
  m4_tail.csv              Student-t fit (nu, scale) to the pooled pair z, bootstrap CIs
  m5_funnel.csv            per edition: (x - x_2022)/x_2022 and u/|x_2022|
  m6_events.csv            transitions measured <-> exact
  sens_all_rows.csv        sensitivity: consecutive pairs over every ASCII row with an unchanged name
  summary.json             headline numbers for the site

Conventions
  * 'measured' = has a standard uncertainty > 0 in that edition.
  * Edition year = the year in the edition's name (data cut-off), not publication year.
  * Confidence intervals for rates: cluster bootstrap that resamples quantities (not pairs),
    B = 10,000, seed 2026, percentile 95%.

  python src/metrics.py
"""
from __future__ import annotations

import csv
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np
from scipy import optimize, stats

getcontext().prec = 40
ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
LATEST = 2022
B = 10_000
SEED = 2026
NORMAL = {1: 2 * stats.norm.sf(1), 2: 2 * stats.norm.sf(2), 3: 2 * stats.norm.sf(3)}
IQ_K = stats.norm.ppf(0.75)        # 0.6745: inside the 25-75 percentiles
SI_K = stats.norm.ppf(0.99)        # 2.326: outside the 98% interval (Henrion & Fischhoff)


def load():
    qmap = {r["qid"]: r for r in csv.DictReader(open(DER / "quantity_map.csv", encoding="utf-8"))}
    data = {}
    for r in csv.DictReader(open(DER / "constants_long.csv", encoding="utf-8")):
        data.setdefault(r["qid"], {})[int(r["edition"])] = dict(
            x=Decimal(r["value"]), u=Decimal(r["u"]), exact=r["exact"] == "1")
    return qmap, data


def measured(row):
    return (not row["exact"]) and row["u"] > 0


def write(name, rows, fields=None):
    if not rows:
        return
    fields = fields or list(rows[0].keys())
    with open(DER / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def cluster_boot(groups: dict, stat, rng):
    """groups: qid -> array of values. stat: function(concatenated array) -> float."""
    keys = list(groups)
    out = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, len(keys), len(keys))
        arr = np.concatenate([groups[keys[i]] for i in pick])
        out[b] = stat(arr) if arr.size else np.nan
    return np.nanpercentile(out, [2.5, 97.5])


# ---------------------------------------------------------------- M1
def m1(qmap, data):
    rows = []
    for q, eds in data.items():
        pts = [(y, float(r["u"] / abs(r["x"]))) for y, r in sorted(eds.items()) if measured(r)]
        if len(pts) < 4:
            continue
        x = np.array([p[0] for p in pts], float)
        yv = np.log2([p[1] for p in pts])
        res = stats.linregress(x, yv)
        n = len(pts)
        t = stats.t.ppf(0.975, n - 2)
        lo_s, hi_s = res.slope - t * res.stderr, res.slope + t * res.stderr
        # slopes flatter than -0.001 per year (half-life > 1,000 years) are reported as no decline
        hl = -1 / res.slope if res.slope < -0.001 else math.inf
        # half-life CI: slope interval mapped through -1/slope; open-ended if the interval reaches 0
        hl_lo = -1 / lo_s if lo_s < 0 else math.inf  # steepest slope -> shortest half-life
        hl_hi = -1 / hi_s if hi_s < 0 else math.inf
        rows.append(dict(qid=q, layer=qmap[q]["layer"], n_editions=n, first=int(x[0]), last=int(x[-1]),
                         u_rel_first=f"{pts[0][1]:.3e}", u_rel_last=f"{pts[-1][1]:.3e}",
                         slope_log2_per_year=f"{res.slope:.5f}", slope_se=f"{res.stderr:.5f}",
                         halflife_years=("inf" if math.isinf(hl) else f"{hl:.2f}"),
                         halflife_ci_low=("inf" if math.isinf(hl) else f"{hl_lo:.2f}"),
                         slope_ci_includes_zero=int(lo_s <= 0 <= hi_s),
                         halflife_ci_high=("inf" if math.isinf(hl_hi) else f"{hl_hi:.2f}"),
                         r2=f"{res.rvalue ** 2:.3f}"))
    return rows


# ---------------------------------------------------------------- M2
def m2_pairs(qmap, data):
    rows = []
    for q, eds in data.items():
        ys = sorted(y for y, r in eds.items() if measured(r))
        for a, b in zip(ys, ys[1:]):
            ra, rb = eds[a], eds[b]
            d = rb["x"] - ra["x"]
            den = (ra["u"] ** 2 + rb["u"] ** 2).sqrt()
            rows.append(dict(qid=q, layer=qmap[q]["layer"], ed_from=a, ed_to=b, gap=b - a,
                             diff=str(d), u_from=str(ra["u"]), u_to=str(rb["u"]),
                             z=f"{float(d / den):.4f}", z_old=f"{float(d / ra['u']):.4f}",
                             u_ratio=f"{float(rb['u'] / ra['u']):.4f}"))
    return rows


def rate_table(pairs, label, rng, col="z"):
    groups = {}
    for p in pairs:
        groups.setdefault(p["qid"], []).append(abs(float(p[col])))
    groups = {k: np.array(v) for k, v in groups.items()}
    allz = np.concatenate(list(groups.values()))
    out = []
    for k in (1, 2, 3):
        rate = float(np.mean(allz > k))
        lo, hi = cluster_boot(groups, lambda a, k=k: np.mean(a > k), rng)
        out.append(dict(subset=label, measure=col, threshold=k, n_pairs=int(allz.size), n_quantities=len(groups),
                        exceed=int(np.sum(allz > k)), rate=f"{rate:.4f}", ci_low=f"{lo:.4f}", ci_high=f"{hi:.4f}",
                        normal=f"{NORMAL[k]:.4f}", ratio_to_normal=f"{rate / NORMAL[k]:.2f}"))
    return out


# ---------------------------------------------------------------- M3
def m3(qmap, data):
    rows = []
    for q, eds in data.items():
        if LATEST not in eds:
            continue
        ref = eds[LATEST]
        for y, r in sorted(eds.items()):
            if y == LATEST or not measured(r):
                continue
            d = ref["x"] - r["x"]
            z_old = float(d / r["u"])
            z_both = float(d / (r["u"] ** 2 + ref["u"] ** 2).sqrt())
            rows.append(dict(qid=q, layer=qmap[q]["layer"], edition=y, ref_exact=int(ref["exact"]),
                             diff=str(d), u=str(r["u"]), u_ref=str(ref["u"]),
                             z_old=f"{z_old:.4f}", z_both=f"{z_both:.4f}",
                             miss_1sigma=int(abs(z_old) > 1), miss_2sigma=int(abs(z_old) > 2),
                             inside_iq=int(abs(z_old) < IQ_K), surprise=int(abs(z_old) > SI_K)))
    return rows


def m3_summary(rows, rng):
    out = []
    eds = sorted({r["edition"] for r in rows})
    subsets = [(str(e), [r for r in rows if r["edition"] == e]) for e in eds]
    subsets += [("1969-1986", [r for r in rows if r["edition"] <= 1986]),
                ("1998-2018", [r for r in rows if r["edition"] >= 1998]),
                ("all", rows)]
    for label, rs in subsets:
        groups = {}
        for r in rs:
            groups.setdefault(r["qid"], []).append(abs(float(r["z_old"])))
        groups = {k: np.array(v) for k, v in groups.items()}
        a = np.concatenate(list(groups.values()))
        rec = dict(subset=label, n=int(a.size), n_quantities=len(groups))
        for name, f, exp in (("miss_1sigma", lambda v: np.mean(v > 1), NORMAL[1]),
                             ("miss_2sigma", lambda v: np.mean(v > 2), NORMAL[2]),
                             ("inside_iq", lambda v: np.mean(v < IQ_K), 0.5),
                             ("surprise", lambda v: np.mean(v > SI_K), 0.02)):
            rec[name] = f"{f(a):.3f}"
            if len(groups) >= 3:
                lo, hi = cluster_boot(groups, f, rng)
                rec[name + "_ci"] = f"[{lo:.3f}, {hi:.3f}]"
            else:
                rec[name + "_ci"] = ""
            rec[name + "_normal"] = f"{exp:.3f}"
        rec["median_abs_z"] = f"{np.median(a):.2f}"
        out.append(rec)
    return out


# ---------------------------------------------------------------- M4
def t_fit(z):
    """MLE of a zero-centred Student-t: returns (nu, scale)."""
    z = np.asarray(z, float)

    def nll(p):
        lnu, ls = p
        return -np.sum(stats.t.logpdf(z, df=math.exp(lnu), loc=0, scale=math.exp(ls)))
    best = None
    for lnu0 in (0.0, 1.0, 2.5):
        r = optimize.minimize(nll, x0=[lnu0, math.log(np.median(np.abs(z)) + 1e-9)], method="Nelder-Mead",
                              options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
        if best is None or r.fun < best.fun:
            best = r
    nu, s = math.exp(best.x[0]), math.exp(best.x[1])
    return min(nu, 1e4), s


def m4(pairs, rng, label):
    groups = {}
    for p in pairs:
        groups.setdefault(p["qid"], []).append(float(p["z"]))
    groups = {k: np.array(v) for k, v in groups.items()}
    z = np.concatenate(list(groups.values()))
    nu, s = t_fit(z)
    keys = list(groups)
    nus, ss = [], []
    for b in range(2000):  # t fits are slower; 2,000 resamples
        pick = rng.integers(0, len(keys), len(keys))
        arr = np.concatenate([groups[keys[i]] for i in pick])
        n_, s_ = t_fit(arr)
        nus.append(n_)
        ss.append(s_)
    return dict(subset=label, n_pairs=int(z.size), n_quantities=len(groups), nu=f"{nu:.2f}",
                nu_ci_low=f"{np.percentile(nus, 2.5):.2f}", nu_ci_high=f"{np.percentile(nus, 97.5):.2f}",
                scale=f"{s:.2f}", scale_ci_low=f"{np.percentile(ss, 2.5):.2f}", scale_ci_high=f"{np.percentile(ss, 97.5):.2f}",
                bootstrap=2000)


# ---------------------------------------------------------------- Henrion & Fischhoff style
HF_QUANTITIES = ["alpha", "e", "h", "me", "NA"]


def hf_repro(data):
    """The five constants of Henrion & Fischhoff (1986) table I, last row: alpha^-1, e, h, m_e, N_A.
    z = (x_ref - x_i)/u_i. Reference 1973 (their choice) and 2022 (this site)."""
    out = []
    for ref, earlier in ((1973, [1969]), (2022, [1969, 1973, 1986, 1998, 2002, 2006, 2010, 2014, 2018])):
        zs = []
        for q in HF_QUANTITIES:
            eds = data[q]
            for y in earlier:
                if y in eds and measured(eds[y]) and ref in eds:
                    z = float((eds[ref]["x"] - eds[y]["x"]) / eds[y]["u"])
                    zs.append(z)
                    out.append(dict(reference=ref, qid=q, edition=y, ref_exact=int(eds[ref]["exact"]), z_old=f"{z:.3f}"))
        a = np.abs(np.array(zs))
        out.append(dict(reference=ref, qid="ALL", edition=f"n={a.size}", ref_exact="",
                        z_old=f"IQ={np.mean(a < IQ_K):.3f} SI={np.mean(a > SI_K):.3f} RMS={np.sqrt(np.mean(a ** 2)):.2f}"))
    return out


# ---------------------------------------------------------------- M5, M6
def m5(qmap, data):
    rows = []
    for q, eds in data.items():
        if LATEST not in eds:
            continue
        ref = eds[LATEST]["x"]
        for y, r in sorted(eds.items()):
            rows.append(dict(qid=q, layer=qmap[q]["layer"], edition=y, exact=int(r["exact"]),
                             rel_dev=f"{float((r['x'] - ref) / abs(ref)):.6e}",
                             rel_u=f"{float(r['u'] / abs(ref)):.6e}"))
    return rows


def m6(qmap, data):
    rows = []
    for q, eds in data.items():
        ys = sorted(eds)
        for a, b in zip(ys, ys[1:]):
            ea, eb = eds[a]["exact"], eds[b]["exact"]
            if ea != eb:
                rows.append(dict(qid=q, layer=qmap[q]["layer"], ed_before=a, ed_after=b,
                                 direction="measured->exact" if eb else "exact->measured",
                                 u_rel_measured=f"{float(eds[a if eb else b]['u'] / abs(eds[a if eb else b]['x'])):.3e}"))
    return rows


# ---------------------------------------------------------------- sensitivity: all rows
def sensitivity(rng):
    rows = list(csv.DictReader(open(DER / "constants_all_rows.csv", encoding="utf-8")))
    by = {}
    for r in rows:
        if r["exact"] == "0" and Decimal(r["u"]) > 0:
            by.setdefault(r["name"], {})[int(r["edition"])] = (Decimal(r["value"]), Decimal(r["u"]))
    pairs = []
    order = [1998, 2002, 2006, 2010, 2014, 2018, 2022]
    for name, eds in by.items():
        for a, b in zip(order, order[1:]):
            if a in eds and b in eds:
                (xa, ua), (xb, ub) = eds[a], eds[b]
                pairs.append(dict(qid=name, z=f"{float((xb - xa) / (ua * ua + ub * ub).sqrt()):.4f}"))
    return pairs, rate_table(pairs, "all ASCII rows 1998-2022 (same name)", rng)


def main():
    rng = np.random.default_rng(SEED)
    qmap, data = load()
    core = {q: v for q, v in data.items() if qmap[q]["layer"] == "K"}

    r1 = m1(qmap, data)
    write("m1_halflife.csv", r1)

    pairs = m2_pairs(qmap, data)
    write("m2_pairs.csv", pairs)
    kp = [p for p in pairs if p["layer"] == "K"]
    summ = []
    summ += rate_table(kp, "core: all consecutive pairs", rng)
    summ += rate_table([p for p in kp if p["ed_from"] >= 1998], "core: 1998-2022 (4-year gaps)", rng)
    summ += rate_table([p for p in kp if p["ed_from"] < 1998], "core: 1969-1998 (4-13-year gaps)", rng)
    summ += rate_table(kp, "core: all consecutive pairs", rng, col="z_old")
    write("m2_summary.csv", summ)

    r3 = [r for r in m3(qmap, data) if r["layer"] == "K"]
    write("m3_vs_latest.csv", m3(qmap, data))
    s3 = m3_summary(r3, rng)
    write("m3_summary.csv", s3)

    t_all = m4(kp, rng, "core: all consecutive pairs")
    t_new = m4([p for p in kp if p["ed_from"] >= 1998], rng, "core: 1998-2022")
    t_nz = m4([p for p in kp if float(p["z"]) != 0], rng, "core: pairs with a nonzero change")
    write("m4_tail.csv", [t_all, t_new, t_nz])
    write("hf_repro.csv", hf_repro(data))

    write("m5_funnel.csv", m5(qmap, data))
    write("m6_events.csv", m6(qmap, data))

    sp, ss = sensitivity(rng)
    write("sens_all_rows.csv", ss)

    k1 = [r for r in r1 if r["layer"] == "K"]
    hl = sorted(float(r["halflife_years"]) for r in k1 if r["halflife_years"] != "inf")
    summary = dict(
        n_quantities_core=len(core),
        editions=sorted({y for v in data.values() for y in v}),
        m1_median_halflife_core=float(np.median(hl)), m1_n=len(hl),
        m2=summ, m3=s3, m4=[t_all, t_new, t_nz], sensitivity=ss,
        n_zero_change_pairs=sum(1 for p in kp if float(p["z"]) == 0), n_core_pairs=len(kp),
    )
    (DER / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")

    # console digest
    print("M1 median half-life (core):", f"{np.median(hl):.1f} y over {len(hl)} quantities")
    for s in summ:
        print("M2", s["subset"], s["measure"], f">{s['threshold']}", s["rate"], f"[{s['ci_low']}, {s['ci_high']}]",
              "normal", s["normal"], "n", s["n_pairs"], "q", s["n_quantities"])
    for s in s3:
        print("M3", s["subset"], "n", s["n"], "miss1", s["miss_1sigma"], s["miss_1sigma_ci"], "miss2", s["miss_2sigma"],
              "IQ", s["inside_iq"], "SI", s["surprise"])
    print("M4", t_all)
    print("M4", t_new)
    print("M4", t_nz)
    for s in ss:
        print("SENS", s["threshold"], s["rate"], s["n_pairs"], s["n_quantities"])


if __name__ == "__main__":
    main()
