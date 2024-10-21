from datetime import datetime, timedelta
import pandas as pd
import pandas as pd
def jiffies_to_date(jiffies):
 #Convert jiffies to seconds
    start_date=datetime(1980, 1, 1)
    seconds = jiffies / 65535.0 # Calculate the resulting date
    result_date = start_date + timedelta(seconds=seconds)
    return result_date.strftime('%d-%m-%Y %H:%M:%S.%f')

def get_unique_symbols(df:pd.DataFrame):
    unique_symbols = df['symbol'].unique()  # Get unique symbols
    number_unique_symbols = len(unique_symbols)  # Count the number of unique symbols
    return unique_symbols, number_unique_symbols

def get_number_of_orders(df: pd.DataFrame, symbols: list):
    # Count the number of instances each symbol occurs in the 'symbol' column and return a dictionary
    order_counts = {}
    for symbol in symbols:
        order_counts[symbol] = df[df['symbol'] == symbol].shape[0]  # Count occurrences of the symbol
    return order_counts

def get_closing_price(df:pd.DataFrame,symbols:list):
    #Here df is the order book
    import pandas as pd

def get_last_traded_price(df: pd.DataFrame, symbols: list):
    #Here df is the order book
    # Create a dictionary with symbols and their last traded price
    last_trade_prices = {}
    for symbol in symbols:
        # Get the last traded price for the symbol
        last_price = df[df['symbol'] == symbol]['trade_price'].iloc[-1]
        last_trade_prices[symbol] = last_price  # Store the last trade price in the dictionary
    return last_trade_prices



def quoted_bid_ask_spread(df:pd.DataFrame, symbols:list,start_jiffy: int, end_jiffy: int):
    import pandas as pd

def quoted_bid_ask_spread(df: pd.DataFrame, symbols: list, start_jiffy: int, end_jiffy: int):
    spread_dict = {}
    df_filtered = df[(df['transaction_time'] >= start_jiffy) & (df['transaction_time'] <= end_jiffy)]
    for symbol in symbols:
        df_symbol = df_filtered[df_filtered['symbol'] == symbol]
        avg_bid = df_symbol[df_symbol['buy_sell'] == 0]['trigger_price'].mean()
        avg_ask = df_symbol[df_symbol['buy_sell'] == 1]['trigger_price'].mean()
        if avg_bid is not None and avg_ask is not None:
            spread = avg_ask - avg_bid
            spread_dict[symbol] = spread
        else:
            spread_dict[symbol] = None  # Handle cases where there might be no bid or ask prices
    return spread_dict




def get_quoted_bid_ask_spread(df:pd.DataFrame,symbols:list,frequency: int):
    #Here frequency is in minutes
    assert frequency%5==0, "Make sure that the frequency is a mutiple of 5 minutes"
    assert frequency>=5 and frequency<=375, "Make sure to enter a valid frequency"
    start_jiffy=df.iloc[0]['transaction_time']
    end_jiffy=df.iloc[-1]['transaction_time']
    frequency_in_jiffies=frequency*60*65535.0
    bid_totals = {symbol: 0 for symbol in symbols}
    ask_totals = {symbol: 0 for symbol in symbols}
    count_totals = {symbol: 0 for symbol in symbols}
    # Loop over each jiffy range
    for jiffy in range(start_jiffy, end_jiffy, frequency_in_jiffies):
        # Get the quoted bid-ask spreads for the current jiffy range
        quoted_spreads = quoted_bid_ask_spread(df, symbols, start_jiffy=jiffy, end_jiffy=jiffy + frequency_in_jiffies)
        # Accumulate bid and ask prices for each symbol
        for symbol, spread in quoted_spreads.items():
            if spread is not None:
                bid_totals[symbol] += spread['bid']
                ask_totals[symbol] += spread['ask']
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
    return avg_bid_ask_spreads

