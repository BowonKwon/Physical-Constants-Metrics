# -*- coding: utf-8 -*-
"""1.3.9: chart explanations of the Hubble-constant chapter. Numbers come in v, computed by h0_site.py from the data."""
from __future__ import annotations

_UNIT_KO = ("H0 의 단위 km s⁻¹ Mpc⁻¹ 은 「1메가파섹(Mpc, 약 326만 광년) 멀어질 때마다 은하가 초속 몇 km 더 빨리 멀어지는가」다.")
_UNIT_EN = ("The unit of H0, km s⁻¹ Mpc⁻¹, reads \"how many kilometres per second faster a galaxy recedes for every megaparsec (Mpc, about 3.26 million light-years) of distance\".")
_DATE_KO = "연도는 목록에 적힌 해로, 출판·프리프린트·학회 발표 가운데 하나의 날짜다."
_DATE_EN = "Years are those recorded in the lists: the date of publication, of a preprint or of a conference talk."
_REF_KO = "두 기준값은 초기 우주(우주배경복사)로 잰 Planck 2018(67.36 ± 0.54)과 거리 사다리로 잰 Riess 외 2022(73.04 ± 1.04)다. 이 장은 둘 가운데 어느 쪽이 맞는지 판정하지 않는다."
_REF_EN = "The two references are Planck 2018 (67.36 ± 0.54), from the early universe (the cosmic microwave background), and Riess et al. 2022 (73.04 ± 1.04), from the distance ladder. The chapter does not decide which is right."


def timeline(lang, v):
    """v: d30 (n, med, q1, q3), late_lo, late_hi, n_fa, fa0, fa1, n_dec_missing (list), d20_n."""
    d = v["d30"]
    if lang == "ko":
        return ("허블 상수 H0, 1929~2022",
                "1929~2022년에 발표된 허블 상수(H0) 추정값을 두 목록에서 모아 두 기준값과 함께 그린 그림이다.",
                [("glance", f"Huchra 목록의 10년 단위 중앙값은 1930년대 {d['med']}에서, 1970년대 이후 {v['late_lo']}~{v['late_hi']} 사이로 내려왔다."),
                 ("how", "가로는 연도, 세로는 H0 값이고 세로 눈금은 로그 축이다(같은 간격이 같은 배수: 50에서 100, 100에서 200이 같은 거리). " + _UNIT_KO + " "
                         f"파란 점은 표 A2 의 추정 하나({v['fa0']}~{v['fa1']}년, {v['n_fa']}건)이고 세로 막대는 ± 인용 오차(위아래가 다르면 평균)다. "
                         "회색 상자는 Huchra 목록의 10년 단위 묶음에서 가운데 절반의 추정이 놓인 범위(사분위 범위), 상자 안 가로줄은 중앙값, 아래 n= 은 그 10년의 건수다. "
                         "가로 점선 둘은 기준값(초록 Planck 2018, 주황 Riess 외 2022)이고, 맨 위의 띠와 점은 연대기의 사건이다."),
                 ("one", f"1930년대 상자는 그 10년 Huchra 목록 추정 {d['n']}건의 가운데 값이 {d['med']}이고, 가운데 절반이 {d['q1']}~{d['q3']} 사이에 있다는 뜻이다."),
                 ("mis", "Huchra 목록은 재게시 허락이 없어 행 하나하나는 그리지 않고 10년 단위 묶음만 그렸다. 개별 추정의 점은 표 A2 뿐이다. "
                         f"1920년대는 {v['d20_n']}건뿐이라 상자 없이 n= 만 적었고, {v['missing_txt']}는 목록에 행이 없어 비어 있다. "
                         "로그 축이라 위쪽(값이 큰 쪽)의 차이가 실제보다 좁아 보인다. " + _REF_KO + " " + _DATE_KO),
                 ("terms", "H0(허블 상수) = 은하가 멀어지는 속도를 거리로 나눈 값. 사분위 범위 = 크기순으로 늘어놓았을 때 아래 4분의 1과 위 4분의 1을 뺀 가운데 절반의 범위. "
                           "중앙값 = 한가운데 오는 값. 로그 축 = 같은 간격이 같은 배수를 뜻하는 눈금.")])
    return ("The Hubble constant H0, 1929–2022",
            "published estimates of the Hubble constant (H0) from 1929 to 2022, gathered from two lists and shown with the two references.",
            [("glance", f"The decade medians of Huchra's list came down from {d['med']} in the 1930s to between {v['late_lo']} and {v['late_hi']} from the 1970s on."),
             ("how", "The horizontal axis is the year and the vertical axis H0, on a log scale (equal distances are equal ratios: 50 to 100 is as far as 100 to 200). " + _UNIT_EN + " "
                     f"Blue dots are single estimates of Table A2 ({v['fa0']}–{v['fa1']}, {v['n_fa']} rows), with bars of ± the quoted error (the mean if asymmetric). "
                     "Gray boxes show, for each decade of Huchra's list, the range holding the middle half of the estimates (the interquartile range); the line in the box is the median, and n= below gives the decade's count. "
                     "The two dashed horizontal lines are the references (green Planck 2018, orange Riess et al. 2022); the bands and dots along the top are the events of the chronology."),
             ("one", f"The 1930s box means that the {d['n']} estimates of Huchra's list in that decade have a median of {d['med']}, with the middle half between {d['q1']} and {d['q3']}."),
             ("mis", "Huchra's list carries no permission to republish, so its rows are not drawn one by one, only as decade aggregates; the only single estimates shown are those of Table A2. "
                     f"The 1920s have {v['d20_n']} row, so only n= is shown and no box; {v['missing_txt_en']} have no rows in the list and are empty. "
                     "On a log axis differences at the top (the larger values) look narrower than they are. " + _REF_EN + " " + _DATE_EN),
             ("terms", "H0 (the Hubble constant): the speed at which galaxies recede divided by their distance. Interquartile range: the middle half of the values, leaving out the lowest and highest quarters. "
                       "Median: the middle value. Log axis: equal distances stand for equal ratios.")])


def zoom(lang, v):
    """v: n_out, out_txt, n_between, n_fa."""
    if lang == "ko":
        return ("1970년부터 확대한 H0",
                "위 그림과 같은 자료를 1970년부터, 세로 40~110의 고른 간격으로 확대한 그림이다.",
                [("glance", f"표 A2 {v['n_fa']}건 가운데 두 기준값(67.36과 73.04) 사이에 놓인 추정은 {v['n_between']}건이다."),
                 ("how", "가로는 연도, 세로는 H0(km s⁻¹ Mpc⁻¹)이고 세로 눈금은 고른 간격이다. 파란 점과 세로 막대는 표 A2 의 추정과 ± 인용 오차, 회색 상자와 가로줄은 Huchra 목록 10년 단위의 사분위 범위와 중앙값, 점선 둘은 기준값이다. "
                         + (f"40~110 밖의 값은 위나 아래 끝에 세모로 붙였다({v['out_txt']})." if v["n_out"] else "표 A2 의 값은 모두 40~110 안에 있다(세로 막대의 끝만 잘릴 수 있다).")),
                 ("mis", ("세모의 자리는 실제 값이 아니라 그림의 끝이다. 실제 값은 세모 위 말풍선에 있다. " if v["n_out"] else "") + "회색 상자는 10년을 묶은 것이라 상자 안의 위치는 해를 뜻하지 않는다.")])
    return ("H0 from 1970, enlarged",
            "the same data as above from 1970, on an evenly spaced vertical axis from 40 to 110.",
            [("glance", f"Of the {v['n_fa']} rows of Table A2, {v['n_between']} lie between the two references (67.36 and 73.04)."),
             ("how", "The horizontal axis is the year and the vertical axis H0 (km s⁻¹ Mpc⁻¹), evenly spaced. Blue dots and bars are Table A2 estimates with ± their quoted error; gray boxes and lines are the decade interquartile ranges and medians of Huchra's list; the two dashed lines are the references. "
                     + (f"Values outside 40–110 are drawn as triangles at the top or bottom edge ({v['out_txt_en']})." if v["n_out"] else "All Table A2 values lie within 40–110 (only the ends of some error bars may be cut off).")),
             ("mis", ("A triangle sits at the edge of the chart, not at its value; the value is in its tooltip. " if v["n_out"] else "") + "Gray boxes span a decade, so a position inside a box does not mark a year.")])


def types(lang, v):
    """v: d (decade), code, name, k, n, pct, top_txt, top_txt_en, n_rows."""
    if lang == "ko":
        return ("10년마다 쓰인 측정 방법",
                "Huchra 목록의 추정이 10년마다 어떤 측정 방법(1차 Type 부호)으로 나왔는지 칸으로 그린 그림이다.",
                [("glance", v["top_txt"]),
                 ("how", "가로 칸은 10년(위에 그 10년의 행 수 n=), 세로 줄은 측정 방법 부호다(이름은 아래 풀이). 칸의 숫자는 건수이고, 칸의 파란색이 선명할수록 그 10년 행 가운데 몫이 크다. 숫자가 없는 칸은 그 10년에 그 부호의 행이 없다는 뜻이다."),
                 ("one", f"{v['d']}년대의 「{v['code']} · {v['name']}」 칸({v['k']}건)은 그 10년 행 {v['n']}건 가운데 {v['k']}건, 곧 {v['pct']}%가 이 방법이라는 뜻이다."),
                 ("mis", f"칸의 색은 그 10년 안의 몫이어서, 행이 아주 적은 10년({v['few']})은 몇 건만으로도 색이 선명하다. 전체 건수가 10건 미만인 부호는 「그 밖의 부호」로 묶었다. 1929년 이후 오차가 있는 행만 셌다. 부호는 목록 파일의 범례 그대로이고 한 행에 1차 부호 하나만 센다.")])
    return ("Methods used, decade by decade",
            "a grid of which method (primary type code) produced the estimates of Huchra's list in each decade.",
            [("glance", v["top_txt_en"]),
             ("how", "Columns are decades (with the decade's row count, n=, on top) and rows are method codes (names explained below). The number in a cell is the count, and the stronger the blue, the larger that code's share of the decade's rows. A cell without a number has no rows of that code in that decade."),
             ("one", f"The cell \"{v['code']} · {v['name']}\" in the {v['d']}s, {v['k']}, means that {v['k']} of the decade's {v['n']} rows ({v['pct']}%) used this method."),
             ("mis", f"The colour is a share within the decade, so decades with very few rows ({v['few_en']}) show strong colour from a few rows. Codes with fewer than 10 rows in all are folded into \"other codes\". Only rows with an error from 1929 on are counted. Codes are as given in the file legend, one primary code per row.")])


def urel_yearly(lang, v):
    """v: hl, hl_ci, n_years, n_small, yr (year, n, med, q1, q3)."""
    y = v["yr"]
    if lang == "ko":
        return ("Huchra 목록, 해마다의 상대 오차",
                "Huchra 목록에서 해마다 발표된 추정값들의 상대 오차(인용 오차 ÷ H0)를 묶어 그린 그림이다.",
                [("glance", f"해별 중앙값에 맞춘 직선으로 보면 상대 오차는 약 {v['hl']}년마다 절반이 되었다(95% 구간 {v['hl_ci']}년)."),
                 ("how", "가로는 목록에 적힌 연도, 세로는 상대 오차(1%~100%)이고 세로 눈금은 로그 축이다(1%에서 10%, 10%에서 100%가 같은 거리). "
                         "회색 굵은 막대는 그해 추정들의 가운데 절반이 놓인 범위(사분위 범위), 점은 중앙값이다. 아래일수록 그해 추정들이 오차를 작게 적었다는 뜻이다. "
                         f"추정이 3건 미만인 해({v['n_years']}개 해 가운데 {v['n_small']}개)는 막대 없이 맨 아래에 ×만 두었다(건수는 커서를 대면 보인다)."),
                 ("one", f"{y['year']}년은 추정 {y['n']}건의 상대 오차 중앙값이 {y['med']}%이고, 가운데 절반이 {y['q1']}~{y['q3']}% 사이에 있다."),
                 ("mis", "아래로 갈수록 「오차를 좁게 적었다」는 뜻이지, 그 값이 참값에 더 가까웠다(실제로 정밀해졌다)는 뜻은 아니다. 적은 오차가 기준값과의 차이를 담았는지는 H3 이 센다. "
                         "오차가 통계 오차만인지 계통 오차까지 넣은 것인지는 행마다 다를 수 있고 목록이 밝히지 않는다. " + _DATE_KO),
                 ("terms", "상대 오차 = 인용된 오차 ÷ H0 값. 사분위 범위 = 가운데 절반의 범위. 반감기 = log₂(해별 중앙값)를 연도에 직선으로 맞췄을 때 절반이 되는 데 걸리는 햇수. 로그 축 = 같은 간격이 같은 배수를 뜻하는 눈금.")])
    return ("Huchra's list: relative error year by year",
            "the relative error (quoted error ÷ H0) of the estimates published each year in Huchra's list, in aggregate.",
            [("glance", f"On a straight line fitted to the yearly medians, the relative error halved about every {v['hl']} years (95% interval {v['hl_ci']} years)."),
             ("how", "The horizontal axis is the year recorded in the list; the vertical axis is the relative error (1%–100%) on a log scale (1% to 10% is as far as 10% to 100%). "
                     "The thick gray bar is the range of the middle half of that year's estimates (the interquartile range) and the dot the median. Lower means that year's estimates stated smaller errors. "
                     f"Years with fewer than three estimates ({v['n_small']} of {v['n_years']} years) show only an × at the bottom, without a bar (the count is in the tooltip)."),
             ("one", f"In {y['year']} the {y['n']} estimates have a median relative error of {y['med']}%, with the middle half between {y['q1']}% and {y['q3']}%."),
             ("mis", "Lower means \"stated a narrower error\", not that the value was closer to the truth (more precise in fact). Whether the stated errors covered the distance to the references is what H3 counts. "
                     "Whether an error is statistical only or includes systematics may differ from row to row; the list does not say. " + _DATE_EN),
             ("terms", "Relative error: quoted error ÷ the H0 value. Interquartile range: the middle half. Half-life: with log₂ of the yearly median fitted to the year by a straight line, the years it takes to halve. Log axis: equal distances stand for equal ratios.")])


def urel_points(lang, v):
    """v: n, hl, hl_ci, lo (year, h0, err, pct), ex (year, h0, err, pct)."""
    lo, ex = v["lo"], v["ex"]
    if lang == "ko":
        return ("표 A2, 추정마다의 상대 오차",
                "표 A2 의 추정 하나마다 점 하나로 상대 오차(인용 오차 ÷ H0)를 그린 그림이다.",
                [("glance", f"{v['n']}건의 해별 중앙값으로 보면 상대 오차는 약 {v['hl']}년마다 절반이 되었다(95% 구간 {v['hl_ci']}년). 가장 작은 것은 {lo['year']}년 {lo['h0']} ± {lo['err']}({lo['pct']}%)다."),
                 ("how", "가로는 연도, 세로는 상대 오차이고 세로 눈금은 로그 축이다. 점 하나가 표 A2 의 행 하나이고, 위아래 오차가 다르면 평균을 썼다. 아래일수록 오차를 작게 적었다는 뜻이다."),
                 ("one", f"{ex['year']}년의 점은 H0 = {ex['h0']} ± {ex['err']} 이라는 추정으로, 오차가 값의 {ex['pct']}%다."),
                 ("mis", "아래에 있다고 참값에 더 가깝다는 뜻은 아니다(위 그림의 풀이와 같다). " + _DATE_KO)])
    return ("Table A2: relative error of each estimate",
            "the relative error (quoted error ÷ H0) of each estimate in Table A2, one dot per row.",
            [("glance", f"On the yearly medians of the {v['n']} rows, the relative error halved about every {v['hl']} years (95% interval {v['hl_ci']} years). The smallest is {lo['year']}, {lo['h0']} ± {lo['err']} ({lo['pct']}%)."),
             ("how", "The horizontal axis is the year and the vertical axis the relative error, on a log scale. Each dot is one row of Table A2; where the upper and lower errors differ, their mean is used. Lower means a smaller stated error."),
             ("one", f"The {ex['year']} dot is the estimate H0 = {ex['h0']} ± {ex['err']}: an error of {ex['pct']}% of the value."),
             ("mis", "A lower dot does not mean a value closer to the truth (as for the chart above). " + _DATE_EN)])


def rates(lang, v):
    """v: hp_m2, hr_m2, fp_m2, fr_m2, n_bad, n_all, ex (n, k, pct)."""
    e = v["ex"]
    if lang == "ko":
        return ("기준값에서 벗어난 추정의 비율",
                "추정값이 두 기준값에서 인용 오차의 몇 배 떨어졌는지(z)로 네 가지 비율을 세어, 정규분포의 기대와 견준 그림이다.",
                [("glance", f"Planck 2018 기준으로 Huchra 목록의 {v['hp_m2']}%, Riess 외 2022 기준으로 {v['hr_m2']}% 가 인용 오차의 2배 밖에 있다(정규 기대 4.6%). 표 A2 는 {v['fp_m2']}% 와 {v['fr_m2']}% 다. "
                                    + (f"점 {v['n_all']}개 모두 정규 기대에서 같은 쪽으로 벗어난다. 앞의 세 비율은 기대보다 높고 사분위 비율은 기대보다 낮다." if v["n_bad"] == v["n_all"] else f"점 {v['n_all']}개 가운데 {v['n_bad']}개가 앞의 세 비율은 기대보다 높고 사분위 비율은 기대보다 낮은 쪽에 놓인다.")),
                 ("how", "네 묶음이 지표 하나씩이다(1σ 놓침, 2σ 놓침, 놀람 지수, 사분위 지수). 묶음마다 점 넷: 앞의 둘은 Huchra 목록(원), 뒤의 둘은 표 A2(마름모)이고, 색은 기준값(초록 Planck 2018, 주황 Riess 외 2022)이다. "
                         "세로선은 95% 구간, 짧은 회색 점선은 정규분포 기대다. 앞의 세 지표는 점이 점선보다 위일수록 자주 벗어났다는 뜻이고, 사분위 지수만은 방향이 반대여서, 점선(50%)보다 아래일수록 인용 오차의 약 3분의 2 안에 든 추정이 정규 기대보다 적다는 뜻이다(그림 아래 굵은 글자)."),
                 ("one", f"2σ 놓침 묶음의 초록 원 {e['pct']}%는 Huchra 목록 추정 {e['n']}건 가운데 {e['k']}건이 Planck 2018 값에서 자기 인용 오차의 2배보다 멀리 떨어져 있다는 뜻이다."),
                 ("mis", "인용 오차가 어떤 신뢰수준(1σ 인지, 통계 오차만인지)으로 적혔는지 목록에 없으므로, 이 벗어남을 곧 「오차를 너무 좁게 적었다」로 읽을 수는 없다. 1σ·2σ 는 「인용 오차의 1배·2배」라는 계산의 이름이다. 같은 쪽으로 벗어난 점 16개도 서로 독립인 증거 16개가 아니다(같은 추정을 네 지표·두 기준으로 다시 센 것). z 에는 추정의 인용 오차만 들어가고 기준값 자체의 오차는 넣지 않았다. 같은 팀·같은 자료를 쓴 추정이 여러 건 있어 서로 독립이 아니고, 연도 군집 부트스트랩은 그 일부만 반영한다. " + _REF_KO),
                 ("terms", "z = (기준값 − 추정값) ÷ 그 추정의 인용 오차. 1σ·2σ 놓침 = |z| 가 1·2를 넘는 비율. 놀람 지수 = |z| > 2.326, 곧 오차를 약 2.3배로 넓힌 범위 밖의 비율(정규분포라면 98%가 이 범위 안에 들어 기대 2%). "
                           "사분위 지수 = |z| < 0.674, 곧 오차의 약 3분의 2 안에 든 비율(정규분포라면 가운데 50%가 들어 기대 50%). 연도 군집 부트스트랩 95% 구간 = 목록에 적힌 연도 단위의 묶음을 무작위로 다시 뽑아 같은 계산을 되풀이했을 때 결과의 가운데 95%.")])
    return ("Shares of estimates away from the references",
            "four shares counted from how many quoted errors each estimate lay from each reference (z), set against the normal distribution.",
            [("glance", f"Against Planck 2018, {v['hp_m2']}% of Huchra's list lies beyond twice the quoted error, against Riess et al. 2022 {v['hr_m2']}% (normal: 4.6%); Table A2 gives {v['fp_m2']}% and {v['fr_m2']}%. "
                        + (f"All {v['n_all']} marks depart from the normal expectation the same way: the first three shares are above it and the interquartile share below it." if v["n_bad"] == v["n_all"] else f"{v['n_bad']} of the {v['n_all']} marks lie above the expectation for the first three shares or below it for the interquartile share.")),
             ("how", "Each of the four groups is one index (1σ miss, 2σ miss, surprise index, interquartile index). Each group has four marks: the first two are Huchra's list (circles), the last two Table A2 (diamonds); the colour is the reference (green Planck 2018, orange Riess et al. 2022). "
                     "Vertical lines are 95% intervals and the short gray dashed line the normal expectation. For the first three indices a mark above its dashed line means values fell outside more often than expected; the interquartile index alone runs the other way: a mark below its dashed line (50%) means fewer estimates lay within about two-thirds of their quoted error than a normal distribution expects (bold text under the chart)."),
             ("one", f"The green circle of the 2σ-miss group, {e['pct']}%, means that {e['k']} of the {e['n']} estimates in Huchra's list lie more than twice their own quoted error from the Planck 2018 value."),
             ("mis", "The lists do not say at what confidence level the errors were quoted (1σ or not, statistical only or not), so these departures cannot be read as \"the errors were quoted too narrow\". 1σ and 2σ name the calculation, one and two quoted errors. The 16 marks departing the same way are not 16 independent pieces of evidence (the same estimates counted for four indices and two references). Only the estimate's quoted error enters z; the uncertainty of the reference itself does not. Several estimates share a team or data and are not independent; the year-cluster bootstrap handles only part of that. " + _REF_EN),
             ("terms", "z = (reference − estimate) ÷ the estimate's quoted error. 1σ and 2σ miss: the shares with |z| above 1 and 2. Surprise index: |z| > 2.326, outside about 2.3 times the error (a range that holds 98% under a normal distribution, so 2% expected). "
                       "Interquartile index: |z| < 0.674, inside about two-thirds of the error (the middle 50% under a normal distribution, so 50% expected). Year-cluster bootstrap 95% interval: bundles of rows by recorded year are drawn again at random and the count repeated; the middle 95% of the results.")])


def zpanels(lang, v):
    """v: p (n, n2, up), r (n, n2, up), ex (year, h0, err, z), clipped."""
    p, r, e = v["p"], v["r"], v["ex"]
    if lang == "ko":
        return ("표 A2 추정의 z, 두 기준값에 대해",
                "표 A2 의 추정마다 두 기준값에서의 z 를 연도별로 찍은 그림이다(위 Planck 2018, 아래 Riess 외 2022).",
                [("glance", f"|z| 가 2를 넘는 추정은 Planck 2018 기준 {p['n']}건 중 {p['n2']}건, Riess 외 2022 기준 {r['n']}건 중 {r['n2']}건이다. 위쪽(기준값보다 작은 추정)에 놓인 것은 각각 {p['up']}건, {r['up']}건이다."),
                 ("how", "점 하나가 추정 하나다. 세로는 z = (기준값 − 추정값) ÷ 그 추정의 인용 오차이고 고른 간격이다. 추정이 기준값보다 작으면 위(양수), 크면 아래(음수)에 놓인다. "
                         "±1 점선 안이면 그 추정의 오차 막대가 기준값에 닿고, ±2 점선 밖이면 오차의 2배보다 멀다(눈금 글자는 0과 ±2, ±4, ±8에만 적었다). "
                         f"±8 을 넘는 값은 가장자리에 세모로 잘랐다({v['clipped']}건)."),
                 ("one", f"{e['year']}년 추정 {e['h0']} ± {e['err']}은 위 그림에서 z = (67.36 − {e['h0']}) ÷ {e['err']} = {e['z']}로 계산된다. {e['ko']}"),
                 ("mis", "위 그림에서는 2018년의 반올림 Planck 값 행을 뺐다(자기 자신과 견주는 셈이어서). 위아래 오차가 다른 행은 평균을 썼다. 같은 추정이 두 그림에 다른 높이로 나오는 것은 기준값이 달라서다. " + _REF_KO)])
    return ("z of the Table A2 estimates against the two references",
            "for each estimate in Table A2, its z against each reference by year (top: Planck 2018; bottom: Riess et al. 2022).",
            [("glance", f"|z| exceeds 2 for {p['n2']} of {p['n']} estimates against Planck 2018 and {r['n2']} of {r['n']} against Riess et al. 2022; {p['up']} and {r['up']} respectively lie in the upper half (below the reference)."),
             ("how", "Each dot is one estimate. The vertical axis is z = (reference − estimate) ÷ the estimate's quoted error, evenly spaced. An estimate below the reference sits above zero, one above it below zero. "
                     "Within the dashed lines at ±1 its error bar reaches the reference; beyond ±2 it lies more than twice its error away (tick labels only at 0, ±2, ±4 and ±8). "
                     f"Values beyond ±8 are clipped to triangles at the edge ({v['clipped']})."),
             ("one", f"The {e['year']} estimate {e['h0']} ± {e['err']} has, in the upper panel, z = (67.36 − {e['h0']}) ÷ {e['err']} = {e['z']}: {e['en']}"),
             ("mis", "The upper panel leaves out the 2018 row with the rounded Planck value (it would be compared with itself). Rows with unequal upper and lower errors use their mean. The same estimate appears at different heights in the two panels because the references differ. " + _REF_EN)])


def tail(lang, v):
    """v: ref, n, r2, k2, nu, s, zmax."""
    if lang == "ko":
        return (f"표 A2 의 꼬리, {v['ref']} 기준",
                f"표 A2 의 추정이 {v['ref']} 값에서 인용 오차의 몇 배 떨어졌는지(|z|), 그 크기를 넘은 추정의 비율을 정규분포와 견준 그림이다.",
                [("glance", f"|z| 가 2를 넘는 추정은 {v['n']}건 중 {v['k2']}건({v['r2']}%)으로 정규분포 기대 4.55%보다 많다. 오른쪽에서 관측 선이 정규분포 곡선보다 높이 떠 있다."),
                 ("how", "가로는 |z| = |기준값 − 추정값| ÷ 그 추정의 인용 오차, 세로는 |z| 가 가로 값을 넘는 추정의 비율이고 눈금 한 칸이 10배인 로그 축이다. 모든 선은 왼쪽 위(100%)에서 시작해 오른쪽으로 내려간다. "
                         "파란 계단 선이 관측, 회색 점선이 정규분포(z 가 표준정규분포를 따를 때의 기대), 기준값 색의 선이 관측에 맞춘 Student-t 분포다. 파란 점 셋은 |z| > 1·2·3 의 관측 비율이다. 오른쪽에서 높이 떠 있을수록 기준값에서 크게 벗어난 추정이 잦다."),
                 ("one", f"가로 2 자리의 파란 점 {v['r2']}%는 {v['n']}건 가운데 {v['k2']}건이 {v['ref']} 값에서 자기 인용 오차의 2배보다 멀다는 뜻이다."),
                 ("mis", f"Huchra 목록은 집계만 싣는 자료라 이 그림을 그리지 않는다. Student-t 는 z = 0 인 행을 빼고 맞췄다. 관측 선은 가장 큰 |z|({v['zmax']}) 또는 가로 7에서 끝난다. " + _REF_KO),
                 ("terms", f"Student-t 분포 = 정규분포보다 꼬리가 두꺼운 분포. 자유도 ν 가 작을수록 꼬리가 두껍다. 여기서 맞춘 값은 ν = {v['nu']}, 척도 s = {v['s']}(가로를 늘이고 줄이는 배율)다. 로그 축 = 같은 간격이 같은 배수를 뜻하는 눈금.")])
    return (f"Tail of Table A2 against {v['ref']}",
            f"the share of Table A2 estimates lying more than a given number of quoted errors (|z|) from the {v['ref']} value, set against the normal distribution.",
            [("glance", f"{v['k2']} of {v['n']} estimates ({v['r2']}%) have |z| above 2, more than the normal expectation of 4.55%. On the right the observed line lies well above the normal curve."),
             ("how", "The horizontal axis is |z| = |reference − estimate| ÷ the estimate's quoted error; the vertical axis is the share of estimates whose |z| exceeds that value, on a log axis (one step per factor of ten). Every line starts at the top left (100%) and falls to the right. "
                     "The blue step line is observed, the gray dashed line the normal distribution (the expectation if z followed a standard normal distribution), and the line in the reference's colour a Student-t distribution fitted to the observations. The three blue dots are the observed shares above 1, 2 and 3. The higher a line stays on the right, the more often estimates lay far from the reference."),
             ("one", f"The blue dot at 2 on the horizontal axis, {v['r2']}%, means that {v['k2']} of the {v['n']} estimates lie more than twice their own quoted error from the {v['ref']} value."),
             ("mis", f"Huchra's list is published only in aggregate, so it has no such chart. The Student-t is fitted without rows where z = 0. The observed line ends at the largest |z| ({v['zmax']}) or at 7 on the horizontal axis. " + _REF_EN),
             ("terms", f"Student-t distribution: like the normal but with heavier tails; the smaller its degrees of freedom ν, the heavier the tails. The fitted values here are ν = {v['nu']} and scale s = {v['s']} (a factor that stretches the horizontal axis). Log axis: equal distances stand for equal ratios.")])
