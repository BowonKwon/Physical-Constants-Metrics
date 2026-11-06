# -*- coding: utf-8 -*-
"""1.3: recommended values before CODATA (1929-1963) and the Henrion & Fischhoff (1986) check.

Inputs
  data/transcribed/pre_codata_reviews.csv   hand transcription from the original papers (value and ± as printed,
                                             page, kind of ±, atomic-weight scale)
  data/transcribed/atomic_scale_factors.csv conversion factors to the unified (12C = 12) scale, from
                                             Cohen & DuMond, Rev. Mod. Phys. 37, 537 (1965), pp. 547-548
  data/derived/constants_long.csv           1969, 1973 and 2022 values (already on the site)

Outputs (data/derived/)
  pre_codata_values.csv   one row per review x constant: SI value, standard uncertainty, z and ppm against 1973 and 2022
  pre_codata_hf.csv       R_B, IQ and SI for the main set and the sensitivity variants, next to H&F's printed row

Conventions (owner decisions D1-D6, 2026-11-06)
  * Five constants of the "Recommended values" row of H&F's Table I (second to last, p. 794): alpha^-1, h, e, m_e, N_A.
  * Main set: the seven reviews held, 1929, 1941, 1950, 1952, 1955, 1963, 1969 (35 values). H&F counted
    "eight reviews from 1929 to 1969" (40 values) without listing them; their references also include the
    1957 book of Cohen, Crowe & DuMond, which is not held.
  * A probable error (PE) is turned into a standard uncertainty by 1/Phi^-1(0.75) = 1.4826022 (PE/0.6745); H&F used 1.48.
  * The scale factors are applied as exact numbers; their own uncertainty (at most 5 ppm) is not propagated.
  * N_A is put on the unified scale with the factors of the 1965 paper; for 1929 and 1941 (old chemical scale)
    the 1965 chemical factor is applied as an assumption.
  * e: the emu (or coulomb) figure is used where printed, so the value does not depend on the speed of light
    of the time; 1950 prints esu only and is converted with that table's own c.
  * z = (x_ref - x_i) / u_i, the reference uncertainty not included (H&F's definition).
  * R_B as H&F's eq. (1), p. 792: R_B^2 = sum(z^2)/(N-1), residuals taken about the reference (their p. 795).
    The RMS, sqrt(sum(z^2)/N), is given beside it.

  python src/pre_codata.py
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np
from scipy import stats

getcontext().prec = 40
ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "data" / "transcribed"
DER = ROOT / "data" / "derived"

QIDS = ["alpha_inv", "h", "e", "me", "NA"]
PE_FACTOR = Decimal(1) / Decimal(str(stats.norm.ppf(0.75)))   # 1.4826
PE_FACTOR_HF = Decimal("1.48")
IQ_K = stats.norm.ppf(0.75)
SI_K = stats.norm.ppf(0.99)   # 2.326; H&F printed 2.33
MAIN = [1929, 1941, 1950, 1952, 1955, 1963, 1969]
HF_PRINTED = dict(n=40, rb="7.42", iq="22%", si="57%", source="Henrion & Fischhoff, Am. J. Phys. 54, 791 (1986), p. 794, Table I")
C_1950_CM_S = Decimal("2.997902E10")   # Phys. Rev. 82, 556, Table I: c = 299790.2 km/s


def scale_factors():
    return {r["from_scale"]: Decimal(r["factor_mass_ratio_to_unified"])
            for r in csv.DictReader(open(TRANS / "atomic_scale_factors.csv", encoding="utf-8"))}


def to_si(r, factors, convert_scale=True):
    """Printed value and ± -> (qid, value in SI, ± in SI). The ± keeps its printed kind (PE/SE/SD)."""
    x = Decimal(r["printed_value"]) * Decimal(10) ** int(r["exp10"])
    u = Decimal(r["printed_unc"]) * Decimal(10) ** int(r["exp10"])
    q, unit = r["qid"], r["unit"]
    if q == "h" and unit == "erg s":
        x, u = x * Decimal("1e-7"), u * Decimal("1e-7")
    elif q == "me" and unit == "g":
        x, u = x * Decimal("1e-3"), u * Decimal("1e-3")
    elif q == "e_emu":
        q, x, u = "e", x * 10, u * 10
    elif q == "e_C":
        q = "e"
    elif q == "e_esu":
        q, x, u = "e", x / C_1950_CM_S * 10, u / C_1950_CM_S * 10
    elif q == "NA" and unit == "kmol^-1":
        x, u = x * Decimal("1e-3"), u * Decimal("1e-3")
    if q == "NA" and convert_scale and r["atomic_scale"] in ("physical", "chemical"):
        f = factors[r["atomic_scale"]]
        x, u = x / f, u / f
    return q, x, u


def load_refs():
    out = {}
    for r in csv.DictReader(open(DER / "constants_long.csv", encoding="utf-8")):
        if r["qid"] in QIDS and r["edition"] in ("1969", "1973", "2022"):
            out[(int(r["edition"]), r["qid"])] = (Decimal(r["value"]), Decimal(r["u"]))
    return out


def values(pe_factor=PE_FACTOR, convert_scale=True):
    """List of dicts: review, qid, x (SI), u_std, kind, scale, page, source."""
    factors = scale_factors()
    rows = []
    for r in csv.DictReader(open(TRANS / "pre_codata_reviews.csv", encoding="utf-8")):
        q, x, u = to_si(r, factors, convert_scale)
        u_std = u * pe_factor if r["unc_kind"] == "PE" else u
        rows.append(dict(review=int(r["review"]), qid=q, x=x, u_printed=u, u_std=u_std, kind=r["unc_kind"],
                         scale=r["atomic_scale"], page=r["page"], source=r["source"]))
    refs = load_refs()
    for q in QIDS:   # 1969 from the site's own transcription (Taylor, Parker & Langenberg 1969)
        x, u = refs[(1969, q)]
        rows.append(dict(review=1969, qid=q, x=x, u_printed=u, u_std=u, kind="SD",
                         scale="unified" if q == "NA" else "", page="", source="1969 edition (site data)"))
    return rows, refs


def indices(z):
    z = np.asarray(z, float)
    a = np.abs(z)
    return dict(n=int(z.size), rb_hf=float(np.sqrt(np.sum(z ** 2) / (z.size - 1))), rb_rms=float(np.sqrt(np.mean(z ** 2))),
                iq=float(np.mean(a < IQ_K)), si=float(np.mean(a > SI_K)))


def zs(rows, refs, ref_year, reviews):
    out = []
    for r in rows:
        if r["review"] in reviews and r["review"] < ref_year:
            xr, _ = refs[(ref_year, r["qid"])]
            out.append(float((xr - r["x"]) / r["u_std"]))
    return out


def main():
    rows, refs = values()
    table = []
    for r in sorted(rows, key=lambda r: (r["review"], QIDS.index(r["qid"]))):
        d = dict(review=r["review"], qid=r["qid"], value_si=f"{r['x']:.10g}", u_std_si=f"{r['u_std']:.10g}",
                 printed_kind=r["kind"], atomic_scale=r["scale"], page=r["page"], source=r["source"])
        for ref in (1973, 2022):
            xr, _ = refs[(ref, r["qid"])]
            d[f"z_vs_{ref}"] = f"{float((xr - r['x']) / r['u_std']):.3f}"
            d[f"ppm_vs_{ref}"] = f"{float((r['x'] - xr) / xr * 1_000_000):.1f}"
        table.append(d)
    write("pre_codata_values.csv", table)

    variants = [("main", MAIN, PE_FACTOR, True),
                ("without 1950 (only reviews H&F cite)", [y for y in MAIN if y != 1950], PE_FACTOR, True),
                ("PE factor 1.48 (H&F)", MAIN, PE_FACTOR_HF, True),
                ("N_A not put on the unified scale", MAIN, PE_FACTOR, False),
                ("probable errors not converted", MAIN, Decimal(1), True)]
    out = []
    for label, revs, pef, conv in variants:
        rws, _ = values(pef, conv)
        for ref in (1973, 2022):
            s = indices(zs(rws, refs, ref, revs))
            out.append(dict(variant=label, reference=ref, reviews=" ".join(map(str, revs)), n=s["n"],
                            rb_hf=f"{s['rb_hf']:.2f}", rb_rms=f"{s['rb_rms']:.2f}",
                            iq=f"{s['iq']:.3f}", si=f"{s['si']:.3f}"))
    out.append(dict(variant="H&F printed", reference=1973, reviews="eight reviews 1929-1969 (not listed)",
                    n=HF_PRINTED["n"], rb_hf=HF_PRINTED["rb"], rb_rms="", iq=HF_PRINTED["iq"], si=HF_PRINTED["si"]))
    write("pre_codata_hf.csv", out)
    for o in out:
        print(o)


def write(name, rows):
    with open(DER / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
