import helper as hp
import pandas as pd
import time
st=time.time()
# Path to your text file
def get_average_bid_ask_spread(stock_symbols,dates):
    cumulative_bid = {symbol: 0 for symbol in stock_symbols}
    cumulative_ask = {symbol: 0 for symbol in stock_symbols}
    count = {symbol: 0 for symbol in stock_symbols}
    for date in dates:
        # df=pd.read_csv(f'CASH_Orders_{date}122012.csv')
        df=pd.read_csv('sample.csv')
        bid_frequencies,ask_frequencies,avg_bid_ask=hp.get_quoted_bid_ask_spread(df,stock_symbols,frequency=50)
        for symbol in stock_symbols:
            if symbol in avg_bid_ask:
                    cumulative_bid[symbol] += avg_bid_ask[symbol]['average_bid']
                    count[symbol] += 1
                    cumulative_ask[symbol] += avg_bid_ask[symbol]['average_ask']
    final_avg_bid_ask = {}
    for symbol in stock_symbols:
        if count[symbol] > 0:
            avg_bid = cumulative_bid[symbol] / count[symbol]
            avg_ask = cumulative_ask[symbol] / count[symbol]
            final_avg_bid_ask[symbol] = {'average_bid': avg_bid, 'average_ask': avg_ask}
        else:
            final_avg_bid_ask[symbol] = {'average_bid': None, 'average_ask': None}

    return final_avg_bid_ask

    