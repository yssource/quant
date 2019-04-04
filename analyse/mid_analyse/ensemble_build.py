import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *
import build_align_map as bam
import sys
import numpy as np
import pandas as pd
import os
import get_datelist as gd

date_list = gd.get()
mode_list = ['', '_night']

for dl in date_list:
  for ml in mode_list:
    file_name = '/root/quant/data/Ali/'+dl+'/data' + ml + '.log'
    if os.path.exists(file_name) == False or os.path.getsize(file_name) < 1000000:
      continue
    print 'handling ' + file_name
    bam.build(file_name)

print 'running time is ', time.time()-start_sec
