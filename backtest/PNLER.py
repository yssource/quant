import struct
import matplotlib.pyplot as plt
from Reader import *
#from caler import *
from common.order import *
from common.market_snapshot import *

class BackTester:
  def __init__(self):
    self.reader = Reader()
    self.order_file_size = 0
    self.shot_file_size = 0
    self.pos= {}
    self.pnl = {}
    self.avgcost = {}
    self.realtime_pnl = {}

  def load_binary_order(self, file_path):
    self.reader.load_order_file(file_path)
    self.order_file_size = self.reader.get_ordersize()

  def load_csv_data(self, file_path):
    pass

  def clear(self):
    self.reader = Reader()
    self.order_file_size = 0
    self.shot_file_size = 0
    self.pos = {}
    self.pnl = {}
    self.avgcost = {}
    self.realtime_pnl = {}

  def RunOrder(self):
    for i in range(self.order_file_size):
      o = self.reader.read_border(i).Filter()
      #o.Show()
      true_size = (o.size if o.side == 1 else -o.size)
      if not self.pos.has_key(o.contract):
        self.pos[o.contract] = 0 
        self.avgcost[o.contract] = 0.0 
        self.pnl[o.contract] = 0 
      self.pos[o.contract] += true_size
      is_close = (self.pos[o.contract]*true_size <= 0)
      if is_close == True:
        this_pnl = true_size * (self.avgcost[o.contract] - o.price)# * contract_size[con]
        self.pnl[o.contract] += this_pnl
        if self.pos[o.contract] == 0:
            self.avgcost[o.contract] = 0.0 
        #if contract in hedge:
        self.realtime_pnl[o.shot_time] = (np.sum(self.pnl.values()), o.contract)
      else:
        self.avgcost[o.contract] = abs((self.avgcost[o.contract] * (self.pos[o.contract] - true_size) + o.price * true_size) / self.pos[o.contract])

  def Plot(self):
    realtime_list = sorted(self.realtime_pnl.items(), key=lambda x: x[0])
    #plt.plot([ r[0] for r in realtime_list ], [ r[1][0] for r in realtime_list ], label=cfg_str)
    plt.plot([r[1][0] for r in realtime_list], label="")
    plt.legend(loc='upper left')
    plt.title('pnl curve')
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
  bt.Run()
  bt.Plot()

if __name__ == '__main__':
  main()
