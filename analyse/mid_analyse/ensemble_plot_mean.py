import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import build_align_map as bam
import sys
import numpy as np
import pandas as pd
import self_input as si
import math
import get_datelist as gd
import os

date_list = gd.get()
mode_list = ['', '_night']
target_list = ['ni1905', 'ni1903']
tick = "ni"
#print date_list

count = 0
nrow = 3
ncol = 2
fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
for date in date_list:
  for mode in mode_list:
    file_name ='/root/quant/data/Mid/'+tick+'/'+target_list[0]+target_list[1]+'_'+date+mode+'_df.pds'
    if not os.path.exists(file_name):
      continue
    count += 1
    df = pd.read_csv(file_name)
    diff_list = df['mid_delta'][~np.isnan(df['mid_delta'])]
    
    avg_list = [0]
    std_list = []
    s = 0.0
    std = 0.0
    var = 0.0
    diff_list=list(diff_list)
    for i in range(len(diff_list)):
      s += diff_list[i]
      avg = s / (i+1)
      var += diff_list[i]**2 + (avg-avg_list[-1])**2*i+avg**2-2*avg*diff_list[i]
      std = math.sqrt(var/(i+1))
      std_list.append(std)
      avg_list.append(avg)
      
    avg_list = avg_list[1:]

    ax[int((count-1)/ncol)%nrow, count%ncol].set_title(date+mode)
    ax[int((count-1)/ncol)%nrow, count%ncol].plot(avg_list, label='avg')
    ax[int((count-1)/ncol)%nrow, count%ncol].plot(std_list, label='std')
    ax[int((count-1)/ncol)%nrow, count%ncol].legend()
    if count % (nrow*ncol) == 0:
      plt.show()
      fig,ax = plt.subplots(nrow,ncol,figsize=(15,8))

    '''
    a=[]
    st=[]
    for i in range(len(diff_list)):
      a.append(np.array(diff_list[0:i+1]).mean())
      st.append(math.sqrt(np.array(diff_list[0:i+1]).var()))
    
    plt.plot(a, label='avg_real')
    plt.plot(st, label='std_real')
    plt.legend()
    plt.show()
    '''
