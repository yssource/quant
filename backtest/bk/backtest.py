import time
start_sec = time.time()
import matplotlib.pyplot as plt 
from market_snapshot import *
import sys 
import numpy as np
import pandas as pd

train_file = open('sfit')
#test_file = open('market_data_test')

pair = ('SFIT/PTK9/', 'SFIT/PTH9/')


buy_loss = []
sell_pro = []

time_map = {}
shot_map = {}
for i in pair:
  time_map[i] = -1
  shot_map[i] = MarketSnapshot()

time_diff_threshhold = 13*60  # 13 min

temp = []
# training
for line in train_file:
  shot=MarketSnapshot()
  if shot.construct(line) == True:
    if shot.ticker in pair:
      time_map[shot.ticker] = shot.time
      shot_map[shot.ticker] = shot
      if abs(time_map[pair[0]] - time_map[pair[1]]) > time_diff_threshhold:
        continue
      buy_loss.append(shot_map[pair[0]].asks[0] - shot_map[pair[1]].bids[0])
      sell_pro.append(shot_map[pair[0]].bids[0] - shot_map[pair[1]].asks[0])
      temp.append(buy_loss[-1]-sell_pro[-1])

#plt.plot(temp)
#plt.show()
#sys.exit(1)

pct = 70
train_ratio = 0.8
train_size = int(len(buy_loss)*train_ratio)


buy_up_pt = np.percentile(np.array(buy_loss[0:train_size]), pct)
buy_down_pt = np.percentile(np.array(buy_loss[0:train_size]), 100-pct)
print buy_up_pt
print buy_down_pt
sell_up_pt = np.percentile(np.array(sell_pro[0:train_size]), pct)
sell_down_pt = np.percentile(np.array(sell_pro[0:train_size]), 100-pct)

#plt.plot(buy_loss, color='blue', label='buy_loss')
#plt.plot(sell_pro, color='red', label='sell_pro')
plt.axhline(y=buy_up_pt, color='blue', linestyle='-', label='buy_up')
plt.axhline(y=buy_down_pt, color='grey', linestyle='-', label='buy_down')
plt.axhline(y=sell_up_pt, color='red', linestyle='-')
plt.axhline(y=sell_down_pt, color='red', linestyle='-')


plt.plot(buy_loss[train_size:], color='green', label='buy_loss_test')
plt.plot(sell_pro[train_size:], color='pink', label='sell_pro_test')

plt.legend()
plt.show()
# testing

print 'running time is ', time.time()-start_sec
