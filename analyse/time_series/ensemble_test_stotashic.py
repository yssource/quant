import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
import test_stationarity as ts
import time
import sys
import math
import os
import self_input as si
import get_datelist as gd

date_list = gd.get()
mode_list = ['', '_night']


for i in range(len(date_list)):
  for j in range(len(mode_list)):
    date = date_list[i]
    mode = mode_list[j]
    file_path = '/root/quant/data/Mid/'
    file_name = file_path+'ni1905ni1903_' + date +mode+'_mid.npy'
    if os.path.exists(file_name) == False:
      continue
    m = np.load(file_name)
    ts.draw_acf_pacf(m)
    print 'for ', date+mode
    print acorr_ljungbox(m, lags=5)[1]
