# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import zmq
import sys
import struct
import numpy as np
import copy
from market_snapshot import *
import get_main as gm
import get_datelist as gd
import pandas as pd
import os
import get_cwd as gc

tick_list = gm.get_tick()
ticker_list = gm.get_ticker()

quant_path = gc.get_quant()
path_prefix = quant_path+'/data/Ali/'
date_list = sorted(os.listdir(path_prefix))
files = [path_prefix+d+'/data.log' for d in date_list]
night_files = [path_prefix+d+'/data_night.log' for d in date_list]
file_list=[]
for i in zip(files, night_files):
  file_list.extend(list(i))

time_mid_map = {}
last_min = 0.0
for fl in file_list:
  if os.path.exists(fl):
    f = open(fl)
    for s in f:
      shot=MarketSnapshot()
      if shot.construct(s) == True:
        if shot.ticker not in time_mid_map:
          time_mid_map[shot.ticker] = {}
        time_min = round(shot.time,2)
        time_mid_map[shot.ticker][time_min] = ((shot.asks[0]+shot.bids[0])/2, (shot.asks[0]-shot.bids[0])/2)
      else:
        if s == 'End':
          break

np.save(quant_path+'/data/Mid/time_mid_map.npy', time_mid_map)

last = pd.DataFrame() 
for t in tick_list:
  print 'handling ' + t
  pair = gm.get_main(t)
  print pair
  if len(pair) < 2:
   continue
  map1 = time_mid_map[pair[0]]
  map2 = time_mid_map[pair[1]]
  temp1 = pd.DataFrame({'time':map1.keys(), pair[0]:[mv[0] for mv in map1.values()], 'spread':[mv[1] for mv in map1.values()]})
  temp2 = pd.DataFrame({'time':map2.keys(), pair[1]:[mv[0] for mv in map2.values()], 'spread':[mv[1] for mv in map2.values()]})
  df = pd.merge(temp1, temp2, how='outer', on='time')
  df.to_csv(quant_path+'/data/Mid/'+str(pair)+'.csv')
