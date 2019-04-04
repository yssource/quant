import matplotlib.pyplot as plt
from market_snapshot import *

f = open('data.txt', 'r')
bids = []
asks = []
last = []
for line in f:
  shot = MarketSnapshot()
  if shot.construct(line) == True:
    bids.append(shot.bids[0])
    asks.append(shot.asks[0])
    last.append(shot.last_trade)

plt.plot(bids, label='bid', color='blue')
plt.plot(asks, label='ask', color='green')
plt.plot(last, label='last', color='red')
plt.show()
