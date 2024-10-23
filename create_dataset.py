import helper as hp 
import pandas as pd
import numpy as np
import OHCLVC
df_ground_truth=pd.read_csv('ground_truth_daily.csv')
df_corwin_spread=pd.read_csv('corwin_spread.csv')
columns=['log_open','log_high','log_low','log_close','log_volume','corwin_spread','actual_spread']
stock_symbols=list(df_corwin_spread['stock_symbol'])
data=[]
high_prices_dict,low_prices_dict,open_prices_dict,closing_prices_dict,volume_dict=OHCLVC.ohclv()
dates=df_corwin_spread.columns[1:]
for i,date in enumerate(dates):
    for symbol in stock_symbols:
        data.append([open_prices_dict[symbol][i],high_prices_dict[symbol][i],low_prices_dict[symbol][i],closing_prices_dict[symbol][i],volume_dict[symbol][i],df_corwin_spread[df_corwin_spread['stock_symbol']==symbol][date].values[0],df_ground_truth[df_ground_truth['stock_symbol']==symbol][date].values[0]])
df=pd.DataFrame(data,columns=columns)
print(df.shape)
df.to_csv('dataset_regression.csv',index=False)

