# -*- coding: utf-8 -*-
"""Hand-check sample: 10 random rows per ASCII edition (fixed seed), each looked up in
NIST's separately typeset 'all values' PDF of the same edition.

For every sampled row the parsed value and standard uncertainty are re-expressed in the
concise notation 'mantissa(uu)' and searched for in the PDF text (spaces removed). The
script prints both lines so the result can also be read by eye; the outcome is written to
data/derived/handcheck_ascii.csv. The 1969/1973/1986 transcriptions were checked against
page images row by row and against the PDF text layer (see data/derived/handcheck_early.csv).

  python src/handcheck.py
"""
from __future__ import annotations

import csv
import random
import re
from decimal import Decimal
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DER = ROOT / "data" / "derived"
SEED = 2026
EDITIONS = [1998, 2002, 2006, 2010, 2014, 2018, 2022]


def concise(value: str, u: str, value_text: str) -> str:
    """Rebuild 'digits(uu)' from the ASCII value text and the parsed uncertainty."""
    vt = value_text.replace(" ", "").replace("...", "")
    mant = vt.split("e")[0].lstrip("-")
    exp = int(vt.split("e")[1]) if "e" in vt else 0
    d = len(mant.split(".")[1]) if "." in mant else 0
    if Decimal(u) == 0:
        return mant
    digits = (Decimal(u).scaleb(-exp)).scaleb(d)
    return f"{mant}({int(digits.to_integral_value())})"


def main():
    rows = list(csv.DictReader(open(DER / "constants_all_rows.csv", encoding="utf-8")))
    rng = random.Random(SEED)
    out = []
    for y in EDITIONS:
        pdf = fitz.open(RAW / f"{y}_all.pdf")
        txt = re.sub(r"\s+", "", "".join(p.get_text() for p in pdf))
        pool = [r for r in rows if int(r["edition"]) == y]
        # value_text is not in all_rows; re-read it from the ASCII source line
        lines = (RAW / f"{y}_allascii.txt").read_text(encoding="latin-1").splitlines()
        for r in rng.sample(pool, 10):
            ln = int(r["source"].split(":")[1])
            raw_line = lines[ln - 1]
            f = re.split(r"\s{2,}", raw_line.strip())
            vtxt = f[1]
            if "(" in vtxt:  # old concise notation: compare as printed
                key = vtxt.split(" e")[0].replace(" ", "").lstrip("-")
            else:
                key = concise(r["value"], r["u"], vtxt)
            found = key in txt
            out.append(dict(edition=y, name=r["name"], parsed_value=r["value"], parsed_u=r["u"], exact=r["exact"],
                            concise=key, found_in_pdf=int(found), ascii_line=raw_line.strip()))
            print(f"{y} {'OK ' if found else '?? '} {r['name'][:46]:46s} {key:28s} | {raw_line.strip()[60:110]}")
    with open(DER / "handcheck_ascii.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("found:", sum(o["found_in_pdf"] for o in out), "/", len(out))


if __name__ == "__main__":
    main()


def check_mapped():
    """Every mapped (K and D) ASCII row against the edition's 'all values' PDF."""
    long = [r for r in csv.DictReader(open(DER / "constants_long.csv", encoding="utf-8")) if int(r["edition"]) >= 1998]
    cache, out = {}, []
    for r in long:
        y = int(r["edition"])
        if y not in cache:
            cache[y] = re.sub(r"\s+", "", "".join(p.get_text() for p in fitz.open(RAW / f"{y}_all.pdf")))
        vtxt = r["value_text"]
        key = vtxt.split(" e")[0].replace(" ", "").replace("...", "").lstrip("-") if "(" in vtxt else concise(r["value"], r["u"], vtxt)
        out.append(dict(qid=r["qid"], edition=y, concise=key, found_in_pdf=int(key in cache[y])))
    with open(DER / "handcheck_mapped.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    miss = [o for o in out if not o["found_in_pdf"]]
    print("mapped rows found in PDF:", len(out) - len(miss), "/", len(out))
    for m in miss:
        print("  not found:", m)


if __name__ == "__main__":
    check_mapped()
