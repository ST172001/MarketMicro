import pandas as pd
import helper as hp
import numpy as np
from tqdm import tqdm
dates=['03', '04', '05', '06', '07','10', '11', '12', '13', '14', '17', '18']
file_path = 'symbols.txt'
stock_symbols = set(hp.read_txt_file(file_path))
high_prices_dict={}
low_prices_dict={}#symbol:[]
for symbol in stock_symbols:
    high_prices_dict[symbol]=[]
    low_prices_dict[symbol]=[]
for date in tqdm(dates):
    df=pd.read_csv(f'CASH_Trades_{date}122012.csv')
    high_prices=hp.get_high_prices(df,stock_symbols)
    low_prices=hp.get_low_prices(df,stock_symbols)
    for symbol in stock_symbols:
        high_prices_dict[symbol].append(high_prices[symbol])
        low_prices_dict[symbol].append(low_prices[symbol])
corwin_spread={}
for stock in stock_symbols:
    corwin_spread[stock]=[]
for stock in stock_symbols:
    for i in range(0,len(dates)-2):
        gamma=np.square(np.log(np.max(high_prices_dict[stock][i:i+2])/np.min(low_prices_dict[stock][i+2])))
        beta=(np.square(np.log(high_prices_dict[stock][i]/low_prices_dict[stock][i]))+np.square(np.log(high_prices_dict[stock][i+1]/low_prices_dict[stock][i+1])))
        alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / (3 - 2 * np.sqrt(2)) - np.sqrt(gamma) / np.sqrt(3 - 2 * np.sqrt(2))
        exp_alpha = np.exp(alpha)
        corwin_spread[stock].append((2 * (exp_alpha - 1)) / (1 + exp_alpha)*(np.max(high_prices_dict[stock][i:i+2])+np.min(high_prices_dict[stock][i:i+2]))/2)
        if corwin_spread[stock][-1]<0:
            corwin_spread[stock][-1]=0

df_corwin_spread = pd.DataFrame(corwin_spread, index=dates[:-2]).T
df_corwin_spread.reset_index(inplace=True)
df_corwin_spread.rename(columns={'index': 'stock_symbol'}, inplace=True)
df_corwin_spread.to_csv('corwin_spread.csv',index=False)

