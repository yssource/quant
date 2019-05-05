from Reader import *

r =Reader()
r.load_strat_file("/running/2019-04-30/data_binary.dat")
size = r.get_stratsize()
for i in range(size):
  r.read_bstrat(i).Show()
