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
import os
from scipy.stats import kstest

date_list = ["2018-12-"+str(i) for i in range(11,22)]
mode_list = ['', '_night']

fig, ax = plt.subplots(int(len(date_list)/2)+1, 4)


for i in range(len(date_list)):
  for j in range(len(mode_list)):
    date = date_list[i]
    mode = mode_list[j]
    file_path = '/root/quant/data/Mid/'
    file_name = file_path+'ni1905ni1903_' + date +mode+'_mid.npy'
    if os.path.exists(file_name) == False:
      continue
    m = np.load(file_name)
    test_ratio = 0.1
    train_size = int(len(m)*(1-test_ratio))
    train_m = m[0:train_size]
    test_m = m[train_size:]
    
    #normalize m
    train_m_mean = train_m.mean()
    train_m_std = train_m.std()
    test_m_mean = test_m.mean()
    
    train_m = (train_m - train_m_mean)/train_m.std()
    test_m = (test_m - train_m_mean)/train_m_std
    #plt.hist(train_m, bins=128)
    #plt.show()
    
    #check normality
    temp_ax = ax[int(i/2),(i%2!=0)*2+j]
    temp_ax.set_title(date+mode)
    sm.qqplot(train_m, line='45', ax=temp_ax)
    print 'For '+date+mode+" kstest_result:"
    print kstest(train_m, 'norm')
    '''
    plt.pause(1)
    save_path = '/root/quant/data/normality/' + date +mode+'.png'
    plt.savefig(save_path)
    plt.close()
    '''
    
    '''
    fig = sm.graphics.tsa.plot_acf(train_m, lags=32, ax=ax[0])
    fig = sm.graphics.tsa.plot_pacf(train_m, lags=32, ax=ax[1])
    plt.show()
    p = acorr_ljungbox(train_m, lags=20)
    print 'stotastic test, p-value is', p[1]
    '''
    
    # select train_models
    '''
    res = arima.resid
    fig,ax=plt.subplots(2, 1, figsize=(15,8))
    fig = sm.graphics.tsa.plot_acf(res, lags=32, ax=ax[0])
    fig = sm.graphics.tsa.plot_acf(res, lags=32, ax=ax[1])
    plt.show()
    '''
save_path = '/root/quant/data/normality/' + date_list[0] +'-' + date_list[-1]+'.png'
plt.savefig(save_path)
plt.show()
plt.close()
