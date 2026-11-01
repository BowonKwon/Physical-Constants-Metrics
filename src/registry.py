# -*- coding: utf-8 -*-
"""Metric registry: every published metric, in Korean and English.
The site builder reads this; nothing about a metric is defined elsewhere.
Numbers in braces are filled in by build_site.py from data/derived/*.csv.

Fields: id, file (derived CSV), ko/en: name, short, definition, formula, denominator, reading, caveat
"""

EDITIONS = [1969, 1973, 1986, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
LATEST = 2022

SOURCES = {'codata': {'ko': 'CODATA 기본 물리 상수 권고값, 1973·1986·1998·2002·2006·2010·2014·2018·2022 판. 미국 국립표준기술연구원(NIST)이 판별로 공개한 표에서 옮겼다. 1998 판 이후는 NIST의 ASCII '
                  '표, 1973·1986 판은 논문의 표(1973: Cohen & Taylor, J. Phys. Chem. Ref. Data 2, 663; 1986: Cohen & Taylor, J. Res. Natl. Bur. Stand. '
                  '92(2), 1987).',
            'en': 'CODATA recommended values of the fundamental physical constants, editions 1973, 1986, 1998, 2002, 2006, 2010, 2014, 2018 and '
                  "2022, taken from the tables NIST publishes for each edition: NIST's ASCII tables from 1998 on, and the published tables for 1973 "
                  '(Cohen & Taylor, J. Phys. Chem. Ref. Data 2, 663) and 1986 (Cohen & Taylor, J. Res. Natl. Bur. Stand. 92(2), 1987).',
            'url': 'https://physics.nist.gov/cuu/Constants/'},
 'tpl1969': {'ko': 'CODATA 이전 조정값 하나를 함께 싣는다: B. N. Taylor, W. H. Parker, D. N. Langenberg (1969), Rev. Mod. Phys. 41, 375, 표 XXXII. NIST가 「역사 참고」로 '
                   '같은 자리에 제공한다.',
             'en': 'One pre-CODATA adjustment is included: B. N. Taylor, W. H. Parker and D. N. Langenberg (1969), Rev. Mod. Phys. 41, 375, table '
                   'XXXII, which NIST provides alongside the CODATA archive for historical reference.',
             'url': 'https://physics.nist.gov/cuu/Constants/archive1969.html'}}

METRICS = [{'id': 'm1',
  'file': 'm1_halflife.csv',
  'takeaway': {'ko': ['상대 표준불확도(값에 견준 오차 막대의 폭)는 대략 {m1_median}년마다 절반이 되었다 — 불확도가 줄어든 핵심 상수 {m1_n_dec}개의 반감기 중앙값.',
                      '반감기가 가장 짧은 상수는 {m1_min_name}({m1_min}년), 가장 긴 상수는 {m1_max_name}({m1_max}년)이다.'],
               'en': ['The relative standard uncertainty (the error-bar width relative to the value) halved roughly every {m1_median} years: the '
                      'median half-life over the {m1_n_dec} core constants whose uncertainty declined.',
                      "The shortest half-life is the {m1_min_name_en}'s ({m1_min} years), the longest the {m1_max_name_en}'s ({m1_max} years)."]},
  'ko': {'name': '상대 불확도 반감기',
         'short': '상대 불확도가 절반이 되는 데 걸린 햇수',
         'definition': '상수마다 판별 상대 표준불확도(u/|x| — 값에 견준 오차 막대의 폭)가 얼마나 빨리 줄었는지 본다. log₂(상대 표준불확도)를 판 연도에 직선 회귀해, 불확도가 절반이 되는 데 걸린 햇수(반감기)를 구한다.',
         'formula': 'log₂(u/|x|) = a + b·연도,  반감기 = −1/b (년).  95% 구간은 b ± t(0.975, n−2)·SE(b) 를 같은 식에 넣는다(회귀 구간이며 부트스트랩이 아니다). b 가 −0.001/년보다 '
                    '완만하면(반감기 1,000년 초과) 「감소 없음」으로 적는다.',
         'denominator': '측정값(정의값 아님)이 있는 판이 4개 이상인 상수. 핵심 상수 {m1_n_core}개, 표시용 상수 포함 {m1_n_all}개.',
         'reading': '불확도가 줄어든 핵심 상수 {m1_n_dec}개의 반감기 중앙값은 {m1_median}년이다 — 대략 그 햇수마다 상대 표준불확도가 절반이 되었다는 뜻이다(줄지 않은 1개를 포함한 {m1_n_core}개의 중앙값은 '
                    '{m1_median_all}년). 반감기가 가장 짧은 상수는 {m1_min_name}({m1_min}년), 가장 긴 상수는 {m1_max_name}({m1_max}년)이다. 중성자 자기 모멘트는 1986 판부터 불확도가 거의 '
                    '그대로여서(기울기 −7×10⁻¹¹/년, 95% 구간이 0을 포함) 「감소 없음」으로 적었다.',
         'caveat': '판 사이 간격이 4년에서 13년까지 고르지 않다. 플랑크 상수·볼츠만 상수처럼 도중에 정의값(측정하지 않고 약속으로 정한 값)이 된 상수는 그 뒤 판을 빼고 계산한다. 직선은 요약일 뿐이어서, 새 측정법이 들어온 판에서 불확도가 '
                   '계단처럼 확 줄어든 상수는 직선에 잘 맞지 않는다(결정계수 R² 이 낮다).'},
  'en': {'name': 'Relative-uncertainty half-life',
         'short': 'Years for the relative uncertainty to halve',
         'definition': 'For each constant, how fast the relative standard uncertainty (u/|x| — the error-bar width relative to the value) fell. log₂ '
                       'of the relative standard uncertainty is regressed on edition year, giving the years for the uncertainty to halve (the '
                       'half-life).',
         'formula': 'log₂(u/|x|) = a + b·year,  half-life = −1/b (years). The 95% interval maps b ± t(0.975, n−2)·SE(b) through the same expression '
                    '(a regression interval, not a bootstrap). A slope flatter than −0.001 per year (half-life above 1,000 years) is reported as no '
                    'decline.',
         'denominator': 'Constants with a measured (not exact) value in at least four editions: {m1_n_core} core constants, {m1_n_all} including '
                        'display constants.',
         'reading': 'Over the {m1_n_dec} core constants whose uncertainty declined, the median half-life is {m1_median} years: roughly every '
                    '{m1_median} years the relative standard uncertainty halved ({m1_median_all} years over all {m1_n_core}, counting the one with '
                    "no decline). The shortest half-life is the {m1_min_name_en}'s ({m1_min} years), the longest the {m1_max_name_en}'s ({m1_max} "
                    'years). The neutron magnetic moment kept almost the same uncertainty from 1986 on (slope −7×10⁻¹¹ per year, interval including '
                    "zero) and is shown as 'no decline'.",
         'caveat': 'Editions are 4 to 13 years apart. Constants that became exact along the way (fixed by definition rather than measured), such as '
                   'the Planck and Boltzmann constants, are counted only up to that point. A straight line is a summary: constants whose uncertainty '
                   'dropped in one step when a new method arrived fit it poorly (low R²).'}},
 {'id': 'm2',
  'file': 'm2_summary.csv',
  'takeaway': {'ko': ['연속한 두 판 사이 이동이 두 판의 표준불확도를 합친 값의 2배를 넘은 경우(|z|>2)가 {m2_r2}%, 약 {m2_1in2}번에 1번이다. 정규분포 기대는 4.55%(22번에 1번) — 오차 막대가 맞다면 이 정도여야 '
                      '한다.',
                      '3배를 넘은 경우(|z|>3)는 {m2_r3}%(약 {m2_1in3}번에 1번)로, 정규분포 기대 0.27%(370번에 1번)보다 훨씬 잦다.',
                      '반대로 |z|>1 은 정규분포 기대보다 적다. 판끼리 자료를 공유해 값은 대개 그대로 있다가, 새 측정이나 이론 수정이 들어오면 한 번에 크게 움직인다.'],
               'en': ['Moves between consecutive editions exceeded twice the combined standard uncertainty of the two editions (|z| > 2) in {m2_r2}% '
                      'of pairs, about once in {m2_1in2}. The normal expectation is 4.55% (once in 22): what correct error bars would give.',
                      'Moves beyond three times (|z| > 3) occurred in {m2_r3}% (about once in {m2_1in3}), far more often than the normal 0.27% (once '
                      'in 370).',
                      '|z| > 1, by contrast, is rarer than the normal expectation: editions share data, so values mostly stay put and then move a '
                      'long way at once when a new measurement or a corrected calculation arrives.']},
  'ko': {'name': '판간 이동 초과율',
         'short': '연속한 두 판 사이 이동이 두 불확도로 설명되지 않은 비율',
         'definition': '같은 상수의 연속한 두 판(측정값끼리)에서 값의 이동을 두 판의 표준불확도를 합친 값 √(u_옛²+u_새²)으로 나눈 것을 z 라 한다. z 가 2면 두 판의 오차 막대를 합친 폭의 2배를 움직였다는 뜻이다. |z| 가 '
                       '1·2·3 을 넘는 비율을 센다.',
         'formula': 'z = (x_새 − x_옛) / √(u_옛² + u_새²).  두 판이 독립이고 정규분포라면 |z|>1 은 31.7%, >2 는 4.55%, >3 은 0.27%.',
         'denominator': '핵심 상수 {m2_q}개의 연속 판 쌍 {m2_n}개. 1998 판 이후 4년 간격 쌍 {m2_n_new}개, 그 이전(4~13년 간격) 쌍 {m2_n_old}개.',
         'reading': '|z|>2 는 {m2_r2}%(95% 구간 {m2_r2_ci}), 약 {m2_1in2}번에 1번이다. 정규분포 기대는 4.55%(22번에 1번) — 불확도가 맞고 판끼리 독립이라면 이 정도여야 한다. |z|>3 은 '
                    '{m2_r3}%({m2_r3_ci}), 약 {m2_1in3}번에 1번으로 정규분포 기대 0.27%(370번에 1번)보다 훨씬 많다. 반대로 |z|>1 은 {m2_r1}%({m2_r1_ci})로 정규분포 기대 31.7%보다 적다. '
                    '작은 이동은 드물고 큰 이동은 잦다.',
         'caveat': '연속한 두 판은 같은 실험 자료를 상당 부분 공유하므로 독립이 아니다. 새 자료가 없으면 값이 거의 그대로 남고(값이 한 자리도 바뀌지 않은 쌍이 {m2_zero}개), z 가 0 쪽으로 쏠린다. 그래서 |z|>1 이 적은 것을 '
                   '「불확도가 넉넉했다(오차 막대가 넓었다)」로 읽으면 안 된다. 큰 이동의 비율은 이런 사정에도 정규분포 기대보다 높다. 95% 구간은 상수를 통째로 다시 뽑는 군집 부트스트랩이다. 같은 선정 규칙에 맞는 후보 '
                   '3개(헬리온·삼중수소핵의 상대 원자 질량, 중양성자 자기 모멘트)를 더한 20개로 다시 세면 |z|>2 {k20_r2}%, |z|>3 {k20_r3}% 다.'},
  'en': {'name': 'Edition-to-edition exceedance',
         'short': 'Share of moves between consecutive editions not covered by the two uncertainties',
         'definition': 'For each constant and each pair of consecutive editions in which it is measured, z is the change in value divided by the '
                       'combined standard uncertainty √(u_old² + u_new²). z = 2 means a move of twice the combined width of the two error bars. The '
                       'shares with |z| above 1, 2 and 3 are counted.',
         'formula': 'z = (x_new − x_old) / √(u_old² + u_new²). If the two editions were independent and normal, |z|>1 would occur 31.7% of the time, '
                    '>2 4.55%, >3 0.27%.',
         'denominator': '{m2_n} consecutive pairs over {m2_q} core constants: {m2_n_new} four-year pairs from 1998 on, {m2_n_old} earlier pairs (4 '
                        'to 13 years apart).',
         'reading': '|z| > 2 occurs in {m2_r2}% of pairs (95% interval {m2_r2_ci}), about once in {m2_1in2}. The normal expectation is 4.55% (once '
                    'in 22), what correct, independent uncertainties would give. |z| > 3 occurs in {m2_r3}% ({m2_r3_ci}), about once in {m2_1in3}, '
                    'far above the normal 0.27% (once in 370). |z| > 1, by contrast, occurs in {m2_r1}% ({m2_r1_ci}), below the normal 31.7%. Small '
                    'moves are rare and large ones common.',
         'caveat': 'Consecutive editions share much of their experimental data, so they are not independent. Without new data a value barely moves '
                   '({m2_zero} pairs did not change in any printed digit), pulling z toward zero. That is why the low share of |z| > 1 cannot be '
                   'read as generous uncertainties (wide error bars). The share of large moves exceeds the normal expectation despite this. '
                   'Intervals are a cluster bootstrap that resamples whole constants. Adding three candidates that meet the same selection rule '
                   '(helion and triton relative atomic masses, deuteron magnetic moment), 20 constants give |z| > 2 in {k20_r2}% and |z| > 3 in '
                   '{k20_r3}%.'}},
 {'id': 'm3',
  'file': 'm3_summary.csv',
  'takeaway': {'ko': ['옛 판의 ±2σ 범위(표준불확도의 2배 — 넉넉한 오차 막대)가 2022 판 값을 담지 못한 경우가 {m3_m2}%, 10개 중 약 {m3_m2_10}개다. 정규분포 기대는 4.55%(20개 중 1개 꼴).',
                      '1969~1986 판({m3_old_m2}%)과 1998~2018 판({m3_new_m2}%)의 놓침률이 비슷하다. 불확도는 만 배 넘게 줄었지만 놓침률은 줄지 않았다.'],
               'en': ['The ±2σ ranges of earlier editions (twice the standard uncertainty: generous error bars) miss the 2022 value in {m3_m2}% of '
                      'cases, about {m3_m2_10} in 10. The normal expectation is 4.55% (about 1 in 20).',
                      'The 1969–1986 editions ({m3_old_m2}%) and the 1998–2018 editions ({m3_new_m2}%) miss about equally often: uncertainties '
                      'shrank more than ten-thousand-fold, the miss rate did not.']},
  'ko': {'name': '2022 판 기준 놓침률',
         'short': '옛 판의 오차 막대가 2022 판 값을 담지 못한 비율',
         'definition': '옛 판의 값과 표준불확도로, 2022 판 값이 ±1σ(그 판의 오차 막대) 안에, 그리고 ±2σ(막대를 두 배로 넓힌 범위) 안에 들어오는지 센다. Henrion & Fischhoff(1986)의 두 지표도 함께 낸다 — '
                       '사분위 지수(±0.674σ 안에 든 비율. 막대 길이의 약 3분의 2 안으로, 정확히는 정규분포 75% 분위수 0.67449. 정규분포 기대 50%)와 놀람 지수(±2.326σ, 즉 98% 구간 밖 비율. 막대를 약 '
                       '2.3배로 넓혀도 빗나간 경우로, 정확히는 99% 분위수 2.32635. 정규분포 기대 2%).',
         'formula': 'z = (x_2022 − x_옛) / u_옛.  놓침(kσ) = |z| > k.  정규 기대: 1σ 밖 31.7%, 2σ 밖 4.55%, 사분위 지수 50%, 놀람 지수 2%.',
         'denominator': '판별로, 그 판에서 측정값이고 2022 판에도 있는 핵심 상수(10~17개; 예컨대 2018 판은 정의값이 된 h·k 를 빼고 15개). 전체 {m3_n}개 (판, 상수) 조합, 상수 {m3_q}개.',
         'reading': '2022 판 값이 옛 판의 ±1σ 밖에 있는 경우가 {m3_m1}%(95% 구간 {m3_m1_ci}), ±2σ 밖이 {m3_m2}%({m3_m2_ci})다. 정규분포 기대는 각각 31.7%, 4.55%. 놀람 지수(±2.326σ '
                    '밖)는 {m3_si}%({m3_si_ci}, 정규분포 기대 2%). 판이 오래되었다고 놓침률이 뚜렷이 높지는 않다 — ±2σ 기준 1969~1986 판 {m3_old_m2}%, 1998~2018 판 {m3_new_m2}%.',
         'caveat': '같은 규칙의 후보 3개를 더한 20개로는 ±2σ 밖이 {k20_m3}% 다. 2022 판은 참값이 아니라 지금의 권고값이어서 다음 판에서 바뀔 수 있다. 플랑크 상수·볼츠만 상수처럼 2018 판부터 정의값(측정하지 않고 약속으로 '
                   '정한 값)이 된 상수는 그 정의값을 기준으로 삼았다(정의값은 2017년 특별 조정의 결과로 정했다). 같은 상수의 여러 판은 서로 독립이 아니므로, 판을 합친 비율의 표본 크기는 겉보기보다 작다.'},
  'en': {'name': 'Miss rate against the 2022 edition',
         'short': 'Share of earlier error bars that do not contain the 2022 value',
         'definition': "Using each earlier edition's value and standard uncertainty, count whether the 2022 value falls inside ±1σ (that edition's "
                       "error bar) and inside ±2σ (the bar doubled). Henrion & Fischhoff's (1986) two indices are given too: the interquartile "
                       'index, the share within ±0.674σ (about two-thirds of the bar; exactly the normal 75% quantile, 0.67449; normal expectation '
                       '50%), and the surprise index, the share outside ±2.326σ, the 98% interval (the bar stretched about 2.3 times; exactly the '
                       '99% quantile, 2.32635; normal expectation 2%).',
         'formula': 'z = (x_2022 − x_old) / u_old. Miss at kσ: |z| > k. Normal expectation: 31.7% outside 1σ, 4.55% outside 2σ, interquartile index '
                    '50%, surprise index 2%.',
         'denominator': 'By edition, the core constants measured in that edition and present in 2022 (10 to 17; the 2018 edition has 15, h and k '
                        'being exact). Overall {m3_n} (edition, constant) combinations over {m3_q} constants.',
         'reading': "The 2022 value lies outside the earlier edition's ±1σ in {m3_m1}% of cases (95% interval {m3_m1_ci}) and outside ±2σ in "
                    '{m3_m2}% ({m3_m2_ci}); the normal expectations are 31.7% and 4.55%. The surprise index (outside ±2.326σ) is {m3_si}% '
                    '({m3_si_ci}; normal 2%). Older editions do not miss clearly more often: at ±2σ, {m3_old_m2}% for 1969–1986 and {m3_new_m2}% for '
                    '1998–2018.',
         'caveat': 'With the three candidates meeting the same rule added (20 constants), {k20_m3}% fall outside ±2σ. The 2022 edition is the '
                   'current recommendation, not the true value, and may change. For constants exact from 2018 (fixed by definition rather than '
                   'measured), such as the Planck and Boltzmann constants, the defined value is the reference (it was set from the 2017 special '
                   'adjustment). Editions of the same constant are not independent, so pooled rates rest on fewer effective observations than their '
                   'count suggests.'}},
 {'id': 'm4',
  'file': 'm4_tail.csv',
  'takeaway': {'ko': ['판간 이동 z 의 분포는 정규분포(종 모양)보다 꼬리가 훨씬 두껍다 — 아주 크게 빗나가는 일이 정규분포가 예상하는 것보다 훨씬 잦다.',
                      'Student-t 자유도는 ν = {m4_nu} 로 코시 분포(ν = 1)에 가깝다(정규분포는 ν = ∞, 작을수록 꼬리가 두껍다).',
                      '실무로 옮기면, 공표된 표준불확도의 3배 밖으로 움직이는 일(|z|>3)도 드물지 않다 — 판 쌍의 {m2_r3}%.'],
               'en': ['The distribution of moves between editions (z) has much heavier tails than the normal (bell curve): very large misses happen '
                      'far more often than the normal predicts.',
                      'The Student-t degrees of freedom are ν = {m4_nu}, close to the Cauchy distribution (ν = 1); the normal has ν = ∞, and smaller '
                      'means heavier tails.',
                      'In practice, a move of more than three published standard uncertainties (|z| > 3) is not rare: {m2_r3}% of pairs.']},
  'ko': {'name': '꼬리 두께',
         'short': '판간 이동 z 분포에 맞춘 Student-t 자유도',
         'definition': '값이 바뀐 연속 판 쌍의 z(M2)에 중심 0인 Student-t 분포를 최대우도로 맞춘다. Student-t 는 꼬리(분포의 양 끝) 두께를 자유도 ν 로 조절하는 분포다. ν 가 작을수록 꼬리가 두꺼워 아주 큰 이동이 '
                       '잦다(ν=1 이면 코시 분포, ν→∞ 이면 정규분포).',
         'formula': 'z ~ s · t_ν,  ν·s 를 최대우도로 추정.  95% 구간은 상수 군집 부트스트랩 2,000회.  값이 한 자리도 바뀌지 않은 쌍(z = 0)은 뺀다.',
         'denominator': '핵심 상수 {m2_q}개의 연속 판 쌍 {m2_n}개 중 값이 바뀐 {m4_n}개.',
         'reading': 'ν = {m4_nu}(95% 구간 {m4_nu_ci}), 척도 s = {m4_s}({m4_s_ci}). ν 가 1 안팎이면 코시 분포에 가까운 꼬리로, 아주 큰 이동이 정규분포보다 훨씬 흔하다. 1998 판 이후 쌍만으로는 ν '
                    '= {m4_new_nu}({m4_new_nu_ci}). 참고로 Bailey(2017)가 상수 7개의 개별 측정 쌍에서 얻은 값은 ν = 1.81 ± 0.15 다.',
         'caveat': '값이 한 자리도 바뀌지 않은 쌍(z = 0)을 남기면 최대우도 추정량이 존재하지 않는다 — 척도 s 를 0 쪽으로 보낼수록 우도가 끝없이 커지기 때문이다(ν 가 0.08 미만일 때). 그래서 그 {m2_zero}개 쌍은 빼고 '
                   '맞췄고, 그 수는 M2 에 따로 적었다. Bailey 의 값은 개별 실험 측정끼리의 비교이고 이 사이트의 z 는 권고값 판끼리의 비교라서 두 ν 는 같은 양이 아니다 — 권고값은 여러 측정을 가중 평균하고 일부를 빼거나 불확도를 '
                   '키운(확장 인자) 결과다. 척도 s 가 1보다 작은 것은 판 사이 자료 공유(M2 한계)를 반영한다. 표본이 작아 구간이 넓다.'},
  'en': {'name': 'Tail heaviness',
         'short': 'Student-t degrees of freedom fitted to edition-to-edition z',
         'definition': 'A zero-centred Student-t is fitted by maximum likelihood to the z (M2) of consecutive pairs whose value changed. The '
                       'Student-t distribution sets the thickness of its tails (the two ends) through its degrees of freedom ν: the smaller ν, the '
                       'thicker the tails and the more common very large moves (ν = 1 is the Cauchy distribution; ν → ∞ the normal).',
         'formula': 'z ~ s · t_ν, ν and s by maximum likelihood; 95% intervals from 2,000 cluster-bootstrap resamples of constants. Pairs whose '
                    'printed value did not change (z = 0) are left out.',
         'denominator': '{m4_n} of the {m2_n} consecutive pairs over {m2_q} core constants: those whose value changed.',
         'reading': 'ν = {m4_nu} (95% interval {m4_nu_ci}), scale s = {m4_s} ({m4_s_ci}). A ν near 1 means tails close to the Cauchy distribution: '
                    'very large moves far more common than under the normal. Pairs from 1998 on alone give ν = {m4_new_nu} ({m4_new_nu_ci}). For '
                    'reference, Bailey (2017) obtained ν = 1.81 ± 0.15 from pairs of individual measurements of seven constants.',
         'caveat': 'With the pairs whose printed value did not change (z = 0) kept, no maximum-likelihood estimate exists: the likelihood grows '
                   'without bound as the scale s goes to zero (for ν below 0.08). Those {m2_zero} pairs are left out and counted in M2 instead. '
                   'Bailey compares individual experimental results and this site compares editions of recommended values, so the two ν are not the '
                   'same quantity: recommended values are weighted averages from which some results are dropped or whose uncertainties are expanded '
                   '(expansion factors). A scale below 1 reflects the data shared between editions (see M2). The sample is small and the intervals '
                   'wide.'}},
 {'id': 'm5',
  'file': 'm5_funnel.csv',
  'takeaway': {'ko': ['상수마다 판별 값과 ±1σ 오차 막대를 2022 판 값에서의 상대 편차로 그린다. 속이 빈 원은 그 판의 ±1σ 범위가 2022 판 값을 담지 못한 경우다.',
                      '양성자 전하 반지름처럼 여러 판 내내 같은 쪽으로 벗어나 있다가 한 판에서 크게 옮겨 간 상수가 있다.'],
               'en': ["Each constant's values by edition with ±1σ error bars, drawn as relative deviations from the 2022 value. An open circle marks "
                      'an edition whose ±1σ range does not contain the 2022 value.',
                      'Some constants, such as the proton charge radius, sat off to the same side for several editions and then moved a long way in '
                      'one.']},
  'ko': {'name': '상수별 수렴 그림',
         'short': '판별 값과 오차 막대를 2022 판 기준 편차로',
         'definition': '상수마다 각 판의 값이 2022 판 값에서 얼마나 떨어져 있었는지(상대 편차)와 그 판의 ±1σ 오차 막대를 판 순서로 그린다.',
         'formula': '상대 편차 = (x_판 − x_2022) / |x_2022|,  막대 = ± u_판 / |x_2022|.  세로축은 0 근처를 직선, 바깥을 로그로 그리는 대칭 로그 축.',
         'denominator': '상수별 면에 하나씩.',
         'reading': '가운데 점선이 2022 판 값(상대 편차 0)이다. 막대가 이 선에 닿지 않는 점(속이 빈 원)이 그 판이 2022 판 값을 ±1σ 로 놓친 경우다.',
         'caveat': '옛 판의 큰 편차와 최근 판의 아주 작은 편차를 한 그림에 넣으려고 세로축을 대칭 로그 축(0 근처는 일정 간격, 바깥은 10배 간격)으로 그렸다. 그래서 바깥쪽에서는 막대 길이를 눈으로 비교하기 어렵다.'},
  'en': {'name': 'Convergence plot by constant',
         'short': "Each edition's value and error bar as a deviation from 2022",
         'definition': "For each constant, each edition's relative deviation from the 2022 value and its ±1σ error bar, in edition order.",
         'formula': 'relative deviation = (x_edition − x_2022) / |x_2022|, bar = ± u_edition / |x_2022|. The vertical axis is symmetric-log: linear '
                    'near zero, logarithmic beyond.',
         'denominator': 'One per constant page.',
         'reading': 'The dashed line in the middle is the 2022 value (relative deviation 0). A point whose bar does not reach it (open circle) is an '
                    'edition that missed the 2022 value at ±1σ.',
         'caveat': 'To fit the large deviations of early editions and the tiny ones of recent editions into one plot, the vertical axis is '
                   'symmetric-log (evenly spaced near zero, by factors of ten further out), so bar lengths are hard to compare by eye in the outer '
                   'region.'}},
 {'id': 'm6',
  'file': 'm6_events.csv',
  'takeaway': {'ko': ['2019년 SI 개정으로 플랑크 상수·기본 전하·볼츠만 상수·아보가드로 상수는 2018 판부터 정의값(측정 대상이 아니라 약속으로 정한 값, 불확도 0)이 되었다.',
                      '반대로 진공 투자율 μ₀ 와 몰질량 상수는 정의값에서 측정값으로 바뀌었다. 불확도는 사라지지 않고 다른 양으로 옮겨 간다.'],
               'en': ['With the 2019 revision of the SI, the Planck constant, elementary charge, Boltzmann constant and Avogadro constant are exact '
                      'from the 2018 edition (fixed by definition rather than measured; uncertainty zero).',
                      'Conversely, the vacuum magnetic permeability μ₀ and the molar mass constant went from exact to measured: uncertainty does not '
                      'vanish, it moves to other quantities.']},
  'ko': {'name': '정의값 전환',
         'short': '측정값이 정의값이 된 상수, 정의값이 측정값이 된 상수',
         'definition': '판과 판 사이에 측정값(불확도가 있는 값)에서 정의값(측정하지 않고 약속으로 정한 값, 불확도 0)으로, 또는 그 반대로 바뀐 상수와 그 시점.',
         'formula': '연속한 두 판에서 「정의값 여부」가 바뀐 경우.',
         'denominator': '이 사이트가 다루는 27개 양.',
         'reading': '빛의 속력은 1983년 미터를 빛으로 다시 정의하면서 정의값이 되어 1986 판부터 불확도가 0이다. 2019년 SI 개정으로 플랑크 상수·기본 전하·볼츠만 상수·아보가드로 상수와, 이 값들로 계산되는 패러데이 상수·몰 기체 '
                    '상수·슈테판–볼츠만 상수가 2018 판부터 정의값이다. 반대로 진공 투자율 μ₀ 와 몰질량 상수 M_u 는 2014 판까지 정의값이었다가 2018 판부터 측정값이다.',
         'caveat': '정의값이 된 상수는 그 판부터 M1~M4 계산에서 빠진다. 정의값이 되었다고 그 양에 대한 지식이 완성된 것은 아니다 — 불확도는 그 상수로 계산하던 다른 양으로 옮겨 간다.'},
  'en': {'name': 'Exact-value transitions',
         'short': 'Constants that became exact, and exact ones that became measured',
         'definition': 'Constants whose status changed between editions, from measured (with an uncertainty) to exact (fixed by definition rather '
                       'than measured, uncertainty zero), or the reverse, and when.',
         'formula': 'A change in the exact flag between two consecutive editions.',
         'denominator': 'The 27 quantities on this site.',
         'reading': 'The speed of light became exact when the metre was redefined in terms of light in 1983, and has zero uncertainty from the 1986 '
                    'edition. With the 2019 revision of the SI, the Planck constant, elementary charge, Boltzmann constant and Avogadro constant, '
                    'and the Faraday constant, molar gas constant and Stefan–Boltzmann constant computed from them, are exact from the 2018 edition. '
                    'Conversely, the vacuum magnetic permeability μ₀ and the molar mass constant M_u were exact up to the 2014 edition and are '
                    'measured from 2018.',
         'caveat': 'A constant leaves the M1–M4 calculations from the edition in which it becomes exact. Becoming exact does not mean knowledge of '
                   'the quantity is complete: the uncertainty moves to the quantities derived from it.'}}]
