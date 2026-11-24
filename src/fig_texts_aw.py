# -*- coding: utf-8 -*-
"""1.3.9: chart explanations of the atomic-weights chapter. Numbers come in v, computed by aw_site.py from the data."""
from __future__ import annotations

from fig_explain import about, frac, sci, symlog_misread, symlog_sentence, symlog_term

_CIAAW_KO = "CIAAW 의 불확도는 표준불확도(1σ)가 아니라, 정상 물질의 원자량이 매우 확실하게 들어갈 것으로 보는 넓은 범위(확장 범위)다."
_CIAAW_EN = "CIAAW's uncertainty is not a standard uncertainty (1σ) but a wide range within which the atomic weight of normal materials is expected to lie with great certitude (an expanded range)."


def zplot(lang, v):
    """v: n, out, out_pct, dis, dis_list, med, half, clipped, clipped_txt, ex (dict: sym, y0, y1, prev, new, z)."""
    e = v["ex"]
    if lang == "ko":
        return ("개정마다 직전 값에서 움직인 크기",
                "직전 권고에 불확도가 있었던 개정마다, 새 값이 직전 값에서 직전 불확도의 몇 배만큼 움직였는지(z_옛)를 그린 그림이다.",
                [("glance", f"{v['n']}건 가운데 {v['out']}건({v['out_pct']}%)에서 새 값이 직전 범위 밖(±1 점선 밖)에 놓였다. |z_옛| 의 중앙값은 {v['med']}이고, {v['half']}%가 0.5 이하다."),
                 ("how", "점 하나가 개정 하나다. 가로는 새 값을 권고한 해, 세로는 z_옛 = (새 값 − 직전 값) ÷ 직전 불확도다. 0보다 위면 값이 올라간 개정, 아래면 내려간 개정이다. "
                         "±1 의 회색 점선 사이에 있으면 새 값이 직전 권고의 범위 안에 놓였다는 뜻이다. 주황 점은 범위 밖으로 옮겨 간 개정, 파란 반투명 점은 범위 안의 개정이다. "
                         f"세로 눈금은 고른 간격이고, ±8 을 넘는 값은 가장자리에 주황 세모로 붙이고 원소 기호와 z 를 적었다({v['clipped_txt']})."),
                 ("one", f"{e['sym']}의 {e['y1']}년 개정({e['y0']}년 {e['prev']} → {e['y1']}년 {e['new']})은 값이 직전 불확도의 {e['az']}배만큼 {'내려가' if e['z'].startswith('−') else '올라가'} 직전 범위 밖에 놓였다(z_옛 = {e['z']})."),
                 ("mis", _CIAAW_KO + " 그래서 ±1 은 1σ 가 아니라 그 넓은 범위의 끝이고, 물리 상수 장의 z 와 같은 눈금으로 견주지 않는다. "
                         f"「직전 범위 밖」(기준 ①, {v['out']}건)과 「두 범위가 아예 겹치지 않음」(기준 ②, {v['dis']}건: {v['dis_list']})은 다른 기준이다. 직전 권고에 불확도가 없던 개정은 그림에 없다."),
                 ("terms", "z_옛 = (새 값 − 직전 값) ÷ 직전 권고의 불확도. 직전 범위 = 직전 값 ± 직전 불확도. 확장 범위 = CIAAW 가 원자량 뒤 괄호에 붙이는 넓은 범위(예: 65.38(2) 의 0.02).")])
    return ("How far each revision moved from the previous value",
            "for each revision whose previous recommendation had an uncertainty, how many times that uncertainty the new value moved from the previous one (z_old).",
            [("glance", f"In {v['out']} of {v['n']} revisions ({v['out_pct']}%) the new value lies outside the previous range (beyond the dashed lines at ±1). The median |z_old| is {v['med']}, and {v['half']}% are 0.5 or less."),
             ("how", "Each mark is one revision. The horizontal axis is the year of the new recommendation; the vertical axis is z_old = (new value − previous value) ÷ previous uncertainty. Above 0 the value was revised upward, below 0 downward. "
                     "Between the gray dashed lines at ±1 the new value lies within the range of the previous recommendation. Orange dots are revisions that moved out of that range, translucent blue dots revisions that stayed inside. "
                     f"The axis is evenly spaced; values beyond ±8 are drawn at its edge as orange triangles labelled with the element symbol and z ({v['clipped_txt_en']})."),
             ("one", f"The {e['y1']} revision of {e['sym']} changed the {e['y0']} value {e['prev']} to {e['new']}, z_old = {e['z']}: the new value lies {e['az']} times the previous uncertainty from the previous value, outside the previous range."),
             ("mis", _CIAAW_EN + " So ±1 is the edge of that wide range, not 1σ, and these z are not read on the same scale as those of the physical-constants chapter. "
                     f"\"Outside the previous range\" (criterion 1, {v['out']}) and \"the two ranges do not overlap\" (criterion 2, {v['dis']}: {v['dis_list']}) are different criteria. Revisions whose previous recommendation had no uncertainty are not in the chart."),
             ("terms", "z_old = (new value − previous value) ÷ uncertainty of the previous recommendation. Previous range: previous value ± previous uncertainty. Expanded range: the wide range CIAAW prints in parentheses after an atomic weight (the 0.02 in 65.38(2)).")])


def bars_a1(lang, v):
    """v: top_dec, top_n, total, last_year, d_ex, d_ex_n."""
    if lang == "ko":
        return ("10년마다의 권고·개정 기록 수",
                "표준 원자량이 10년마다 몇 번 권고·개정되었는지 센 막대그래프다.",
                [("glance", f"기록 {v['total']}건 가운데 가장 많은 10년은 {v['top_dec']}년대({v['top_n']}건)다."),
                 ("how", "막대 하나가 10년이다(예: 1960 = 1960~1969년). 막대 높이는 그 10년 동안의 기록 수이고, 원소가 처음 권고된 기록과 철회 기록도 한 건으로 센다. 막대 위에 커서를 대면 수가 보인다."),
                 ("one", f"{v['d_ex']} 막대는 {v['d_ex']}~{int(v['d_ex']) + 9}년에 원소별 권고·개정 기록이 {v['d_ex_n']}건이라는 뜻이다."),
                 ("mis", f"막대 높이는 원소 수가 아니라 기록 수다. 한 원소가 같은 10년에 두 번 바뀌면 두 건이다. 자료는 {v['last_year']}년까지여서 2020 막대는 2020~{v['last_year']}년만 센다."),
                 ("terms", "권고·개정 기록 = CIAAW 원자량표에서 한 원소의 값이나 표기가 새로 정해진 한 번.")])
    return ("Recommendations and revisions per decade",
            "how many times standard atomic weights were recommended or revised in each decade.",
            [("glance", f"Of the {v['total']} records, the most fall in the {v['top_dec']}s ({v['top_n']})."),
             ("how", "Each bar is a decade (1960 = 1960–1969). Its height is the number of records in that decade; an element's first recommendation and a withdrawal also count as one record each. Rest the pointer on a bar to see the number."),
             ("one", f"The {v['d_ex']} bar means {v['d_ex_n']} recommendations or revisions of single elements in {v['d_ex']}–{int(v['d_ex']) + 9}."),
             ("mis", f"The height counts records, not elements: an element revised twice in a decade counts twice. The data end in {v['last_year']}, so the 2020 bar covers only 2020–{v['last_year']}."),
             ("terms", "Record: one occasion on which the value or notation of one element was set anew in CIAAW's table.")])


def bars_a4(lang, v):
    """v: n_saw, top_dec, top_n, old_n, last_year."""
    if lang == "ko":
        return ("마지막 개정 연도별 원소 수",
                f"표준 원자량이 있는 원소 {v['n_saw']}개를, 값이 마지막으로 바뀐 10년에 따라 센 막대그래프다.",
                [("glance", f"가장 많은 원소가 마지막으로 바뀐 10년은 {v['top_dec']}년대({v['n_saw']}개 가운데 {v['top_n']}개)다. 1960년대 이후로 한 번도 바뀌지 않은 원소는 {v['old_n']}개다."),
                 ("how", "막대 하나가 10년이고, 높이는 마지막 기록이 그 10년에 있는 원소의 수다. 막대 높이를 모두 더하면 원소 수가 된다."),
                 ("mis", f"마지막 개정이 오래되었다고 그 값이 정확하다는 뜻은 아니다. 다시 잴 까닭이 없었거나 새 측정이 범위를 바꾸지 않았다는 뜻일 수 있다. 2020 막대는 {v['last_year']}년까지다. 표준 원자량이 없는 방사성 원소는 세지 않았다.")])
    return ("Elements by decade of latest revision",
            f"the {v['n_saw']} elements with a standard atomic weight, counted by the decade in which their value last changed.",
            [("glance", f"The largest group last changed in the {v['top_dec']}s ({v['top_n']} of {v['n_saw']}). {v['old_n']} have not changed since the 1960s."),
             ("how", "Each bar is a decade and its height the number of elements whose latest record falls in it; the heights add up to the number of elements."),
             ("mis", f"An old latest revision does not mean the value is more accurate; there may have been no reason to measure again, or new measurements did not change the range. The 2020 bar runs to {v['last_year']}. Radioactive elements without a standard atomic weight are not counted.")])


def element(lang, v):
    """v: name, n_rec, n_pts, n_unc, n_none, n_int, n_exact, lt_txt, far (dict yr, dv, txt), first (dict yr, dv, txt), ref_txt, ref_kind."""
    f, far = v["first"], v["far"]
    ko = lang == "ko"
    if f is None:   # every plotted value equals the reference
        f = far = dict(yr="", dv=0, txt="")
    if ko:
        fw, fr = frac(f["dv"], "ko")
        aw, ar = frac(far["dv"], "ko")
        refnote = {"interval": "구간의 가운데", "none_saw": "마지막 값(지금은 표준 원자량이 없다)", "value": "현재 값"}[v["ref_kind"]]
        kinds = ", ".join(x for x in [f"불확도가 붙은 값 {v['n_unc']}" if v["n_unc"] else "", f"불확도 없는 값 {v['n_none']}" if v["n_none"] else "",
                                     f"구간 {v['n_int']}" if v["n_int"] else "", f"정확한 기준값 {v['n_exact']}" if v["n_exact"] else ""] if x)
        now = "마지막 값" if v["ref_kind"] == "none_saw" else "현재 값"
        return (f"{v['name']} — 권고마다 {now}에서 떨어진 정도",
                f"{v['name']}의 원자량이 권고될 때마다 {now}에서 값에 견주어 얼마나 떨어져 있었는지 그린 그림이다.",
                [("glance", f"기록 {v['n_rec']}건 가운데 그림에 놓인 것은 {v['n_pts']}건({kinds})이다." + (f" 기준값에서 가장 멀리 떨어진 것은 {far['yr']}년 값으로, 값의 {about('ko', ar)}{aw}만큼 {'컸다' if far['dv'] > 0 else '작았다'}." if far["dv"] else " 그림에 놓인 값은 모두 기준값과 같다.")),
                 ("how", f"가로는 연도, 세로는 (그때 값 − 기준값) ÷ 기준값이고 기준값은 {refnote}이다. 회색 0의 점선이 기준값이고 위는 그보다 큰 값이다. "
                         + " ".join(x for x in ["속이 찬 파란 원에 붙은 세로 막대는 CIAAW 가 붙인 불확도(확장 범위)다." if v["n_unc"] else "",
                                                "파란 ×는 불확도 없이 적은 값이다." if v["n_none"] else "", "주황 테두리 상자는 하한~상한으로 적은 구간이다." if v["n_int"] else "",
                                                "네모는 정확한 기준값이다." if v["n_exact"] else ""] if x) + " "
                         "세로 점선 「1961 기준 변경」은 원자량의 척도가 산소 = 16에서 ¹²C = 12로 바뀐 해이고, 그보다 앞선 산소 = 16 척도의 값은 ¹²C 척도로 환산해 그렸다. "
                         + symlog_sentence("ko", v["lt_txt"])),
                 ("one", (f"{f['yr']}년 기록({f['txt']})을 ¹²C 척도로 바꾼 값은" if f["yr"] and int(f["yr"]) < 1961 else f"{f['yr']}년 기록({f['txt']})은") + f" 기준값보다 값의 {about('ko', fr)}{fw}만큼 {'컸다' if f['dv'] > 0 else '작았다'}." if f["dv"] else ""),
                 ("mis", _CIAAW_KO + " 그래서 이 막대는 상수 면의 ±1σ 막대와 같은 눈금으로 읽지 않는다. 구간은 불확도가 아니라 정상 물질에서 실제로 나타나는 값의 범위다. " + symlog_misread("ko")),
                 ("terms", "표준 원자량 = 지구의 정상 물질에서 그 원소 원자들의 평균 질량을 ¹²C 원자 질량의 1/12 로 나눈 값. 확장 범위 = CIAAW 가 값 뒤 괄호에 붙이는 넓은 범위. "
                           "구간 = 2009년부터 동위원소 조성의 자연 변동이 큰 원소에 쓰는 [하한, 상한] 표기. ¹²C 척도 = 탄소-12 원자 질량을 정확히 12로 두는 원자량의 눈금. " + symlog_term("ko"))])
    fw, fr = frac(f["dv"], "en")
    aw, ar = frac(far["dv"], "en")
    refnote = {"interval": "the middle of the interval", "none_saw": "the last value (it has no standard atomic weight today)", "value": "the current value"}[v["ref_kind"]]
    kinds = ", ".join(x for x in [f"{v['n_unc']} with an uncertainty" if v["n_unc"] else "", f"{v['n_none']} without one" if v["n_none"] else "",
                                  f"{v['n_int']} interval{'s' if v['n_int'] != 1 else ''}" if v["n_int"] else "", f"{v['n_exact']} exact reference" if v["n_exact"] else ""] if x)
    now = "the last value" if v["ref_kind"] == "none_saw" else "the current value"
    return (f"{v['name']}: distance of each recommendation from {now}",
            f"how far each recommended atomic weight of {v['name_lc']} lay from {now}, relative to that value.",
            [("glance", f"Of {v['n_rec']} records, {v['n_pts']} are drawn ({kinds})." + (f" The farthest from the reference is the {far['yr']} value, {about('en', ar)}{aw} of the value {'above' if far['dv'] > 0 else 'below'} it." if far["dv"] else " Every drawn value equals the reference.")),
             ("how", f"The horizontal axis is the year; the vertical axis is (value then − reference) ÷ reference, where the reference is {refnote}. The gray dashed zero line is the reference; above it are larger values. "
                     + " ".join(x for x in ["A vertical bar on a filled blue circle is the uncertainty CIAAW attached (an expanded range)." if v["n_unc"] else "",
                                            "A blue × is a value given without an uncertainty." if v["n_none"] else "", "An orange outlined box is an interval from lower to upper bound." if v["n_int"] else "",
                                            "A square is an exact reference value." if v["n_exact"] else ""] if x) + " "
                     "The dotted vertical line \"1961 scale change\" marks the year the scale of atomic weights changed from oxygen = 16 to ¹²C = 12; earlier values on the oxygen = 16 scale are drawn converted to the ¹²C scale. "
                     + symlog_sentence("en", v["lt_txt"])),
             ("one", f"The {f['yr']} record {f['txt']}" + (", once converted to the ¹²C scale," if f["yr"] and int(f["yr"]) < 1961 else "") + f" lay {about('en', fr)}{fw} of the value {'above' if f['dv'] > 0 else 'below'} the reference." if f["dv"] else ""),
             ("mis", _CIAAW_EN + " So these bars are not read on the same scale as the ±1σ bars of the constant pages. An interval is not an uncertainty but the range of values actually found in normal materials. " + symlog_misread("en")),
             ("terms", "Standard atomic weight: the mean mass of an element's atoms in normal terrestrial material, relative to 1/12 of the mass of a ¹²C atom. Expanded range: the wide range CIAAW prints in parentheses after a value. "
                       "Interval: the [lower, upper] notation used since 2009 for elements whose isotopic composition varies widely in nature. ¹²C scale: atomic weights measured with the carbon-12 atom set at exactly 12. " + symlog_term("en"))])
