# -*- coding: utf-8 -*-
"""Parse CODATA value tables into one long table.

Inputs
  data/raw/{1998..2018}_allascii.txt, data/raw/2022_allascii.txt   NIST ASCII tables
  data/transcribed/early_editions.csv                              hand transcription of
                                                                   1969 (Taylor-Parker-Langenberg),
                                                                   CODATA 1973 and 1986
Output
  data/derived/constants_all_rows.csv   every ASCII row (edition, name, value, u, unit, exact)
  data/derived/constants_long.csv       mapped quantities only (data/manual/quantity_map.csv), all editions

Values are kept as decimal strings (Python Decimal) so that differences of
values agreeing to 12 digits are exact; floats are written for convenience.

  python src/parse_codata.py
"""
from __future__ import annotations

import csv
import re
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DER = ROOT / "data" / "derived"
# hand-maintained map of the 27 quantities; kept outside data/derived so that clearing derived/ cannot lose it
QMAP = ROOT / "data" / "manual" / "quantity_map.csv"
ASCII_EDITIONS = [1998, 2002, 2006, 2010, 2014, 2018, 2022]

PAREN = re.compile(r"^(?P<m>-?[\d .]+?)\s*\((?P<u>[\d.]+)\)\s*(?:e(?P<e>[-+]?\d+))?$")
PLAIN = re.compile(r"^(?P<m>-?[\d .]+?)(?P<dots>\.\.\.)?\s*(?:e(?P<e>[-+]?\d+))?$")


def _decimals(mant: str) -> int:
    return len(mant.split(".")[1]) if "." in mant else 0


def parse_paren(text: str):
    """'6.022 141 99(47) e23' -> (value, u) as Decimal; None if no parentheses."""
    m = PAREN.match(text.strip())
    if not m:
        return None
    mant = m.group("m").replace(" ", "")
    e = int(m.group("e") or 0)
    val = Decimal(mant).scaleb(e)
    u = (Decimal(m.group("u")).scaleb(-_decimals(mant))).scaleb(e)
    return val, u


def parse_plain(text: str):
    """'6.022 141 29 e23' or '12.566 370 614... e-7' -> (value, truncated?)."""
    m = PLAIN.match(text.strip())
    if not m:
        raise ValueError(f"cannot parse value {text!r}")
    mant = m.group("m").replace(" ", "")
    return Decimal(mant).scaleb(int(m.group("e") or 0)), bool(m.group("dots"))


def load_corrections():
    path = ROOT / "data" / "transcribed" / "ascii_corrections.csv"
    with open(path, encoding="utf-8") as fh:
        return {(int(r["edition"]), r["name"]): r["corrected_value_text"] for r in csv.DictReader(fh)}


CORR = None


def read_ascii(year: int):
    global CORR
    if CORR is None:
        CORR = load_corrections()
    lines = (RAW / (f"{year}_allascii.txt")).read_text(encoding="latin-1").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("-----")) + 1
    rows = []
    for ln, line in enumerate(lines[start:], start=start + 1):
        if not line.strip():
            continue
        f = re.split(r"\s{2,}", line.strip())
        name = f[0]
        if (year, name) in CORR:
            f[1] = CORR[(year, name)]
        if year <= 2006:  # 'value(unc) [e..]' then unit
            vtxt = f[1]
            unit = f[2] if len(f) > 2 else ""
            p = parse_paren(vtxt)
            if p:
                val, u, exact, trunc = p[0], p[1], False, False
            else:
                val, trunc = parse_plain(vtxt)
                u, exact = Decimal(0), True
            utxt = ""
        else:  # value | uncertainty or (exact) | unit
            vtxt, utxt = f[1], f[2]
            unit = f[3] if len(f) > 3 else ""
            val, trunc = parse_plain(vtxt)
            if utxt == "(exact)":
                u, exact = Decimal(0), True
            else:
                u, _ = parse_plain(utxt)
                exact = False
        rows.append(dict(edition=year, name=name, value=val, u=u, unit=unit, exact=exact,
                         truncated=trunc, value_text=vtxt, u_text=utxt, source=f"{year}_allascii.txt:{ln}"))
    return rows


def read_early():
    out = []
    with open(ROOT / "data" / "transcribed" / "early_editions.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            p = parse_paren(r["value_text"])
            exact = p is None  # printed without an uncertainty: exact by definition
            val, u = p if p else (Decimal(r["value_text"]), Decimal(0))
            e = int(r["exp10"])
            val, u = val.scaleb(e), u.scaleb(e)
            out.append(dict(edition=int(r["edition"]), qid=r["qid"], name=r["source_label"], value=val, u=u,
                            unit=r["unit"], exact=exact, truncated=False, value_text=r["value_text"] + (f" e{e}" if e else ""),
                            u_text="", source=f"{r['journal_page']} table {r['table']}", note=r["note"]))
    return out


def load_map():
    with open(QMAP, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# quantities stored in the early tables as 1 + anomaly (g/2 or mu/mu_B); subtract 1
ONE_PLUS = {"a_e", "a_mu"}
EARLY_ONE_PLUS = {(1969, "a_e"), (1973, "a_e"), (1973, "a_mu")}


def main():
    DER.mkdir(parents=True, exist_ok=True)
    all_rows = [r for y in ASCII_EDITIONS for r in read_ascii(y)]
    with open(DER / "constants_all_rows.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["edition", "name", "value", "u", "u_rel", "unit", "exact", "truncated", "source"])
        for r in all_rows:
            ur = (r["u"] / abs(r["value"])) if r["value"] and not r["exact"] else Decimal(0)
            w.writerow([r["edition"], r["name"], str(r["value"].normalize()), str(r["u"].normalize()), f"{float(ur):.3e}",
                        r["unit"], int(r["exact"]), int(r["truncated"]), r["source"]])
    print("ASCII rows:", len(all_rows), {y: sum(1 for r in all_rows if r["edition"] == y) for y in ASCII_EDITIONS})

    qmap = load_map()
    by_name = {}
    for r in all_rows:
        by_name[(r["edition"], r["name"])] = r
    long = []
    missing = []
    for q in qmap:
        names = [n.strip() for n in q["ascii_names"].split("|") if n.strip()]
        for y in ASCII_EDITIONS:
            hit = next((by_name[(y, n)] for n in names if (y, n) in by_name), None)
            if hit is None:
                if int(q["first_ascii"] or 9999) <= y:
                    missing.append((q["qid"], y))
                continue
            long.append(dict(qid=q["qid"], **hit))
    for r in read_early():
        if (r["edition"], r["qid"]) in EARLY_ONE_PLUS:
            r["value"] = r["value"] - 1
            r["note"] = (r.get("note") or "") + " (value - 1)"
        long.append(r)
    # exact flags for the early editions: c, mu0 were exact from 1983; nothing early is exact in this list
    long.sort(key=lambda r: (r["qid"], r["edition"]))
    with open(DER / "constants_long.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["qid", "edition", "value", "u", "u_rel", "unit", "exact", "source_name", "source_unit", "value_text", "source"])
        unit_of = {q["qid"]: q["unit"] for q in qmap}
        for r in long:
            ur = (r["u"] / abs(r["value"])) if r["value"] and not r["exact"] else Decimal(0)
            w.writerow([r["qid"], r["edition"], str(r["value"].normalize()), str(r["u"].normalize()), f"{float(ur):.4e}",
                        unit_of[r["qid"]], int(r["exact"]), r["name"], r["unit"], r["value_text"], r["source"]])
    print("long rows:", len(long), "quantities:", len({r['qid'] for r in long}))
    if missing:
        print("MISSING (expected but not found):", missing)


if __name__ == "__main__":
    main()
