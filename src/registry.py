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
  'takeaway': {'ko': ['상수마다 함께 발표되는 오차 막대는 대략 {m1_median}년마다 절반으로 좁아졌다(막대가 좁아진 핵심 상수 {m1_n_dec}개의 중앙값).',
                      '빠른 상수는 {m1_min_name}로 {m1_min}년, 느린 상수는 {m1_max_name}로 {m1_max}년마다 절반이 되었다.'],
               'en': ['The error bars published with each constant narrowed by half roughly every {m1_median} years (median over the {m1_n_dec} core '
                      'constants whose bars narrowed).',
                      'The fastest, the {m1_min_name_en}, halved every {m1_min} years; the slowest, the {m1_max_name_en}, every {m1_max} years.']},
  'ko': {'name': '상대 불확도 반감기',
         'short': '상대 불확도가 절반이 되는 데 걸린 햇수',
         'definition': '상수마다 판별로 발표된 오차 막대의 상대 크기(값에 견준 막대 폭, u/|x|)가 얼마나 빨리 줄었는지 본다. 판 연도에 따라 직선을 맞춰, 막대가 절반으로 좁아지는 데 걸린 햇수(반감기)를 구한다.',
         'formula': 'log₂(u/|x|) = a + b·연도,  반감기 = −1/b (년).  95% 구간은 b ± t(0.975, n−2)·SE(b) 를 같은 식에 넣는다(회귀 구간이며 부트스트랩이 아니다). b 가 −0.001/년보다 '
                    '완만하면(반감기 1,000년 초과) 「감소 없음」으로 적는다.',
         'denominator': '측정값(정의값 아님)이 있는 판이 4개 이상인 상수. 핵심 상수 {m1_n_core}개, 표시용 상수 포함 {m1_n_all}개.',
         'reading': '막대가 좁아진 핵심 상수 {m1_n_dec}개의 반감기 중앙값은 {m1_median}년이다 — 대략 그 햇수마다 막대가 절반이 되었다는 뜻이다(막대가 줄지 않은 1개를 포함한 {m1_n_core}개의 중앙값은 '
                    '{m1_median_all}년). 가장 빠른 상수는 {m1_min_name}({m1_min}년), 가장 느린 상수는 {m1_max_name}({m1_max}년)이다. 중성자 자기 모멘트는 1986 판부터 막대가 거의 '
                    '그대로여서(기울기 −7×10⁻¹¹/년, 95% 구간이 0을 포함) 「감소 없음」으로 적었다.',
         'caveat': '판 사이 간격이 4년에서 13년까지 고르지 않다. 플랑크 상수·볼츠만 상수처럼 도중에 약속으로 정한 값(정의값)이 된 상수는 그 뒤 판을 빼고 계산한다. 직선은 요약일 뿐이어서, 새 측정법이 들어온 판에서 막대가 계단처럼 확 '
                   '줄어든 상수는 직선에 잘 맞지 않는다(결정계수 R² 가 낮다).'},
  'en': {'name': 'Relative-uncertainty half-life',
         'short': 'Years for the relative uncertainty to halve',
         'definition': 'For each constant, how fast the relative size of its published error bar (bar width relative to the value, u/|x|) shrank. A '
                       'straight line against edition year gives the number of years for the bar to halve (the half-life).',
         'formula': 'log₂(u/|x|) = a + b·year,  half-life = −1/b (years). The 95% interval maps b ± t(0.975, n−2)·SE(b) through the same expression '
                    '(a regression interval, not a bootstrap). A slope flatter than −0.001 per year (half-life above 1,000 years) is reported as no '
                    'decline.',
         'denominator': 'Constants with a measured (not exact) value in at least four editions: {m1_n_core} core constants, {m1_n_all} including '
                        'display constants.',
         'reading': 'Across the {m1_n_dec} core constants whose bars narrowed, the median half-life is {m1_median} years: roughly every {m1_median} '
                    'years the bar halved ({m1_median_all} years over all {m1_n_core}, counting the one that did not narrow). The fastest is the '
                    '{m1_min_name_en} ({m1_min} years), the slowest the {m1_max_name_en} ({m1_max} years). The neutron magnetic moment kept almost '
                    "the same bar from 1986 on (slope −7×10⁻¹¹ per year, interval including zero) and is shown as 'no decline'.",
         'caveat': 'Editions are 4 to 13 years apart. Constants that became fixed by definition along the way, such as the Planck and Boltzmann '
                   'constants, are counted only up to that point. A straight line is a summary: constants whose bar dropped in one step when a new '
                   'method arrived fit it poorly (low R²).'}},
 {'id': 'm2',
  'file': 'm2_summary.csv',
  'takeaway': {'ko': ['새 판이 나올 때 값이 오차 막대 폭의 2배 넘게 움직인 경우가 약 {m2_1in2}번에 1번({m2_r2}%)이다. 막대가 말하는 대로라면 22번에 1번이어야 한다.',
                      '3배 넘게 움직인 경우는 약 {m2_1in3}번에 1번({m2_r3}%)으로, 기대치(370번에 1번)보다 훨씬 잦다.',
                      '반대로 조금만 움직인 경우는 기대보다 많다. 값은 대개 그대로 있다가, 새 실험이나 계산 수정이 들어오면 한 번에 크게 바뀐다.'],
               'en': ['When a new edition came out, a value moved by more than twice its error bars about once in {m2_1in2} times ({m2_r2}%). If the '
                      'bars were right, it would be once in 22.',
                      'Moves of more than three times the bars happened about once in {m2_1in3} times ({m2_r3}%), far more often than the expected '
                      'once in 370.',
                      'Small moves, on the other hand, were more common than expected: values mostly stay put, then jump at once when a new '
                      'experiment or a corrected calculation arrives.']},
  'ko': {'name': '판간 이동 초과율',
         'short': '연속한 두 판 사이 이동이 두 불확도로 설명되지 않은 비율',
         'definition': '같은 상수가 연속한 두 판 사이에 얼마나 움직였는지를 두 판의 오차 막대를 합친 폭과 견준다. 이 비를 z 라 한다 — z 가 2면 막대 폭의 2배를 움직였다는 뜻이다. |z| 가 1·2·3 을 넘은 비율을 센다.',
         'formula': 'z = (x_새 − x_옛) / √(u_옛² + u_새²).  두 판이 독립이고 정규분포라면 |z|>1 은 31.7%, >2 는 4.55%, >3 은 0.27%.',
         'denominator': '핵심 상수 {m2_q}개의 연속 판 쌍 {m2_n}개. 1998 판 이후 4년 간격 쌍 {m2_n_new}개, 그 이전(4~13년 간격) 쌍 {m2_n_old}개.',
         'reading': '막대 폭의 2배 넘게 움직인 경우가 {m2_r2}%(95% 구간 {m2_r2_ci}), 약 {m2_1in2}번에 1번이다. 막대가 맞다면 4.55%, 22번에 1번이어야 한다. 3배 넘게는 {m2_r3}%({m2_r3_ci}), '
                    '약 {m2_1in3}번에 1번으로 기대치(0.27%, 370번에 1번)보다 훨씬 많다. 반대로 1배 넘게 움직인 경우는 {m2_r1}%({m2_r1_ci})로 기대치(31.7%)보다 적다. 작은 이동은 드물고 큰 이동은 잦다.',
         'caveat': '연속한 두 판은 같은 실험 자료를 상당 부분 함께 쓴다. 그래서 새 자료가 없으면 값이 거의 그대로 남고(한 자리도 안 바뀐 쌍이 {m2_zero}개), 이동이 작게 나오는 쪽으로 기운다. 작은 이동이 적은 것을 「막대가 '
                   '넉넉했다」로 읽으면 안 되는 까닭이다. 큰 이동은 이런 사정에도 기대보다 많다. 95% 구간은 상수를 통째로 다시 뽑는 방식(군집 부트스트랩)으로 냈다. 같은 선정 규칙에 맞는 후보 3개(헬리온·삼중수소핵의 상대 원자 질량, '
                   '중양성자 자기 모멘트)를 더한 20개로 다시 세도 2배 초과 {k20_r2}%, 3배 초과 {k20_r3}% 로 비슷하다.'},
  'en': {'name': 'Edition-to-edition exceedance',
         'short': 'Share of moves between consecutive editions not covered by the two uncertainties',
         'definition': "How far the same constant moved between two consecutive editions, compared with the combined width of the two editions' "
                       'error bars. The ratio is called z: z = 2 means a move of twice the bar width. The shares of moves with |z| above 1, 2 and 3 '
                       'are counted.',
         'formula': 'z = (x_new − x_old) / √(u_old² + u_new²). If the two editions were independent and normal, |z|>1 would occur 31.7% of the time, '
                    '>2 4.55%, >3 0.27%.',
         'denominator': '{m2_n} consecutive pairs over {m2_q} core constants: {m2_n_new} four-year pairs from 1998 on, {m2_n_old} earlier pairs (4 '
                        'to 13 years apart).',
         'reading': 'Moves of more than twice the bar width occurred in {m2_r2}% of pairs (95% interval {m2_r2_ci}), about once in {m2_1in2}. If the '
                    'bars were right it would be 4.55%, once in 22. Moves of more than three times occurred in {m2_r3}% ({m2_r3_ci}), about once in '
                    '{m2_1in3}, far more than the expected 0.27% (once in 370). Moves of more than once the bar width, by contrast, occurred in '
                    '{m2_r1}% ({m2_r1_ci}), fewer than the expected 31.7%. Small moves are rare and large ones common.',
         'caveat': 'Consecutive editions share much of their experimental data, so without new data a value barely moves ({m2_zero} pairs did not '
                   'change in any printed digit) and moves come out small. That is why fewer small moves cannot be read as generous bars. Large '
                   'moves exceed the expectation despite this. Intervals come from resampling whole constants (cluster bootstrap). Adding three '
                   'candidates that meet the same selection rule (helion and triton relative atomic masses, deuteron magnetic moment), 20 constants '
                   'give {k20_r2}% beyond twice and {k20_r3}% beyond three times: about the same.'}},
 {'id': 'm3',
  'file': 'm3_summary.csv',
  'takeaway': {'ko': ['옛 판에 실린 넉넉한 오차 막대(±2σ)를 오늘의(2022 판) 값에 대 보면 10개 중 약 {m3_m2_10}개가 빗나간다. 막대가 맞다면 20개 중 1개 꼴이어야 한다.',
                      '오래된 판(1969~1986, {m3_old_m2}%)과 최근 판(1998~2018, {m3_new_m2}%)이 비슷하다. 막대는 만 배 넘게 좁아졌지만 빗나가는 비율은 줄지 않았다.'],
               'en': ["Hold the generous error bars (±2σ) of earlier editions against today's (2022) values and about {m3_m2_10} in 10 miss. If the "
                      'bars were right, it would be about 1 in 20.',
                      'Old editions (1969–1986, {m3_old_m2}%) and recent ones (1998–2018, {m3_new_m2}%) miss about equally often: the bars narrowed '
                      'more than ten-thousand-fold, the miss rate did not fall.']},
  'ko': {'name': '2022 판 기준 놓침률',
         'short': '옛 판의 오차 막대가 2022 판 값을 담지 못한 비율',
         'definition': '옛 판이 발표한 값과 오차 막대를 오늘의(2022 판) 값에 대 본다. 오늘의 값이 옛 막대(±1σ) 안에, 그리고 막대를 두 배로 넓힌 범위(±2σ) 안에 들어오는지 센다. Henrion & Fischhoff(1986)가 '
                       '쓴 두 지표도 함께 낸다 — 막대 길이의 약 3분의 2(±0.674σ, 정확히는 정규분포 75% 분위수 0.67449) 안에 든 비율(사분위 지수, 막대가 맞다면 50%)과, 막대를 약 2.3배(±2.326σ, 정확히는 '
                       '99% 분위수 2.32635)로 넓혀도 빗나간 비율(놀람 지수, 막대가 맞다면 2%).',
         'formula': 'z = (x_2022 − x_옛) / u_옛.  놓침(kσ) = |z| > k.  정규 기대: 1σ 밖 31.7%, 2σ 밖 4.55%, 사분위 지수 50%, 놀람 지수 2%.',
         'denominator': '판별로, 그 판에서 측정값이고 2022 판에도 있는 핵심 상수(10~17개; 예컨대 2018 판은 정의값이 된 h·k 를 빼고 15개). 전체 {m3_n}개 (판, 상수) 조합, 상수 {m3_q}개.',
         'reading': '오늘의 값이 옛 막대(±1σ) 밖에 있는 경우가 {m3_m1}%(95% 구간 {m3_m1_ci}), 두 배로 넓혀도(±2σ) 밖인 경우가 {m3_m2}%({m3_m2_ci})다. 막대가 맞다면 각각 31.7%, 4.55% 여야 '
                    '한다. 2.3배로 넓혀도 빗나간 경우(놀람 지수)는 {m3_si}%({m3_si_ci}, 기대 2%). 오래된 판이라고 더 많이 빗나가지는 않는다 — ±2σ 기준 1969~1986 판 {m3_old_m2}%, 1998~2018 '
                    '판 {m3_new_m2}%.',
         'caveat': '후보 3개를 더한 20개로는 ±2σ 밖이 {k20_m3}% 다. 2022 판도 참값이 아니라 지금의 권고값이어서 다음 판에서 바뀔 수 있다. 플랑크 상수·볼츠만 상수처럼 2018 판부터 약속으로 정한 값(정의값)이 된 상수는 그 '
                   '정의값을 기준으로 삼았다(정의값은 2017년 특별 조정의 결과로 정했다). 같은 상수의 여러 판은 서로 독립이 아니므로, 판을 합친 비율은 겉보기 개수만큼 정보가 많지 않다.'},
  'en': {'name': 'Miss rate against the 2022 edition',
         'short': 'Share of earlier error bars that do not contain the 2022 value',
         'definition': "Hold each earlier edition's value and error bar against today's (2022) value, and count whether today's value falls inside "
                       "the old bar (±1σ) and inside the bar doubled (±2σ). Henrion & Fischhoff's (1986) two indices are given too: the share within "
                       'about two-thirds of the bar (±0.674σ; exactly the normal 75% quantile, 0.67449), the interquartile index, 50% if the bars '
                       'were right; and the share outside the bar stretched about 2.3 times (±2.326σ; exactly the 99% quantile, 2.32635), the '
                       'surprise index, 2% if the bars were right.',
         'formula': 'z = (x_2022 − x_old) / u_old. Miss at kσ: |z| > k. Normal expectation: 31.7% outside 1σ, 4.55% outside 2σ, interquartile index '
                    '50%, surprise index 2%.',
         'denominator': 'By edition, the core constants measured in that edition and present in 2022 (10 to 17; the 2018 edition has 15, h and k '
                        'being exact). Overall {m3_n} (edition, constant) combinations over {m3_q} constants.',
         'reading': "Today's value lies outside the old bar (±1σ) in {m3_m1}% of cases (95% interval {m3_m1_ci}), and outside the doubled bar (±2σ) "
                    'in {m3_m2}% ({m3_m2_ci}). If the bars were right these would be 31.7% and 4.55%. Outside the bar stretched 2.3 times (surprise '
                    'index): {m3_si}% ({m3_si_ci}; expected 2%). Older editions do not miss more often: at ±2σ, {m3_old_m2}% for 1969–1986 and '
                    '{m3_new_m2}% for 1998–2018.',
         'caveat': 'With the three candidates added (20 constants), {k20_m3}% fall outside ±2σ. The 2022 edition is not the true value but the '
                   'current recommendation, and may change. For constants fixed by definition from 2018, such as the Planck and Boltzmann constants, '
                   'the defined value is the reference (it was set from the 2017 special adjustment). Editions of the same constant are not '
                   'independent, so pooled rates carry less information than their count suggests.'}},
 {'id': 'm4',
  'file': 'm4_tail.csv',
  'takeaway': {'ko': ['값이 움직인 폭을 모아 보면 종 모양(정규분포)보다 양 끝이 훨씬 두껍다. 아주 크게 빗나가는 일이 종 모양이 예상하는 것보다 훨씬 자주 생긴다는 뜻이다.',
                      '이 두께를 숫자로 나타낸 Student-t 자유도는 ν = {m4_nu} 이다(정규분포라면 무한대, 작을수록 두껍다).',
                      '실무로 옮기면, 발표된 오차의 3배 밖으로 빗나가는 일도 드물지 않다 — 판 쌍의 {m2_r3}%.'],
               'en': ['Collect the sizes of the moves and the distribution has much fatter ends than the bell curve: very large misses happen far '
                      'more often than a bell curve predicts.',
                      'The Student-t degrees of freedom that measure this are ν = {m4_nu} (infinite for the bell curve; smaller means fatter ends).',
                      'In practice, a miss of more than three published uncertainties is not rare: {m2_r3}% of pairs.']},
  'ko': {'name': '꼬리 두께',
         'short': '판간 이동 z 분포에 맞춘 Student-t 자유도',
         'definition': '판 사이에 값이 움직인 폭(M2 의 z)을 모아, 종 모양(정규분포)보다 양 끝이 얼마나 두꺼운지 잰다. 양 끝 두께를 조절할 수 있는 Student-t 분포를 맞추고 그 자유도 ν 를 보고한다. ν 가 작을수록 아주 큰 '
                       '이동이 잦다(ν=1 이면 코시 분포, ν 가 무한대면 정규분포).',
         'formula': 'z ~ s · t_ν,  ν·s 를 최대우도로 추정.  95% 구간은 상수 군집 부트스트랩 2,000회.  값이 한 자리도 바뀌지 않은 쌍(z = 0)은 뺀다.',
         'denominator': '핵심 상수 {m2_q}개의 연속 판 쌍 {m2_n}개 중 값이 바뀐 {m4_n}개.',
         'reading': 'ν = {m4_nu}(95% 구간 {m4_nu_ci}), 척도 s = {m4_s}({m4_s_ci}). ν 가 1 안팎이면 아주 큰 이동이 정규분포보다 훨씬 흔한, 코시 분포에 가까운 모양이다. 1998 판 이후 쌍만으로는 ν '
                    '= {m4_new_nu}({m4_new_nu_ci}). 참고로 Bailey(2017)가 상수 7개의 개별 측정끼리 비교해 얻은 값은 ν = 1.81 ± 0.15 다.',
         'caveat': '값이 한 자리도 안 바뀐 쌍(z = 0)을 넣으면 계산이 수학적으로 성립하지 않는다(척도를 0 쪽으로 보낼수록 우도가 끝없이 커져 최대우도 추정값이 없다). 그래서 그 {m2_zero}개 쌍은 빼고 맞췄고, 그 수는 M2 에 따로 '
                   '적었다. Bailey 의 값은 개별 실험끼리의 비교이고 이 사이트는 권고값 판끼리의 비교라서 두 ν 는 같은 양이 아니다 — 권고값은 여러 측정을 가중 평균하고 일부를 빼거나 막대를 넓힌 결과다. 척도 s 가 1보다 작은 것은 '
                   '판끼리 자료를 공유하기 때문이다(M2). 표본이 작아 구간이 넓다.'},
  'en': {'name': 'Tail heaviness',
         'short': 'Student-t degrees of freedom fitted to edition-to-edition z',
         'definition': 'Collect the moves between editions (the z of M2) and measure how much fatter their ends are than the bell curve (normal '
                       'distribution). A Student-t distribution, whose tail thickness can vary, is fitted and its degrees of freedom ν reported. The '
                       'smaller ν, the more common very large moves (ν = 1 is the Cauchy distribution; ν infinite is the normal).',
         'formula': 'z ~ s · t_ν, ν and s by maximum likelihood; 95% intervals from 2,000 cluster-bootstrap resamples of constants. Pairs whose '
                    'printed value did not change (z = 0) are left out.',
         'denominator': '{m4_n} of the {m2_n} consecutive pairs over {m2_q} core constants: those whose value changed.',
         'reading': 'ν = {m4_nu} (95% interval {m4_nu_ci}), scale s = {m4_s} ({m4_s_ci}). A ν near 1 means a shape close to Cauchy, in which very '
                    'large moves are far more common than under the bell curve. Pairs from 1998 on alone give ν = {m4_new_nu} ({m4_new_nu_ci}). For '
                    'reference, Bailey (2017) obtained ν = 1.81 ± 0.15 comparing individual measurements of seven constants.',
         'caveat': 'Including the pairs whose value did not change (z = 0) makes the calculation break down mathematically: the likelihood grows '
                   'without limit as the scale goes to zero, so no maximum-likelihood estimate exists. Those {m2_zero} pairs are left out and '
                   'counted in M2 instead. Bailey compares individual experiments and this site compares editions of recommended values, so the two '
                   'ν are not the same quantity: recommended values are weighted averages from which some results are dropped or whose bars are '
                   'widened. A scale below 1 reflects the data editions share (M2). The sample is small and the intervals wide.'}},
 {'id': 'm5',
  'file': 'm5_funnel.csv',
  'takeaway': {'ko': ['상수마다 판별 값과 오차 막대를 오늘의 값을 0으로 놓고 그린 그림이다. 속이 빈 원은 그 판의 막대가 오늘의 값을 품지 못한 경우다.',
                      '양성자 전하 반지름처럼 여러 판 내내 같은 쪽으로 빗나가 있다가 한 판에서 크게 옮겨 간 상수도 있다.'],
               'en': ["For each constant, every edition's value and error bar, drawn with today's value at zero. An open circle means that edition's "
                      "bar did not reach today's value.",
                      'Some constants, such as the proton charge radius, sat off to one side for several editions and then moved a long way in '
                      'one.']},
  'ko': {'name': '상수별 수렴 그림',
         'short': '판별 값과 오차 막대를 2022 판 기준 편차로',
         'definition': '상수마다 각 판의 값이 오늘의(2022 판) 값에서 얼마나 떨어져 있었는지와 그 판의 오차 막대(±1σ)를 판 순서로 그린다.',
         'formula': '상대 편차 = (x_판 − x_2022) / |x_2022|,  막대 = ± u_판 / |x_2022|.  세로축은 0 근처를 직선, 바깥을 로그로 그리는 대칭 로그 축.',
         'denominator': '상수별 면에 하나씩.',
         'reading': '가운데 점선이 오늘의 값이다. 막대가 이 선에 닿지 않는 점(속이 빈 원)이 그 판의 막대가 오늘의 값을 품지 못한 경우다.',
         'caveat': '옛 판의 큰 차이와 최근 판의 아주 작은 차이를 한 그림에 넣으려고, 세로축을 0 근처는 일정 간격으로, 바깥은 10배 간격으로 그렸다(대칭 로그 축). 그래서 바깥쪽에서는 막대 길이를 눈으로 비교하기 어렵다.'},
  'en': {'name': 'Convergence plot by constant',
         'short': "Each edition's value and error bar as a deviation from 2022",
         'definition': "For each constant, how far each edition's value lay from today's (2022) value, and that edition's error bar (±1σ), in "
                       'edition order.',
         'formula': 'relative deviation = (x_edition − x_2022) / |x_2022|, bar = ± u_edition / |x_2022|. The vertical axis is symmetric-log: linear '
                    'near zero, logarithmic beyond.',
         'denominator': 'One per constant page.',
         'reading': "The dashed line in the middle is today's value. A point whose bar does not reach it (open circle) is an edition whose bar did "
                    "not contain today's value.",
         'caveat': 'To fit the large differences of early editions and the tiny ones of recent editions into one plot, the vertical axis is evenly '
                   'spaced near zero and spaced by factors of ten further out (symmetric-log axis), so bar lengths are hard to compare by eye in the '
                   'outer region.'}},
 {'id': 'm6',
  'file': 'm6_events.csv',
  'takeaway': {'ko': ['2019년 국제단위계 개정으로 플랑크 상수·기본 전하·볼츠만 상수·아보가드로 상수는 「잴 대상」이 아니라 「이 값으로 정한다」는 약속이 되었다. 그래서 2018 판부터 오차 막대가 없다.',
                      '반대로 진공 투자율은 약속이던 값이 잴 대상으로 바뀌었다. 불확도는 사라지지 않고 다른 상수로 옮겨 간다.'],
               'en': ['With the 2019 revision of the SI, the Planck constant, elementary charge, Boltzmann constant and Avogadro constant stopped '
                      'being things to measure and became values fixed by agreement, so from the 2018 edition they have no error bars.',
                      'Conversely, the vacuum magnetic permeability went from a fixed value to something measured: uncertainty does not vanish, it '
                      'moves to other constants.']},
  'ko': {'name': '정의값 전환',
         'short': '측정값이 정의값이 된 상수, 정의값이 측정값이 된 상수',
         'definition': '판과 판 사이에 「재는 값(오차 막대 있음)」에서 「약속으로 정한 값(정의값, 막대 없음)」으로, 또는 그 반대로 바뀐 상수와 그 시점.',
         'formula': '연속한 두 판에서 「정의값 여부」가 바뀐 경우.',
         'denominator': '이 사이트가 다루는 27개 양.',
         'reading': '빛의 속력은 1983년에 미터를 빛으로 다시 정의하면서 약속으로 정한 값이 되어 1986 판부터 막대가 없다. 2019년 국제단위계 개정으로 플랑크 상수·기본 전하·볼츠만 상수·아보가드로 상수와, 이 값들로 계산되는 패러데이 '
                    '상수·몰 기체 상수·슈테판–볼츠만 상수가 2018 판부터 정의값이다. 반대로 진공 투자율 μ₀ 와 몰질량 상수 M_u 는 2014 판까지 정의값이었다가 2018 판부터 재는 값이 되었다.',
         'caveat': '정의값이 된 상수는 그 판부터 M1~M4 계산에서 빠진다. 약속으로 정했다고 그 양을 다 알게 된 것은 아니다 — 막대는 그 상수로 계산하던 다른 양으로 옮겨 간다.'},
  'en': {'name': 'Exact-value transitions',
         'short': 'Constants that became exact, and exact ones that became measured',
         'definition': 'Constants whose status changed between editions, from measured (with an error bar) to fixed by definition (exact, no bar), '
                       'or the reverse, and when.',
         'formula': 'A change in the exact flag between two consecutive editions.',
         'denominator': 'The 27 quantities on this site.',
         'reading': 'The speed of light became a defined value when the metre was redefined in terms of light in 1983, and has had no error bar '
                    'since the 1986 edition. With the 2019 revision of the SI, the Planck constant, elementary charge, Boltzmann constant and '
                    'Avogadro constant, and the Faraday constant, molar gas constant and Stefan–Boltzmann constant computed from them, are exact '
                    'from the 2018 edition. Conversely, the vacuum magnetic permeability μ₀ and the molar mass constant M_u were exact up to the '
                    '2014 edition and are measured from 2018.',
         'caveat': 'A constant leaves the M1–M4 calculations from the edition in which it becomes exact. Fixing a value by agreement does not mean '
                   'the quantity is fully known: the error bar moves to the quantities that used to be computed from it.'}}]
