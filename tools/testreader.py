from Reader import *

r =Reader()
r.load_shot_file("/running/2019-09-05/data_binary.dat")
size = r.get_shotsize()
for i in range(size):
  r.read_bshot(i).Show()
