import pandas as pd
df=pd.read_csv('CASH_Orders_03122012_symbols.csv')
df=df.head(10000)
df.to_csv('sample.csv',index=False)
