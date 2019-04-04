import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd

pair=('NIF9', 'NIK9')
pair=('IFH9', 'IFZ8')

target_list = ['IFH9', 'IFZ8']
target_list = ['IFH9']
target_list = ['NI1901', 'NI1904']

data_map = {}
spread_map = {}
spread_percent_map = {}
volume_map = {}
last_price_map = {}

#f = open('market_data.log')
f = open('/root/data.log')
#f = open('sfit')

count = -1
for line in f:
  count = count+1
  #print count
  shot=MarketSnapshot()
  if shot.sql_construct(line) == True:
    #shot.Show()
    if shot.bid_sizes[0] < 0.1 or shot.ask_sizes[0] < 0.1:
      continue
    if len(shot.ticker) > 10:
      continue
    if shot.last_trade < 0.1:
      continue
    if shot.ticker in spread_map:
      spread_map[shot.ticker].append(shot.asks[0]-shot.bids[0])
      spread_percent_map[shot.ticker].append((shot.asks[0]-shot.bids[0])*1.0/shot.last_trade)
      volume_map[shot.ticker] = shot.volume
      last_price_map[shot.ticker] = shot.last_trade
    else:
      spread_map[shot.ticker] = []
      spread_percent_map[shot.ticker] = []
      last_price_map[shot.ticker] = []
      spread_map[shot.ticker].append(shot.asks[0]-shot.bids[0])
      spread_percent_map[shot.ticker].append((shot.asks[0]-shot.bids[0])*1.0/shot.last_trade)
      volume_map[shot.ticker] = shot.volume
      last_price_map[shot.ticker].append(shot.last_trade)
  '''
  else:
    print "bad data "+line
    #sys.exit(1)
  '''

for tl in target_list:
  plt.plot(spread_map[tl], label=tl)
  plt.axhline(y=np.percentile(np.array(spread_map[tl]), 90), color='blue', linestyle='-')
  plt.axhline(y=np.percentile(np.array(spread_map[tl]), 10), color='blue', linestyle='-')
  plt.legend()
  plt.show()

sorted_list = sorted(spread_percent_map.items(), key=lambda x:np.array(x[1]).mean()) 
for key, value in sorted_list:
  print key + ' : mean_spread=' + str(np.array(value).mean()) + ' volume=' + str(volume_map[key]) + ' avg_price=' + str(np.array(last_price_map[key]).mean())

print 'running time is ' + str(time.time()-start_sec)
