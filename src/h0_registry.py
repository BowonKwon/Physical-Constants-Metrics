# -*- coding: utf-8 -*-
"""Registry for the Hubble-constant chapter (1.2). Same fields as registry.METRICS and aw_registry.AW_METRICS.
Numbers in braces are filled in by h0_site.py from data/h0_*.csv (stage 1b results and the Huchra aggregates).
Every sentence describes observed records; none states a cause."""

H0_SOURCES = {
    "huchra": dict(
        key="huchra", short_ko="Huchra 목록", short_en="Huchra's list",
        ko="J. Huchra, 「Estimates of the Hubble Constant」(hubble.plot.dat, 2010-10-07 최종판). NASA/HST Key Project 의 일부로 작성된, 1927~2010년의 발표 H0 추정값 553건(오차가 적힌 행 550건)의 목록. 파일에는 저작권 표시와 「쓰거나 파생물을 만들면 저자와 Key Project 를 인용해 달라」는 요청만 있고 재게시를 허락하는 문장은 없다. 그래서 이 사이트는 집계만 싣는다 — 행 단위 값, 개별 추정을 점으로 찍은 그림, 행 단위 CSV 는 싣지 않는다.",
        en="J. Huchra, \"Estimates of the Hubble Constant\" (hubble.plot.dat, final update 2010-10-07): a list of 553 published H0 estimates from 1927 to 2010 (550 with an error), assembled as part of the NASA/HST Key Project. The file carries a copyright line and a request to \"reference the author and the Key Project\" and grants no right to republish. This site therefore shows aggregates only: no row values, no chart that plots individual estimates, no row-level CSV.",
        url="https://www.cfa.harvard.edu/~huchra/hubble.plot.dat",
        credit="J. Huchra, Estimates of the Hubble Constant (hubble.plot.dat, last updated 2010-10-07), Harvard-Smithsonian Center for Astrophysics; assembled as part of the NASA/HST Key Project on the Extragalactic Distance Scale. Aggregates only.",
    ),
    "faerber": dict(
        key="faerber", short_ko="표 A2", short_en="Table A2",
        ko="T. Faerber, M. López-Corredoira, 「A Chi-Squared Analysis of the Measurements of Two Cosmological Parameters over Time」, Universe 6, 114 (2020), 부록 표 A2 — 1976~2019년의 H0 163건. CC BY 4.0. 행 단위로 싣는다. 1990~2010년의 120건은 모두 Croft & Dailey 의 집성에서 왔다고 논문이 밝히며 표에는 그 원 논문이 적혀 있지 않다. 표는 arXiv 판(2008.04035v1)에서 읽었고 출판본과는 아직 대조하지 못했다.",
        en="T. Faerber and M. López-Corredoira, \"A Chi-Squared Analysis of the Measurements of Two Cosmological Parameters over Time\", Universe 6, 114 (2020), Appendix Table A2: 163 H0 values from 1976 to 2019. CC BY 4.0; published here row by row. The paper states that all 120 values of 1990–2010 come from the compilation of Croft and Dailey, whose original papers the table does not name. The table was read from the arXiv preprint (2008.04035v1) and has not yet been checked against the published version.",
        url="https://doi.org/10.3390/universe6080114",
        credit="Faerber, T.; López-Corredoira, M. A Chi-Squared Analysis of the Measurements of Two Cosmological Parameters over Time. Universe 2020, 6, 114, doi:10.3390/universe6080114, Appendix Table A2 (read from arXiv:2008.04035v1). CC BY 4.0.",
    ),
}

# Reference values of H3 (owner decision D5). Pages and tables as recorded in stage 1 (notes/1.2-hubble-sources.md, section 8).
REFS = {
    "planck18": dict(value="67.36", u="0.54", ko="Planck 2018", en="Planck 2018",
                     cite_ko="Planck Collaboration, Planck 2018 results. VI (arXiv:1807.06209), 표 2의 TT,TE,EE+lowE+lensing 열, 68% 한계. ΛCDM 가정 위의 값.",
                     cite_en="Planck Collaboration, Planck 2018 results. VI (arXiv:1807.06209), Table 2, column TT,TE,EE+lowE+lensing, 68% limits. A value within the ΛCDM model."),
    "riess22": dict(value="73.04", u="1.04", ko="Riess 외 2022", en="Riess et al. 2022",
                    cite_ko="A. G. Riess 외 2022 (SH0ES, arXiv:2112.04510), 초록의 기본 결과(계통 오차 포함).",
                    cite_en="A. G. Riess et al. 2022 (SH0ES, arXiv:2112.04510), baseline result of the abstract (with systematics)."),
}

# Huchra's type codes as printed in the file's legend (decision D7: no new classification). Meaning = the legend's text.
TYPE_PRIMARY = {"S": "SnI", "2": "SnII", "G": "GCLF", "L": "Lens", "r": "Red Giants", "B": "BTF", "R": "ITF, RTF", "H": "IRTF",
                "F": "Fluctuations", "D": "Dn-Sig/Fund Plane", "A": "Global Summary", "Z": "Sunyaev-Zeldovich", "T": "TF",
                "O": "Other", "N": "Novae", "P": "PNLF", "C": "CMB Fit"}
TYPE_SECONDARY = {"C": "Cosmology dependent", "M": "Theory with assumed Omega", "K": "Key Project or Key Project team member",
                  "S": "Sandage and/or Tammann", "V": "deVaucouleurs or van den Bergh", "I": "results presented at Irvine conf"}
UNVERIFIED = ("I", "M", "T")   # codes printed in rows but absent from the legend (primary I, M; secondary T)

H0_METRICS = [
    dict(id="h1", file="h0_h1_halflife.csv",
         ko=dict(name="정밀도 반감기", short="발표된 H0 추정값의 상대 오차가 절반이 되는 데 걸린 햇수",
                 definition="해마다 그해 발표된 추정값들의 상대 오차(u/|x|, u 는 인용된 오차)의 중앙값을 취해, 그 log₂ 를 출판 연도에 회귀한다(본값). 해마다 가장 작은 상대 오차만 쓰는 「정밀도 최전선」을 참고로 나란히 둔다. 두 집성을 각각 따로 계산한다.",
                 formula="반감기 = −1 / b,  b = log₂(해별 중앙값 u/|x|) 를 연도에 회귀한 기울기.  95% 구간은 기울기의 t(n−2) 구간. 위·아래 오차가 다른 행은 평균을 쓴다.",
                 denominator="Huchra 목록: 1929~2010년의 오차 있는 행 {h1_hu_rows}건, 해 {h1_hu_years}개(1950년부터는 {h1_hu50_rows}건, {h1_hu50_years}개). 표 A2: 1976~2019년 {h1_fa_rows}건, 해 {h1_fa_years}개. 1927·1928년 행 2개는 뺀다.",
                 reading="Huchra 목록의 해별 중앙값 반감기는 {h1_hu_med}년(95% 구간 {h1_hu_med_ci})이고, 1950년부터로 끊으면 {h1_hu50_med}년({h1_hu50_med_ci})이다. 표 A2 는 {h1_fa_med}년({h1_fa_med_ci}). 정밀도 최전선은 각각 {h1_hu_fr}년·{h1_hu50_fr}년·{h1_fa_fr}년으로, 어느 계열에서도 최전선이 중앙값보다 짧다. 물리 상수 장 M1 의 핵심 상수 중앙값은 {m1_median}년이다.",
                 caveat="한 해에 추정이 여럿이라 해별 요약에 기대며, 초기에는 점이 하나뿐인 해가 많다({h1_hu_small}개 해가 3건 미만). 두 집성 모두 오차가 몇 σ 인지 적지 않아 행마다 뜻이 다를 수 있다. 두 집성은 기간과 수록 범위가 달라 두 반감기를 직접 견주지 않는다. 최전선은 「가장 작게 인용된 오차」라 과소평가된 오차가 그대로 반감기를 짧게 만든다."),
         en=dict(name="Precision half-life", short="Years for the relative error of published H0 estimates to halve",
                 definition="For each year, the median of the relative error (u/|x|, u the quoted error) over that year's estimates; its log₂ is regressed on publication year (main value). The \"precision frontier\", the smallest relative error of each year, is shown as a reference. The two compilations are computed separately.",
                 formula="Half-life = −1 / b,  b = slope of log₂(yearly median u/|x|) on year.  95% interval: t(n−2) interval of the slope. Asymmetric errors enter as the mean of the two.",
                 denominator="Huchra's list: {h1_hu_rows} rows with an error from 1929 to 2010 over {h1_hu_years} years ({h1_hu50_rows} rows, {h1_hu50_years} years from 1950). Table A2: {h1_fa_rows} rows from 1976 to 2019 over {h1_fa_years} years. The two rows of 1927 and 1928 are left out.",
                 reading="The yearly-median half-life of Huchra's list is {h1_hu_med} years (95% interval {h1_hu_med_ci}), or {h1_hu50_med} years ({h1_hu50_med_ci}) from 1950. Table A2 gives {h1_fa_med} years ({h1_fa_med_ci}). The precision frontier is shorter in every series: {h1_hu_fr}, {h1_hu50_fr} and {h1_fa_fr} years. The median over the core constants of the physical-constants chapter (M1) is {m1_median} years.",
                 caveat="Several estimates share a year, so the metric rests on a yearly summary, and many early years have a single point ({h1_hu_small} years have fewer than three rows). Neither compilation states the confidence level of its errors, so their meaning may differ from row to row. The two compilations differ in span and coverage, so their half-lives are not compared directly. The frontier is the smallest quoted error of the year, so an underestimated error shortens it as it stands."),
         takeaway=dict(ko=["Huchra 목록(1929~2010)에서 해별 중앙값 상대 오차는 {h1_hu_med}년마다 절반이 되었다(95% 구간 {h1_hu_med_ci}). 1950년부터로 끊으면 {h1_hu50_med}년이다.",
                           "표 A2(1976~2019)는 {h1_fa_med}년({h1_fa_med_ci})이다. 해마다 가장 작은 오차만 보는 정밀도 최전선은 어느 계열에서나 더 짧다."],
                       en=["In Huchra's list (1929–2010) the yearly median relative error halved every {h1_hu_med} years (95% interval {h1_hu_med_ci}); from 1950 on, every {h1_hu50_med} years.",
                           "Table A2 (1976–2019) gives {h1_fa_med} years ({h1_fa_med_ci}). The precision frontier, the smallest error of each year, is shorter in every series."])),
    dict(id="h2", file="",
         ko=dict(name="내지 않음", short="연속 측정 쌍의 |z| 초과 비율은 묶는 방식에 따라 결론이 갈려 내지 않는다"),
         en=dict(name="Not produced", short="The exceedance rate of consecutive pairs changes its verdict with the grouping, so it is not published")),
    dict(id="h3", file="h0_h3_summary.csv",
         ko=dict(name="기준값 대비 놀람 지수", short="각 추정값과 기준값의 차이를 그 추정값의 오차로 나눈 z 의 분포 — Planck 2018 과 Riess 외 2022 를 나란히",
                 definition="추정값마다 z = (기준값 − x)/u_x 를 구하고 |z| > 1, |z| > 2 인 비율(놓침), |z| < 0.674 인 비율(사분위 지수), |z| > 2.326 인 비율(놀람 지수)을 센다. 기준값은 하나로 정하지 않고 Planck 2018(67.36 ± 0.54)과 Riess 외 2022(73.04 ± 1.04)를 나란히 둔다. 정규분포라면 기대값은 차례로 31.7%, 4.6%, 50%, 2% 다.",
                 formula="z = (기준값 − x) / u_x.  기준값의 불확도는 z 에 들어가지 않는다. 위·아래 오차가 다른 행은 평균.",
                 denominator="Huchra 목록 1929~2010년 {h3_hu_n}건(1950년부터 {h3_hu50_n}건). 표 A2 1976~2019년 {h3_fa_n_r}건 — Planck 기준에서는 {h3_fa_n_p}건으로, 표의 2018년 행 「67.4 ± 0.5」(Planck 2018 의 반올림 값) 1개를 뺐다. 95% 구간은 출판 연도를 군집으로 한 부트스트랩 10,000회(시드 2026).",
                 reading="Planck 2018 기준으로 Huchra 목록의 ±1σ 놓침은 {h3_hu_p_m1}%(정규 기대 31.7%), ±2σ 놓침 {h3_hu_p_m2}%(4.6%), 놀람 지수 {h3_hu_p_si}%(2%), 사분위 지수 {h3_hu_p_iq}%(50%)다. Riess 외 2022 기준으로는 {h3_hu_r_m1}%·{h3_hu_r_m2}%·{h3_hu_r_si}%·{h3_hu_r_iq}%. 표 A2 는 Planck 기준 {h3_fa_p_m1}%·{h3_fa_p_m2}%·{h3_fa_p_si}%·{h3_fa_p_iq}%, Riess 기준 {h3_fa_r_m1}%·{h3_fa_r_m2}%·{h3_fa_r_si}%·{h3_fa_r_iq}%. 모든 칸에서 놓침·놀람 비율의 구간은 정규 기대값보다 위에, 사분위 지수는 아래에 있다. 물리 상수 장 M3 의 ±2σ 놓침은 {m3_m2}% 다.",
                 caveat="어느 쪽이 「놀람」이 되는지는 기준값에 달려 있다 — 두 기준을 나란히 두는 까닭이다. 이 수치는 인용된 오차가 기준값과의 차이를 담았는가를 셀 뿐, 두 기준 중 어느 쪽이 맞는지, 긴장이 실재하는지는 말하지 않는다. 기준값도 측정이며 참값이 아니고, Planck 값은 ΛCDM 가정 위의 값이다. 같은 보정자(세페이드 영점, LMC 거리)·같은 자료를 공유하는 추정은 독립이 아니며, 연도 군집 부트스트랩은 그 의존의 일부만 다룬다. 두 집성 모두 전수 조사가 아니다."),
         en=dict(name="Surprise against a reference", short="Each estimate's distance from a reference value divided by its own error: Planck 2018 and Riess et al. 2022 side by side",
                 definition="For each estimate z = (reference − x)/u_x, and the shares with |z| > 1 and |z| > 2 (misses), |z| < 0.674 (interquartile index) and |z| > 2.326 (surprise index). Two references are shown side by side instead of one: Planck 2018 (67.36 ± 0.54) and Riess et al. 2022 (73.04 ± 1.04). Under a normal distribution the expectations are 31.7%, 4.6%, 50% and 2%.",
                 formula="z = (reference − x) / u_x.  The reference's uncertainty does not enter z. Asymmetric errors enter as the mean.",
                 denominator="Huchra's list: {h3_hu_n} rows from 1929 to 2010 ({h3_hu50_n} from 1950). Table A2: {h3_fa_n_r} rows from 1976 to 2019; against Planck, {h3_fa_n_p} rows, the table's 2018 row \"67.4 ± 0.5\" (the rounded Planck 2018 value) being left out. 95% intervals: cluster bootstrap by publication year, 10,000 resamples, seed 2026.",
                 reading="Against Planck 2018, Huchra's list misses at ±1σ in {h3_hu_p_m1}% (normal: 31.7%), at ±2σ in {h3_hu_p_m2}% (4.6%), with a surprise index of {h3_hu_p_si}% (2%) and an interquartile index of {h3_hu_p_iq}% (50%). Against Riess et al. 2022: {h3_hu_r_m1}%, {h3_hu_r_m2}%, {h3_hu_r_si}% and {h3_hu_r_iq}%. Table A2 against Planck: {h3_fa_p_m1}%, {h3_fa_p_m2}%, {h3_fa_p_si}% and {h3_fa_p_iq}%; against Riess: {h3_fa_r_m1}%, {h3_fa_r_m2}%, {h3_fa_r_si}% and {h3_fa_r_iq}%. In every cell the intervals of the miss and surprise shares lie above the normal expectation and the interquartile index below it. The ±2σ miss rate of the physical-constants chapter (M3) is {m3_m2}%.",
                 caveat="Which side counts as \"surprising\" depends on the reference; that is why two are shown. These shares count whether quoted errors covered the distance to a reference; they do not say which reference is right or whether the tension is real. The references are measurements too, not true values, and the Planck value holds within the ΛCDM model. Estimates that share a calibrator (Cepheid zero point, LMC distance) or the same data are not independent, and the year-cluster bootstrap handles only part of that dependence. Neither compilation is complete."),
         takeaway=dict(ko=["Planck 2018 을 기준으로 하면 Huchra 목록 {h3_hu_n}건 가운데 ±2σ 밖이 {h3_hu_p_m2}%(정규 기대 4.6%), 놀람 지수(|z| > 2.326)가 {h3_hu_p_si}%(기대 2%)다. Riess 외 2022 를 기준으로 하면 {h3_hu_r_m2}% 와 {h3_hu_r_si}% 다.",
                           "표 A2 {h3_fa_n_r}건은 Planck 기준 ±2σ 밖 {h3_fa_p_m2}%, Riess 기준 {h3_fa_r_m2}%. 어느 기준에서도, 두 집성 모두, 인용된 오차 안에 기준값이 드는 비율은 정규분포가 예상하는 것보다 낮다.",
                           "이 지표는 긴장의 어느 편이 맞는지를 판정하지 않는다. 기준을 바꾸면 어느 추정이 「놀람」이 되는지가 바뀐다."],
                       en=["Against Planck 2018, {h3_hu_p_m2}% of the {h3_hu_n} estimates in Huchra's list lie beyond ±2σ (normal: 4.6%) and the surprise index (|z| > 2.326) is {h3_hu_p_si}% (2%). Against Riess et al. 2022: {h3_hu_r_m2}% and {h3_hu_r_si}%.",
                           "Of the {h3_fa_n_r} rows of Table A2, {h3_fa_p_m2}% lie beyond ±2σ against Planck and {h3_fa_r_m2}% against Riess. Under either reference, in both compilations, the reference falls inside the quoted error less often than a normal distribution predicts.",
                           "The metric does not decide which side of the tension is right: change the reference and different estimates become the surprising ones."])),
    dict(id="h4", file="h0_h4_tail.csv",
         ko=dict(name="t 분포 자유도", short="H3 의 z 에 맞춘 Student-t 의 자유도 — 꼬리의 두께",
                 definition="H3 의 z 에 중심 0 의 Student-t 분포를 최대우도로 맞춘 자유도 ν 와 척도 s. ν 가 작을수록 꼬리가 두껍다(정규분포는 ν → ∞). 기준값마다 따로 맞춘다.",
                 formula="z ~ s · t(ν),  ν·s 는 최대우도.  z = 0 인 행은 뺀다(척도 0 에서 우도가 발산). 95% 구간은 연도 군집 부트스트랩 2,000회.",
                 denominator="H3 과 같은 행: Huchra 목록 {h3_hu_n}건, 표 A2 {h3_fa_n_r}건(Planck 기준 {h3_fa_n_p}건).",
                 reading="Huchra 목록의 ν 는 Planck 기준 {h4_hu_p_nu}(95% 구간 {h4_hu_p_ci}), Riess 기준 {h4_hu_r_nu}({h4_hu_r_ci})다. 표 A2 는 {h4_fa_p_nu}({h4_fa_p_ci})와 {h4_fa_r_nu}({h4_fa_r_ci}). 물리 상수 장 M4 의 판 쌍 ν 는 {m4_nu}, Bailey(2017)가 기본 상수의 개별 측정 쌍에서 얻은 ν 는 1.81 ± 0.15 다.",
                 caveat="ν 가 2 안팎이면 분산이 정의되지 않는 꼬리다. 표 A2 의 Planck 기준 구간은 위쪽이 넓게 열려 있어({h4_fa_p_ci}) 표본 163건으로는 꼬리 두께를 좁혀 말하기 어렵다. H3 과 같은 한계(기준값 선택, 독립성, 오차 수준 미표기)가 그대로 적용된다."),
         en=dict(name="Student-t degrees of freedom", short="Degrees of freedom of a Student-t fitted to the z of H3: how heavy the tail is",
                 definition="The degrees of freedom ν and scale s of a zero-centered Student-t fitted by maximum likelihood to the z of H3. A smaller ν means a heavier tail (a normal distribution has ν → ∞). Fitted separately for each reference.",
                 formula="z ~ s · t(ν),  ν and s by maximum likelihood.  Rows with z = 0 are left out (the likelihood diverges at scale 0). 95% intervals: year-cluster bootstrap, 2,000 resamples.",
                 denominator="The same rows as H3: {h3_hu_n} in Huchra's list, {h3_fa_n_r} in Table A2 ({h3_fa_n_p} against Planck).",
                 reading="For Huchra's list ν = {h4_hu_p_nu} against Planck (95% interval {h4_hu_p_ci}) and {h4_hu_r_nu} against Riess ({h4_hu_r_ci}). Table A2: {h4_fa_p_nu} ({h4_fa_p_ci}) and {h4_fa_r_nu} ({h4_fa_r_ci}). The edition-pair ν of the physical-constants chapter (M4) is {m4_nu}; Bailey (2017) found ν = 1.81 ± 0.15 for pairs of individual measurements of fundamental constants.",
                 caveat="A ν near 2 is a tail whose variance is undefined. The Planck interval of Table A2 is open upward ({h4_fa_p_ci}): 163 rows do not pin the tail down. The limits of H3 (choice of reference, dependence, unstated error levels) apply unchanged."),
         takeaway=dict(ko=["Huchra 목록의 z 에 맞춘 Student-t 의 자유도는 Planck 기준 ν = {h4_hu_p_nu}({h4_hu_p_ci}), Riess 기준 {h4_hu_r_nu}({h4_hu_r_ci})다 — 정규분포(ν → ∞)보다 훨씬 두꺼운 꼬리다.",
                           "표 A2 는 {h4_fa_p_nu} 와 {h4_fa_r_nu} 로 같은 자릿수이고, 물리 상수 장의 판 쌍 ν {m4_nu}, Bailey(2017)의 1.81 과도 같은 자릿수다."],
                       en=["A Student-t fitted to the z of Huchra's list has ν = {h4_hu_p_nu} ({h4_hu_p_ci}) against Planck and {h4_hu_r_nu} ({h4_hu_r_ci}) against Riess: a far heavier tail than a normal distribution (ν → ∞).",
                           "Table A2 gives {h4_fa_p_nu} and {h4_fa_r_nu}, the same order as the edition-pair ν of the physical-constants chapter ({m4_nu}) and Bailey's (2017) 1.81."])),
]

# H2: the one paragraph of the chapter that explains why no number is published (owner decision D4).
H2_TEXT = {
    "ko": ("물리 상수 장의 M2 는 연속한 두 판 사이의 이동을 두 판의 불확도와 견준다. H0 에서 그에 대응하는 「연속 측정 쌍」은 출판 순서일 뿐이다. 같은 해에 여러 추정이 있어 쌍을 어떻게 잇느냐가 임의이고, 쌍을 하나로 묶느냐 방법 부호로 묶느냐에 따라 1단계 감도 표에서 판정이 「정규 기대값보다 위」와 「겹침」 사이를 오갔다. "
           "같은 팀의 후속 측정만 짝짓는 정의가 M2 의 뜻에 가장 가깝지만, 두 집성에는 팀을 가려내는 열이 없다. 그래서 이 장은 H2 의 번호를 비워 두고 수치를 내지 않는다. H1·H3·H4 가 M1·M3·M4 에 대응한다는 것이 번호에서 보이도록 번호는 그대로 둔다."),
    "en": ("M2 of the physical-constants chapter compares the move between two consecutive editions with their uncertainties. The H0 analogue, a pair of consecutive estimates, is only a publication order: several estimates share a year, so how the pairs are joined is arbitrary, and in the stage-1 sensitivity tables the verdict moved between \"above the normal expectation\" and \"overlapping\" depending on whether pairs were pooled or grouped by type code. "
           "Pairing only the follow-ups of the same team would come closest to M2, but neither compilation has a column that identifies teams. The chapter therefore leaves H2 empty and publishes no number under it; the numbering stays so that H1, H3 and H4 visibly correspond to M1, M3 and M4."),
}
