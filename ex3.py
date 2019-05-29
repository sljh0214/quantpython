from utils_magic import *
import pandas as pd
import matplotlib.pyplot as plt

fs_path = r'D:/work/stock/quant/재무제표데이터_2018.xlsx'
fr_path = r'D:/work/stock/quant/재무비율데이터_2018.xlsx'
invest_path = r'D:/work/stock/quant/투자지표데이터_2018.xlsx'
price_path = r'D:/work/stock/quant/가격데이터.xlsx'

fs_df = get_finance_data(fs_path)
fr_df = get_finance_data(fr_path)
invest_df = get_finance_data(invest_path)
price_df = pd.read_excel(price_path, index_col=0)

def test1():
    # per, pbr 포트폴리오 백테스트 (Ch5. 백테스트.ipynb)
    strategy_date = '2015/12'
    start_date = '2016-6'
    end_date = '2017-5'
    initial_money = 100000000
    low_pbr = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PBR', strategy_date, 20)
    low_per = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PER', strategy_date, 20)
    pbr_backtest = backtest_beta(price_df, low_pbr, start_date, end_date, initial_money)
    per_backtest = backtest_beta(price_df, low_per, start_date, end_date, initial_money)

    # 초기 투자금 대비 변화율 그래프 그리기
    plt.figure(figsize=(10, 6))
    pbr_backtest['총변화율'].plot(label='PBR')
    per_backtest['총변화율'].plot(label='PER')
    plt.legend()
    plt.show()

def test2():
    # pbr 구간별 수익률 비교 (Ch5. 백테스트.ipynb)
    strategy_date = '2015/12'
    start_date = '2016-6'
    end_date = '2017-5'
    #strategy_date = '2016/12'
    #start_date = '2017-6'
    #end_date = '2018-5'
    initial_money = 100000000
    all_pbr = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PBR', strategy_date, None).dropna()
    length = int(len(all_pbr)/5)
    pbr_backtest1 = backtest_beta(price_df, all_pbr[:length], start_date, end_date, initial_money)
    pbr_backtest2 = backtest_beta(price_df, all_pbr[length:length*2], start_date, end_date, initial_money)
    pbr_backtest3 = backtest_beta(price_df, all_pbr[length*2:length*3], start_date, end_date, initial_money)
    pbr_backtest4 = backtest_beta(price_df, all_pbr[length*3:length*4], start_date, end_date, initial_money)
    pbr_backtest5 = backtest_beta(price_df, all_pbr[length*4:], start_date, end_date, initial_money)

    plt.figure(figsize=(11, 7))
    pbr_backtest1['총변화율'].plot(label='PBR1')
    pbr_backtest2['총변화율'].plot(label='PBR2')
    pbr_backtest3['총변화율'].plot(label='PBR3')
    pbr_backtest4['총변화율'].plot(label='PBR4')
    pbr_backtest5['총변화율'].plot(label='PBR5')
    plt.legend()
    plt.show()

def test3():
    # fscroe pbr per 백테스트 (Ch5. 백테스트.ipynb)
    strategy_date = '2015/12'
    start_date = '2016-6'
    end_date = '2017-5'
    initial_money = 100000000
    f_score_result = get_fscore(select_code_by_price(price_df, fs_df, start_date), strategy_date, 20)
    f_score_backtest = backtest_beta(price_df, f_score_result, start_date, end_date, initial_money)

    low_pbr = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PBR', strategy_date, 20)
    low_per = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PER', strategy_date, 20)
    pbr_backtest = backtest_beta(price_df, low_pbr, start_date, end_date, initial_money)
    per_backtest = backtest_beta(price_df, low_per, start_date, end_date, initial_money)

    plt.figure(figsize=(10, 6))
    pbr_backtest['총변화율'].plot(label='PBR')
    per_backtest['총변화율'].plot(label='PER')
    f_score_backtest['총변화율'].plot(label='F-Score')
    plt.legend()
    plt.show()

#test1()
#test2()
#test3()


'''
# 백테스트 기간이 주어지면 리밸런싱 주기로 나누기
start_date = '2015-6'
end_date = '2018-5'
start_year = int(start_date.split('-')[0])
end_year = int(end_date.split('-')[0])
for temp in range(start_year, end_year):
    print(str(temp) + '-6', str(temp+1) + '-6')
'''


'''
# 2기간 동안 리밸런싱 한 번 하면서 백테스트 하기
start_date1 = '2016-6'
end_date1 = '2017-5'
strategy_date1 = get_strategy_date(start_date1)
initial_money1 = 100000000

low_per1 = get_value_rank(select_code_by_price(price_df, invest_df, start_date1), 'PER', strategy_date1, 20)
per_backtest1 = backtest_beta(price_df, low_per1, start_date1, end_date1, initial_money1)

start_date2 = '2017-6'
end_date2 = '2018-5'
strategy_date2 = get_strategy_date(start_date2)
initial_money2 = 100000000

low_per2 = get_value_rank(select_code_by_price(price_df, invest_df, start_date2), 'PER', strategy_date2, 20)
per_backtest2 = backtest_beta(price_df, low_per2, start_date2, end_date2, initial_money2)

print(per_backtest1)
print(per_backtest2)
'''

'''
# [코드 5.27] 2기간 동안 리밸런싱 한 번 하면서 백테스트 하기 개선 (Ch5. 백테스트.ipynb)
start_date1 = '2016-6'
end_date1 = '2017-6'
strategy_date1 = get_strategy_date(start_date1)
initial_money1 = 100000000

low_per1 = get_value_rank(select_code_by_price(price_df, invest_df, start_date1), 'PER', strategy_date1, 20)
per_backtest1 = backtest_beta(price_df, low_per1, start_date1, end_date1, initial_money1)
temp_end1 = per_backtest1[end_date1].index[0]  # 6월까지의 결과
per_backtest1 = per_backtest1[:temp_end1]  # 6월 1일 첫째일까지의 결과

start_date2 = '2017-6'
end_date2 = '2018-6'
strategy_date2 = get_strategy_date(start_date2)
initial_money2 = per_backtest1['종합포트폴리오'][-1]  # 다음분기의 init money

low_per2 = get_value_rank(select_code_by_price(price_df, invest_df, start_date2), 'PER', strategy_date2, 20)
per_backtest2 = backtest_beta(price_df, low_per2, start_date2, end_date2, initial_money2)
temp_end2 = per_backtest2[end_date2 ].index[0]
per_backtest2 = per_backtest2[:temp_end2]

# 붙이기, 변화율 재계산
total_backtest = pd.concat([per_backtest1[:-1], per_backtest2])
total_backtest['일변화율'] = total_backtest['종합포트폴리오'].pct_change()
total_backtest['총변화율'] = total_backtest['종합포트폴리오']/ total_backtest['종합포트폴리오'][0] - 1

print(total_backtest)
'''


'''
# 리밸런싱 코드 for문으로 정리 (Ch5. 백테스트.ipynb)
start_date = '2016-6'
end_date = '2018-5'
initial_money = 100000000

start_year = int(start_date.split('-')[0])
end_year = int(end_date.split('-')[0])

total_df = 0
for temp in range(start_year, end_year):
    this_term_start = str(temp) + '-6'
    this_term_end = str(temp + 1) + '-6'
    strategy_date = get_strategy_date(this_term_start)
    low_per = get_value_rank(select_code_by_price(price_df, invest_df, this_term_start), 'PER',
                                          strategy_date, 20)
    per_backtest = backtest_beta(price_df, low_per, this_term_start, this_term_end, initial_money)
    temp_end = per_backtest[this_term_end].index[0]
    per_backtest = per_backtest[:temp_end]
    initial_money = per_backtest['종합포트폴리오'][-1]
    if temp == start_year:
        total_df = per_backtest
    else:
        total_df = pd.concat([total_df[:-1], per_backtest])

total_df['일변화율'] = total_df['종합포트폴리오'].pct_change()
total_df['총변화율'] = total_df['종합포트폴리오'] / total_df['종합포트폴리오'][0] - 1

print(total_df)
total_df.to_excel('total_df.xlsx')
'''


'''
# [코드 5.31] 저PER 전략 리밸러싱 있는 경우와 없는 경우 비교 (Ch5. 백테스트.ipynb)
start_date = '2016-6'
end_date = '2018-5'
initial_money = 100000000

start_year = int(start_date.split('-')[0])
end_year = int(end_date.split('-')[0])

total_df = 0
for temp in range(start_year, end_year):
    this_term_start = str(temp) + '-6'
    this_term_end = str(temp + 1) + '-6'
    strategy_date = get_strategy_date(this_term_start)
    low_per = get_value_rank(select_code_by_price(price_df, invest_df, this_term_start), 'PER',
                                          strategy_date, 20)
    per_backtest = backtest_beta(price_df, low_per, this_term_start, this_term_end, initial_money)
    temp_end = per_backtest[this_term_end].index[0]
    per_backtest = per_backtest[:temp_end]
    initial_money = per_backtest['종합포트폴리오'][-1]
    if temp == start_year:
        total_df = per_backtest
    else:
        total_df = pd.concat([total_df[:-1], per_backtest])

total_df['일변화율'] = total_df['종합포트폴리오'].pct_change()
total_df['총변화율'] = total_df['종합포트폴리오'] / total_df['종합포트폴리오'][0] - 1

low_per = get_value_rank(select_code_by_price(price_df, invest_df, start_date), 'PER',
                                      get_strategy_date(start_date), 20)
per_backtest = backtest_beta(price_df, low_per, start_date, end_date, initial_money)

plt.figure(figsize=(10, 6))
total_df['총변화율'].plot(label='rebal')  # code 수정
per_backtest['총변화율'].plot(label='No-rebal')
plt.legend()
plt.show()
'''


# 리밸런싱 백테스트 함수화 (Ch5. 백테스트.ipynb)
def backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, num, value_type=None,
                value_list=None, date_range=None):
    start_year = int(start_date.split('-')[0])
    end_year = int(end_date.split('-')[0])

    total_df = 0
    for temp in range(start_year, end_year):
        this_term_start = str(temp) + '-' + start_date.split('-')[1]
        this_term_end = str(temp + 1) + '-' + start_date.split('-')[1]
        strategy_date = get_strategy_date(this_term_start)

        if strategy.__name__ == 'high_roa':
            st_df = strategy(select_code_by_price(price_df, fr_df, this_term_start), strategy_date, num)
        elif strategy.__name__ == 'magic_formula':
            st_df = strategy(select_code_by_price(price_df, invest_df, this_term_start), strategy_date, num)
        elif strategy.__name__ == 'get_value_rank':
            st_df = strategy(select_code_by_price(price_df, invest_df, this_term_start), value_type, strategy_date, num)
        elif strategy.__name__ == 'make_value_combo':
            st_df = strategy(value_list, select_code_by_price(price_df, invest_df, this_term_start), strategy_date, num)
        elif strategy.__name__ == 'get_fscore':
            st_df = strategy(select_code_by_price(price_df, fs_df, this_term_start), strategy_date, num)
        elif strategy.__name__ == 'get_momentum_rank':
            st_df = strategy(price_df, price_df[this_term_start].index[0], date_range, num)
        elif strategy.__name__ == 'get_value_quality':
            st_df = strategy(select_code_by_price(price_df, invest_df, this_term_start),
                             select_code_by_price(price_df, fs_df, this_term_start), strategy_date, num)

        backtest = backtest_beta(price_df, st_df, this_term_start, this_term_end, initial_money)
        temp_end = backtest[this_term_end].index[0]
        backtest = backtest[:temp_end]
        initial_money = backtest['종합포트폴리오'][-1]
        if temp == start_year:
            total_df = backtest
        else:
            total_df = pd.concat([total_df[:-1], backtest])

    total_df['일변화율'] = total_df['종합포트폴리오'].pct_change()
    total_df['총변화율'] = total_df['종합포트폴리오'] / total_df['종합포트폴리오'][0] - 1

    return total_df


'''
# [코드 5.33] 저PER과 저PBR 비교 (Ch5. 백테스트.ipynb)
start_date = '2015-6'
end_date = '2018-5'
initial_money = 100000000
strategy = get_value_rank

back_test_result1 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PER')
back_test_result2 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PBR')

plt.figure(figsize=(10, 6))
back_test_result1['총변화율'].plot(label='PER')
back_test_result2['총변화율'].plot(label='PBR')
plt.legend()
plt.show()
'''

'''
# [코드 5.34] 저PER과 저PBR, 혼합 전략 비교 (Ch5. 백테스트.ipynb)
start_date = '2015-6'
end_date = '2018-5'
initial_money = 100000000
strategy = get_value_rank
strategy2 = make_value_combo

back_test_result1 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PER')
back_test_result2 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PBR')
back_test_result3 = backtest_re(strategy2, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_list=['PER','PBR'])

plt.figure(figsize=(10, 6))
back_test_result1['총변화율'].plot(label='PER')
back_test_result2['총변화율'].plot(label='PBR')
back_test_result3['총변화율'].plot(label='Combo')
plt.legend()
plt.show()
'''

'''
# F-score와 혼합 전략 비교 (Ch5. 백테스트.ipynb)
start_date = '2016-6'
end_date = '2018-6'
initial_money = 100000000
strategy1 = make_value_combo
strategy2 = get_fscore

back_test_result1 = backtest_re(strategy1, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_list=['PER','PBR'])
back_test_result2 = backtest_re(strategy2, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20)

plt.figure(figsize=(10, 6))
back_test_result1['총변화율'].plot(label='Combo')
back_test_result2['총변화율'].plot(label='F-score')
plt.legend()
plt.show()
'''

'''
# F-score, PBR+PER, F-score+PBR+PER 전략 비교 (Ch5. 백테스트.ipynb)
start_date = '2016-6'
end_date = '2018-6'
initial_money = 100000000
strategy1 = make_value_combo
strategy2 = get_fscore
strategy3 = get_value_quality

back_test_result1 = backtest_re(strategy1, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_list=['PER','PBR'])
back_test_result2 = backtest_re(strategy2, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20)
back_test_result3 = backtest_re(strategy3, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20)

plt.figure(figsize=(10, 6))
back_test_result1['총변화율'].plot(label='PER+PBR')
back_test_result2['총변화율'].plot(label='F-score')
back_test_result3['총변화율'].plot(label='Value + F-score')
plt.legend()
plt.show()
'''


'''
# CAGR 계산 (Ch5. 백테스트.ipynb)
start_date = '2015-6'
end_date = '2018-5'
initial_money = 100000000
strategy = get_value_rank
back_test_result = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PER')

num_of_year = int(end_date.split('-')[0]) - int(start_date.split('-')[0])
CAGR = (back_test_result.iloc[-1]['종합포트폴리오'] / back_test_result.iloc[0]['종합포트폴리오']) ** (1/num_of_year) - 1
print(CAGR)
'''

'''
# MDD 계산 (Ch5. 백테스트.ipynb)
max_list = [0]
mdd_list = [0]
for i in back_test_result.index[1:]:
    max_list.append(back_test_result['총변화율'][:i].max())
    if max_list[-1] > max_list[-2]:
        mdd_list.append(0)
    else:
        mdd_list.append(min(back_test_result['총변화율'][i] - max_list[-1], mdd_list[-1]))
back_test_result['max'] = max_list
back_test_result['MDD'] = mdd_list


# [코드 5.39] MDD 그래프 그리기 (Ch5. 백테스트.ipynb)
plt.figure(figsize=(10, 7))
plt.subplot(2,1,1)
back_test_result['총변화율'].plot(label='return')
back_test_result['max'].plot(label='max')
plt.legend()

plt.subplot(2,1,2)
back_test_result['MDD'].plot(label='MDD', c='black')
plt.legend()
plt.show()
'''


# [코드 5.40] MDD 함수화 (Ch5. 백테스트.ipynb)
def get_mdd(back_test_df):
    max_list = [0]
    mdd_list = [0]
    for i in back_test_df.index[1:]:
        max_list.append(back_test_df['총변화율'][:i].max())
        if max_list[-1] > max_list[-2]:
            mdd_list.append(0)
        else:
            mdd_list.append(min(back_test_df['총변화율'][i] - max_list[-1], mdd_list[-1]))
    back_test_df['max'] = max_list
    back_test_df['MDD'] = mdd_list
    return back_test_df

# MDD 비교하기 (Ch5. 백테스트.ipynb)
start_date = '2015-6'
end_date = '2018-5'
initial_money = 100000000
strategy = get_value_rank
back_test_result1 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PER')
back_test_result2 = backtest_re(strategy, start_date, end_date, initial_money, price_df, fr_df, fs_df, 20, value_type='PBR')
back_test_result1 = get_mdd(back_test_result1)
back_test_result2 = get_mdd(back_test_result2)

plt.figure(figsize=(10, 7))
plt.subplot(2,1,1)
back_test_result1['총변화율'].plot(label='PER')
back_test_result1['max'].plot(label='PER')
back_test_result2['총변화율'].plot(label='PBR')
back_test_result2['max'].plot(label='PBR')
plt.legend()

plt.subplot(2,1,2)
back_test_result1['MDD'].plot(label='PER')
back_test_result2['MDD'].plot(label='PBR')
plt.legend()
plt.show()
