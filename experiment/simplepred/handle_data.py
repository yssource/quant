import numpy as np
import pandas as pd
from market_snapshot import *

read_file = "/root/quant/data/Ali/2019-01-31/data.log"
out_file = "data.csv"
rf = open(read_file)
of = open(out_file, 'w')

for line in rf:
  shot=MarketSnapshot(depth=1)
  if shot.construct(line) == True:
    #print shot.to_csv()
    of.write("%s\n" % shot.to_csv())

rf.close()
of.close()
