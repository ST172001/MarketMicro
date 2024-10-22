import pandas as pd
import helper as hp
from tqdm import tqdm
import numpy as np
dates=['03', '04', '05', '06', '07','10', '11', '12', '13', '14', '17', '18']
file_path = 'symbols.txt'
stock_symbols = set(hp.read_txt_file(file_path))
transaction_prices=[]
for date in tqdm(dates):
    df=pd.read_csv(f'CASH_Trades_{date}122012.csv')
    transaction_prices_dict=hp.get_closing_prices(df,stock_symbols)
    print(transaction_prices_dict)
    transaction_prices.append(transaction_prices_dict)

#get eth rolls estimate
rolls_spread={}
closing_prices={}
for symbol in stock_symbols:
    closing_prices[symbol]=[]
    for ele in transaction_prices:
        closing_prices[symbol].append(ele[symbol])

rolls_spread = {}
for symbol, prices in closing_prices.items():
    if len(prices) > 2:
        deltas = np.diff(prices)
        cov_matrix = np.cov(deltas[:-1], deltas[1:])
        print(symbol,cov_matrix[0,1])
        if cov_matrix[0,1] <0:
            covariance = 2*np.sqrt(-1*cov_matrix[0, 1])
            rolls_spread[symbol] = covariance
        else:
            rolls_spread[symbol] = None 
    else:
        rolls_spread[symbol] = None 
for stock,spread in rolls_spread.items():
    print(stock,spread)
print(hp.get_average_bid_ask_spread(stock_symbols,['03']))