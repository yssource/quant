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

date,mode = si.init()

target_list = ['ni1905', 'ni1903']
file_name ='/root/quant/data/Mid/'+target_list[0][0:2]+'/'+target_list[0]+target_list[1]+'_'+date+mode+'_df.pds'
df = pd.read_csv(file_name)
diff_list = df['mid_delta'][~np.isnan(df['mid_delta'])]
print diff_list

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
  print var
  std = math.sqrt(var/(i+1))
  std_list.append(std)
  avg_list.append(avg)
  
avg_list = avg_list[1:]

plt.plot(avg_list, label='avg')
plt.plot(std_list, label='std')

a=[]
st=[]
for i in range(len(diff_list)):
  a.append(np.array(diff_list[0:i+1]).mean())
  st.append(math.sqrt(np.array(diff_list[0:i+1]).var()))

plt.plot(a, label='avg_real')
plt.plot(st, label='std_real')
plt.legend()
plt.show()
