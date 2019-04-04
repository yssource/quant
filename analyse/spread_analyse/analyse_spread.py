import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd

pair=('NIF9', 'NIK9')
pair=('IFH9', 'IFZ8')

target_list = ['IFH9', 'IFZ8']
target_list = ['IFH9']

data_map = {}
spread_map = {}
for tl in target_list:
  data_map[tl] = {'bids':[], 'asks':[], 'last_trade':[], 'spread':[]}
  spread_map[tl] = []

f = open('out.txt')

for line in f:
  shot = MarketSnapshot()
  if shot.s_construct(line) == True:
    #ticker, time, bids, asks, bsize, asize, last_trade, volume = line.split(' ')
    ticker = shot.ticker
    time = shot.time
    bids = shot.bids[0]
    bsize = shot.bid_sizes[0]
    asks = shot.asks[0]
    asize = shot.ask_sizes[0]
    last_trade = shot.last_trade
    volume = shot.volume
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
    if ticker in data_map:
      data_map[ticker]['bids'].append(bids)
      data_map[ticker]['asks'].append(asks)
      data_map[ticker]['last_trade'].append(last_trade)
      data_map[ticker]['spread'].append(asks-bids)
      spread_map[ticker].append(asks-bids)
      #if asks-bids > 10:
        #print line

for tl in target_list:
  plt.plot(spread_map[tl], label=tl)
plt.legend()
plt.show()
