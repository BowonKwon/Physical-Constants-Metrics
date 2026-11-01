# Physical Constants Metrics — 물리 상수 메트릭스

과학자들이 스스로 밝힌 오차 막대는 다음 판의 값을 얼마나 자주 놓쳤을까요. 이 사이트는 CODATA 기본 물리 상수 권고값 아홉 판(1973~2022)과 그 직전의 1969년 조정값을 이어 붙여, 값과 불확도가 판마다 어떻게 바뀌었는지를 지표로 셉니다. 지표마다 정의·공식·분모·한계를 함께 두고, 모든 수치에 표본 수와 95% 구간을 붙였습니다.

- **사이트:** https://bowonkwon.github.io/Physical-Constants-Metrics/ ([한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/))
- **읽기:** 핵심 결과를 글로 읽는 면 — [한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/reading.html) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/reading.html)
- **판:** 1.0 (2026. 11. 1.)
- **다른 공개 자료:** https://bowonkwon.github.io/

## 무엇이 들어 있나

| 지표 | 내용 |
|---|---|
| M1 상대 불확도 반감기 | 상수별로 상대 불확도가 절반이 되는 데 걸린 햇수(로그 회귀, 95% 구간) |
| M2 판간 이동 초과율 | 연속한 두 판 사이 이동이 두 불확도의 1·2·3배를 넘은 비율과 정규 기대치 |
| M3 2022 판 기준 놓침률 | 옛 판의 ±1σ·±2σ 막대가 2022 판 값을 담지 못한 비율, 사분위 지수·놀람 지수 |
| M4 꼬리 두께 | 판간 이동 z 에 맞춘 Student-t 자유도 |
| M5 상수별 수렴 그림 | 판별 값과 오차 막대를 2022 판 기준 편차로 |
| M6 정의값 전환 | 측정값이 정의값이 된 상수(빛의 속력 1983, 2019년 SI 개정)와 그 반대(진공 투자율·몰질량 상수) |

M2~M4 의 분모는 서로 정확한 환산 관계가 없도록 고른 핵심 상수 17개입니다(같은 규칙에 맞는 후보 3개를 더한 민감도 결과도 싣습니다). 상수별 면은 표시용 상수 11개와 민감도 후보 3개를 더해 31개입니다. Henrion & Fischhoff(1986)의 보정 지표를 이 자료로 다시 계산한 면이 따로 있습니다.

## 자료와 검증

- 1998~2022 판은 NIST ASCII 표에서, 1973·1986 판과 1969년 조정값은 원 논문의 표에서 옮겼습니다. 1969·1973·1986 판 값 66개는 쪽 이미지에서 손으로 옮긴 뒤 PDF 문자층과 대조했고, 1998~2022 판의 사용 행 213개는 전부 NIST 가 따로 조판한 PDF 표와 대조했습니다.
- 대조에서 2002 판 ASCII 보관본의 볼츠만 상수 등 세 행이 출판된 보고서와 마지막 자리에서 다른 것을 찾아 출판본 값으로 고쳤습니다(`data/transcribed/ascii_corrections.csv`).
- NIST 의 원 파일(ASCII 표·PDF)은 이 저장소에 싣지 않습니다. NIST 는 표준참조자료의 복제에 사전 허락을 요구한다고 밝힙니다. 원 파일의 주소·내려받은 날짜·SHA-256 은 `data/raw_manifest.json` 에 있습니다.

## 저장소 구성

```
docs/   사이트(GitHub Pages). docs/data/ 에 파생 CSV
data/   파생 CSV, 손 입력표와 원자료 보정표(data/transcribed/), raw_manifest.json, datapackage.json
src/    fetch_raw.py → parse_codata.py → handcheck.py → metrics.py → build_site.py, 지표 정의(registry.py)
```

재현: `python src/fetch_raw.py` 가 NIST 원 파일을 `data/raw/` 에 내려받고 해시를 확인합니다. 이어서 위 순서로 돌리면 `data/` 의 CSV 와 `docs/` 가 다시 만들어집니다(Python 3.11+, numpy, scipy, PyMuPDF).

## 이용 허락

- 사이트의 글과 지표 설명에서 엮은이에게 권리가 있는 부분은 [CC BY-NC 4.0](LICENSE.md)으로 공개합니다. 이 요약은 이해를 돕기 위한 것이고, 조건은 라이선스 원문을 따릅니다.
- 코드(`src/`)는 [PolyForm Noncommercial 1.0.0](LICENSE.md)으로 공개합니다. 상업적으로 이용하시려면 [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues)로 연락해 주십시오.
- 파생 데이터(`data/`)는 **CC BY 4.0** 입니다. 값의 출처로 CODATA·NIST 를 함께 밝혀 주십시오.
- © 2026 권보원(Bowon Kwon)

## 일러두기

지표 설계·코드·본문 초고는 Claude(Anthropic)의 도움으로 작성했고, 엮은이가 원자료와 대조해 검증했습니다. 그래도 틀린 서술이나 계산이 남아 있을 수 있습니다. 찾으시면 [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues)로 알려 주십시오. 이 저장소는 엮은이가 개인적으로 만든 것이며 엮은이가 속한 기관의 견해와 관계가 없습니다.

---

## English

How often did the error bars that scientists published miss the next edition's value? This site joins the nine editions of the CODATA recommended values of the fundamental physical constants (1973–2022) and the 1969 adjustment that preceded them, and turns the changes in values and uncertainties into metrics. Every metric carries its definition, formula, denominator and caveats; every number carries its sample size and a 95% interval.

- **Site:** https://bowonkwon.github.io/Physical-Constants-Metrics/en/ · **Reading:** [en/reading.html](https://bowonkwon.github.io/Physical-Constants-Metrics/en/reading.html)
- **Version:** 1.0 (Nov 1, 2026)
- **Other public materials:** https://bowonkwon.github.io/en/

| Metric | Contents |
|---|---|
| M1 Relative-uncertainty half-life | Years for each constant's relative uncertainty to halve (log regression, 95% interval) |
| M2 Edition-to-edition exceedance | Share of moves between consecutive editions beyond 1, 2, 3 times the combined uncertainty, against the normal expectation |
| M3 Miss rate against 2022 | Share of earlier ±1σ and ±2σ error bars that do not contain the 2022 value; interquartile and surprise indices |
| M4 Tail heaviness | Student-t degrees of freedom fitted to edition-to-edition z |
| M5 Convergence plot by constant | Each edition's value and error bar as a deviation from 2022 |
| M6 Exact-value transitions | Constants that became exact (speed of light 1983; the 2019 SI revision) and the reverse (vacuum magnetic permeability, molar mass constant) |

The denominator of M2–M4 is 17 core constants, chosen so that none is an exact function of the others (a sensitivity check adds three candidates meeting the same rule); the constant pages add 11 display constants and the 3 candidates (31 in all). A separate page recomputes Henrion & Fischhoff's (1986) calibration indices on these data.

**Data and checks.** 1998–2022 values come from NIST's ASCII tables; 1973, 1986 and the 1969 adjustment from the published tables. Values for 1969, 1973 and 1986 were transcribed by hand from page images and compared with the PDF text layer; every 1998–2022 row used was checked against NIST's separately typeset PDF tables. The check found three rows of the archived 2002 ASCII table, the Boltzmann constant among them, that differ from the published report in the last digit; the published values are used (`data/transcribed/ascii_corrections.csv`). NIST's original files are not included, as NIST states that its Standard Reference Data may not be reproduced without prior permission; their URLs, retrieval dates and SHA-256 hashes are in `data/raw_manifest.json`.

**Reproduction.** `python src/fetch_raw.py` downloads the NIST files into `data/raw/` and checks their hashes; then run `parse_codata.py`, `handcheck.py`, `metrics.py`, `build_site.py` (Python 3.11+, numpy, scipy, PyMuPDF).

**License.** Text: [CC BY-NC 4.0](LICENSE.md). Code (`src/`): [PolyForm Noncommercial 1.0.0](LICENSE.md); for commercial use, open an [issue](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). Derived data (`data/`): **CC BY 4.0**; please also cite CODATA/NIST as the source of the values. © 2026 Bowon Kwon.

**Note.** The metric design, code and first drafts were written with the help of Claude (Anthropic) and checked against the sources by the editor. Errors may remain; please report them via [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). This is a personal project and does not represent the views of any institution the editor belongs to.
