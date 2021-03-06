import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import math

class Plotor:
  def __init__(self, one_width=5, area=80):
    self.one_width = one_width
    self.graph_area = area

  def PlotList(self, l, ax, label):
    ax.plot(l, label=label)

  def PlotTimeMap(self, pmap, ax, label):
    items = pmap.items()
    items = sorted(items, key=lambda x:x[0])
    ax.plot([i[0] for i in items], [i[1] for i in items], label=label)

  def PlotMultiMap(self, mmap, label, path = '', show=False):
    tickers = mmap.keys()
    ksize = len(tickers)
    ncol, nrow = max(1, int(math.sqrt(ksize))), int(math.sqrt(ksize))+1
    fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(self.one_width*ncol,int(self.graph_area/(ncol*self.one_width))))
    count = 0
    for t in tickers:
      if count % (ncol*nrow) == 0 and count > 0:
        fig.tight_layout()
        fig.savefig('%s%s@%d' %(path, label, count))
        fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(self.one_width*ncol,int(self.graph_area/(ncol*self.one_width))))
      if ncol == 1:
        this_ax = ax[int(count/ncol)%nrow]
      else:
        this_ax = ax[int(count/ncol)%nrow, count%ncol]
      if isinstance(mmap[t], list):
        self.PlotList([0.0]+mmap[t], this_ax, t)
      elif isinstance(mmap[t], map):
        start = min(mmap[t].keys())- 100
        mmap[t][start] = 0.0
        self.PlotTimeMap(mmap[t], this_ax, t)
      else:
        print('unsupport type %s' %(type(mmap[t])))
        sys.exit(1)
      this_ax.set_title('%s' % (t))
      this_ax.grid()
      this_ax.legend()
      count += 1
    plt.tight_layout()
    if show == True:
      plt.show()
    else:
      plt.savefig('%s%s@%d' %(path, label, count))

if __name__ == '__main__':
  pt = Plotor()
  m = {"a":[i**2 for i in range(100)], "b":[i**3 for i in range(100)]}
  tm = {"a":{i:i**2 for i in range(100)}, "b":{i:i**3 for i in range(100)}}
  m = {'IH': [398.26281569824187, 676.8502469238279], 'IC': [543.9928998046876, 1008.4046122070322, 1472.891766406251, 1937.4634248046896], 'ni': [86.0, 142.0], 'IF': [430.87182810058596, 742.1164718994141]}
  pt.PlotMultiMap(m, 'test', 'pnl')
