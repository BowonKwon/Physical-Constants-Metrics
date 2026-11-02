# Physical Constants Metrics — 물리 상수 메트릭스

과학자들이 스스로 밝힌 오차 막대는 다음 판의 값을 얼마나 자주 놓쳤을까요. 이 사이트는 CODATA 기본 물리 상수 권고값 아홉 판(1973~2022)과 그 직전의 1969년 조정값을 이어 붙여, 값과 불확도가 판마다 어떻게 바뀌었는지를 지표로 셉니다. 지표마다 정의·공식·분모·한계를 함께 두고, 모든 수치에 표본 수와 95% 구간을 붙였습니다.

- **사이트:** https://bowonkwon.github.io/Physical-Constants-Metrics/ ([한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/))
- **읽기:** 핵심 결과를 글로 읽는 면 — [한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/reading.html) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/reading.html)
- **판:** 1.1.1 (2026. 11. 2.) — 영어 면 교정과 계산 코드 정비. 1.1(원자량 장)과 같은 날, 1.0은 2026. 11. 1.
- **다른 공개 자료:** https://bowonkwon.github.io/

## 무엇이 들어 있나

| 지표 | 내용 |
|---|---|
| M1 상대 불확도 반감기 | 상수별로 상대 불확도가 절반이 되는 데 걸린 햇수(로그 회귀, 95% 구간) |
| M2 판간 이동 초과율 | 연속한 두 판 사이 이동이 두 불확도의 1·2·3배를 넘은 비율과 정규 기대치 |
| M3 2022 판 기준 놓침률 | 옛 판의 ±1σ·±2σ 막대가 2022 판 값을 담지 못한 비율, 사분위 지수·놀람 지수 |
| M4 꼬리 두께 | 판간 이동 z에 맞춘 Student-t 자유도 |
| M5 상수별 수렴 그림 | 판별 값과 오차 막대를 2022 판 기준 편차로 |
| M6 정의값 전환 | 측정값이 정의값이 된 상수(빛의 속력 1983, 2019년 SI 개정)와 그 반대(진공 투자율·몰질량 상수) |

M2~M4의 분모는 서로 정확한 환산 관계가 없도록 고른 핵심 상수 17개입니다(같은 규칙에 맞는 후보 3개를 더한 민감도 결과도 싣습니다). 상수별 면은 표시용 상수 11개와 민감도 후보 3개를 더해 31개입니다. Henrion & Fischhoff(1986)의 보정 지표를 이 자료로 다시 계산한 면이 따로 있습니다.

## 1.1.1 — 교정 (2026. 11. 2.)

- 공개된 수치는 바뀌지 않았습니다. 원자료부터 다시 계산해 지표 CSV 전부가 1.1과 바이트 단위로 같음을 확인했습니다.
- 기본 전하 면의 메모에 자리표시자 `{e}`가 그대로 드러나던 것을 고쳤습니다(한·영).
- 영어 면: 한국어 면과 뜻이 달랐던 곳(상수 면 메모 10개, A2 「공개 자료로는 확인되지 않는다」, 불확도가 늘어난 상수를 「거의 바뀌지 않았다」로 적던 문장 등)을 맞추고, 원소 면의 단수·복수(「1 times」 등), 문법·용어(상대 표준불확도, Stefan–Boltzmann, Table I)와 표 머리글 대소문자를 고쳤습니다. 철자는 미국식으로 통일했습니다.
- 계산 코드: 지표 정의 문장과 코드가 드문 경계에서 어긋나던 8곳을 정리했습니다. M2·M3 의 |z| 기준 비교를 반올림하지 않은 z 로, 「값이 바뀌지 않은 쌍」을 값의 차이로 판정하고, M1 의 기울기 −0.001 경계와 불확도가 변하지 않을 때의 표준오차, A1 의 짝수 개 중앙값, A2 의 1961년 이전 새 범위 환산을 정의대로 고쳤습니다. M2 의 쌍 정의(측정값인 판끼리 이웃, 사이 판은 건너뜀)는 문장을 코드에 맞췄습니다.
- 재현: Python 3.11 에서 빌드 스크립트가 구문 오류를 내던 곳을 고쳤고, `requirements.txt` 와 `.gitattributes`(CSV 줄 끝 LF 고정)를 더했습니다.

## 1.1 — 원자량 장

CIAAW(국제순수·응용화학연맹 동위원소 존재비·원자량 위원회)가 1902년부터 권고한 표준 원자량의 개정 기록 701건(원소 88개)에 같은 질문을 던진다. CIAAW의 불확도는 표준불확도(1σ)가 아니라 확장 범위(정상 물질이 매우 확실하게 들어갈 넓은 범위)여서, 새 값이 직전 범위 밖에 놓인 개정은 204건 중 12건, 두 범위가 아예 겹치지 않은 개정은 2건(1965년 브로민, 2007년 아연)이다. 원자량 값은 © IUPAC/CIAAW이며, 출처 전체·©·IUPAC 또는 CIAAW·연도를 표시하는 조건으로 재게시가 허용된다. 번역 게시는 IUPAC 회원 기구의 사전 승인, 상업 이용은 CIAAW 사무국 문의 대상이다(데이터 면 참조).

## 자료와 검증

- 1998~2022 판은 NIST ASCII 표에서, 1973·1986 판과 1969년 조정값은 원 논문의 표에서 옮겼습니다. 1969·1973·1986 판 값 66개는 쪽 이미지에서 손으로 옮긴 뒤 PDF 문자층과 대조했고, 1998~2022 판의 사용 행 213개는 전부 NIST가 따로 조판한 PDF 표와 대조했습니다.
- 대조에서 2002 판 ASCII 보관본의 볼츠만 상수 등 세 행이 출판된 보고서와 마지막 자리에서 다른 것을 찾아 출판본 값으로 고쳤습니다(`data/transcribed/ascii_corrections.csv`).
- NIST의 원 파일(ASCII 표·PDF)은 이 저장소에 싣지 않습니다. NIST는 표준참조자료의 복제에 사전 허락을 요구한다고 밝힙니다. 원 파일의 주소·내려받은 날짜·SHA-256은 `data/raw_manifest.json`에 있습니다.

## 저장소 구성

```
docs/   사이트(GitHub Pages). docs/data/ 에 파생 CSV
data/   파생 CSV, 손 입력표와 원자료 보정표(data/transcribed/), raw_manifest.json, datapackage.json
src/    fetch_raw.py → parse_codata.py → handcheck.py → metrics.py → build_site.py, 지표 정의(registry.py)
```

재현: `python src/fetch_raw.py`가 NIST 원 파일을 `data/raw/`에 내려받고 해시를 확인합니다. 이어서 위 순서로 돌리고, 원자량 장은 `aw_metrics.py`를 `build_site.py` 앞에 돌리면 `data/`의 CSV와 `docs/`가 다시 만들어집니다(Python 3.11+, `requirements.txt`).

## 이용 허락

- 사이트의 글과 지표 설명에서 엮은이에게 권리가 있는 부분은 [CC BY-NC 4.0](LICENSE.md)으로 공개합니다. 이 요약은 이해를 돕기 위한 것이고, 조건은 라이선스 원문을 따릅니다.
- 코드(`src/`)는 [PolyForm Noncommercial 1.0.0](LICENSE.md)으로 공개합니다. 상업적으로 이용하시려면 [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues)로 연락해 주십시오.
- 파생 데이터(`data/`)는 **CC BY 4.0** 입니다. 값의 출처로 CODATA·NIST를 함께 밝혀 주십시오.
- © 2026 권보원(Bowon Kwon)

## 일러두기

지표 설계·코드·본문 초고는 Claude(Anthropic)의 도움으로 작성했고, 엮은이가 원자료와 대조해 검증했습니다. 그래도 틀린 서술이나 계산이 남아 있을 수 있습니다. 찾으시면 [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues)로 알려 주십시오. 이 저장소는 엮은이가 개인적으로 만든 것이며 엮은이가 속한 기관의 견해와 관계가 없습니다.

---

## English

How often did the error bars that scientists published miss the next edition's value? This site joins the nine editions of the CODATA recommended values of the fundamental physical constants (1973–2022) and the 1969 adjustment that preceded them, and turns the changes in values and uncertainties into metrics. Every metric carries its definition, formula, denominator and caveats; every number carries its sample size and a 95% interval.

- **Site:** https://bowonkwon.github.io/Physical-Constants-Metrics/en/ · **Reading:** [en/reading.html](https://bowonkwon.github.io/Physical-Constants-Metrics/en/reading.html)
- **Version:** 1.1.1 (Nov 2, 2026), English corrections and code fixes; 1.1 (atomic-weights chapter) came out the same day, 1.0 on Nov 1, 2026
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

**1.1.1: corrections.** No published number changed: rerunning everything from the raw files reproduces every metric CSV of 1.1 byte for byte. The placeholder `{e}` that showed in the note on the elementary-charge page is fixed (both languages). English pages: passages whose meaning differed from the Korean (ten constant-page notes; A2's "cannot be determined from the public material"; a sentence that called a growing uncertainty "barely changed") now match, and singular/plural forms on the element pages ("1 times"), grammar, terms (relative standard uncertainty, Stefan–Boltzmann, Table I) and table-header capitalization are corrected; spelling is now American. Code: eight places where a metric's definition and its code disagreed at rare edge cases are settled. M2 and M3 compare unrounded z with the thresholds; "pairs whose value did not change" are decided from the change in value; the M1 slope boundary of −0.001, the standard error when an uncertainty never changes, the A1 median of an even count, and the A2 conversion of a pre-1961 new range now follow the definitions. For M2's pairing (neighboring measured editions, skipping any in between), the definition was reworded to match the code. Python 3.11 no longer fails on the build script; `requirements.txt` and `.gitattributes` (CSV line endings fixed to LF) are added.

**1.1: atomic-weights chapter.** The same question is asked of the 701 revisions (88 elements) of the standard atomic weights recommended by CIAAW since 1902. CIAAW uncertainties are not standard uncertainties (1σ) but expanded ranges, so 12 of 204 revisions put the new value outside the previous range, and in 2 the two ranges did not overlap at all (bromine 1965, zinc 2007). Atomic-weight values are © IUPAC/CIAAW and may be republished with the full reference, ©, IUPAC or CIAAW and the year shown; translations need prior approval from the relevant IUPAC National Adhering Organization and commercial use an arrangement with the CIAAW Secretariat (see the Data page).

**Data and checks.** 1998–2022 values come from NIST's ASCII tables; 1973, 1986 and the 1969 adjustment from the published tables. Values for 1969, 1973 and 1986 were transcribed by hand from page images and compared with the PDF text layer; every 1998–2022 row used was checked against NIST's separately typeset PDF tables. The check found three rows of the archived 2002 ASCII table, the Boltzmann constant among them, that differ from the published report in the last digit; the published values are used (`data/transcribed/ascii_corrections.csv`). NIST's original files are not included, as NIST states that its Standard Reference Data may not be reproduced without prior permission; their URLs, retrieval dates and SHA-256 hashes are in `data/raw_manifest.json`.

**Reproduction.** `python src/fetch_raw.py` downloads the NIST files into `data/raw/` and checks their hashes; then run `parse_codata.py`, `handcheck.py`, `metrics.py`, `aw_metrics.py` (atomic-weights chapter), `build_site.py` (Python 3.11+; packages in `requirements.txt`).

**License.** Text: [CC BY-NC 4.0](LICENSE.md). Code (`src/`): [PolyForm Noncommercial 1.0.0](LICENSE.md); for commercial use, open an [issue](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). Derived data (`data/`): **CC BY 4.0**; please also cite CODATA/NIST as the source of the values. © 2026 Bowon Kwon.

**Note.** The metric design, code and first drafts were written with the help of Claude (Anthropic) and checked against the sources by the editor. Errors may remain; please report them via [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). This is a personal project and does not represent the views of any institution the editor belongs to.
