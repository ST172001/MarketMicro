import helper as hp
import pandas as pd
import numpy as np
from tqdm import tqdm
dates=['03', '04', '05', '06', '07','10', '11', '12', '13', '14', '17', '18']
# dates=['03']

file_path = 'symbols.txt'
stock_symbols = set(hp.read_txt_file(file_path))
average_bid_ask_date_wise={}
for stock in stock_symbols:
    average_bid_ask_date_wise[stock]=[]
for date in tqdm(dates):
    df=pd.read_csv(f'CASH_Orders_{date}122012.csv')
    # df=pd.read_csv('sample.csv')
    bid_frequencies,ask_frequencies,avg_bid_ask=hp.get_quoted_bid_ask_spread(df,stock_symbols,frequency=50)
    for stock in stock_symbols:
        if avg_bid_ask[stock]['average_ask'] is not None and avg_bid_ask[stock]['average_bid'] is not None: 
            average_bid_ask_date_wise[stock].append(avg_bid_ask[stock]['average_ask']-avg_bid_ask[stock]['average_bid'])
        else:
            average_bid_ask_date_wise[stock].append(None)


df_avg_bid_ask = pd.DataFrame(average_bid_ask_date_wise, index=dates).T
df_avg_bid_ask.reset_index(inplace=True)
df_avg_bid_ask.rename(columns={'index': 'stock_symbol'}, inplace=True)
df_avg_bid_ask.to_csv('ground_truth_daily.csv',index=False)


