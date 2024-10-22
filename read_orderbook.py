import pandas as pd
import tqdm
import helper as hp
file_path = 'symbols.txt'
stock_symbols = set(hp.read_txt_file(file_path))
file_path = 'CASH_Orders_18122012.DAT'
count=0
message_layout=[2,4,16,14,1,1,10,2,8,8,8,8,1,1,1,1,1]
def extract_message(message, message_layout):
    data=[]
    start=0
    for ele in message_layout:
        data.append(message[start:start+ele])
        start+=ele
    return data
data=[]
import time
st=time.time()
column_names=['record_indicator', 'segment', 'order_number', 'transaction_time',
       'buy_sell', 'activity_type', 'symbol', 'series', 'volumne_disclosed',
       'volume_original', 'limit_price', 'trigger_price', 'market_order_flag',
       'stop_loss_flag', 'io_flag', 'algo_indicator', 'client_identity_flag']
with open(file_path, 'r') as file:
    for line in tqdm.tqdm(file):
        cur_data=extract_message(line.strip(),message_layout)
        symb=cur_data[6]
        if symb.lstrip('b') not in stock_symbols or cur_data[0]=='PO':
            continue
        data.append(extract_message(line.strip(),message_layout))
        count+=1
df = pd.DataFrame(data, columns=column_names)
df.to_csv(file_path.split('.')[0]+'.csv',index=False)
print(count)
print(f'Time required to complete is {time.time()-st}')
#RM CASH 2012091100008965 67621495462032 B 4 bbbbbbBHEL EQ 00000000 00000020 00019000 00000000 NNN 1 3