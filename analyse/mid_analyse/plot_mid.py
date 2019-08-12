import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd
import self_input as si
import get_main as gm

date,mode = si.init()

#target_list = ['ni1905', 'ni1903']
#target_list = ['AP905', 'AP907']
#target_list = ['i1905', 'i1903']

tick="AP"
target_list = gm.get_main(tick)
#target_list = ['AP910', 'AP905']

file_name ='/root/quant/data/Mid/'+target_list[0][0:2]+'/'+target_list[0]+target_list[1]+'_'+date+mode+'_df.pds'
df = pd.read_csv(file_name)
diff_list = df['mid_delta'][~np.isnan(df['mid_delta'])]

train_rate = 1.0
train_size = int(len(diff_list)*train_rate)

train_diff_list = diff_list[0:train_size]
test_diff_list = diff_list[train_size:]

upline = np.percentile(np.array(train_diff_list), 90)
downline = np.percentile(np.array(train_diff_list), 10)
print 'up and down'
print upline
print downline

plt.plot(list(diff_list))
plt.axhline(y=upline, color='red', linestyle='-')
plt.axhline(y=downline, color='red', linestyle='-')
plt.legend()
plt.show()

for tl in target_list:
  plt.plot(list(df[tl+'_mid'][~np.isnan(df['mid_delta'])]), label=tl)
plt.legend()
plt.show()

print 'mean = '+ str(np.array(diff_list).mean()) + ', variance = '+ str(np.array(diff_list).var())

print 'running time is ' + str(time.time()-start_sec)
