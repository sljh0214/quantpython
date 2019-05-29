import xlrd
import operator
import pandas as pd
import numpy as np
import requests
import bs4

# 마법공식
def magic(file_path):
    wb = xlrd.open_workbook(file_path)

    per_sh = wb.sheet_by_name('PER')
    per_dict = {}
    for i in range(1, per_sh.nrows):
        data = per_sh.row_values(i)
        name = data[0]
        per = data[1]
        if per > 0:
            per_dict[name] = per
    sorted_per = sorted(per_dict.items(), key=operator.itemgetter(1))
    per_rank = {}
    for num, firm in enumerate(sorted_per):
        per_rank[firm[0]] = num + 1

    roa_sh = wb.sheet_by_name('ROA')
    roa_dict = {}
    for i in range(1, roa_sh.nrows):
        data = roa_sh.row_values(i)
        name = data[0]
        roa = data[1]
        if roa != '':
            roa_dict[name] = roa
    sorted_roa = sorted(roa_dict.items(), key=operator.itemgetter(1), reverse=True)
    roa_rank = {}
    for num, firm in enumerate(sorted_roa):
        roa_rank[firm[0]] = num + 1

    total_rank = {}
    for name in roa_rank.keys():
        if name in per_rank.keys():
            total_rank[name] = per_rank[name] + roa_rank[name]
    sorted_total = sorted(total_rank.items(), key=operator.itemgetter(1))

    magic_rank = {}
    for num, firm in enumerate(sorted_total):
        magic_rank[firm[0]] = num + 1

    return magic_rank

# 마법공식 pandas
def magic_by_pd(path):
    per_data = pd.read_excel(path, sheet_name='PER', index_col=0)
    filtered_per = per_data[per_data['PER'] > 0]
    sorted_per = filtered_per.sort_values(by='PER')
    sorted_per['PER랭킹'] = sorted_per['PER'].rank()

    roa_data = pd.read_excel(path, sheet_name='ROA', index_col=0)
    filtered_roa = roa_data.dropna()
    filtered_roa.columns = ['ROA']
    sorted_roa = filtered_roa.sort_values(by='ROA', ascending=False)
    sorted_roa['ROA랭킹'] = sorted_roa.rank(ascending=False)

    total_df = pd.merge(sorted_per, sorted_roa, how='inner', left_index=True, right_index=True)

    total_df['종합랭크'] = (total_df['PER랭킹'] + total_df['ROA랭킹']).rank()
    return total_df.sort_values(by='종합랭크')

def make_price_dataframe(code, timeframe, count):
    url = 'https://fchart.stock.naver.com/sise.nhn?requestType=0'
    price_url = url + '&symbol=' + code + '&timeframe=' + timeframe + '&count=' + count
    price_data = requests.get(price_url)
    price_data_bs = bs4.BeautifulSoup(price_data.text, 'lxml')
    item_list = price_data_bs.find_all('item')

    date_list = []
    price_list = []
    for item in item_list:
        temp_data = item['data']
        datas = temp_data.split('|')
        date_list.append(datas[0])
        price_list.append(datas[4])

    price_df = pd.DataFrame({code: price_list}, index=date_list)
    return price_df

def make_code(x):
    x = str(x)
    return 'A' + '0' * (6-len(x)) + x

def make_code2(x):
    x = str(x)
    return '0' * (6 - len(x)) + x

# 시세 가격
def price_to_excel(inpath, outpath):
    code_data = pd.read_excel(inpath)
    code_data = code_data[['종목코드', '기업명']]
    code_data['종목코드'] = code_data['종목코드'].apply(make_code2)

    for num, code in enumerate(code_data['종목코드']):
        try:
            print(num, code)
            time.sleep(1)
            try:
                price_df = make_price_dataframe(code, 'day', '1500')
            except requests.exceptions.Timeout:
                time.sleep(60)
                price_df = make_price_dataframe(code, 'day', '1500')
            if num == 0:
                total_price = price_df
            else:
                total_price = pd.merge(total_price, price_df, how='outer', right_index=True, left_index=True)
        except ValueError:
            continue
        except KeyError:
            continue

    #  [코드 3.45] 인덱스 시간 데이터로 바꾸고 엑셀로 저장하기 (CH3. 데이터 수집하기 2.ipynb)
    total_price.index = pd.to_datetime(total_price.index)
    total_price.to_excel(outpath + '.xlsx')

# 포괄손익계산서, 재무상태표, 현금흐름표
def make_fs_dataframe(firm_code):
    # fs_tables[0] # 포괄손익계산서 연간 #fs_tables[1] # 포괄손익계산서 분기
    # fs_tables[2] # 재무상태표 연간 #fs_tables[3] # 재무상태표 분기
    # fs_tables[4] # 현금흐름표 연간 #fs_tables[5] # 현금흐름표 분기
    fs_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=103&stkGb=701&gicode=' + firm_code
    fs_page = requests.get(fs_url)
    fs_tables = pd.read_html(fs_page.text)

    temp_df = fs_tables[0]
    temp_df = temp_df.set_index(temp_df.columns[0])
    temp_df = temp_df[temp_df.columns[:4]]
    temp_df = temp_df.loc[['매출액', '영업이익', '당기순이익']]

    temp_df2 = fs_tables[2]
    temp_df2 = temp_df2.set_index(temp_df2.columns[0])
    temp_df2 = temp_df2.loc[['자산', '부채', '자본']]

    temp_df3 = fs_tables[4]
    temp_df3 = temp_df3.set_index(temp_df3.columns[0])
    temp_df3 = temp_df3.loc[['영업활동으로인한현금흐름']]

    fs_df = pd.concat([temp_df, temp_df2, temp_df3])

    return fs_df

# code, dataframe -> total df merge
def change_df(firm_code, dataframe):
    for num, col in enumerate(dataframe.columns):
        temp_df = pd.DataFrame({firm_code: dataframe[col]})
        temp_df = temp_df.T
        temp_df.columns = [[col] * len(dataframe), temp_df.columns]
        if num == 0:
            total_df = temp_df
        else:
            total_df = pd.merge(total_df, temp_df, how='outer', left_index=True, right_index=True)

    return total_df

# 재무 비율 df
def make_fr_dataframe(firm_code):
    fr_url = 'https://comp.fnguide.com/SVO2/asp/SVD_FinanceRatio.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=104&stkGb=701&gicode=' + firm_code
    fr_page = requests.get(fr_url)
    fr_tables = pd.read_html(fr_page.text)

    temp_df = fr_tables[0]
    temp_df = temp_df.set_index(temp_df.columns[0])
    temp_df = temp_df.loc[['유동비율계산에 참여한 계정 펼치기',  # 유동비율(유동자산 / 유동부채) * 100
                           '부채비율계산에 참여한 계정 펼치기',  # 부채비율(총부채 / 총자본) * 100
                           '영업이익률계산에 참여한 계정 펼치기',  # 영업이익률(영업이익 / 영업수익) * 100
                           'ROA계산에 참여한 계정 펼치기',  # ROA(당기순이익(연율화) / 총자산(평균)) * 100
                           'ROIC계산에 참여한 계정 펼치기']]  # ROIC(세후영업이익(연율화)/영업투하자본(평균))*100
    temp_df.index = ['유동비율', '부채비율', '영업이익률', 'ROA', 'ROIC']
    return temp_df

# [코드 3.23] 투자지표 데이터프레임을 만드는 함수 (CH3. 데이터 수집하기.ipynb)
def make_invest_dataframe(firm_code):
    invest_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=105&stkGb=701&gicode=' + firm_code
    invest_page = requests.get(invest_url)
    invest_tables = pd.read_html(invest_page.text)
    temp_df = invest_tables[1]

    temp_df = temp_df.set_index(temp_df.columns[0])
    temp_df = temp_df.loc[['PER계산에 참여한 계정 펼치기',  # PER수정주가(보통주) / 수정EPS
                           'PCR계산에 참여한 계정 펼치기',  # PCR수정주가(보통주) / 수정CFPS
                           'PSR계산에 참여한 계정 펼치기',  # PSR수정주가(보통주) / 수정SPS
                           'PBR계산에 참여한 계정 펼치기',  # PBR수정주가(보통주) / 수정BPS
                           '총현금흐름']]  # 총현금흐름세후영업이익 + 유무형자산상각비
    temp_df.index = ['PER', 'PCR', 'PSR', 'PBR', '총현금흐름']
    return temp_df

#  재무 데이터 전처리하는 함수
def get_finance_data(path):
    data_path = path
    raw_data = pd.read_excel(data_path, index_col=0)
    big_col = list(raw_data.columns)
    small_col = list(raw_data.iloc[0])
    new_big_col = []
    for num, col in enumerate(big_col):
        if 'Unnamed' in col:
            new_big_col.append(new_big_col[num - 1])
        else:
            new_big_col.append(big_col[num])
    raw_data.columns = [new_big_col, small_col]
    clean_df = raw_data.loc[raw_data.index.dropna()]
    return clean_df

# ROA 컬럼에서 N/A(IFRS) NaN으로 바꾸기
def check_IFRS(x):
    if x == 'N/A(IFRS)':
        return np.NaN
    else:
        return x

# PER기준으로 오름차순으로 정렬하여 주는 함수
def low_per(invest_df, index_date, num):
    invest_df[(index_date, 'PER')] = pd.to_numeric(invest_df[(index_date, 'PER')])
    per_sorted = invest_df.sort_values(by=(index_date, 'PER'))
    return per_sorted[index_date][:num]

# ROA기준으로 내림차순으로 정렬하여 주는 함수
def high_roa(fr_df, index_date, num):
    fr_df[(index_date, 'ROA')] = fr_df[(index_date, 'ROA')].apply(check_IFRS)
    fr_df[(index_date, 'ROA')] = pd.to_numeric(fr_df[(index_date, 'ROA')] )
    sorted_roa = fr_df.sort_values(by=(index_date, 'ROA'), ascending=False)
    return sorted_roa[index_date][:num]

# 마법공식 함수로 만들기
def magic_formula(fr_df, invest_df, index_date, num):
    per = low_per(invest_df, index_date, None)
    roa = high_roa(fr_df, index_date, None)
    per['per순위'] = per['PER'].rank()
    roa['roa순위'] = roa['ROA'].rank(ascending=False)
    magic = pd.merge(per, roa, how='outer', left_index=True, right_index=True)
    magic['마법공식 순위'] = (magic['per순위'] + magic['roa순위']).rank().sort_values()
    magic = magic.sort_values(by='마법공식 순위')
    return magic[:num]
#print(magic_formula(fr_df, invest_df, '2018/12', 10))

# 저평가 지수를 기준으로 정렬하여 순위 만들어 주는 함수
def get_value_rank(invest_df, value_type, index_date, num):
    invest_df[(index_date,  value_type)] = pd.to_numeric(invest_df[(index_date,  value_type)])
    value_sorted = invest_df.sort_values(by=(index_date,  value_type))[index_date]
    value_sorted[  value_type + '순위'] = value_sorted[value_type].rank()
    return value_sorted[[value_type, value_type + '순위']][:num]
#print(get_value_rank(invest_df, 'PSR', '2018/12', 20))

# 저평가 지표 조합 함수 (CH4. 전략 구현하기.ipynb)
def make_value_combo(value_list, invest_df, index_date, num):
    for i, value in enumerate(value_list):
        temp_df = get_value_rank(invest_df, value, index_date, None)
        if i == 0:
            value_combo_df = temp_df
            rank_combo = temp_df[value + '순위']
        else:
            value_combo_df = pd.merge(value_combo_df, temp_df, how='outer', left_index=True, right_index=True)
            rank_combo = rank_combo + temp_df[value + '순위']

    value_combo_df['종합순위'] = rank_combo.rank()
    value_combo_df = value_combo_df.sort_values(by='종합순위')

    return value_combo_df[:num]
#r = make_value_combo(['PER', 'PBR'], invest_df, '2015/12', 20)
#r = make_value_combo(['PER', 'PBR', 'PSR', 'PCR'], invest_df, '2015/12', 20)

# F-score 함수
def get_fscore(fs_df, index_date, num):
    # pd.set_option('chained', None)
    fscore_df = fs_df[index_date]
    fscore_df['당기순이익점수'] = fscore_df['당기순이익'] > 0
    fscore_df['영업활동점수'] = fscore_df['영업활동으로인한현금흐름'] > 0
    fscore_df['더큰영업활동점수'] = fscore_df['영업활동으로인한현금흐름'] > fscore_df['당기순이익']
    fscore_df['종합점수'] = fscore_df[['당기순이익점수', '영업활동점수', '더큰영업활동점수']].sum(axis=1)
    fscore_df = fscore_df[fscore_df['종합점수'] == 3]
    return fscore_df[:num]
#print(get_fscore(fs_df, '2018/12', 10))

# 모멘텀 데이터프레임 만들기 함수화
def get_momentum_rank(price_df, index_date, date_range, num):
    momentum_df = pd.DataFrame(price_df.pct_change(date_range).loc[index_date])
    momentum_df.columns = ['모멘텀']
    momentum_df['모멘텀순위'] = momentum_df['모멘텀'].rank(ascending=False)
    momentum_df = momentum_df.sort_values(by='모멘텀순위')
    return momentum_df[:num]
#print(get_momentum_rank(price_df, '2016-12-29', 250, 20))

# 저평가 + Fscore 함수화
def get_value_quality(invest_df, fs_df, index_date, num):
    value = make_value_combo(['PER', 'PBR', 'PSR', 'PCR'], invest_df, index_date, None)
    quality = get_fscore(fs_df, index_date, None)
    value_quality = pd.merge(value, quality, how='outer', left_index=True, right_index=True)
    value_quality_filtered = value_quality[value_quality['종합점수'] == 3]
    vq_df = value_quality_filtered.sort_values(by='종합순위')
    return vq_df[:num]
#print(get_value_quality(invest_df, fs_df, '2015/12', 20))

# 백테스트 함수 버젼1
def backtest_beta(price_df, strategy_df, start_date, end_date, initial_money):
    code_list = []
    for code in strategy_df.index:
        code_list.append(code.replace('A', ''))
    strategy_price = price_df[code_list][start_date:end_date]
    pf_stock_num = {}
    stock_amount = 0
    stock_pf = 0
    each_money = initial_money / len(strategy_df)
    for code in strategy_price.columns:
        #strategy_price.fillna(1, inplace=True)  # 수정 code
        temp = int(each_money / strategy_price[code][0])
        pf_stock_num[code] = temp
        stock_amount = stock_amount + temp * strategy_price[code][0]
        stock_pf = stock_pf + strategy_price[code] * pf_stock_num[code]
    cash_amount = initial_money - stock_amount
    backtest_df = pd.DataFrame({'주식포트폴리오': stock_pf})
    backtest_df['현금포트폴리오'] = [cash_amount] * len(backtest_df)
    backtest_df['종합포트폴리오'] = backtest_df['주식포트폴리오'] + backtest_df['현금포트폴리오']
    backtest_df['일변화율'] = backtest_df['종합포트폴리오'].pct_change()
    backtest_df['총변화율'] = backtest_df['종합포트폴리오'] / initial_money - 1
    return backtest_df

# 해당 날짜에 가격이 없으면 투자 관련 데이터에서 해당 종목 없애는 함수
# get_value_rank 저PER 종목 037030 종목이 2016년 6월 데이터가 없음
# CompanyGuide 에는 2015/12 PER 데이터 있지만, 네이버에는 당시 가격 데이터가 존재하지 않음 (당시 비상장기업 때문)
# 비상장기업 CompanyGuide에 재무 데이터 등록된 경우. 전략 적용전 데이터프레임에서 제외
def select_code_by_price(price_df, data_df, start_date):
    new_code_list = []
    for code in price_df[start_date].iloc[0].dropna().index:
        new_code_list.append('A' + code)
    selected_df = data_df.loc[new_code_list]
    return selected_df


# 백테스트 시작날짜가 주어지면 전략 기준 날짜를 계산하는 함수
# 12월 재무 결과 다음 연도 6월에 사용
# 1월부터 시작하려면 2년전 데이터 사용
def get_strategy_date(start_date):
    temp_year = int(start_date.split('-')[0])
    temp_month = start_date.split('-')[1]
    if temp_month in '1 2 3 4 5'.split(' '):
        strategy_date = str(temp_year - 2) + '/12'
    else:
        strategy_date = str(temp_year - 1) + '/12'
    return strategy_date
