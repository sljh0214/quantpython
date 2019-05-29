import requests
import bs4
import pandas as pd
import time
from utils_magic import *
#file_path = '마법공식 데이터.xlsx'
#path = 'data.xls'

'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    fs_df = make_fs_dataframe(code)
    fs_df_changed = change_df(code, fs_df)
    if num == 0 :
        total_fs = fs_df_changed
    else:
        total_fs = pd.concat([total_fs, fs_df_changed])
print(total_fs)
'''

'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    fr_df = make_fr_dataframe(code)
    fr_df_changed = change_df(code, fr_df)
    if num == 0 :
        total_fr = fr_df_changed
    else:
        total_fr = pd.concat([total_fr, fr_df_changed])
print(total_fr)
'''

'''
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']
for num, code in enumerate(firmcode_list):
    invest_df = make_invest_dataframe(code)
    invest_df_changed = change_df(code, invest_df)
    if num == 0 :
        total_invest = invest_df_changed
    else:
        total_invest = pd.concat([total_invest, invest_df_changed])
print(total_invest)
'''

path = 'data.xls'
code_data = pd.read_excel(path)
code_data = code_data[['종목코드', '기업명']]
code_data['종목코드'] = code_data['종목코드'].apply(make_code)

'''
# 재무제표데이터
for num, code in enumerate(code_data['종목코드']):
    try:
        print(num, code)
        time.sleep(1)
        try:
            fs_df = make_fs_dataframe(code)
        except requests.exceptions.Timeout:
            time.sleep(60)
            fs_df = make_fs_dataframe(code)
        fs_df_changed = change_df(code, fs_df)
        if num == 0 :
            total_fs = fs_df_changed
        else:
            total_fs = pd.concat([total_fs, fs_df_changed])
    except ValueError:
        continue
    except KeyError:
        continue
total_fs.to_excel('재무제표데이터.xlsx')
'''

'''
# 재무비율데이터
for num, code in enumerate(code_data['종목코드']):
    try:
        print(num, code)
        time.sleep(1)
        try:
            fr_df = make_fr_dataframe(code)
        except requests.exceptions.Timeout:
            time.sleep(60)
            fr_df = make_fr_dataframe(code)
        fr_df_changed = change_df(code, fr_df)
        if num == 0 :
            total_fr = fr_df_changed
        else:
            total_fr = pd.concat([total_fr, fr_df_changed])
    except ValueError:
        continue
    except KeyError:
        continue
total_fr.to_excel('재무비율데이터.xlsx')
'''

'''
# 투자지표데이터
for num, code in enumerate(code_data['종목코드']):
    try:
        print(num, code)
        time.sleep(1)
        try:
            invest_df = make_invest_dataframe(code)
        except requests.exceptions.Timeout:
            time.sleep(60)
            invest_df = make_invest_dataframe(code)
        invest_df_changed = change_df(code, invest_df)
        if num == 0 :
            total_invest = invest_df_changed
        else:
            total_invest = pd.concat([total_invest, invest_df_changed])
    except ValueError:
        continue
    except KeyError:
        continue
total_invest.to_excel('투자지표데이터.xlsx')
'''