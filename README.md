# Physical Constants Metrics — 물리 상수 메트릭스

과학자들이 스스로 밝힌 오차 막대는 다음 판의 값을 얼마나 자주 놓쳤을까요. 이 사이트는 CODATA 기본 물리 상수 권고값 아홉 판(1973~2022)과 그 직전의 1969년 조정값을 이어 붙여, 값과 불확도가 판마다 어떻게 바뀌었는지를 지표로 셉니다. 지표마다 정의·공식·분모·한계를 함께 두고, 모든 수치에 표본 수와 95% 구간을 붙였습니다.

- **사이트:** https://bowonkwon.github.io/Physical-Constants-Metrics/ ([한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/))
- **읽기:** 핵심 결과를 글로 읽는 면 — [한국어](https://bowonkwon.github.io/Physical-Constants-Metrics/ko/reading.html) · [English](https://bowonkwon.github.io/Physical-Constants-Metrics/en/reading.html)
- **판:** 1.2.1 (2026. 11. 6.) 표 A2 출판본 대조. 1.2 (2026. 11. 4.) — 허블 상수 장(H0 추정값의 정밀도 반감기·기준값 대비 놀람 지수·t 분포 자유도, 연대기, 방법). 1.1.3 (2026. 11. 4.) 같은 층 면 사이 이동(위치 표시줄·같은 계열 목록·이전/다음). 1.1.2 (2026. 11. 3.) 공개본 점검 반영(표시·표기). 1.1.1(2026. 11. 2.) 영어 면 교정과 계산 코드 정비, 1.1(원자량 장)도 같은 날, 1.0은 2026. 11. 1.
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

## 1.2.1 — 표 A2 출판본 대조 (2026. 11. 6.)

- Faerber & López-Corredoira (2020) 표 A2 는 arXiv 판에서 읽었습니다. 출판본(MDPI 웹판) 표의 164행 전부를 연도·값·오차 표기·참고문헌 번호로 대조해 모두 같음을 확인했습니다. 수치는 바뀌지 않았고, 「출판본 대조 전」이라고 적었던 방법·데이터 면 문장과 CSV 머리말을 고쳤습니다.
- 방법 면의 「Planck 2018·Riess 외 2022 원문의 쪽·표 재확인을 하지 못했다」는 문장을 확인한 쪽(Planck 결과 VI 16쪽 표 2, Riess 외 2022 1쪽·33쪽)으로 바꿨습니다.

## 1.2 — 허블 상수 장 (2026. 11. 4.)

발표된 허블 상수 H0 추정값의 기록에 같은 질문을 던진다. 자료는 둘이다: Huchra 의 H0 목록(1927~2010, 553건)은 재게시 허락 문장이 없어 집계(연도별·10년별 건수와 사분위, 부호별 건수, 지표)만 싣고, Faerber & López-Corredoira (2020) 표 A2(1976~2019, 163건, CC BY 4.0)는 행 단위로 싣는다. 지표는 H1 정밀도 반감기(해별 중앙값 상대 오차의 반감기), H3 기준값 대비 놀람 지수(Planck 2018 67.36 ± 0.54 와 Riess 외 2022 73.04 ± 1.04 를 나란히), H4 t 분포 자유도이고, H2(연속 쌍)는 묶는 방식에 따라 결론이 갈려 내지 않는다. 연대기 면은 두 집성의 값과 오차의 흐름, 10년 단위 방법 부호 분포, 자료에서 확인되는 사건을 한데 둔다. 두 집성 모두 오차의 신뢰 수준을 적지 않아 「수준 미표기」로 다룬다. 기존 장의 수치는 바뀌지 않았다.

## 1.1.3 — 면 사이 이동 (2026. 11. 4.)

- 지표·상수·원자량 지표·원소 면에 위치 표시줄(홈 › 상수 › …), 같은 계열의 다른 면 목록(넓은 화면은 왼쪽, 좁은 화면은 제목 위 접힘 상자), 본문 끝의 이전·다음 링크를 넣었습니다. ←·→ 키로도 넘어갑니다.
- M3 면 한국어 요약의 「20개 중 1개 꼴」을 「22개 중 1개 꼴」로 고쳤습니다(1.1.2 에서 영어만 고쳤던 것).
- 수치는 바뀌지 않았습니다.

## 1.1.2 — 공개본 점검 반영 (2026. 11. 3.)

- 공개된 지표 값은 바뀌지 않았습니다.
- 언어 전환 링크가 상대 언어의 첫 면이 아니라 같은 면으로 갑니다.
- 「이 사이트가 다루는 27개 양」을 31개로 고쳤습니다(대응표 31행: 핵심 17·표시 11·후보 3, M6 의 분모).
- 표와 그림 눈금의 음수 부호를 −로, 툴팁과 M1 표의 지수 표기(5.597e-06)를 ×10ⁿ 꼴로, 한국어 면의 연도 범위를 물결표(1998~2022)로, 영어 면 표의 연도 범위를 줄표로 맞췄습니다.
- 그림의 대체 글을 면의 언어로, 상수 면·원소 면의 다른 언어 부제에 언어 표시를 달았습니다.
- 영어 면: 범례·표 머리글·꼬리표 첫 글자 대문자, 「digits in brackets」→「in parentheses」, 4.55% 를 「22번에 1번」으로 통일, 홑따옴표를 겹따옴표로, 원소 나열의 가운뎃점을 쉼표로, 공식의 분모 괄호, M1 표 머리글(Editions (n)·Span), 「(y)」→「(years)」 등.

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
- **Version:** 1.2.1 (Nov 6, 2026), Table A2 checked against the published version; 1.2 (Nov 4, 2026), Hubble-constant chapter (precision half-life, surprise against a reference and Student-t degrees of freedom of published H0 estimates; chronology; method); 1.1.3 (Nov 4, 2026), navigation between pages of the same level; 1.1.2 (Nov 3, 2026) review of the public site applied (display and notation); 1.1.1 (Nov 2, 2026) English corrections and code fixes and 1.1 (atomic-weights chapter) the same day, 1.0 on Nov 1, 2026
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

**1.2.1: Table A2 checked against the published version.** Table A2 of Faerber & López-Corredoira (2020) was read from the arXiv version; all 164 rows of the table in the published (MDPI web) version were compared for year, value, error as printed and reference number, and all agree. No number changed; the sentences on the method and data pages and the CSV header that said the check was pending are updated. The method page now gives the pages where the two reference values were checked (Planck Results VI, p. 16, Table 2; Riess et al. 2022, pp. 1 and 33) instead of saying the check could not be done.

**1.2: Hubble-constant chapter.** The same question, asked of the record of published Hubble-constant estimates. Two sources: Huchra's H0 list (1927–2010, 553 rows) grants no right to republish and appears only in aggregate (counts and quartiles by year and decade, counts by type code, the metrics); Table A2 of Faerber & López-Corredoira (2020) (1976–2019, 163 rows, CC BY 4.0) is published row by row. The metrics are H1, the precision half-life (of the yearly median relative error), H3, surprise against a reference (Planck 2018, 67.36 ± 0.54, and Riess et al. 2022, 73.04 ± 1.04, side by side) and H4, Student-t degrees of freedom; H2 (consecutive pairs) is not produced because its verdict changes with the grouping. A chronology page joins the values and errors of both compilations, the decade-by-decade mix of method codes and the events traceable in the data. Neither compilation states the confidence level of its errors, so they are treated as unstated. No number of the earlier chapters changed.

**1.1.3: navigation.** Metric, constant, atomic-weight metric and element pages now have a breadcrumb, a list of the other pages in the same series (a sidebar on wide screens, a collapsed box above the title on narrow ones) and previous/next links at the end; the arrow keys move between them. The Korean takeaway on M3 now says once in 22 (1.1.2 fixed only the English). No number changed.

**1.1.2: review of the public site.** No published metric value changed. The language link now opens the same page in the other language instead of its home page. 'The 27 quantities on this site' is corrected to 31 (the map has 31 rows: 17 core, 11 display, 3 candidates; the denominator of M6). Negative numbers in tables and axis labels use the minus sign (−); tooltips and the M1 table use the ×10ⁿ form instead of e-notation; Korean pages write year ranges with a wave dash and English tables with an en dash. Chart alternative text follows the page language, and the other-language subtitle on constant and element pages is marked with its language. English pages: sentence case for legends, headers and tags; 'digits in parentheses'; 4.55% given as 'once in 22' throughout; double quotation marks; commas in element lists; parenthesized denominators in formulas; clearer M1 headers (Editions (n), Span); '(years)' for '(y)'.

**1.1.1: corrections.** No published number changed: rerunning everything from the raw files reproduces every metric CSV of 1.1 byte for byte. The placeholder `{e}` that showed in the note on the elementary-charge page is fixed (both languages). English pages: passages whose meaning differed from the Korean (ten constant-page notes; A2's "cannot be determined from the public material"; a sentence that called a growing uncertainty "barely changed") now match, and singular/plural forms on the element pages ("1 times"), grammar, terms (relative standard uncertainty, Stefan–Boltzmann, Table I) and table-header capitalization are corrected; spelling is now American. Code: eight places where a metric's definition and its code disagreed at rare edge cases are settled. M2 and M3 compare unrounded z with the thresholds; "pairs whose value did not change" are decided from the change in value; the M1 slope boundary of −0.001, the standard error when an uncertainty never changes, the A1 median of an even count, and the A2 conversion of a pre-1961 new range now follow the definitions. For M2's pairing (neighboring measured editions, skipping any in between), the definition was reworded to match the code. Python 3.11 no longer fails on the build script; `requirements.txt` and `.gitattributes` (CSV line endings fixed to LF) are added.

**1.1: atomic-weights chapter.** The same question is asked of the 701 revisions (88 elements) of the standard atomic weights recommended by CIAAW since 1902. CIAAW uncertainties are not standard uncertainties (1σ) but expanded ranges, so 12 of 204 revisions put the new value outside the previous range, and in 2 the two ranges did not overlap at all (bromine 1965, zinc 2007). Atomic-weight values are © IUPAC/CIAAW and may be republished with the full reference, ©, IUPAC or CIAAW and the year shown; translations need prior approval from the relevant IUPAC National Adhering Organization and commercial use an arrangement with the CIAAW Secretariat (see the Data page).

**Data and checks.** 1998–2022 values come from NIST's ASCII tables; 1973, 1986 and the 1969 adjustment from the published tables. Values for 1969, 1973 and 1986 were transcribed by hand from page images and compared with the PDF text layer; every 1998–2022 row used was checked against NIST's separately typeset PDF tables. The check found three rows of the archived 2002 ASCII table, the Boltzmann constant among them, that differ from the published report in the last digit; the published values are used (`data/transcribed/ascii_corrections.csv`). NIST's original files are not included, as NIST states that its Standard Reference Data may not be reproduced without prior permission; their URLs, retrieval dates and SHA-256 hashes are in `data/raw_manifest.json`.

**Reproduction.** `python src/fetch_raw.py` downloads the NIST files into `data/raw/` and checks their hashes; then run `parse_codata.py`, `handcheck.py`, `metrics.py`, `aw_metrics.py` (atomic-weights chapter), `build_site.py` (Python 3.11+; packages in `requirements.txt`).

**License.** Text: [CC BY-NC 4.0](LICENSE.md). Code (`src/`): [PolyForm Noncommercial 1.0.0](LICENSE.md); for commercial use, open an [issue](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). Derived data (`data/`): **CC BY 4.0**; please also cite CODATA/NIST as the source of the values. © 2026 Bowon Kwon.

**Note.** The metric design, code and first drafts were written with the help of Claude (Anthropic) and checked against the sources by the editor. Errors may remain; please report them via [Issues](https://github.com/BowonKwon/Physical-Constants-Metrics/issues). This is a personal project and does not represent the views of any institution the editor belongs to.
