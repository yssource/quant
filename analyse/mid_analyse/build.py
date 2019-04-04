import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import build_align_map as bam
import sys
import numpy as np
import pandas as pd
import os
import self_input as si
import get_main as gm

tick_list = gm.get_tick()
ticker_list = gm.get_ticker()

date,mode = si.init()
print date
print mode
file_name = '/root/quant/data/Ali/'+date+'/data' + mode + '.log'
if os.path.exists(file_name) == False:
  print file_name + ' not exsit'
  sys.exit(1)
else:
  print file_name

bam.build(file_name)
