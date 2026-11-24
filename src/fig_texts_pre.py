# -*- coding: utf-8 -*-
"""1.3.9: explanation of the five-constant chart of the before-CODATA chapter. Numbers come in v from pre_site.py."""
from __future__ import annotations

from fig_explain import symlog_misread, symlog_sentence, symlog_term


def chart(lang, v):
    """v: n_pre, n_cod, h29_pct, h29_ppm, zh29, n_out (pre-CODATA values whose bar misses the 2022 value), n_pre_all."""
    if lang == "ko":
        return ("다섯 상수, 1929~2018년 값과 2022 판 값의 차이",
                "CODATA 이전 검토(1929~1963)와 CODATA 판(1969~2018)의 다섯 상수 값이 2022 판 값에서 얼마나 떨어져 있었는지, 상수마다 한 칸씩 그린 그림이다.",
                [("glance", f"CODATA 이전 검토의 값 {v['n_pre_all']}개 가운데 {v['n_out']}개는 오차 막대가 2022 판 값(0의 선)에 닿지 않는다. 1929년 Birge 의 h 는 2022 판 값보다 {'약 ' if v['h29_round'] else ''}{v['h29_pct']}%({v['h29_ppm']} ppm) 작았다."),
                 ("how", "칸 하나가 상수 하나다(α⁻¹, h, e, mₑ, N_A — 이름은 칸 왼쪽 위). 가로는 연도, 세로는 (그때 값 − 2022 판 값) ÷ 2022 판 값을 ppm(100만분의 1) 단위로 나타낸 것이다. 0의 선이 2022 판 값이고 위는 그보다 큰 값이다. "
                         "파란 점은 CODATA 이전 검토, 초록 점은 CODATA 판(1969~2018)이고, 세로 막대는 ± 표준불확도다. 확률오차로 적은 검토는 1.4826배 해서 표준불확도로 바꿨다. "
                         + symlog_sentence("ko", "1 ppm") + " 눈금은 ±10, ±100, ±10³, ±10⁴ ppm 이다."),
                 ("one", f"h 칸 1929년의 파란 점은 Birge 의 값이 2022 판 값보다 {v['h29_ppm']} ppm, 곧 {'약 ' if v['h29_round'] else ''}{v['h29_pct']}% 작았다는 뜻이다. 그 차이는 Birge 가 붙인 오차(표준불확도로 바꾼 것)의 {v['zh29']}배다."),
                 ("mis", symlog_misread("ko") + " 2022 판에서 h·e·N_A 는 정의값이어서 0의 선은 측정값이 아니라 약속으로 정한 값이다. 그림에는 2022 판 점이 없다. "
                         "1957 단행본은 1955년 조정값을 그대로 다시 실어서, 두 해의 점은 같은 높이에 놓인다."),
                 ("terms", "ppm = parts per million, 100만분의 1. 확률오차(probable error) = 옛 문헌이 쓰던 오차 표기로, 참값이 그 안에 있을 확률이 반반인 반폭. 표준불확도로 바꾸려면 1.4826배 한다. "
                           "표준불확도 = 참값이 대략 이 범위 안에 있다는 오차 막대의 반폭(±1σ). " + symlog_term("ko"))])
    return ("Five constants: values 1929–2018 against the 2022 value",
            "how far the values of five constants in the reviews before CODATA (1929–1963) and in the CODATA editions (1969–2018) lay from the 2022 value, one panel per constant.",
            [("glance", f"Of the {v['n_pre_all']} values from the reviews before CODATA, {v['n_out']} have an error bar that does not reach the 2022 value (the zero line). Birge's 1929 h was {'about ' if v['h29_round'] else ''}{v['h29_pct']}% ({v['h29_ppm']} ppm) below the 2022 value."),
             ("how", "Each panel is one constant (α⁻¹, h, e, mₑ, N_A; the name at its top left). The horizontal axis is the year; the vertical axis is (value then − 2022 value) ÷ 2022 value in ppm (parts per million). The zero line is the 2022 value; above it are larger values. "
                     "Blue dots are the reviews before CODATA, green dots the CODATA editions (1969–2018), and vertical bars ± one standard uncertainty; reviews that gave probable errors were converted by multiplying by 1.4826. "
                     + symlog_sentence("en", "1 ppm") + " The ticks are at ±10, ±100, ±10³ and ±10⁴ ppm."),
             ("one", f"The blue dot at 1929 in the h panel means Birge's value was {v['h29_ppm']} ppm, that is {'about ' if v['h29_round'] else ''}{v['h29_pct']}%, below the 2022 value: {v['zh29']} times the error he gave, converted to a standard uncertainty."),
             ("mis", symlog_misread("en") + " In 2022 h, e and N_A are exact, so the zero line is a value fixed by agreement, not a measurement; the chart has no 2022 marks. "
                     "The 1957 book reprints the 1955 adjustment unchanged, so the marks of those two years sit at the same height."),
             ("terms", "ppm: parts per million. Probable error: the older notation for an error, the half-width with even odds of containing the true value; multiplying by 1.4826 turns it into a standard uncertainty. "
                       "Standard uncertainty: the half-width (±1σ) of an error bar saying the true value is probably inside it. " + symlog_term("en"))])
