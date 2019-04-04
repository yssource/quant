import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import sys
import numpy as np
import pandas as pd
import automail as am

pair=('NIF9', 'NIK9')
pair=('IFH9', 'IFZ8')

target_list = ['IFH9', 'IFZ8']
target_list = ['SFIT/NIK9/', 'SFIT/NIF9/']
target_list = ['ni1904', 'ni1901']

data_map = {}
spread_map = {}
spread_percent_map = {}
volume_map = {}
last_price_map = {}

print 'running example: python snapshot_analyse.py 2018-12-10 _night'
#f = open('out.txt')
#f = open('market_data.log')
#f = open('/root/Desktop/data.log')
#f = open('market_data.log')
date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
mode = ''
if len(sys.argv) == 2:
  date = sys.argv[1]
if len(sys.argv) == 3:
  date = sys.argv[1]
  mode = sys.argv[2]
#print date

f = open('/root/quant/data/Ali/'+date+'/data' + mode + '.log')
#f = open('/root/quant/data/Ali/data.log')

for line in f:
  shot=MarketSnapshot()
  if shot.construct(line) == True:
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
for tl in spread_map:
  plt.plot(spread_map[tl], label=tl)
  plt.legend()
  plt.show()
for tl in target_list:
  up = np.percentile(np.array(spread_map[tl]), 90)
  down = np.percentile(np.array(spread_map[tl]), 10)
  plt.plot(spread_map[tl], label=tl)
  plt.axhline(y=up, color='blue', linestyle='-')
  plt.axhline(y=down, color='blue', linestyle='-')
  plt.legend()
  plt.show()
  print tl
  print up
  print down
'''

report_threshold = 1000
report_count = 100
temp_count = 0

f=open('/root/quant/report/spread_report/spread_report_'+date+mode, 'w')
sorted_list = sorted(spread_percent_map.items(), key=lambda x:np.array(x[1]).mean(), reverse=True) 
f.write('Top '+str(report_count) +' contract(volume > '+str(report_threshold)+') record:\n')
for key, value in sorted_list:
  if volume_map[key] > report_threshold:
    temp_count = temp_count+1
    if temp_count > report_count:
      break;
    s = key + ' : mean_spread=' + str(np.array(value).mean()) + ' volume=' + str(volume_map[key]) + ' avg_price=' + str(np.array(last_price_map[key]).mean())
    f.write(s+'\n')

f.close()

f=open('/root/quant/report/spread_report/spread_report_'+date+mode, 'r')
email_content = f.read()
am.sendEmail(title='spread_report_'+date+mode, content=email_content)
f.close()
print 'running time is ' + str(time.time()-start_sec)
