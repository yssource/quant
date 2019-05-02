import struct
import sys
import time
from common.market_snapshot import *

f = open('data_binary.dat')

fmt = "!32s25589s"
fmt = "32s5d5d5i5id2i2d1?2Q?7s"
size = struct.calcsize(fmt)
start = 0
count =0
l = f.read()
length = len(l)
start_sec=time.time()
while start < length:
  p = l[start:start+size]
  shot = MarketSnapshot()
  _, time_sec, time_usec='',0,0
  shot.ticker, shot.bids[0], shot.bids[1], shot.bids[2], shot.bids[3], shot.bids[4], shot.asks[0], shot.asks[1], shot.asks[2], shot.asks[3], shot.asks[4], shot.bid_sizes[0], shot.bid_sizes[1], shot.bid_sizes[2], shot.bid_sizes[3], shot.bid_sizes[4], shot.ask_sizes[0], shot.ask_sizes[1], shot.ask_sizes[2], shot.ask_sizes[3], shot.ask_sizes[4], shot.last_trade, shot.last_trade_size, shot.volume, shot.turnover, shot.open_interest, _, time_sec, time_usec, shot.is_initialized, res = struct.unpack(fmt, p)
  shot.time = int(time_sec) + float("0."+str(time_usec))
  struct.unpack(fmt, p)
  start += size
  count += 1
print(time.time()-start_sec)
