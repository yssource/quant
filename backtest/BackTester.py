from caler import *
from Trader import *
from Reader import *
from order import *

class BackTestor:
  def __init__(self, order_path):
    self.r = Reader()
    self.t = Trader()
    self.LoadOrder(order_path)

  def LoadOrder(self, order_path):
    self.r.load_order_file(order_path)
    for i in range(self.r.get_ordersize()):
      o = self.r.read_border(i)
      if o.price > 0:
        self.t.RegisterOneTrade(o.contract, o.size if o.side == 1 else -o.size, o.price)

  def Plot(self):
    self.t.PlotStratPnl()

if __name__ == '__main__':
  btr = BackTestor("/today/order_backtest.dat")
  btr.Plot()
