from caler import *
import pandas as pd
from Plotor import *
from Reader import *

no_today = {'IF', 'IH', 'IC'}

def GetCon(ticker):
  for i, c in enumerate(ticker):
    if c.isdigit():
      return ticker[:i]

class Trader:
  def __init__(self, enable_fee = False, fee_rate=0.0, record=False):
    self.caler = CALER('/root/hft/config/contract/contract.config')
    self.pt = Plotor()
    self.pos = {}
    self.avgcost = {}
    self.pnl = {}
    self.fee = {}
    self.trade_count = {}
    self.fee_rate = fee_rate
    self.record = record
    self.pnl_hist = {}
    if record == True:
      self.f = open('traders_record.txt', 'w')

  def __def__(self):
    if self.record:
      self.f.close()

  def RegisterOneTrade(self, ticker, size, price):
    assert price > 0
    assert isinstance(size, int)
    assert isinstance(ticker, str)
    if ticker not in self.pos:
      self.pos[ticker] = size
      self.avgcost[ticker] = price
      self.pnl[ticker] = 0.0
      self.trade_count[ticker] = 1.0
      self.fee[ticker] = 0.0
      self.pnl_hist[ticker] = []
      return
    if self.pos[ticker] * size < 0:  # close position
      if abs(size) > self.pos[ticker]:  # over close
        c = self.caler.CalFee(ticker, self.avgcost[ticker], abs(self.pos[ticker]), price, abs(self.pos[ticker]), GetCon(ticker) in no_today)
        self.fee[ticker] += c.open_fee + c.close_fee
        self.pnl[ticker] += self.caler.CalNetPnl(ticker, self.avgcost[ticker], abs(self.pos[ticker]), price, abs(self.pos[ticker]), OrderSide.Buy if size > 0 else OrderSide.Sell, GetCon(ticker) in no_today)
        self.avgcost[ticker] = price
      else: # normal close
        c = self.caler.CalFee(ticker, self.avgcost[ticker], abs(size), price, abs(size), GetCon(ticker) in no_today)
        self.fee[ticker] += c.open_fee + c.close_fee
        self.pnl[ticker] += self.caler.CalNetPnl(ticker, self.avgcost[ticker], abs(size), price, abs(size), OrderSide.Buy if size > 0 else OrderSide.Sell, GetCon(ticker) in no_today)
      self.pnl_hist[ticker].append(self.pnl[ticker])
    else:  # open position
      self.avgcost[ticker] += (price-self.avgcost[ticker])*size/(self.pos[ticker]+size)
    self.pos[ticker] += size
    if self.pos[ticker] == 0:
      self.avgcost[ticker] = 0.0
    self.trade_count[ticker] += 1
    trade_record = "Trade %s %d@%f" %(ticker, size, price)
    if self.record:
      self.f.write(trade_record+'\n')

  def PlotStratPnl(self):
    self.strat_pnl_hist = {}
    for t in self.pnl_hist:
      con = GetCon(t)
      if con not in self.strat_pnl_hist:
        self.strat_pnl_hist[con] = self.pnl_hist[t]
        continue
      for i, c in enumerate(self.strat_pnl_hist[con]):
        self.strat_pnl_hist[con][i] += self.pnl_hist[t][i]
    print(self.strat_pnl_hist)
    self.pt.PlotMultiMap(self.strat_pnl_hist, 'strat_pnl_hist')

  def Summary(self):
    print('================================================================================================================')
    sort_key = sorted(self.pos.keys())
    for t in sort_key:
      #print('for %s trade_count=%d, pnl=%.2f, left_pos=%.2f, avgcost=%.2f, for feerate %f, rough_fee is %.2f' %(t, self.trade_count[t], self.pnl[t], self.pos[t], self.avgcost[t], self.fee_rate, abs(self.fee_rate*self.trade_count[t]*self.avgcost[t])))
      print('for %s trade_count=%d, pnl=%.2f, left_pos=%.2f, avgcost=%.2f, rough_fee is %.2f' %(t, self.trade_count[t], self.pnl[t], self.pos[t], self.avgcost[t], self.fee[t]))
    print('===============================================================================================================')

  def GenDFReport(self):
    r = []
    sort_key = sorted(self.pos.keys())
    for t in sort_key:
      #print('for %s trade_count=%d, pnl=%.2f, left_pos=%.2f, avgcost=%.2f, rough_fee is %.2f' %(t, self.trade_count[t], self.pnl[t], self.pos[t], self.avgcost[t], self.fee[t]))
      r.append([t, self.trade_count[t], round(self.pnl[t],1), self.pos[t], self.avgcost[t], round(self.fee[t],1)])
    df = pd.DataFrame(r, columns = ['ticker', 'trade_count', 'net_pnl', 'left_position', 'avgcost', 'fee'])
    df = df.set_index('ticker')
    return df

  def GenStratReport(self, df=''):
    if len(df) == 0:
      df = self.GenDFReport()
    ticker_strat = {}
    for k in df.index:
      ticker_strat[k] = GetCon(k)
    m = df.T.to_dict()
    self.strat_pnl = {}
    for k in m:
      con = GetCon(k)
      if con not in self.strat_pnl:
        self.strat_pnl[con] = m[k]
        continue
      self.strat_pnl[con]['net_pnl'] += m[k]['net_pnl']
      self.strat_pnl[con]['trade_count'] = max(m[k]['trade_count'], self.strat_pnl[con]['trade_count'])
      self.strat_pnl[con]['left_position'] = max(m[k]['left_position'], self.strat_pnl[con]['left_position'])
      self.strat_pnl[con]['avgcost'] -= m[k]['avgcost']
      self.strat_pnl[con]['avgcost'] = -self.strat_pnl[con]['avgcost']
      self.strat_pnl[con]['fee'] += m[k]['fee']
    for k in self.strat_pnl:
      for c in self.strat_pnl[k].keys():
        if isinstance(self.strat_pnl[k][c], float):
          self.strat_pnl[k][c] = round(self.strat_pnl[k][c], 1)
    rdf = pd.DataFrame(self.strat_pnl).T
    return rdf[['trade_count', 'net_pnl', 'left_position', 'avgcost', 'fee']]

if __name__=='__main__':
  t = Trader()
  r = Reader()
  r.load_order_file('/today/order_backtest.dat')
  s = r.get_ordersize()
  for i in range(s):
    o = r.read_border(i)
    if o.price > 0:
      t.RegisterOneTrade(o.contract, o.size if o.side == 1 else -o.size, o.price)
  t.Summary()
  t.PlotStratPnl()
