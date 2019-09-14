# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import zmq
import sys
import struct
import numpy as np
import copy
from market_snapshot import *
import get_main as gm
import pandas as pd

tick_list = gm.get_tick()
ticker_list = gm.get_ticker()

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("ipc://backtest_data")
socket.setsockopt(zmq.SUBSCRIBE,'')

time_mid_map = {}
while True:
  response = socket.recv();
  s = response.split('\n')[0]
  shot=MarketSnapshot()
  if shot.construct(s) == True:
    if shot.ticker not in time_mid_map:
      time_mid_map[shot.ticker] = {}
    time_min = round(shot.time,1)
    time_mid_map[shot.ticker][time_min] = (shot.asks[0]+shot.bids[0])/2
  else:
    if s == 'End':
      break

last = pd.DataFrame() 
for t in ticker_list:
  print 'handling '+t
  if time_mid_map.has_key(t):
    temp_map = time_mid_map[t]
    temp = pd.DataFrame({'time':temp_map.keys(), t+'_mid':temp_map.values()})
    last = temp if last.empty else pd.merge(temp, last, how='outer', on='time')

last.to_csv("df")
