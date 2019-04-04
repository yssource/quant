import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import get_cwd as gd
import get_main as gm
import sys
from scipy.stats import kstest
from GetFee import Cal_Fee, Cal_Fee_Point
from get_main import GetContract

if len(sys.argv) < 2:
  tick_list = gm.get_main('AP')
else:
  tick_list = gm.get_main(sys.argv[1])
print tick_list
tick_list = ['IC1903', 'IC1906']

con = GetContract(tick_list[0])

path = gd.get_quant()+'/data/Mid/'+str(tick_list)+'.csv'
df = pd.read_csv(path)
print df.head()

start = min(df['time'])
start='2019-01-27'
print start+' 8:00:00'
start_sep = time.mktime(time.strptime(start+' 08:00:00', "%Y-%m-%d %H:%M:%S"))
end = max(df['time'])
days = int((end-start_sep)/(24*3600)+1)
print 'days is ' + str(days)
#start=time.strftime("%Y-%m-%d", time.localtime(start_sep))
end=time.strftime("%Y-%m-%d", time.localtime(end))

# 16:00 is a sep
sep = [start_sep+i*24*3600 for i in range(days+1)]
print sep

df = df[df['time'] > start_sep].reset_index()

col = df.columns
for i in range(days):
  d = {c:-9.91 for c in col}
  d['time'] = sep[i]
  df.loc[df['time'].count()+i] = d


df = df.sort_values('time').reset_index()
index_list = df[df[tick_list[0]]<0].index
print index_list
print df[tick_list[0]].head()
print df[tick_list[1]].head()
df['delta'] = df[tick_list[0]]-df[tick_list[1]]
m=df[~np.isnan(df['delta'])]#.reset_index()#drop=True)

plt.title(str(tick_list)+str(start)+' to '+str(end))
mid = np.array(m['delta'])
#spread = np.array(m['spread'])
plt.plot(m['delta'], label = 'mid')
#plt.plot(mid+spread, label='ask')
#plt.plot(mid-spread, label='bid')
#plt.plot(spread, label='spread')
#for il in index_list:
#plt.vlines(index_list, 0,1, colors = "c", linestyles = "dashed")
ncol = 3
nrow = 4
#fig,ax = plt.subplots(nrows=int(days/ncol)+1,ncols=ncol,figsize=(15,8))
fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
#plt.subplots_adjust(wspace =0, hspace =0)
fig.tight_layout()

start_flag = time.mktime(time.strptime(start+' 00:00:00', "%Y-%m-%d %H:%M:%S"))
se = [start_flag+i*24*3600 for i in range(days+1)]
count = 0
for i in range(days):
  if count % (ncol*nrow) == 0 and count > 0:
    plt.show()
    fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
    fig.tight_layout()
  temp = se[i]
  p = m[m['time']>temp]
  p = p[p['time']<temp+24*3600]
  p = p[p['delta'] != 0]
  if len(p) < 100:
    print str(pd.to_datetime(temp, unit='s')) +' pass, bc len < 100'
    continue
  train_size = int(0.1*len(p))
  train_size = 600
  train = p[:train_size]
  #pv = [kstest(p['delta'][i-600:i].tolist(), 'norm')[1]*100 if i > 600 else 0.0 for i in range(len(p))]
  #print np.mean(pv)
  mean = np.array(train['delta'].tolist()).mean()
  mean_price_0 = train[tick_list[0]].mean()
  mean_price_1 = train[tick_list[1]].mean()
  std = np.array(train['delta'].tolist()).std()
  ax[int(count/ncol)%nrow, count%ncol].set_title(str(pd.to_datetime(temp, unit='s')))
  up_bound = mean + 2*std
  down_bound = mean - 2*std
  round_fee_point = 2*(Cal_Fee_Point(tick_list[0], price=mean_price_0, flag='open') + Cal_Fee_Point(tick_list[0], price=mean_price_0, flag='close_today')) + 2*(Cal_Fee_Point(tick_list[1], price=mean_price_1, flag='open') + Cal_Fee_Point(tick_list[1], price=mean_price_1, flag='close_today'))
  dev = (max(p['delta']) - min(p['delta']))*0.1
  #ax[int(count/ncol)%nrow, count%ncol].set_ylim((min(min(p['delta']), down_bound-dev), max(max(p['delta']), up_bound+dev)))
  #ax[int(count/ncol)%nrow, count%ncol].plot(pv, label='p-value')
  ax[int(count/ncol)%nrow, count%ncol].plot(p['delta'].tolist(), label='mid')
  ax[int(count/ncol)%nrow, count%ncol].axhline(mean, label='mean',c ='red')
  ax[int(count/ncol)%nrow, count%ncol].axhline(mean+2*std+round_fee_point, label='up bound',c ='green')
  ax[int(count/ncol)%nrow, count%ncol].axhline(mean-2*std-round_fee_point, label='down bound',c ='black')
  ax[int(count/ncol)%nrow, count%ncol].axvline(600, label='train',c ='orange')
  #ax[int(count/ncol)%nrow, count%ncol].legend(loc='upper left')
  count += 1

plt.legend()
plt.show()
