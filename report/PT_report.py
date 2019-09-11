from EmailWorker import *
from Reader import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
  mid_map = {}
  mid_time_map = {}
  EM = EmailWorker()
  r = Reader()
  r.load_shot_file("/today/mid.dat")
  for i in range(r.get_shotsize()):
    shot = r.read_bshot(i)
    ticker = shot.ticker
    mid = shot.last_trade
    time = shot.time
    if ticker not in mid_map:
      mid_map[ticker] = [mid]
      mid_time_map[ticker] = {time:mid}
      continue
    mid_map[ticker].append(mid)
    mid_time_map[ticker][time] = mid
  items = mid_time_map.items()
  plt.plot([i[0] for i in items], [i[1] for i in items])
  plt.show()
