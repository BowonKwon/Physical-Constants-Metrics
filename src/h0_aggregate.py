# -*- coding: utf-8 -*-
"""1.2 Hubble chapter, site stage: publishable AGGREGATES of Huchra's list (hubble.plot.dat) for the site's
figures. The list may be shown only in aggregate (its file grants no right to republish; design note section 4,
grade A; decision D8: no chart that plots individual estimates). Nothing here writes a row value.

  python src/h0_aggregate.py  -> data/h0_huchra_yearly.csv    per publication year: count, quartiles of H0 and of
                                                                the relative error u/|x| (rows with an error, 1929 on)
                                 data/h0_huchra_decades.csv   per decade: count and quartiles of H0
                                 data/h0_huchra_types.csv     per decade and type code: count (primary and secondary codes)
                                 data/h0_huchra_codes.csv     per type code: count, first and last year

Choices (the same as src/h0_stage1b.py): rows with an error, error level 'unstated', asymmetric errors as the
mean (D2), start year 1929 (D6; the 1927 and 1928 rows are left out and described in the method page), type
codes as printed (D7). Quartiles: numpy.percentile with linear interpolation, H0 rounded to one decimal, the
relative error to four. A year or decade with fewer than MIN_N rows keeps its count but no quartile, so that no
group is a single estimate or a pair in disguise (the median of a group of one or two is a printed value).
The 1940s have no row in the list, so that decade is absent from the tables.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h0_huchra  # noqa: E402
import h0_metrics  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_YEARLY = DATA / "h0_huchra_yearly.csv"
OUT_DECADES = DATA / "h0_huchra_decades.csv"
OUT_TYPES = DATA / "h0_huchra_types.csv"
OUT_CODES = DATA / "h0_huchra_codes.csv"

START = 1929
MIN_N = 3
RULE = "mean"
LEVELS = frozenset({"unstated"})


def quartiles(values, digits):
    """(q1, median, q3) of a list of numbers as strings with `digits` decimals; linear interpolation."""
    q1, med, q3 = np.percentile(np.array([float(v) for v in values]), [25, 50, 75])
    return tuple(f"{x:.{digits}f}" for x in (q1, med, q3))


def _cell(values, digits, n):
    return quartiles(values, digits) if n >= MIN_N else ("", "", "")


def compute(records, start=START, min_n=MIN_N):
    """Aggregates of the given h0_huchra records (rows with an error, year >= start). Returns a dict of row lists:
    yearly, decades, types, codes. Groups smaller than min_n keep their count only."""
    kept, _ = h0_metrics.usable(records, levels=LEVELS)
    ms = [m for m in kept if m["year"] >= start]
    yearly, decades, types, codes = [], [], [], []
    by_year, by_dec = {}, {}
    for m in ms:
        by_year.setdefault(m["year"], []).append(m)
        by_dec.setdefault(m["year"] // 10 * 10, []).append(m)
    for y in sorted(by_year):
        g = by_year[y]
        n = len(g)
        h = [m["h0"] for m in g]
        u = [h0_metrics.u_of(m, RULE) / abs(m["h0"]) for m in g]
        hq = quartiles(h, 1) if n >= min_n else ("", "", "")
        uq = quartiles(u, 4) if n >= min_n else ("", "", "")
        yearly.append(dict(year=y, n=n, h0_q1=hq[0], h0_median=hq[1], h0_q3=hq[2],
                           urel_q1=uq[0], urel_median=uq[1], urel_q3=uq[2]))
    for d in sorted(by_dec):
        g = by_dec[d]
        n = len(g)
        hq = quartiles([m["h0"] for m in g], 1) if n >= min_n else ("", "", "")
        decades.append(dict(decade=d, n=n, h0_q1=hq[0], h0_median=hq[1], h0_q3=hq[2]))
        prim = Counter(m["huchra_primary"] for m in g)
        sec = Counter(m["huchra_type"][1:2] for m in g if len(m["huchra_type"]) > 1)
        for code, k in sorted(prim.items()):
            types.append(dict(decade=d, kind="primary", code=code, n=k))
        for code, k in sorted(sec.items()):
            types.append(dict(decade=d, kind="secondary", code=code, n=k))
    for kind, key in (("primary", lambda m: m["huchra_primary"]), ("secondary", lambda m: m["huchra_type"][1:2])):
        by_code = {}
        for m in ms:
            c = key(m)
            if c:
                by_code.setdefault(c, []).append(m["year"])
        for code in sorted(by_code):
            ys = by_code[code]
            codes.append(dict(kind=kind, code=code, n=len(ys), first_year=min(ys), last_year=max(ys)))
    return dict(yearly=yearly, decades=decades, types=types, codes=codes)


def write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    res = h0_huchra.parse(err_level="unstated")
    out = compute(res["records"])
    write(OUT_YEARLY, out["yearly"], ["year", "n", "h0_q1", "h0_median", "h0_q3", "urel_q1", "urel_median", "urel_q3"])
    write(OUT_DECADES, out["decades"], ["decade", "n", "h0_q1", "h0_median", "h0_q3"])
    write(OUT_TYPES, out["types"], ["decade", "kind", "code", "n"])
    write(OUT_CODES, out["codes"], ["kind", "code", "n", "first_year", "last_year"])
    print(f"wrote {OUT_YEARLY.name} ({len(out['yearly'])} years), {OUT_DECADES.name} ({len(out['decades'])} decades), "
          f"{OUT_TYPES.name} ({len(out['types'])} rows), {OUT_CODES.name} ({len(out['codes'])} codes); "
          f"rows used {sum(r['n'] for r in out['yearly'])}")


if __name__ == "__main__":
    main()
