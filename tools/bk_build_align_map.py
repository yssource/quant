import pandas as pd
from market_snapshot import *
import numpy as np
import sys
import time
import os
import get_main as gm

tick_list = gm.get_tick()
ticker_list = gm.get_ticker()

def build(file_name, target_list = ['ni1905', 'ni1903']):
  tick = target_list[0][0:2]
  if os.path.exists('/root/quant/data/Mid/'+tick) == False:
    os.makedirs('/root/quant/data/Mid/'+tick)
  time_mid_map = {}
  mid_map = {}
  date = file_name.split('/')[-2]
  mode = file_name.split('/')[-1].split('.')[0][4:]
  save_file ='/root/quant/data/Mid/'+tick+'/'+target_list[0]+target_list[1]+'_'+date+mode+'_df.pds'
  mid_save_file ='/root/quant/data/Mid/'+tick+'/'+target_list[0]+target_list[1]+'_'+date+mode+'_mid.npy'
  if os.path.exists(save_file) == True:
    print save_file + ' exsited! do nothing'
    return
  if os.path.exists(mid_save_file) == True:
    print mid_save_file + ' exsited! do nothing'
    return
  f = open(file_name)
  for line in f:
    shot=MarketSnapshot()
    if shot.construct(line) == True:
      if shot.ticker not in time_mid_map:
        time_mid_map[shot.ticker] = {}
        mid_map[shot.ticker] = []
      time_min = round(shot.time,1)
      time_mid_map[shot.ticker][time_min] = (shot.asks[0]+shot.bids[0])/2
      mid_map[shot.ticker].append((shot.asks[0]+shot.bids[0])/2)
  
  map1 = time_mid_map[target_list[0]]
  map2 = time_mid_map[target_list[1]]
  map1 = {'time':map1.keys(), target_list[0]+'_mid':map1.values()}
  map2 = {'time':map2.keys(), target_list[1]+'_mid':map2.values()}
  df1 = pd.DataFrame(map1)
  df2 = pd.DataFrame(map2)
  
  df = (df1.set_index('time')).join(df2.set_index('time'))
  df['mid_delta'] = df[target_list[0]+'_mid'] - df[target_list[1]+'_mid']
  df = df.sort_values(by='time').reset_index()

  mid_seq = df['mid_delta'][~np.isnan(df['mid_delta'])]
  np.save(mid_save_file, np.array(list(mid_seq)))
  
  nan_ratio = np.isnan(df['mid_delta']).sum()*1.0 / len(df['mid_delta'])
  print 'nan ratio is ', nan_ratio
  
  df.to_csv(save_file)
