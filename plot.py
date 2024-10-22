avg_bid_ask_spreads = {
    'CIPLA': {'average_bid': 409.30514822541653, 'average_ask': 366.88527256106113},
    'NTPC': {'average_bid': 157.9186158075559, 'average_ask': 160.2037509864947},
    'ASIANPAINT': {'average_bid': 4226.7830771130275, 'average_ask': 4378.720876425628},
    'AXISBANK': {'average_bid': 1303.253664635027, 'average_ask': 1321.4551299088625},
    'HDFC': {'average_bid': 819.7096735507336, 'average_ask': 823.020627773898},
    'BPCL': {'average_bid': 335.3788650114887, 'average_ask': 346.12325130238463},
    'INFY': {'average_bid': 2413.450382305996, 'average_ask': 2434.0626281935574},
    'ACC': {'average_bid': 1393.0000731615607, 'average_ask': 1430.4687668931358},
    'ICICIBANK': {'average_bid': 1084.108408017026, 'average_ask': 1100.2496342331533},
    'WIPRO': {'average_bid': 388.5964430787642, 'average_ask': 397.0372700583727},
    'RELIANCE': {'average_bid': 757.8658468385822, 'average_ask': 779.932711629269},
    'BAJAJ-AUTO': {'average_bid': 1910.5050348270192, 'average_ask': 1944.8507892734826},
    'IDFC': {'average_bid': 148.36694364760308, 'average_ask': 154.42042643868274},
    'ITC': {'average_bid': 291.77330758241766, 'average_ask': 294.80154090519585},
    'TCS': {'average_bid': 1304.3700921559584, 'average_ask': 1309.9893790734482},
    'ONGC': {'average_bid': 231.511653805229, 'average_ask': 248.52019941736242},
    'LT': {'average_bid': 1658.064841425362, 'average_ask': 1668.7422810596645},
    'TATAMOTORS': {'average_bid': 262.75819082251235, 'average_ask': 270.3233257680505},
    'MARUTI': {'average_bid': 1479.8987978181422, 'average_ask': 1485.8164431856917},
    'JPASSOCIAT': {'average_bid': 87.64042336271457, 'average_ask': 93.78103514473901}
}
actual_spreads = {
    'CIPLA': -42.4198756643554, 'NTPC': 2.2851351789388146, 'ASIANPAINT': 151.93779931260033,
    'AXISBANK': 18.201465273835514, 'HDFC': 3.3109542231643366, 'BPCL': 10.744386290895927,
    'INFY': 20.612245887561513, 'ACC': 37.468693731575095, 'ICICIBANK': 16.14122621612723,
    'WIPRO': 8.440826979608514, 'RELIANCE': 22.06686479068681, 'BAJAJ-AUTO': 34.34575444646347,
    'IDFC': 6.053482791079654, 'ITC': 3.028233322778193, 'TCS': 5.619286917489789,
    'ONGC': 17.00854561213342, 'LT': 10.677439634302403, 'TATAMOTORS': 7.565134945538149,
    'MARUTI': 5.917645367549497, 'JPASSOCIAT': 6.140611782024443
}

# Predicted values
predicted_spreads_rolls = {
    'CIPLA': None, 'NTPC': None, 'ASIANPAINT': 20.879601954486454, 'AXISBANK': 14.497482540082457,
    'HDFC': 8.805415000630616, 'BPCL': None, 'INFY': None, 'ACC': 9.696047304615016,
    'ICICIBANK': None, 'WIPRO': 2.2233608194203116, 'RELIANCE': None, 'BAJAJ-AUTO': 8.27896934004061,
    'IDFC': 2.1904337470008004, 'ITC': 3.4735828445248793, 'TCS': 19.764125750122897, 
    'ONGC': None, 'LT': 7.003737097673921, 'TATAMOTORS': None, 'MARUTI': 14.663105628299512
}

predicted_corwin_spreads = {
    'LT': 0, 'JPASSOCIAT': 0, 'ASIANPAINT': 46.92591304878815, 'TCS': 10.473014333575305, 
    'RELIANCE': 0, 'MARUTI': 18.456449810054842, 'HDFC': 7.605945704542663, 
    'BAJAJ-AUTO': 19.993791021575852, 'ICICIBANK': 11.05478352427919, 'ITC': 0, 
    'ONGC': 3.0285265985340177, 'IDFC': 3.577398812089482, 'CIPLA': 3.8764251390212396, 
    'NTPC': 0.20657148517896187, 'TATAMOTORS': 2.068192308898776, 'ACC': 12.539861617562083, 
    'BPCL': 0, 'INFY': 12.014376113098988, 'WIPRO': 1.6264615267880083, 'AXISBANK': 9.916870876507907
}

# Dictionary to store the percentage differences
percentage_differences = {}

# Loop over the actual spreads and calculate percentage difference if predicted is not None
for stock, actual_value in actual_spreads.items():
    predicted_value = predicted_corwin_spreads.get(stock)

    if predicted_value is not None:
        # Calculate percentage difference
        average_value = (avg_bid_ask_spreads[stock]['average_bid']+avg_bid_ask_spreads[stock]['average_ask'])/ 2
        percentage_diff = (abs(actual_value - predicted_value) / average_value) * 100
        percentage_differences[stock] = percentage_diff

# Print the percentage differences for each stock
for stock, percentage_diff in percentage_differences.items():
    print(f"{stock}: {percentage_diff:.2f}%")

import matplotlib.pyplot as plt

# Stock symbols and their percentage differences
stocks = list(percentage_differences.keys())
percentages = list(percentage_differences.values())

# Plotting
plt.figure(figsize=(10, 6))
plt.barh(stocks, percentages, color='skyblue')
plt.xlabel('Percentage Difference (%)')
plt.title('Percentage Difference between Actual and Predicted Bid-Ask Spread')

# Adding data labels on the bars
for index, value in enumerate(percentages):
    plt.text(value + 1, index, f'{value:.2f}%', va='center')

plt.tight_layout()
plt.show()
plt.savefig('cowins_estimate.png')