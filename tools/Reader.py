from common.order import *
from common.market_snapshot import *
import struct

class Reader:
  def __init__(self):
    self.shot_fmt =  "32s5d5d5i5id2i2d1?2Q?7s"
    self.strat_fmt = "32s5d5d5i5id2i2d1?2Q?7s"
    self.order_fmt = "4Q32sd3i32s3i128s"
    self.shot_size = struct.calcsize(self.shot_fmt)
    self.order_size = struct.calcsize(self.order_fmt)
    self.strat_size = struct.calcsize(self.strat_fmt)

  def get_ordersize(self):
    return self.order_struct_size

  def get_shotsize(self):
    return self.shot_struct_size

  def get_stratsize(self):
    return self.strat_struct_size

  def load_order_file(self, file_path):
    self.order_content = open(file_path).read()
    if len(self.order_content) % self.order_size != 0:
      print("%s filesize not order's times" %(file_path))
      #sys.exit(1)
    self.order_struct_size = int(len(self.order_content) / self.order_size)

  def load_shot_file(self, file_path):
    self.shot_content = open(file_path).read()
    if len(self.shot_content) % self.shot_size != 0:
      print("%s filesize not shot's times" %(file_path))
      #sys.exit(1)
    self.shot_struct_size = int(len(self.shot_content) / self.shot_size)

  def load_strat_file(self, file_path):
    self.strat_content = open(file_path).read()
    if len(self.strat_content) % self.strat_size != 0:
      print("%s filesize not strat shot's times" %(file_path))
      #sys.exit(1)
    self.strat_struct_size = int(len(self.strat_content) / self.strat_size)

  def read_bshot(self, i):
    if i >= self.shot_struct_size:
      print("oversize for shot %i > %i" %(i, self.shot_struct_size))
      return MarketSnapshot()
    content = self.shot_content[i*self.shot_size:(i+1)*self.shot_size]
    #print(len(struct.unpack(self.shot_fmt, content)))
    shot = MarketSnapshot()
    _, time_sec, time_usec='',0,0
    shot.ticker, shot.bids[0], shot.bids[1], shot.bids[2], shot.bids[3], shot.bids[4], shot.asks[0], shot.asks[1], shot.asks[2], shot.asks[3], shot.asks[4], shot.bid_sizes[0], shot.bid_sizes[1], shot.bid_sizes[2], shot.bid_sizes[3], shot.bid_sizes[4], shot.ask_sizes[0], shot.ask_sizes[1], shot.ask_sizes[2], shot.ask_sizes[3], shot.ask_sizes[4], shot.last_trade, shot.last_trade_size, shot.volume, shot.turnover, shot.open_interest, _, time_sec, time_usec, shot.is_initialized, res = struct.unpack(self.shot_fmt, content)
    shot.time = int(time_sec) + float("0."+str(time_usec))
    return shot.Filter()

  def read_bstrat(self, i):
    if i >= self.strat_struct_size:
      print("oversize for strat %i > %i" %(i, self.strat_struct_size))
      return MarketSnapshot()
    content = self.strat_content[i*self.strat_size:(i+1)*self.strat_size]
    # print(len(struct.unpack(self.strat_fmt, content)))
    strat = MarketSnapshot()
    _, time_sec, time_usec='',0,0
    strat.ticker, strat.bids[0], strat.bids[1], strat.bids[2], strat.bids[3], strat.bids[4], strat.asks[0], strat.asks[1], strat.asks[2], strat.asks[3], strat.asks[4], strat.bid_sizes[0], strat.bid_sizes[1], strat.bid_sizes[2], strat.bid_sizes[3], strat.bid_sizes[4], strat.ask_sizes[0], strat.ask_sizes[1], strat.ask_sizes[2], strat.ask_sizes[3], strat.ask_sizes[4], strat.last_trade, strat.last_trade_size, strat.volume, strat.turnover, strat.open_interest, _, time_sec, time_usec, strat.is_initialized, res = struct.unpack(self.strat_fmt, content)
    strat.time = int(time_sec) + float("0."+str(time_usec))
    return strat.Filter()

  def read_border(self, i):
    if i >= self.order_struct_size:
      print("oversize for order %i > %i" %(i, self.order_struct_size))
      return Order()
    content = self.order_content[i*self.order_size:(i+1)*self.order_size]
    order = Order()
    #print(struct.unpack(self.order_fmt, content))
    shot_sec, shot_usec, send_sec, send_usec = 0,0,0,0
    shot_sec, shot_usec, send_sec, send_usec, order.contract, order.price,order.size, order.traded_size, order.side, order.order_ref, order.action, order.status, order.offset, order.tbd = struct.unpack(self.order_fmt, content)
    order.shot_time = int(shot_sec) + float("0."+str(shot_usec))
    order.send_time = int(send_sec) + float("0."+str(send_usec))
    return order.Filter()
