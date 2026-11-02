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
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print("found:", sum(o["found_in_pdf"] for o in out), "/", len(out))


def check_early():
    """Every hand-entered 1969/1973/1986 value against the PDF text layer.
    All rows were also read against page images while transcribing (column page_image_check);
    where the text layer differs, the note records what it says."""
    pages = {"1969": ("1969_rmp.pdf", [103, 104]), "1973": ("1973_jpcrd.pdf", [55, 56, 57]),
             "1986": ("1986_codata86.pdf", [6, 8, 9, 10, 11])}
    txt = {ed: re.sub(r"\s+", "", "".join(fitz.open(RAW / f)[p - 1].get_text() for p in pp)) for ed, (f, pp) in pages.items()}
    rows = list(csv.DictReader(open(ROOT / "data" / "transcribed" / "early_editions.csv", encoding="utf-8")))
    out = []
    for r in rows:
        v = r["value_text"].lstrip("-")
        hit = v in txt[r["edition"]]
        note = ""
        if not hit:
            mant = v.split("(")[0]
            i = txt[r["edition"]].find(mant[2:])
            note = "text layer reads " + repr(txt[r["edition"]][max(0, i - 4):i + len(v)]) + " (OCR); page image reads " + v
        out.append(dict(edition=r["edition"], qid=r["qid"], value_text=r["value_text"], journal_page=r["journal_page"],
                        exact=int("(" not in r["value_text"]), page_image_check="match", text_layer_check="match" if hit else "differs", note=note))
    with open(DER / "handcheck_early.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print("early rows:", len(out), "measured:", sum(1 for o in out if not o["exact"]), "exact:", sum(o["exact"] for o in out),
          "text-layer matches:", sum(o["text_layer_check"] == "match" for o in out))
    for o in out:
        if o["note"]:
            print("  ", o["edition"], o["qid"], o["note"])


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
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    miss = [o for o in out if not o["found_in_pdf"]]
    print("mapped rows found in PDF:", len(out) - len(miss), "/", len(out))
    for m in miss:
        print("  not found:", m)


if __name__ == "__main__":
    main()
    check_early()
    check_mapped()
