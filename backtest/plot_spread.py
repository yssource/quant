import matplotlib.pyplot as plt
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

def GetDF(file_path, ask_name, bid_name, time_name, tz_diff=False):
  contract = file_path.split('/')[-1].split('.')[0]
  if not os.path.exists(file_path):
    return pd.DataFrame([])
  df = pd.read_csv(file_path)
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
  df[contract] = (df[ask_name] + df[bid_name]) / 2
  df['time'] = [HandleTime(df[time_name][i], tz_diff) for i in range(len(df))]
  df = df[df['time'] <= 15*3600]
  df = df[df['time'] >= 9*3600]
  df = df.reset_index()
  columns = [time_name, 'time', contract]
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

def PlotSpread(main_path, hedge_path, multiplier=1):
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
    df1 = GetDF(main_path[i], 'AskPrice1', 'BidPrice1', 'TimeStamp')
    df2 = GetDF(hedge_path[i], 'AskPrice1', 'BidPrice1', 'MicroTime')
    if len(df1) == 0:
      print(main_path[i] + ' not found')
      continue
    elif len(df2) == 0:
      print(hedge_path[i] + ' not found')
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
  fig.savefig('singleday[%s-%s]@%s' %(main, hedge, str(count)))
  plt.show()
  plt.title('mid delta of [%s %s] from %s to %s' %(main, hedge, date[0], date[-1]))
  plt.plot(all_mid)
  plt.savefig('all_mid[%s-%s] from %s-%s' %(main, hedge, date[0], date[-1]))

def GetFuturePeriod(month, year=2019):
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
  valid_day.extend([str(last_year) + '/' + last_month_str + '/' + '%02d'%(ld) for ld in last_day])
  valid_day.extend([str(year) + '/' + month_str + '/' + '%02d'%(ld) for ld in this_day])
  return valid_day

def main():
  month = ['01', '02', '03']
  contract_pair = [('IC', '510500'), ('IH', '510050'), ('IF','510300')]
  pairs = [('510050', 'IH1903'), ('510500', 'IC1903'), ('510300', 'IF1903')]
  pairs = [(cp[1], cp[0]+'19'+str(m)) for cp in contract_pair for m in month]
  main_prefix = '/shared/xyang/Data/MarketData_from_dat/2019/'
  hedge_prefix = '/shared/xyang/Data/future_ctp/2019/'
  main_prefix = '/shared/xyang/Data/MarketData_from_dat/'
  hedge_prefix = '/shared/xyang/Data/future_ctp/'
  for p in pairs:
    period = GetFuturePeriod(int(p[1][-1:]))
    main_list = [main_prefix+d+'/' + p[0] + '.csv' for d in period]
    hedge_list = [hedge_prefix+d+'/' + p[1] + '.csv' for d in period]
    PlotSpread(main_list, hedge_list, 1000)

if __name__ =='__main__':
  main()
