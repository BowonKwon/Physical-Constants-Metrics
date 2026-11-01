# -*- coding: utf-8 -*-
"""Atomic-weights chapter (1.1): parse CIAAW's historical standard atomic weights and compute A1-A5.

Input   data/raw/ciaaw_IUPAC-TSAW.csv   CIAAW, historical changes of standard atomic weights 1902-2024
                                        (compiled by J. Meija; one row per recommended revision, with the DOI
                                        of the CIAAW report). Retrieved by src/fetch_raw.py.
Outputs data/derived/aw_long.csv        every revision, parsed
        data/derived/aw_a1_elements.csv  A1/A4 per element: number of revisions, first/last year, gaps
        data/derived/aw_a1_eras.csv      A1 revisions per era
        data/derived/aw_a2_pairs.csv     A2/A3 every revision whose predecessor carried an uncertainty
        data/derived/aw_a5_intervals.csv A5 elements that moved to an interval
        data/derived/aw_summary.json

Conventions
  * Values before 1961 are on the chemical scale (natural oxygen = 16); from 1961 on the 12C = 12 scale.
    Where a pre-1961 value is compared with a later one it is multiplied by f = 15.9994/16, the 1961
    value of oxygen on the new scale (from the same CSV).
  * CIAAW uncertainties are not standard uncertainties: they are ranges within which normal materials are
    expected to lie "with great certitude". A2 therefore reports the share of revisions outside the previous
    range without any normal-distribution expectation.
  * Rows "no changes" (report years without revisions) are kept only as report years. "n/a" marks a
    withdrawn standard atomic weight.

  python src/aw_metrics.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "ciaaw_IUPAC-TSAW.csv"
DER = ROOT / "data" / "derived"
SCALE_YEAR = 1961
# elements in the CSV that have no standard atomic weight today (CIAAW current table): radioactive, no
# characteristic terrestrial isotopic composition
NO_SAW = {"Tc", "Np", "Rn", "Ra"}
ERAS = [(1902, 1960, "1902-1960"), (1961, 2008, "1961-2008"), (2009, 2024, "2009-2024")]


def parse_value(txt: str):
    t = txt.strip()
    if t == "n/a":
        return dict(kind="withdrawn")
    m = re.fullmatch(r"\[\s*([\d .]+),\s*([\d .]+)\]", t)
    if m:
        lo, hi = (Decimal(x.replace(" ", "")) for x in m.groups())
        return dict(kind="interval", lo=lo, hi=hi, value=(lo + hi) / 2)
    m = re.fullmatch(r"([\d .]+)\(exact\)", t)
    if m:
        return dict(kind="exact", value=Decimal(m.group(1).replace(" ", "")), u=Decimal(0))
    m = re.fullmatch(r"([\d .]+)\((\d+)\)", t)
    if m:
        mant = m.group(1).replace(" ", "")
        d = len(mant.split(".")[1]) if "." in mant else 0
        return dict(kind="unc", value=Decimal(mant), u=Decimal(m.group(2)).scaleb(-d))
    m = re.fullmatch(r"[\d .]+", t)
    if m:
        return dict(kind="none", value=Decimal(t.replace(" ", "")))
    raise ValueError(f"unparsed value {txt!r}")


def load_corrections():
    path = ROOT / "data" / "transcribed" / "aw_corrections.csv"
    with open(path, encoding="utf-8") as fh:
        return {(int(r["year"]), r["symbol"]): r for r in csv.DictReader(fh)}


def load():
    corr = load_corrections()
    rows = list(csv.reader(open(RAW, encoding="utf-8")))[3:]
    recs, report_years = [], set()
    for r in rows:
        if len(r) < 5:
            continue
        year = int(re.search(r"\d{4}", re.sub(r"<[^>]*>", "", r[0])).group())
        report_years.add(year)
        if r[1] == "no changes":
            continue
        vt = r[3]
        c = corr.get((year, r[1]))
        if c:
            assert c["csv_value"] == vt, (year, r[1], vt)
            vt = c["corrected_value"]
        rec = dict(year=year, symbol=r[1], element=r[2], value_text=vt, doi=r[4], corrected=int(bool(c)))
        rec.update(parse_value(vt))
        recs.append(rec)
    recs.sort(key=lambda x: (x["symbol"], x["year"]))
    return recs, sorted(report_years)


def main():
    recs, report_years = load()
    f = next(r for r in recs if r["symbol"] == "O" and r["year"] == SCALE_YEAR)["value"] / 16

    def on_12c(rec, key="value"):
        v = rec.get(key)
        if v is None:
            return None
        return v * f if rec["year"] < SCALE_YEAR else v

    DER.mkdir(parents=True, exist_ok=True)
    with open(DER / "aw_long.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["symbol", "element", "year", "value_text", "kind", "value", "u", "lo", "hi", "scale", "value_12C", "doi"])
        for r in recs:
            v12 = on_12c(r)
            w.writerow([r["symbol"], r["element"], r["year"], r["value_text"], r["kind"], str(r.get("value", "")), str(r.get("u", "")),
                        str(r.get("lo", "")), str(r.get("hi", "")), "O=16" if r["year"] < SCALE_YEAR else "12C=12",
                        "" if v12 is None else f"{v12:.8f}", r["doi"]])

    by = defaultdict(list)
    for r in recs:
        by[r["symbol"]].append(r)

    # A1 / A4 per element
    el_rows = []
    for s, rs in sorted(by.items()):
        ys = [r["year"] for r in rs]
        gaps = [b - a for a, b in zip(ys, ys[1:])]
        last = rs[-1]
        el_rows.append(dict(symbol=s, element=rs[0]["element"], n_revisions=len(rs), first=ys[0], last=ys[-1],
                            mean_gap=f"{sum(gaps) / len(gaps):.1f}" if gaps else "", current=last["value_text"], current_kind=last["kind"],
                            has_standard_atomic_weight=int(s not in NO_SAW and last["kind"] != "withdrawn")))
    with open(DER / "aw_a1_elements.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(el_rows[0].keys()))
        w.writeheader()
        w.writerows(el_rows)
    era_rows = []
    for a, b, lab in ERAS:
        n = sum(1 for r in recs if a <= r["year"] <= b)
        ry = [y for y in report_years if a <= y <= b]
        era_rows.append(dict(era=lab, revisions=n, report_years=len(ry), years=b - a + 1, revisions_per_year=f"{n / (b - a + 1):.2f}"))
    with open(DER / "aw_a1_eras.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(era_rows[0].keys()))
        w.writeheader()
        w.writerows(era_rows)

    # A2 / A3: revisions whose predecessor carried an uncertainty
    pairs = []
    for s, rs in by.items():
        for p, n in zip(rs, rs[1:]):
            if p["kind"] != "unc" or n["kind"] not in ("unc", "none"):
                continue
            pv, nv = on_12c(p), on_12c(n)
            d = nv - pv
            z = d / p["u"]
            nu = n.get("u") or Decimal(0)
            disjoint = (pv + p["u"] < nv - nu) or (nv + nu < pv - p["u"])
            pairs.append(dict(symbol=s, element=p["element"], year_prev=p["year"], prev=p["value_text"], year_new=n["year"], new=n["value_text"],
                              diff=f"{d:.8f}", u_prev=str(p["u"]), z_prev=f"{float(z):.3f}", outside_prev_range=int(abs(d) > p["u"]),
                              ranges_disjoint=int(disjoint),
                              scale_change=int(p["year"] < SCALE_YEAR <= n["year"])))
    pairs.sort(key=lambda x: (x["year_new"], x["symbol"]))
    with open(DER / "aw_a2_pairs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(pairs[0].keys()))
        w.writeheader()
        w.writerows(pairs)

    # A5: transitions to an interval
    iv = []
    for s, rs in by.items():
        for p, n in zip(rs, rs[1:]):
            if n["kind"] == "interval" and p["kind"] in ("unc", "none"):
                pu = p.get("u")
                iv.append(dict(symbol=s, element=p["element"], year_prev=p["year"], prev=p["value_text"], year_interval=n["year"], interval=n["value_text"],
                               interval_width=str(n["hi"] - n["lo"]), prev_range_width=str(2 * pu) if pu else "",
                               width_ratio=f"{float((n['hi'] - n['lo']) / (2 * pu)):.1f}" if pu else "",
                               interval_contains_prev_value=int(n["lo"] <= on_12c(p) <= n["hi"])))
    iv.sort(key=lambda x: (x["year_interval"], x["symbol"]))
    with open(DER / "aw_a5_intervals.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(iv[0].keys()))
        w.writeheader()
        w.writerows(iv)

    saw = [e for e in el_rows if e["has_standard_atomic_weight"]]
    nrev = sorted(e["n_revisions"] for e in saw)
    outside = [p for p in pairs if p["outside_prev_range"]]
    zs = sorted(abs(float(p["z_prev"])) for p in pairs)
    summary = dict(
        rows=len(recs), elements=len(by), elements_with_saw=len(saw), report_years=len(report_years), first=min(report_years), last=max(report_years),
        scale_factor=str(f), revisions_mean=sum(nrev) / len(nrev), revisions_median=nrev[len(nrev) // 2], revisions_max=max(nrev),
        a2_pairs=len(pairs), a2_outside=len(outside), a2_outside_list=[(p["symbol"], p["year_prev"], p["prev"], p["year_new"], p["new"], p["z_prev"]) for p in outside],
        a2_first_prev_year=min(p["year_prev"] for p in pairs),
        a2_disjoint=sum(p["ranges_disjoint"] for p in pairs),
        a2_disjoint_list=[(p["symbol"], p["year_prev"], p["prev"], p["year_new"], p["new"]) for p in pairs if p["ranges_disjoint"]],
        a2_outside_since_1971=[(p["symbol"], p["year_new"]) for p in outside if p["year_new"] >= 1971],
        a3_median_abs_z=zs[len(zs) // 2], a3_share_le_half=sum(1 for z in zs if z <= 0.5) / len(zs),
        a4_unchanged_since_1969=sorted(e["symbol"] for e in saw if e["last"] <= 1969),
        a5_intervals=len(iv), a5_contains_prev=sum(i["interval_contains_prev_value"] for i in iv),
        eras=era_rows,
    )
    (DER / "aw_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    for k, v in summary.items():
        print(k, v)


if __name__ == "__main__":
    main()
