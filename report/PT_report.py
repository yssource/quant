from EmailWorker import *
from Reader import *
import math
import matplotlib.pyplot as plt

def LoadShot(r, mid_map, mid_time_map):
  r.load_shot_file("/root/mid.dat")
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

def SaveSpreadPng(mid_map, mid_time_map, png_path):
  tickers = mid_time_map.keys()
  ksize = len(tickers)
  ncol, nrow = 3, 3
  width = int(math.sqrt(ksize)) + 1 
  height = int(math.sqrt(ksize)) +1
  fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(10,6))
  count = 0
  for t in tickers:
    if count % (ncol*nrow) == 0 and count > 0:
      fig.tight_layout()
      fig.savefig('spread_move@%d' %(t, str(count)))
      fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(15,8))
    this_ax = ax[int(count/ncol)%nrow, count%ncol]
    items = mid_time_map[t].items()
    items = sorted(items, key=lambda x:x[0])
    #plt.plot([i[0] for i in items], [i[1] for i in items])
    this_ax.plot(mid_map[t])
    this_ax.set_title('%s\'s spread move' % (t))
    this_ax.grid()
    count += 1
  plt.tight_layout()
  plt.savefig(png_path)


if __name__ == '__main__':
  mid_map = {}
  mid_time_map = {}
  EM = EmailWorker()
  r = Reader()
  LoadShot(r, mid_map, mid_time_map)
  png_path = '/today/spread_move.png'
  SaveSpreadPng(mid_map, mid_time_map, png_path)
  EM.SendHtml(content = render_template('PT_report.html'), png_list=[png_path])
