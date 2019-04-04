import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd

pair=('NIF9', 'NIK9')
pair=('IFH9', 'IFZ8')
f = open('out.txt', 'r')
bids1 = []
asks1 = []
last1 = []

bids2 = []
asks2 = []
last2 = []

delta = []
buy_delta = []
sell_delta = []

for line in f:
    ticker, time, bids, asks, bsize, asize, last_trade, volume = line.split(' ')
    if ticker == 'ticker':
      continue
    if float(bids) <= 0.1:
      continue
    time = int(time)
    bids = float(bids)
    asks = float(asks)
    bsize = float(bsize)
    asize = float(asize)
    last_trade = float(last_trade)
    volume = float(volume)
    raw_ticker = ticker
    if raw_ticker == pair[0]:
      bids1.append(bids)
      asks1.append(asks)
      last1.append(last_trade)
      if len(last2) >0:
        delta.append(last1[-1] - last2[-1])
        buy_delta.append(asks1[-1]-bids2[-1])
        sell_delta.append(bids1[-1]-asks2[-1])
    if raw_ticker == pair[1]:
      bids2.append(bids)
      asks2.append(asks)
      last2.append(last_trade)
      if len(last1) >0:
        delta.append(last1[-1] - last2[-1])
        buy_delta.append(asks1[-1]-bids2[-1])
        sell_delta.append(bids1[-1]-asks2[-1])

#plt.plot(bids, label='bid', color='blue')
#plt.plot(asks, label='ask', color='green')
#plt.plot(last, label='last', color='red')

test_size = 150000
pct = 80
seq_len = len(buy_delta)
buy = buy_delta[0:-test_size]
sell = sell_delta[0:-test_size]
buy_up_pt = np.percentile(np.array(buy), pct)
buy_down_pt = np.percentile(np.array(buy), 100-pct)
sell_up_pt = np.percentile(np.array(sell), pct)
sell_down_pt = np.percentile(np.array(sell), 100-pct)
plt.plot([i for i in range(seq_len-test_size)], buy, label='buy_delta', color='blue')
plt.plot([i for i in range(seq_len-test_size)], sell, label='sell_delta', color='red')
plt.axhline(y=buy_up_pt, color='blue', linestyle='-')
plt.axhline(y=buy_down_pt, color='blue', linestyle='-')
plt.axhline(y=sell_up_pt, color='red', linestyle='-')
plt.axhline(y=sell_down_pt, color='red', linestyle='-')


buy_test = buy_delta[-test_size:]
sell_test = sell_delta[-test_size:]
plt.plot([i for i in range(seq_len-test_size, seq_len)], buy_test, color='green')
plt.plot([i for i in range(seq_len-test_size, seq_len)], sell_test, color='pink')

plt.show()
