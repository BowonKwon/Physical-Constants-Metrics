# -*- coding: utf-8 -*-
"""Download the CODATA source files into data/raw/ and write data/raw/manifest.json
(url, retrieval date, size, SHA-256). The raw files are NOT redistributed; the
public repository carries only the manifest.

  python src/fetch_raw.py
"""
import datetime
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
BASE = "https://physics.nist.gov/cuu/"
FILES = {
    # edition: (file name, url)
    "1969_rmp.pdf": BASE + "pdf/1969RMP.pdf",
    "1973_jpcrd.pdf": BASE + "pdf/1973JPCRD.pdf",
    "1986_codata86.pdf": BASE + "pdf/codata86.pdf",
    "1986_rmp.pdf": BASE + "pdf/1986RMP.pdf",
    "2002_rmp.pdf": BASE + "pdf/CODATA_RMP2005.pdf",
    "2022_jpcrd.pdf": BASE + "pdf/JPCRD2022CODATA.pdf",
    "2022_allascii.txt": BASE + "Constants/Table/allascii.txt",
}
for y in (1998, 2002, 2006, 2010, 2014, 2018):
    FILES[f"{y}_allascii.txt"] = BASE + f"Constants/ArchiveASCII/allascii_{y}.txt"
    FILES[f"{y}_corrcoef.txt"] = BASE + f"Constants/ArchiveASCII/corrcoef{y}"
# NIST "all values" PDF tables: an independent rendering used only for the hand check
for y in (1998, 2002, 2006, 2010, 2014, 2018):
    FILES[f"{y}_all.pdf"] = BASE + f"pdf/all_{y}.pdf"
FILES["2022_all.pdf"] = BASE + "pdf/all.pdf"
for y in (1969, 1973, 1986, 1998, 2002, 2006, 2010, 2014, 2018):
    FILES[f"{y}_archive.html"] = BASE + f"Constants/archive{y}.html"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    man_path = RAW / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {}
    for name, url in FILES.items():
        dst = RAW / name
        if not dst.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "constants-metrics-fetch/1.0"})
            dst.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            time.sleep(1)
            man[name] = {"url": url, "retrieved": datetime.date.today().isoformat()}
        b = dst.read_bytes()
        man.setdefault(name, {"url": url, "retrieved": datetime.date.today().isoformat()})
        h = hashlib.sha256(b).hexdigest()
        if man[name].get("sha256") and man[name]["sha256"] != h:
            print(f"  WARNING: {name} differs from the recorded SHA-256 (source changed or corrupted)")
        man[name].update(bytes=len(b), sha256=h)
        print(f"{name:24s} {len(b):>10,d}")
    man_path.write_text(json.dumps(man, indent=1, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
