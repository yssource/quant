import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from market_snapshot import *
from Trader import *
from Dater import *

tr = Trader()
shot = MarketSnapshot()

def LoadData(start_date, end_date, ticker):
  dl = dateRange(start_date, end_date)
  df=
  for d in dl:
    df = ReadData(d, ticker)

def ReadData(date, ticker):
  path = '/root/'+date+'/'+ticker+'.csv'
  df = pd.read_csv(path, header=None)
  df.columns = shot.get_columns()
  return df

def factor(df):
  df['mid'] = (df['asks[0]'] + df['bids[0]']) / 2
  short_period = 10
  long_period = 20
  dea_period = 12
  ema_long = df['mid'].ewm(span=long_period, adjust=False).mean()
  ema_short = df['mid'].ewm(span=short_period, adjust=False).mean()
  diff = ema_long - ema_short
  dea = diff.ewm(span=dea_period, adjust=False).mean()
  bar = 2*(diff - dea)
  return bar

def test_pnl(df):
  up = df['f1'].quantile(0.99)
  down = df['f1'].quantile(0.01)
  df['money'] = np.where(df['f1'] > up, df['mid'], 0.0)
  df['money'] = np.where(df['f1'] < down, -df['mid'], df['money'])
  for i in df['money'].tolist():
    if abs(i) > 1:
      tr.RegisterOneTrade('ni8888', 1 if i > 0 else -1, abs(i))
  #plt.plot(df['money'])
  #plt.show()
  tr.Summary()
  tr.PNL()
  tr.PlotStratRawPnl(show=True)

def plot(df):
  plt.plot(df['mid'], label='mid', alpha=0.3)
  buy_x = df[df['money'] < 0].index.tolist()
  buy = df[df['money']<-0.1]
  plt.scatter(x=buy.index.tolist(), y=buy['mid'].tolist(), marker='.', s=[4]*len(buy), c='red', label='buy')
  sell = df[df['money']>0.1]
  plt.scatter(x=sell.index.tolist(), y=sell['mid'].tolist(), marker='.', s=[4]*len(sell), c='green', label='sell')
  plt.legend()
  plt.grid()
  plt.show()

if __name__=='__main__':
  df = ReadData('2020-02-28', 'ni8888')
  df['f1'] = factor(df)
  test_pnl(df)
  plot(df)
  #df[['mid', 'f1', 'money']].to_csv('df.csv')
