import matplotlib.pyplot as plt
from market_snapshot import *
import numpy as np

pair=('ni1901', 'ni1905')
f = open('data.txt', 'r')
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
  shot = MarketSnapshot()
  if shot.construct(line) == True:
    raw_ticker = shot.ticker
    if '/' in raw_ticker:
      raw_ticker = raw_ticker.split('/')[-2]
    if raw_ticker == pair[0]:
      bids1.append(shot.bids[0])
      asks1.append(shot.asks[0])
      last1.append(shot.last_trade)
      if len(last2) >0:
        delta.append(last1[-1] - last2[-1])
        buy_delta.append(asks1[-1]-bids2[-1])
        sell_delta.append(bids1[-1]-asks2[-1])
    if raw_ticker == pair[1]:
      bids2.append(shot.bids[0])
      asks2.append(shot.asks[0])
      last2.append(shot.last_trade)
      if len(last1) >0:
        delta.append(last1[-1] - last2[-1])
        buy_delta.append(asks1[-1]-bids2[-1])
        sell_delta.append(bids1[-1]-asks2[-1])
#print delta

#plt.plot(bids, label='bid', color='blue')
#plt.plot(asks, label='ask', color='green')
#plt.plot(last, label='last', color='red')

seq_len = len(buy_delta)
buy = buy_delta[0:-500]
sell = sell_delta[0:-500]
buy_up_pt = np.percentile(np.array(buy), 95)
buy_down_pt = np.percentile(np.array(buy), 5)
sell_up_pt = np.percentile(np.array(sell), 95)
sell_down_pt = np.percentile(np.array(sell), 5)
plt.plot([i for i in range(seq_len-500)], buy, label='buy_delta', color='blue')
plt.plot([i for i in range(seq_len-500)], sell, label='sell_delta', color='red')
plt.axhline(y=buy_up_pt, color='blue', linestyle='-')
plt.axhline(y=buy_down_pt, color='blue', linestyle='-')
plt.axhline(y=sell_up_pt, color='red', linestyle='-')
plt.axhline(y=sell_down_pt, color='red', linestyle='-')


buy_test = buy_delta[-500:]
sell_test = sell_delta[-500:]
plt.plot([i for i in range(seq_len-500, seq_len)], buy_test, color='green')
plt.plot([i for i in range(seq_len-500, seq_len)], sell_test, color='pink')

plt.show()
