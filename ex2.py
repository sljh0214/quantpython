import pandas as pd
from utils_magic import *

#fs_path = r'D:/work/stock/quant/재무제표데이터_2018.xlsx'
#fr_path = r'D:/work/stock/quant/재무비율데이터_2018.xlsx'
#invest_path = 'D:/work/stock/quant/투자지표데이터_2018.xlsx'
fs_path = r'D:/work/stock/quant/재무제표데이터_2019.xlsx'
fr_path = r'D:/work/stock/quant/재무비율데이터_2019.xlsx'
invest_path = 'D:/work/stock/quant/투자지표데이터_2019.xlsx'
fs_df = get_finance_data(fs_path)
fr_df = get_finance_data(fr_path)
invest_df = get_finance_data(invest_path)

# option
pd.set_option('chained', None)

# momentum
price_path = r'D:/work/stock/quant/가격데이터.xlsx'
#price_df = pd.read_excel(price_path, index_col=0)

# 저평가 데이터프레임과 F-score 데이터프레임 만들기 (CH4. 전략 구현하기.ipynb)
date = '2015/12'
value = make_value_combo(['PER', 'PBR', 'PSR', 'PCR'], invest_df, date, None)
quality = get_fscore(fs_df, date, None)

#print(value)
#print(quality)

# index 주식 코드 기준 병합
value_quality = pd.merge(value, quality, how='outer', left_index=True, right_index=True)
#print(value_quality)
#print(len(value_quality)) # 2263

value_quality_filtered = value_quality[value_quality['종합점수'] == 3]
#print(value_quality_filtered)
#print(len(value_quality_filtered)) # 428

vq_df = value_quality_filtered.sort_values(by='종합순위')
print(vq_df)
print(len(vq_df)) #



