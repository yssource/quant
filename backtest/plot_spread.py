import matplotlib.pyplot as plt
from market_snapshot import *
import numpy as np
import pandas as pd
import sys
import os
import math

def plot_spread(df, pair, ax, title):
  df['delta'] = df[pair[0]] - df[pair[1]]
  m = df[~np.isnan(df['delta'])]
  ax.set_title(title)
  ax.plot(m['delta'], label='mid')

def HandleTime(t, with_tz_diff):
  t = str(t)
  # remove unknow char
  legal='1234567890: .'
  ms = 0.0
  for c in t:
    if c not in legal:
      t = t.replace(c, '')
  #print("pure time string is ", t)
  if '.' in t:
    ms = float('0.'+ t.split('.')[-1])
    t=t.split('.')[0]
  if ':' in t:  # readable time format
    l = t.split(':')
    if len(l) != 3:
      print('illegal time ' + t)
      return None
    hour = int(l[0])
    minu = int(l[1])
    sec = int(l[2].split('.')[0])
    #print(str(hour)+':'+str(minu)+':'+str(sec))
    return (hour*3600 + minu*60+sec+8*3600)%(24*3600)+ms if with_tz_diff else hour*3600 + minu*60+sec + ms
  else:  # unix timestamp
    #print('handling unix time')
    if len(t) == 10:
      return (int(t)+8*3600)%(24*3600)
    elif len(t) > 10:
      ms = float('0.'+ t[10:])
      return (int(t[:10])+8*3600)%(24*3600) + ms
    else:
      print('unknown unix time format '+ t)
      return None

def GetDF(file_path, ask_name, bid_name, time_name, tz_diff=False, header=False, using_name=None, ticker_filter=None):
  contract = file_path.split('/')[-1].split('.')[0]
  if not os.path.exists(file_path):
    return pd.DataFrame([])
  if os.path.getsize(file_path) < 100:
    return pd.DataFrame([])
  df = None
  if header == False:
    #print('reading %s' %(file_path))
    df = pd.read_csv(file_path, header=None)
    #print(df)
    shot = MarketSnapshot()
    if len(df.columns) != len(shot.get_columns()):
      print('df.columns len %d, shot.columns len %d' % (len(df.columns), len(shot.get_columns())))
      return pd.DataFrame([])
    df.columns = shot.get_columns()
  else:
    df = pd.read_csv(file_path)
  if ticker_filter != None:
    df = df[df['ticker']==ticker_filter]
  check_list = [ask_name, bid_name, time_name]
  for cl in check_list:
    if cl not in df.columns:
      print(cl+' not in df columns')
      sys.exit(1)
  df[bid_name] = df[bid_name].astype('float')
  df[ask_name] = df[ask_name].astype('float')
  df = df[df[bid_name] > 0.001]
  df = df[df[ask_name] > 0.001]
  df = df.reset_index()
  if using_name == None:
    df[contract] = (df[ask_name] + df[bid_name]) / 2
  else:
    df[using_name] = (df[ask_name] + df[bid_name]) / 2
  df['time'] = [HandleTime(df[time_name][i], tz_diff) for i in range(len(df))]
  df = df[df['time'] <= 15*3600]
  df = df[df['time'] >= 9*3600]
  df = df.reset_index()
  columns = [time_name, 'time', contract if using_name == None else "mid"]
  return df[columns]

def Merge(df1, df2):
  df = pd.merge(df1, df2, how='outer', on=['time'])
  df = df.sort_values(by='time').reset_index()
  return df

def Plot(df, main, hedge, date, ax, all_mid):
  delta = []
  for i in range(len(df)):
    if not np.isnan(df[main][i]):
      delta.append(None)
      for j in range(i,0,-1):
        if not np.isnan(df[hedge][j]):
          delta[-1] = df[main][i] - df[hedge][j]
          break
    else:
      delta.append(None)

  df['delta'] = delta
  d = df[~np.isnan(df['delta'])]
  all_mid.extend(d['delta'])
  train_ratio = 0.1
  mean = np.mean(d['delta'][:int(len(d)*train_ratio)])
  std = np.std(d['delta'][:int(len(d)*train_ratio)])
  ax.set_title('mid delta between[%s %s]@%s' %(main, hedge, date))
  ax.plot([i for i in range(len(d))], d['delta'])
  ax.axhline(mean, label='mean',c ='red')
  ax.axhline(mean+2*std, label='high bound',c ='green')
  ax.axhline(mean-2*std, label='low bound',c ='black')
  ax.axvline(int(train_ratio*len(d)), c ='black')
  ax.legend()

aname = "asks[0]"
bname = "bids[0]"
tname = "time_sec"

def SplitCon(contract):
  pos = 0
  for i,c in enumerate(contract):
    if c.isdigit() == True:
      pos = i
      break
  con = contract[:pos]
  date = contract[pos:]
  return con, date

def PlotSingle(file_list, ticker_filter=None):
  start = file_list[0].split('/')[-1].split('.')[0]
  end = file_list[-1].split('/')[-1].split('.')[0]
  cs, ds = SplitCon(start)
  cd, dd = SplitCon(end)
  ncol = 3
  nrow = 4
  count = 0
  if cs != cd:
    print('diff con %s %s' %(cs, cd))
    sys.exit(1)
  title = "ethusdt high-frequency data from %s-%s" %(ds, dd)
  all_mid = []
  fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(20,16))
  fig.tight_layout()#pad=0.1, w_pad=0.1, h_pad=0.1)
  for f in file_list:
    date = GetDate(f)
    print('count is %d'%(count))
    shot = MarketSnapshot()
    df = GetDF(f, aname, bname, tname, using_name='mid', ticker_filter=ticker_filter)
    if len(df) == 0:
      print('ignoring %s' %(f))
      continue
    if count % (ncol*nrow) == 0 and count > 0:
      fig.tight_layout()#pad=1.4, w_pad=1.5, h_pad=2.0)
      fig.savefig('singleday[%s]@%s' %('ni' if ticker_filter == None else ticker_filter, str(count)))
      fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
      fig.tight_layout()#pad=1.4, w_pad=1.5, h_pad=2.0)
    this_ax = ax[int(count/ncol)%nrow, count%ncol]
    this_ax.set_title('ethusdt' if ticker_filter==None else ticker_filter + " " +date)
    this_ax.set_ylabel('mid price')
    this_ax.grid()
    this_ax.plot(df['mid'].tolist())
    all_mid.extend(df['mid'].tolist())
    count += 1
  plt.show()
  plt.ylabel('mid price')
  plt.grid()
  plt.plot(all_mid)
  plt.title(title)
  plt.tight_layout()
  plt.savefig('all data for %s from %s to %s' %('ni' if ticker_filter == None else ticker_filter, start, end))
  plt.show()

def GetDate(file_name):
  return file_name.split('/')[-1].split('.')[0]

def PlotSingleWithTime(file_list, ticker_filter=None):
  start = file_list[0].split('/')[-1].split('.')[0]
  end = file_list[-1].split('/')[-1].split('.')[0]
  cs, ds = SplitCon(start)
  cd, dd = SplitCon(end)
  if cs != cd:
    print('diff con %s %s' %(cs, cd))
    sys.exit(1)
  title = "%s from %s-%s" %("ni"if ticker_filter==None else ticker_filter, ds, dd)
  all_mid = []
  all_time = []
  for f in file_list:
    df = GetDF(f, aname, bname, tname, using_name='mid', ticker_filter=ticker_filter)
    date = GetDate(f)
    if len(df) == 0:
      print('ignoring %s' %(f))
      continue
    if count % (ncol*nrow) == 0 and count > 0:
      fig.savefig('singleday[%s-%s]@%s' %(main, hedge, str(count)))
      fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
      fig.tight_layout()
    this_ax = ax[int(count/ncol)%nrow, count%ncol]
    df = df.sort_values(by='time').reset_index()
    this_ax.set_title("ni " + date if ticker_filter==None else ticker_filter + " " +date)
    this_ax.set_ylabel('price')
    this_ax.grid()
    this_ax.plot(df['time_sec'].tolist(), df['mid'].tolist())
    all_mid.extend(df['mid'].tolist())
    all_time.extend(df['time_sec'].tolist())
    count += 1
  print(all_time)
  plt.plot(all_time, all_mid)
  plt.title(title)
  plt.show()

def PlotSpread(main_path, hedge_path, multiplier=1):
  ask_name = aname
  bid_name = bname
  time_name = tname
  all_mid = []
  if len(main_path) != len(hedge_path):
    print('different file length! %d %d' %(len(main_path), len(hedge_path)))
    sys.exit(1)
  ncol = 3 
  nrow = 4
  fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
  fig.tight_layout()
  width = int(math.sqrt(len(main_path))) + 1
  height = int(math.sqrt(len(main_path))) +1
  fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
  fig.tight_layout()
  count = 0
  date = []
  main = ''
  hedge= ''
  for i in range(len(main_path)):
    df1 = GetDF(main_path[i], ask_name, bid_name, time_name)
    df2 = GetDF(hedge_path[i], ask_name, bid_name, time_name)
    if len(df1) == 0:
      print(main_path[i] + ' main not found')
      continue
    elif len(df2) == 0:
      print(hedge_path[i] + ' hedge not found')
      continue
    if count % (ncol*nrow) == 0 and count > 0:
      fig.savefig('singleday[%s-%s]@%s' %(main, hedge, str(count)))
      fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
      fig.tight_layout()
    this_ax = ax[int(count/ncol)%nrow, count%ncol]
    main = main_path[i].split('/')[-1].split('.')[0]
    hedge = hedge_path[i].split('/')[-1].split('.')[0]
    main_date = ''.join(main_path[i].split('/')[-4:-1]).strip('/')
    hedge_date = ''.join(hedge_path[i].split('/')[-4:-1]).strip('/')
    print('handling %s' %(main_date))
    if (main_date != hedge_date):
      print('date is not align for %s %s'%(main_date, hedge_date))
      sys.exit(1)
    date.append(main_date)
    df = Merge(df1, df2)
    df[main] = df[main]*multiplier
    Plot(df, main, hedge, main_date, this_ax, all_mid)
    count += 1
  if count > 0:
    fig.savefig('singleday[%s-%s]@%s' %(main, hedge, str(count)))
    plt.show()
    #print("main %s hegde %s date[0] %s date[-1] %s" %(main, hedge, date[0], date[-1]))
    plt.title('mid delta of [%s %s] from %s to %s' %(main, hedge, date[0], date[-1]))
    plt.plot(all_mid)
    plt.savefig('all_mid[%s-%s] from %s-%s' %(main, hedge, date[0], date[-1]))

def GetFuturePeriod(month, year=2019, sep = '-'):
  valid_day = []
  last_day = [i for i in range(16,32)]
  this_day = [i for i in range(1, 16)]
  if month == 1:
    last_year = year-1
    last_month = 12
  else:
    last_year = year
    last_month = month- 1
  last_month_str = '%02d' %(last_month)
  month_str = '%02d' %(month)
  valid_day.extend([str(last_year) + sep + last_month_str + sep + '%02d'%(ld) for ld in last_day])
  valid_day.extend([str(year) + sep + month_str + sep + '%02d'%(ld) for ld in this_day])
  return valid_day

'''
def main():
  month = ['01', '02', '03', '04']
  date = ['18' + str(i).zfill(2) for i in range(1, 13)]
  date.extend(['190'+str(i) for i in range(1,8)])
  contract_pair = [('IC', '510500'), ('IH', '510050'), ('IF','510300')]
  contract_pair = [('IC', 'IC'), ('IH', 'IH'), ('IF','IF')]
  pairs = [('510050', 'IH8888'), ('510500', 'IC8888'), ('510300', 'IF8888')]
  pairs = [(cp[1], cp[0]+'19'+str(m)) for cp in contract_pair for m in month]
  pairs = [(cp[0]+'19'+str(m), cp[1]+'19'+str(int(m)+2).zfill(2)) for cp in contract_pair for m in month]
  pairs = [("ni19"+m, "anything")for m in month]
  pairs = [("ni"+d, "anything")for d in date]
  #main_prefix = '/shared/xyang/Data/MarketData_from_dat/2019/'
  #hedge_prefix = '/shared/xyang/Data/future_ctp/2019/'
  #main_prefix = '/shared/xyang/Data/MarketData_from_dat/'
  #hedge_prefix = '/shared/xyang/Data/future_ctp/'
  main_prefix = '/running/'
  hedge_prefix = '/running/'
  all_list = []
  for p in pairs:
    #period = GetFuturePeriod(int(p[0][-1:]))
    period = GetFuturePeriod(month=int(p[0][-2:]), year=2000+int(p[0][-4:-2]))
    main_list = [main_prefix+d+'/' + p[0] + '.csv' for d in period]
    hedge_list = [hedge_prefix+d+'/' + p[1] + '.csv' for d in period]
    #PlotSpread(main_list, hedge_list, 1000)
    #print(main_list)
    all_list.extend(main_list)
  PlotSingleWithTime(all_list)
'''
# file example crypto2019-08-09.log.gz
def main():
  year = ['2019']
  month = ['0'+str(i) for i in range(1,8)]
  day = [str(i).zfill(2) for i in range(1, 32)]
  date = [y+'-'+m+'-'+d for y in year for m in month for d in day]
  #file_list = ['/root/crypto_cache/crypto'+d+'.log.gz' for d in date]
  file_list = ['/running/'+d+'/zn8888.csv' for d in date]
  PlotSingle(file_list)#, ticker_filter="ETHUSDT")

if __name__ =='__main__':
  main()
