from datetime import datetime, timedelta
import pandas as pd
import pandas as pd
from tqdm import tqdm
def jiffies_to_date(jiffies):
 #Convert jiffies to seconds
    start_date=datetime(1980, 1, 1)
    seconds = jiffies / 65535.0 # Calculate the resulting date
    result_date = start_date + timedelta(seconds=seconds)
    return result_date.strftime('%d-%m-%Y %H:%M:%S.%f')

def save_symbols_dataframe(df: pd.DataFrame, symbols: list):
    # Filter rows where the 'symbol' column ends with one of the symbols in the list
    df_filtered = df[df['symbol'].str.lstrip('b').isin(symbols)]
    df_filtered.to_csv('CASH_Orders_03122012_symbols.csv')

def get_unique_symbols(df:pd.DataFrame):
    unique_symbols = df['symbol'].unique()  # Get unique symbols
    number_unique_symbols = len(unique_symbols)  # Count the number of unique symbols
    return unique_symbols, number_unique_symbols

def get_number_of_orders(df: pd.DataFrame, symbols: list):
    # Count the number of instances each symbol occurs in the 'symbol' column and return a dictionary
    order_counts = {}
    for symbol in symbols:
        order_counts[symbol] = df[df['symbol'].str.lstrip('b') == symbol].shape[0]  # Count occurrences of the symbol
    return order_counts

def quoted_bid_ask_spread(df: pd.DataFrame, symbols: list, start_jiffy: int, end_jiffy: int):
    spread_dict = {}
    df_filtered = df[(df['transaction_time'].astype(int) >= start_jiffy) & (df['transaction_time'].astype(int) <= end_jiffy)]
    for symbol in symbols:
        df_symbol = df_filtered[df_filtered['symbol'].str.lstrip('b') == symbol]
        avg_bid = df_symbol[df_symbol['buy_sell'] == 'B']['limit_price'].astype(int).mean()
        avg_ask = df_symbol[df_symbol['buy_sell'] == 'S']['limit_price'].astype(int).mean()
        if avg_bid is not None and avg_ask is not None and pd.notna(avg_bid) and pd.notna(avg_ask):
            spread_dict[symbol] = (avg_bid,avg_ask)
        else:
            spread_dict[symbol] = None  # Handle cases where there might be no bid or ask prices
    return spread_dict

def get_quoted_bid_ask_spread(df:pd.DataFrame,symbols:list,frequency: int):
    #Here frequency is in minutes
    assert frequency%5==0, "Make sure that the frequency is a mutiple of 5 minutes"
    assert frequency>=5 and frequency<=375, "Make sure to enter a valid frequency"
    start_jiffy=int(df.iloc[0]['transaction_time'])
    end_jiffy=int(df.iloc[-1]['transaction_time'])
    frequency_in_jiffies=frequency*60*65535
    bid_totals = {symbol: 0 for symbol in symbols}
    ask_totals = {symbol: 0 for symbol in symbols}
    count_totals = {symbol: 0 for symbol in symbols}
    bid_frquencies={symbol:[] for symbol in symbols}
    ask_frquencies={symbol:[] for symbol in symbols}
    # Loop over each jiffy range
    for jiffy in tqdm(range(start_jiffy, end_jiffy, frequency_in_jiffies)):
        # Get the quoted bid-ask spreads for the current jiffy range
        quoted_spreads = quoted_bid_ask_spread(df, symbols, start_jiffy=jiffy, end_jiffy=jiffy + frequency_in_jiffies)
        # Accumulate bid and ask prices for each symbol
        for symbol, spread in quoted_spreads.items():
            if spread is not None:
                bid_totals[symbol] += spread[0]/100.0
                ask_totals[symbol] += spread[1]/100.0
                bid_frquencies[symbol].append(spread[0]/100.0)
                ask_frquencies[symbol].append(spread[1]/100.0)
                count_totals[symbol] += 1
    # Calculate the average bid and ask prices for each symbol
    avg_bid_ask_spreads = {}
    for symbol in symbols:
        if count_totals[symbol] > 0:
            avg_bid = bid_totals[symbol] / count_totals[symbol]
            avg_ask = ask_totals[symbol] / count_totals[symbol]
            avg_bid_ask_spreads[symbol] = {'average_bid': avg_bid, 'average_ask': avg_ask}
        else:
            avg_bid_ask_spreads[symbol] = {'average_bid': None, 'average_ask': None}  # Handle cases where no valid intervals
    return bid_frquencies,ask_frquencies,avg_bid_ask_spreads

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().splitlines()  # Read the file and split by lines
    return content

def get_closing_prices(df:pd.DataFrame,symbols:list):
    #This is teh trade book
    closing_prices={}
    for symbol in symbols:
        closing_price = df[df['symbol'].str.lstrip('b') == symbol]['trade_price'].iloc[-1].astype(int)
        closing_prices[symbol]=closing_price/100.0
    return closing_prices

def get_average_bid_ask_spread(stock_symbols,dates):
    cumulative_bid = {symbol: 0 for symbol in stock_symbols}
    cumulative_ask = {symbol: 0 for symbol in stock_symbols}
    count = {symbol: 0 for symbol in stock_symbols}
    for date in dates:
        df=pd.read_csv(f'CASH_Orders_{date}122012.csv')
        bid_frequencies,ask_frequencies,avg_bid_ask=get_quoted_bid_ask_spread(df,stock_symbols,frequency=50)
        for symbol in stock_symbols:
            if symbol in avg_bid_ask:
                    if avg_bid_ask[symbol]['average_bid'] is not None and avg_bid_ask[symbol]['average_ask'] is not None:
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