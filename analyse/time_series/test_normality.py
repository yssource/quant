import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
import time
import sys
import math
import self_input as si

date,mode = si.init()

file_path = '/root/quant/data/Mid/'
m = np.load(file_path+'ni1905ni1903_' + date +mode+'_mid.npy')
test_ratio = 0.1
train_size = int(len(m)*(1-test_ratio))
train_m = m[0:train_size]
test_m = m[train_size:]

#normalize m
'''
train_m_mean = train_m.mean()
train_m_std = train_m.std()
test_m_mean = test_m.mean()

train_m = (train_m - train_m_mean)/train_m.std()
test_m = (test_m - train_m_mean)/train_m_std
#plt.hist(train_m, bins=128)
#plt.show()
'''

#check normality
'''
sm.qqplot(train_m, line='45')
save_path = '/root/quant/data/normality/' + date +mode+'.png'
plt.savefig(save_path)
plt.show()
'''

from scipy.stats import kstest
print kstest(train_m, 'norm')
