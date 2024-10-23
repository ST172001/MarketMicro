import pandas as pd
import helper as hp
import numpy as np
from tqdm import tqdm
def ohclv():
    dates=['03', '04', '05', '06', '07','10', '11', '12', '13', '14', '17', '18']
    file_path = 'symbols.txt'
    stock_symbols = set(hp.read_txt_file(file_path))
    open_prices_dict={}
    high_prices_dict={}
    low_prices_dict={}#symbol:[]
    closing_prices_dict={}
    volume_dict={}
    for symbol in stock_symbols:
        open_prices_dict[symbol]=[]
        high_prices_dict[symbol]=[]
        low_prices_dict[symbol]=[]
        closing_prices_dict[symbol]=[]
        volume_dict[symbol]=[]
    for date in tqdm(dates):
        df=pd.read_csv(f'CASH_Trades_{date}122012.csv')
        open_prices=hp.get_opening_prices(df,stock_symbols)
        high_prices=hp.get_high_prices(df,stock_symbols)
        low_prices=hp.get_low_prices(df,stock_symbols)
        close_prices=hp.get_closing_prices(df,stock_symbols)
        volumes=hp.get_volume(df,stock_symbols)
        for symbol in stock_symbols:
            high_prices_dict[symbol].append(np.log(high_prices[symbol]))
            low_prices_dict[symbol].append(np.log(low_prices[symbol]))
            open_prices_dict[symbol].append(np.log(open_prices[symbol]))
            closing_prices_dict[symbol].append(np.log(close_prices[symbol]))
            volume_dict[symbol].append(volumes[symbol])
    return high_prices_dict,low_prices_dict,open_prices_dict,closing_prices_dict,volume_dict
