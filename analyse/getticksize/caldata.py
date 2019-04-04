import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd
import os
import datetime
import get_datelist as gd
import self_input as si

path_prefix=os.getcwd().split('quant')[0]
date,mode=si.init()

file_name = path_prefix+'quant/data/Ali/'+date+'/data' + mode + '.log'
if os.path.exists(file_name) == False:
  print file_name + ' not exist'
  sys.exit(1)

tick_spread_list_map = {}
volume_list_map = {}
spread_list_map = {}

tick_size_map = {}
volume_map = {}
mean_spread_map = {}

tick_list = []
ticker_list = []

f = open(file_name)
for line in f:
  shot=MarketSnapshot()
  if shot.construct(line) == True:
    ticker = shot.ticker
    count = -1
    for i in range(len(ticker)):
      if not ticker[i].isalpha():
        count = i
        break
    tick = ticker[0:count]
    if tick not in tick_list:
      tick_list.append(tick)
    if ticker not in ticker_list:
      ticker_list.append(ticker)
    if tick not in tick_spread_list_map:
      tick_spread_list_map[tick] = []
    tick_spread_list_map[tick].append(shot.asks[0]-shot.bids[0])
    if ticker not in volume_list_map:
      volume_list_map[ticker] = []
    volume_list_map[ticker].append(shot.volume)
    if ticker not in spread_list_map:
      spread_list_map[ticker] = []
    spread_list_map[ticker].append(shot.asks[0]-shot.bids[0])

for tick in tick_spread_list_map:
  tick_size = sorted(tick_spread_list_map[tick])[0]
  tick_size_map[tick] = tick_size

for ticker in volume_list_map:
  v = sorted(volume_list_map[ticker])[-1]
  volume_map[ticker] = v

for ticker in spread_list_map:
  m = np.array(spread_list_map[ticker]).mean()
  mean_spread_map[ticker] = m

def select_main(topn=2, metric='volume'):
  main_map = {}
  out_map = {}
  for ticker in ticker_list:
    count = -1
    for i in range(len(ticker)):
      if not ticker[i].isalpha():
        count = i
        break
    tick = ticker[0:count]
    if tick not in main_map:
      main_map[tick] = []
      out_map[tick] = []
    if metric == 'volume':
      main_map[tick].append((ticker, volume_map[ticker]))
    else:
      main_map[tick].append((ticker, mean_spread_map[ticker]))
  for ticker in ticker_list:
    count = -1
    for i in range(len(ticker)):
      if not ticker[i].isalpha():
        count = i
        break
    tick = ticker[0:count]
    sorted_list = sorted(main_map[tick], key=lambda x:x[1], reverse=(metric=='volume'))
    main_map[tick] = sorted_list
  for tick in tick_list:
    print main_map[tick][0:topn],
    print "tick_size is :"+str(tick_size_map[tick])
    for con in main_map[tick][0:topn]:
      out_map[tick].append(con[0])
  return out_map

out = select_main()

if os.path.exists(path_prefix+'quant/data/contract/'+date) == False:
  os.mkdir(path_prefix+'quant/data/contract/'+date)

np.save(path_prefix+'quant/data/contract/'+date+'/tick_size_map_'+'.npy', tick_size_map)
np.save(path_prefix+'quant/data/contract/'+date+'/volume_map_'+'.npy', volume_map)
np.save(path_prefix+'quant/data/contract/'+date+'/mean_spread_map_'+'.npy', mean_spread_map)
np.save(path_prefix+'quant/data/contract/'+date+'/tick_list'+'.npy', tick_list)
np.save(path_prefix+'quant/data/contract/'+date+'/ticker_list'+'.npy', ticker_list)
np.save(path_prefix+'quant/data/contract/'+date+'/main_map.npy', out)
    
print 'running time is ' + str(time.time()-start_sec)
