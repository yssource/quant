import struct
import matplotlib.pyplot as plt
from Reader import *
import sys
sys.path.append('/root/hft/external/common/lib/cpp_py')
from caler import *
from common.order import *
from common.market_snapshot import *
import math

contract_config_path = "/root/hft/config/backtest/contract.config"

class BackTester:
  def __init__(self):
    self.reader = Reader()
    self.order_file_size = 0
    self.shot_file_size = 0
    self.pos= {}
    self.net_pnl = {}
    self.gross_pnl = {}
    self.ticker_strat_map = {}
    self.avgcost = {}
    self.gross_time_allpnl_map = {}
    self.net_time_allpnl_map = {}
    self.strat_data_map = {}
    self.gross_strat_pnl_map = {}
    self.net_strat_pnl_map = {}
    self.pnl_contract = set([])
    self.Caler = CALER(contract_config_path)

  def GetStratPair(self, s):
    exec('temp=' + s)
    return temp

  def GetStratPnlKey(self):
    return self.net_strat_pnl_map.keys()

  def load_binary_order(self, file_path):
    self.reader.load_order_file(file_path)
    self.order_file_size = self.reader.get_ordersize()

  def load_binary_shot(self, file_path):
    self.reader.load_shot_file(file_path)
    self.shot_file_size = self.reader.get_shotsize()

  def load_binary_strat(self, file_path):
    self.reader.load_strat_file(file_path)
    self.strat_file_size = self.reader.get_stratsize()
    for i in range(self.strat_file_size):
      strat = self.reader.read_bstrat(i)
      self.pnl_contract.add(self.GetStratPair(strat.ticker)[-1])
      for c in self.GetStratPair(strat.ticker):
        self.ticker_strat_map[c] = strat.ticker
      if not self.strat_data_map.has_key(strat.ticker):
        self.strat_data_map[strat.ticker] = {}
      self.strat_data_map[strat.ticker][strat.time] = strat.last_trade

  def load_csv_data(self, file_path):
    pass

  def clear(self):
    self.reader = Reader()
    self.order_file_size = 0
    self.shot_file_size = 0
    self.pos= {}
    self.net_pnl = {}
    self.gross_pnl = {}
    self.ticker_strat_map = {}
    self.avgcost = {}
    self.gross_time_allpnl_map = {}
    self.net_time_allpnl_map = {}
    self.strat_data_map = {}
    self.gross_strat_pnl_map = {}
    self.net_strat_pnl_map = {}
    self.pnl_contract = set([])
    self.Caler = CALER(contract_config_path)

  def RunShot(self):
    for i in range(self.shot_file_size):
      shot = self.reader.read_bshot(i)

  '''
  def RunStrat(self):
    for i in range(self.strat_file_size):
      strat = self.reader.read_bstrat(i)
      for c in GetStratPair(strat.contract):
        self.ticker_strat_map[c] = strat.contract
      self.strat_map[strat.contract] = strat.last_trade
  '''

  def RunOrder(self):
    for i in range(self.order_file_size):
      o = self.reader.read_border(i)
      if o.action == 4:
        o.Show()
        continue
      true_size = (o.size if o.side == 1 else -o.size)
      if not self.pos.has_key(o.contract):
        self.pos[o.contract] = 0 
        self.avgcost[o.contract] = 0.0 
        self.net_pnl[o.contract] = 0 
        self.gross_pnl[o.contract] = 0 
      pre_pos = self.pos[o.contract]
      self.pos[o.contract] += true_size
      is_close = (self.pos[o.contract]*true_size <= 0)
      if is_close == True:
        this_net_pnl = self.Caler.CalNetPnl(o.contract, self.avgcost[o.contract], abs(pre_pos), o.price, o.size, OrderSide.Buy if o.side==1 else OrderSide.Sell)
        this_gross_pnl = self.Caler.CalPnl(o.contract, self.avgcost[o.contract], abs(pre_pos), o.price, o.size, OrderSide.Buy if o.side==1 else OrderSide.Sell)
        #print("%s %f %i %f %i %i " %(o.contract, self.avgcost[o.contract], abs(pre_pos), o.price, o.size, o.side))
        self.net_pnl[o.contract] += this_net_pnl
        self.gross_pnl[o.contract] += this_gross_pnl
        if self.pos[o.contract] == 0:
            self.avgcost[o.contract] = 0.0 
        if o.contract in self.pnl_contract:  # close contract
          #self.time_allpnl_map[o.shot_time] = (np.sum(self.pnl.values()), o.contract)
          strat_id = self.ticker_strat_map[o.contract]
          strat_pair = self.GetStratPair(strat_id)
          if not self.net_strat_pnl_map.has_key(strat_id):
            self.net_strat_pnl_map[strat_id] = {}
          self.net_strat_pnl_map[strat_id][o.shot_time] = np.sum([self.net_pnl[sp] for sp in strat_pair])
          if not self.gross_strat_pnl_map.has_key(strat_id):
            self.gross_strat_pnl_map[strat_id] = {}
          self.gross_strat_pnl_map[strat_id][o.shot_time] = np.sum([self.gross_pnl[sp] for sp in strat_pair])
      else:
        self.avgcost[o.contract] = abs((self.avgcost[o.contract] * (self.pos[o.contract] - true_size) + o.price * true_size) / self.pos[o.contract])

  def Plot(self):
    keys = self.GetStratPnlKey()
    ksize = len(keys)
    ncol, nrow = 2, 3
    width = int(math.sqrt(ksize)) + 1 
    height = int(math.sqrt(ksize)) +1
    fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
    #fig.tight_layout()
    count = 0
    for i in range(ksize):
      key = keys[i]
      if count % (ncol*nrow) == 0 and count > 0:
        fig.tight_layout()
        fig.savefig('pnl@i' %(count))
        plt.show()
        fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
        #fig.tight_layout()
      this_ax = ax[int(count/ncol)%nrow, count%ncol]
      this_ax.set_title(key)
      data_keys = sorted(self.strat_data_map[key].keys())
      self.net_strat_pnl_map[key][np.min(data_keys)-10] = 0.0
      self.gross_strat_pnl_map[key][np.min(data_keys)-10] = 0.0
      net_pnl_keys = sorted(self.net_strat_pnl_map[key].keys())
      gross_pnl_keys = sorted(self.gross_strat_pnl_map[key].keys())
      print(net_pnl_keys)
      this_ax.plot(net_pnl_keys, [self.net_strat_pnl_map[key][k] for k in net_pnl_keys], label='net_pnl', color='red')
      this_ax.plot(gross_pnl_keys, [self.gross_strat_pnl_map[key][k] for k in gross_pnl_keys], label='gross_pnl', color='black')
      twin_ax = this_ax.twinx()
      twin_ax.plot(data_keys, [self.strat_data_map[key][k] for k in data_keys], label='strat_data', color='blue', alpha=0.3)
      this_ax.legend()
      twin_ax.legend()
      count += 1
    fig.tight_layout()
    fig.savefig('pnl@%i' %(count))
    plt.show()
      
  def Report(self):
    pass

  def Run(self):
    if self.order_file_size != 0:
      self.RunOrder()
    if self.shot_file_size != 0:
      self.RunShot()

def main():
  bt = BackTester()
  bt.load_binary_order("/root/hft/build/bin/order.dat")
  #bt.load_binary_shot("/running/quant/data/Ali/2019-03-07/data_binary.dat")
  bt.load_binary_strat('/root/hft/build/bin/mid.dat')
  bt.Run()
  bt.Plot()

if __name__ == '__main__':
  main()
