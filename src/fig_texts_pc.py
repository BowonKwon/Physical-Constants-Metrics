# -*- coding: utf-8 -*-
"""1.3.9: chart explanations of the physical-constants chapter (home, M1-M3, constant pages). Numbers come in v,
computed by build_site.py from the data files."""
from __future__ import annotations

from fig_explain import about, frac, sci, symlog_misread, symlog_sentence, symlog_term


def _r(x):
    """a ratio printed with enough digits to show which side of 1 it is on."""
    return f"{x:.2f}" if x < 0.1 or abs(x - 1) < 0.05 else f"{x:.1f}"


def home(lang, v):
    """v: med69, n69, med22, n22, ratio, ratio_en, rises [(e1, e2)], exact_names, exact_names_en, n_core."""
    ko = lang == "ko"
    w69, r69 = frac(v["med69"], lang)
    w22, r22 = frac(v["med22"], lang)
    rise = ""
    if v["rises"]:
        a, b = v["rises"][0]
        rise = (f" 예컨대 {a} 판에서 {b} 판으로는 중앙값이 올랐다." if ko else f" From the {a} to the {b} edition, for example, the median rose.")
    if ko:
        return ("판별 상대 표준불확도",
                "판마다 핵심 상수의 오차 막대가 값에 견주어 얼마나 좁았는지(상대 표준불확도)를 그린 그림이다.",
                [("glance", f"핵심 상수의 판별 중앙값은 1969 판 {sci(v['med69'])}에서 2022 판 {sci(v['med22'])}로 내려왔다. 약 {v['ratio']}분의 1이다."),
                 ("how", "가로는 판이고, 판의 이름은 반영한 자료의 마감 연도다(공표는 그 뒤 — 2022 판은 2024년). 간격은 연도에 비례한다. 세로는 상대 표준불확도, 곧 오차 막대의 반폭(±1σ)을 값의 크기로 나눈 수다. "
                         "세로 눈금은 한 칸이 10배인 로그 축이다(10⁻⁶ 은 값의 100만분의 1, 10⁻⁹ 은 10억분의 1). 아래로 갈수록 값에 견준 오차 막대가 좁다. "
                         f"반투명한 작은 점 하나가 (판, 핵심 상수) 하나이고, 색이 꽉 찬 큰 점과 굵은 선은 그 판 점들의 중앙값이다. 핵심 상수는 {v['n_core']}개이지만 판마다 측정값으로 실린 것만 점이 된다."),
                 ("one", f"2022 판의 중앙값 {sci(v['med22'])}은 그 판 핵심 상수 {v['n22']}개를 크기순으로 늘어놓았을 때 가운데 오는 오차 막대의 반폭이 값의 {about(lang, r22)}{w22}라는 뜻이다. "
                         f"1969 판({v['n69']}개)의 중앙값 {sci(v['med69'])}은 {about(lang, r69)}{w69}다."),
                 ("mis", "아래에 있다고 그 값이 참값에 더 가깝다는 뜻은 아니다. 과학자들이 밝힌 오차 막대가 좁다는 뜻이다. 바로 다음 판으로 넘어갈 때의 이동이 두 판의 불확도를 합친 값에 견주어 얼마나 컸는지는 M2 가, 옛 판의 막대가 2022 판 값을 담았는지는 M3 이 센다. "
                         f"판마다 들어간 상수가 달라서(예: 양성자 전하 반지름은 2002 판부터) 중앙값이 판 사이에서 거꾸로 오르기도 한다.{rise}"
                         + (f" 정의값이 된 상수({v['exact_names']})는 그 판부터 불확도가 0이라 점이 없다." if v["exact_names"] else "")),
                 ("terms", "상대 표준불확도 = 표준불확도(참값이 대략 이 범위 안에 있다는 오차 막대의 반폭, ±1σ) ÷ 값의 크기. "
                           "중앙값 = 크기순으로 늘어놓았을 때 한가운데 오는 값(개수가 짝수면 가운데 두 값의 평균). "
                           "로그 축 = 같은 간격이 같은 배수를 뜻하는 눈금. 정의값 = 측정하지 않고 약속으로 정해 불확도가 0인 값.")])
    return ("Relative standard uncertainty by edition",
            "how narrow the error bars of the core constants were, relative to their values (the relative standard uncertainty), edition by edition.",
            [("glance", f"The median over the core constants fell from {sci(v['med69'])} in the 1969 edition to {sci(v['med22'])} in 2022, to about 1/{v['ratio_en']} of its 1969 size."),
             ("how", "The horizontal axis is the edition, named after the closing year of its data (published later: the 2022 edition in 2024), spaced by year. The vertical axis is the relative standard uncertainty: "
                     "the half-width of the error bar (±1σ) divided by the size of the value. It is a log axis, one step per factor of ten (10⁻⁶ is one millionth of the value, 10⁻⁹ one billionth); "
                     "lower means a narrower error bar relative to the value. Each small translucent dot is one (edition, core constant); the large opaque dots and the thick line are the median of each edition's dots. "
                     f"There are {v['n_core']} core constants, but only those measured in an edition give a dot."),
             ("one", f"The 2022 median of {sci(v['med22'])} means that, with the error bars of that edition's {v['n22']} core constants ranked, the middle one has a half-width of {about(lang, r22)}{w22} of its value. "
                     f"The 1969 median ({v['n69']} constants), {sci(v['med69'])}, is {about(lang, r69)}{w69}."),
             ("mis", "A lower dot does not mean a value closer to the truth. It means a narrower stated error bar. How large the move to the next edition was against the two editions' combined uncertainty is what M2 counts, and whether an earlier bar held the 2022 value is what M3 counts. "
                     f"The set of constants changes between editions (the proton charge radius enters in 2002, for example), so the median can rise from one edition to the next.{rise}"
                     + (f" Constants that became exact (the {v['exact_names_en']}) have zero uncertainty from that edition on and no dot." if v["exact_names_en"] else "")),
             ("terms", "Relative standard uncertainty: the standard uncertainty (the half-width, ±1σ, of an error bar saying the true value is probably inside it) divided by the size of the value. "
                       "Median: the middle value when the values are ranked (with an even number, the mean of the middle two). "
                       "Log axis: equal distances stand for equal ratios. Exact value: fixed by agreement rather than measured, so its uncertainty is zero.")])


def halflife(lang, v):
    """v: n_dec, med, min_name(_en), min, min_ci, min_n, max_name(_en), max, n_open, none_names(_en), n_core."""
    if lang == "ko":
        return ("상수별 반감기",
                "핵심 상수마다 상대 표준불확도가 절반이 되는 데 걸린 햇수(반감기)와 그 95% 구간을 그린 그림이다.",
                [("glance", f"불확도가 줄어든 핵심 상수 {v['n_dec']}개의 반감기 중앙값은 {v['med']}년이다. 가장 짧은 것은 {v['min_name']} {v['min']}년, 가장 긴 것은 {v['max_name']} {v['max']}년이다."),
                 ("how", f"한 줄이 핵심 상수 하나다({v['n_core']}개). 점은 반감기, 점에 걸친 가로선은 95% 구간이다. 가로축은 햇수(0~25년)이고, 왼쪽일수록 불확도가 빨리 줄었다. "
                         "구간의 끝이 25년을 넘거나 한없이 열려 있으면 오른쪽 끝에 화살표(→)를 달았다. 「감소 없음」은 맞춘 직선이 거의 평평해서(반감기 1,000년 초과) 반감기를 적지 않은 상수다."),
                 ("one", f"{v['min_name']}의 점 {v['min']}년은, 그 상수가 측정값으로 실린 판 {v['min_n']}개에 맞춘 직선으로 보면 상대 표준불확도가 {v['min']}년마다 절반이 되었다는 뜻이다. 95% 구간은 {v['min_ci']}년이다."),
                 ("mis", "반감기는 판별 값에 직선 하나를 맞춘 요약이다. 새 측정법이 들어온 판에서 불확도가 계단처럼 확 줄어든 상수는 직선에 잘 맞지 않는다(아래 표의 R² 가 낮다). "
                         f"판이 적은 상수일수록 구간이 넓고, 화살표가 달린 상수는 {v['n_open']}개다. 반감기가 짧다고 값이 더 맞았다는 뜻은 아니다. 오차 막대가 빨리 좁아졌다는 뜻이다."
                         + (f" 「감소 없음」은 {v['none_names']}이다." if v["none_names"] else "")),
                 ("terms", "반감기 = log₂(상대 표준불확도)를 판 연도에 직선으로 맞췄을 때, 불확도가 절반이 되는 데 걸리는 햇수(−1 ÷ 기울기). "
                           "95% 구간 = 기울기의 t 분포 구간(자유도 n−2)을 같은 식에 넣은 범위로, 자료가 우연히 조금 달랐다면 반감기가 놓였을 범위의 어림이다. "
                           "R²(결정계수) = 직선이 점들을 얼마나 잘 따라가는지를 0~1로 나타낸 수.")])
    return ("Half-life by constant",
            "for each core constant, the number of years it took the relative standard uncertainty to halve (the half-life), with its 95% interval.",
            [("glance", f"Over the {v['n_dec']} core constants whose uncertainty declined, the median half-life is {v['med']} years; the shortest is the {v['min_name_en']} at {v['min']} years, the longest the {v['max_name_en']} at {v['max']} years."),
             ("how", f"Each row is one core constant ({v['n_core']} in all). The dot is the half-life and the horizontal line through it the 95% interval. The horizontal axis is years (0–25); further left means the uncertainty fell faster. "
                     "Where the interval reaches beyond 25 years or is open-ended, an arrow (→) is drawn at the right edge. \"No decline\" marks a constant whose fitted line is almost flat (half-life above 1,000 years), so no half-life is given."),
             ("one", f"The dot of the {v['min_name_en']} at {v['min']} years means that, on a straight line fitted to its {v['min_n']} editions with a measured value, its relative standard uncertainty halved every {v['min']} years. The 95% interval is {v['min_ci']} years."),
             ("mis", "A half-life summarises the editions with one straight line. A constant whose uncertainty dropped in one step, when a new method came in, does not follow a line well (its R² in the table below is low). "
                     f"The fewer the editions, the wider the interval; {v['n_open']} constants have an arrow. A short half-life does not mean the values were more nearly right, only that the error bars narrowed faster."
                     + (f" \"No decline\": the {v['none_names_en']}." if v["none_names_en"] else "")),
             ("terms", "Half-life: with log₂(relative standard uncertainty) fitted to the edition year by a straight line, the years it takes the uncertainty to halve (−1 ÷ slope). "
                       "95% interval: the t interval of the slope (n−2 degrees of freedom) put through the same formula; a rough range for where the half-life would lie had the data come out slightly differently. "
                       "R² (coefficient of determination): how closely the line follows the dots, from 0 to 1.")])


def tail(lang, v):
    """v: n, q, r1, r2, r3, k1, k2, one_in2, zero, n_fit, nu, s, zmax."""
    if lang == "ko":
        return ("판간 이동의 꼬리",
                "연속한 두 판 사이에 값이 움직인 크기(z)가 어떤 값을 넘은 판 쌍이 얼마나 되는지를, 정규분포의 기대와 견준 그림이다.",
                [("glance", f"|z| 가 2를 넘은 판 쌍은 {v['r2']}%(정규분포 기대 4.55%), 3을 넘은 쌍은 {v['r3']}%(기대 0.27%)다. 큰 이동 쪽(오른쪽)에서 관측 선이 정규분포 곡선보다 높이 떠 있다."),
                 ("how", "가로는 |z|, 곧 두 판 사이 값의 이동을 두 판의 표준불확도를 합친 값 √(u_옛²+u_새²)으로 나눈 크기다(부호는 뗐다). "
                         "세로는 |z| 가 그 가로 값을 넘는 판 쌍의 비율이고, 눈금 한 칸이 10배인 로그 축이다. 모든 선은 왼쪽 위(100%)에서 시작해 오른쪽으로 갈수록 내려간다. "
                         "오른쪽에서 높이 떠 있을수록 큰 이동이 잦다는 뜻이다. 파란 계단 선이 관측, 회색 점선이 정규분포(밝힌 불확도가 맞고 두 판이 독립일 때의 기대), "
                         "초록 선이 관측에 맞춘 Student-t 분포다. 파란 점 셋은 |z| > 1·2·3 의 관측 비율이다."),
                 ("one", f"가로 2 자리의 파란 점 {v['r2']}%는 핵심 상수 {v['q']}개의 판 쌍 {v['n']}개 가운데 {v['k2']}개가 두 판의 표준불확도를 합친 값의 2배보다 크게 움직였다는 뜻이다. "
                         f"정규분포라면 약 22쌍에 1쌍(4.55%)인데, 관측은 약 {v['one_in2']}쌍에 1쌍이다."),
                 ("mis", f"|z| > 1 은 오히려 기대(31.7%)보다 적다({v['r1']}%, {v['k1']}쌍). 연속한 두 판은 같은 실험 자료를 상당 부분 나눠 써서 독립이 아니고, 값이 한 자리도 바뀌지 않은 쌍 {v['zero']}개는 z = 0 으로 들어간다. "
                         "그래서 이것을 「오차 막대가 넉넉했다」로 읽으면 안 된다. "
                         f"Student-t 는 값이 바뀐 쌍 {v['n_fit']}개에만 맞췄다(z = 0 인 쌍이 있으면 맞춤이 성립하지 않는다). 관측 선은 가장 큰 |z|({v['zmax']})에서 끝나고, 그 오른쪽에는 자료가 없다."),
                 ("terms", "z = (새 판 값 − 옛 판 값) ÷ √(옛 판 표준불확도² + 새 판 표준불확도²). "
                           "정규분포 = 오차가 밝힌 크기대로 우연히만 생길 때 기대하는 종 모양 분포. "
                           f"Student-t 분포 = 정규분포보다 꼬리(아주 큰 값이 나올 몫)가 두꺼운 분포. 자유도 ν 가 작을수록 꼬리가 두껍고, ν 가 한없이 커지면 정규분포가 된다. 여기서 맞춘 값은 ν = {v['nu']}, 척도 s = {v['s']}(가로를 늘이고 줄이는 배율)다. "
                           "로그 축 = 같은 간격이 같은 배수를 뜻하는 눈금.")])
    return ("Tail of the moves between editions",
            "the share of edition pairs in which the move between consecutive editions (z) exceeded a given size, set against the normal distribution.",
            [("glance", f"{v['r2']}% of pairs have |z| above 2 (normal: 4.55%) and {v['r3']}% above 3 (normal: 0.27%). On the right, where the moves are large, the observed line lies well above the normal curve."),
             ("how", "The horizontal axis is |z|: the move between two editions divided by their combined standard uncertainty √(u_old² + u_new²), sign removed. "
                     "The vertical axis is the share of pairs whose |z| exceeds that horizontal value, on a log axis (one step per factor of ten). Every line starts at the top left (100%) and falls to the right; "
                     "the higher a line stays on the right, the more common large moves are. The blue step line is observed, the gray dashed line the normal distribution (what to expect if the stated uncertainties were right and the two editions independent), "
                     "and the green line a Student-t distribution fitted to the observations. The three blue dots are the observed shares above 1, 2 and 3."),
             ("one", f"The blue dot at 2 on the horizontal axis, {v['r2']}%, means that {v['k2']} of the {v['n']} pairs of the {v['q']} core constants moved by more than twice their combined standard uncertainty. "
                     f"A normal distribution expects about 1 pair in 22 (4.55%); the data show about 1 in {v['one_in2']}."),
             ("mis", f"Above 1 the share is lower than expected ({v['r1']}%, {v['k1']} pairs, against 31.7%). Consecutive editions share much of their experimental data, so they are not independent, and the {v['zero']} pairs whose value did not change by a single digit enter with z = 0. "
                     "Do not read this as \"the error bars were generous\". "
                     f"The Student-t is fitted only to the {v['n_fit']} pairs whose value changed (pairs with z = 0 make the fit break down). The observed line ends at the largest |z| ({v['zmax']}); to its right there are no data."),
             ("terms", "z = (new value − old value) ÷ √(old standard uncertainty² + new standard uncertainty²). "
                       "Normal distribution: the bell-shaped distribution expected when errors arise only by chance at their stated size. "
                       f"Student-t distribution: like the normal but with heavier tails (more room for very large values); the smaller its degrees of freedom ν, the heavier the tails, and as ν grows without limit it becomes the normal. The fitted values here are ν = {v['nu']} and scale s = {v['s']} (a factor that stretches the horizontal axis). "
                       "Log axis: equal distances stand for equal ratios.")])


def miss(lang, v):
    """v: all_m2, old_m2, new_m2, e0, e0_n, e0_m2, e0_k2, n, q, nmin, nmax."""
    if lang == "ko":
        return ("판별 놓침 비율",
                "판마다, 그 판의 오차 막대(±1σ)와 그것을 두 배로 넓힌 범위(±2σ)가 2022 판 값을 담지 못한 비율을 그린 그림이다.",
                [("glance", f"판을 모두 합치면 ±2σ 밖이 {v['all_m2']}%(정규분포 기대 4.6%)다. 1969~1986 판 묶음은 {v['old_m2']}%, 1998~2018 판 묶음은 {v['new_m2']}% 로, 불확도가 훨씬 작아진 최근 판에서도 줄지 않았다."),
                 ("how", "가로는 판, 세로는 비율(0~100%)이다. 판마다 파란 점이 ±1σ 밖, 주황 점이 ±2σ 밖의 비율이고, 점에 걸친 세로선은 95% 구간이다. "
                         "회색 가로 점선 두 줄은 오차 막대가 맞을 때의 정규분포 기대(위 1σ 31.7%, 아래 2σ 4.6%)다. 점이 짝이 되는 점선보다 위에 있으면 기대보다 자주 놓쳤다는 뜻이다."),
                 ("one", f"{v['e0']} 판의 주황 점 {v['e0_m2']}%는 그 판에 측정값으로 있던 핵심 상수 {v['e0_n']}개 가운데 {v['e0_k2']}개가 2022 판 값을 ±2σ 범위 밖에 두었다는 뜻이다."),
                 ("mis", f"2022 판은 참값이 아니라 지금의 권고값이어서 다음 판에서 바뀔 수 있다. 판마다 들어간 상수가 {v['nmin']}~{v['nmax']}개뿐이라 구간이 넓다. "
                         f"같은 상수가 여러 판에 되풀이해 들어가므로 판을 합친 비율({v['n']}개 조합, 상수 {v['q']}개)의 실제 표본 크기는 겉보기보다 작다. 2022 판 자신은 그림에 없다."),
                 ("terms", "±1σ = 그 판의 오차 막대(표준불확도 하나만큼 위아래). ±2σ = 막대를 두 배로 넓힌 범위. "
                           "군집 부트스트랩 95% 구간 = 상수 하나에 딸린 판들을 한 묶음으로 삼아 묶음째 무작위로 다시 뽑고 같은 비율을 되풀이해 셌을 때, 결과의 가운데 95%가 놓인 범위.")])
    return ("Miss rate by edition",
            "for each edition, the share of core constants whose error bar (±1σ), or the range twice as wide (±2σ), did not contain the 2022 value.",
            [("glance", f"Pooled over the editions, {v['all_m2']}% fall outside ±2σ (normal: 4.6%). The 1969–1986 editions give {v['old_m2']}% and the 1998–2018 editions {v['new_m2']}%: no lower in the recent editions, whose uncertainties are far smaller."),
             ("how", "The horizontal axis is the edition and the vertical axis the share (0–100%). For each edition the blue dot is the share outside ±1σ and the orange dot the share outside ±2σ; the vertical lines through them are 95% intervals. "
                     "The two gray dashed lines are what a normal distribution expects if the error bars were right (upper: 1σ, 31.7%; lower: 2σ, 4.6%). A dot above its dashed line means the value was missed more often than expected."),
             ("one", f"The orange dot of the {v['e0']} edition, {v['e0_m2']}%, means that {v['e0_k2']} of the {v['e0_n']} core constants measured in that edition had the 2022 value outside their ±2σ range."),
             ("mis", f"The 2022 edition is not the truth but the current recommendation, and may change in the next edition. Each edition has only {v['nmin']} to {v['nmax']} constants, so the intervals are wide. "
                     f"The same constants recur across editions, so the pooled share ({v['n']} combinations, {v['q']} constants) rests on a smaller sample than it seems. The 2022 edition itself is not in the chart."),
             ("terms", "±1σ: the edition's error bar (one standard uncertainty either side). ±2σ: the range twice as wide. "
                       "Cluster-bootstrap 95% interval: the editions of each constant are taken as one bundle, bundles are drawn again at random and the share counted again, many times; the middle 95% of the results is the interval.")])


def funnel(lang, v):
    """v: name, name_en, n_meas (editions before 2022 with a measured value), n_miss, miss_eds, exact_eds, lt_txt (ko/en), first (dict or None), ex22."""
    f = v["first"]
    if lang == "ko":
        nm = v["name"]
        if v["n_meas"]:
            gl = f"2022 판을 뺀 측정값 판 {v['n_meas']}개 가운데 오차 막대가 2022 판 값(0의 점선)에 닿지 않은 판은 " + (f"{v['n_miss']}개다({v['miss_eds']})." if v["n_miss"] else "없다.")
        else:
            gl = "2022 판 말고는 측정값으로 실린 판이 없다."
        if v["exact_eds"]:
            gl += f" {v['exact_eds']} 판은 정의값이라 네모로 그렸다."
        one = ""
        if f:
            dw, dr = frac(f["dv"], "ko")
            ratio = abs(f["dv"]) / f["uu"]
            one = (f"{f['ed']} 판 값은 2022 판 값보다, 2022 판 값의 크기에 견주어 {about('ko', dr)}{dw}({'+' if f['dv'] > 0 else '−'}{sci(abs(f['dv']))})만큼 {'컸고' if f['dv'] > 0 else '작았고'}, "
                   f"그 판 오차 막대의 반폭을 2022 판 값의 크기로 나누면 ±{sci(f['uu'])} 이므로 떨어진 거리는 막대 반폭의 {_r(ratio)}배다. "
                   + ("막대가 0의 점선에 닿지 않아 속이 빈 원으로 그렸다." if ratio > 1 else "막대가 0의 점선에 닿아 속이 찬 원으로 그렸다."))
        return (f"{nm} — 2022 판 값에서 떨어진 정도",
                f"{nm}의 판별 값이 2022 판 값에서, 그 값의 크기에 견주어 얼마나 떨어져 있었는지를, 그 판의 오차 막대(±1σ)와 함께 그린 그림이다.",
                [("glance", gl),
                 ("how", "가로는 판, 세로는 (그 판 값 − 2022 판 값) ÷ |2022 판 값|(2022 판 값의 크기, 곧 절댓값)이다. 값이 음수인 상수도 위가 더 큰 값이다. 회색 0의 점선이 2022 판 값이고 위는 그보다 큰 값, 아래는 작은 값이다. "
                         "점 하나가 판 하나이고, 세로 막대는 그 판의 ±1σ(표준불확도)를 같은 |2022 판 값|으로 나눈 것이다(그 판 값의 절댓값으로 나눈 상대 표준불확도와는 조금 다를 수 있다). 속이 찬 원은 막대가 0의 점선에 닿은 판, 속이 빈 원은 닿지 않은 판이다. "
                         + ("네모는 정의값(불확도 0)이다. " if v["exact_eds"] else "")
                         + symlog_sentence("ko", v["lt_txt"])),
                 ("one", one),
                 ("mis", symlog_misread("ko") + (" 2022 판은 정의값이라 0의 자리에 네모로 놓인다." if v["ex22"] else " 2022 판 점은 정의상 0에 놓인다. 2022 판 값도 참값이 아니라 지금의 권고값이다.")),
                 ("terms", "상대 편차 = (그 판 값 − 2022 판 값) ÷ |2022 판 값|. σ(시그마) = 표준불확도를 나타내는 기호. ±1σ = 표준불확도 하나만큼 위아래로 그은 오차 막대. 정의값 = 측정하지 않고 약속으로 정해 불확도가 0인 값. " + symlog_term("ko"))])
    nm = v["name_en"]
    if v["n_meas"]:
        gl = f"Of the {v['n_meas']} editions before 2022 with a measured value, {v['n_miss'] or 'none'} {'has' if v['n_miss'] in (0, 1) else 'have'} an error bar that does not reach the 2022 value (the dashed zero line)" + (f" ({v['miss_eds']})." if v["n_miss"] else ".")
    else:
        gl = "No edition other than 2022 gives it as a measured value."
    if v["exact_eds"]:
        gl += f" In {v['exact_eds']} it is exact, drawn as a square."
    one = ""
    if f:
        dw, dr = frac(f["dv"], "en")
        ratio = abs(f["dv"]) / f["uu"]
        one = (f"The {f['ed']} value lay {about('en', dr)}{dw} of the size of the 2022 value ({'+' if f['dv'] > 0 else '−'}{sci(abs(f['dv']))}) {'above' if f['dv'] > 0 else 'below'} the 2022 value, "
               f"and that edition's error-bar half-width divided by the size of the 2022 value is ±{sci(f['uu'])}. The distance is {_r(ratio)} times the half-width, so "
               + ("the bar does not reach the zero line and the circle is open." if ratio > 1 else "the bar reaches the zero line and the circle is filled."))
    return (f"{nm[:1].upper() + nm[1:]}: distance from the 2022 value",
            f"how far each edition's value of the {nm} lay from the 2022 value, relative to the size of that value, with that edition's error bar (±1σ).",
            [("glance", gl),
             ("how", "The horizontal axis is the edition; the vertical axis is (edition value − 2022 value) ÷ |2022 value| (the size, i.e. absolute value, of the 2022 value), so above is larger even for a constant with a negative value. The gray dashed zero line is the 2022 value; above it are larger values, below it smaller ones. "
                     "Each mark is one edition and the vertical bar its ±1σ (standard uncertainty) divided by the same |2022 value| (which can differ slightly from that edition's own relative standard uncertainty). A filled circle is an edition whose bar reaches the zero line, an open circle one whose bar does not. "
                     + ("A square is an exact value (zero uncertainty). " if v["exact_eds"] else "")
                     + symlog_sentence("en", v["lt_txt"])),
             ("one", one),
             ("mis", symlog_misread("en") + (" The 2022 value is exact and sits at zero as a square." if v["ex22"] else " The 2022 mark sits at zero by definition; the 2022 value is not the truth either, only the current recommendation.")),
             ("terms", "Relative deviation: (edition value − 2022 value) ÷ |2022 value|. σ (sigma): the symbol for the standard uncertainty. ±1σ: an error bar one standard uncertainty either side. Exact value: fixed by agreement rather than measured, zero uncertainty. " + symlog_term("en"))])
