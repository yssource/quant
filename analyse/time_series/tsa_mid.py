import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

file_path = '/root/quant/data/Mid/'
m = np.load(file_path+'ni1905ni1903_2018-12-17_mid.npy')
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
print len(train_m)
'''
#plt.hist(train_m, bins=128)
#plt.show()

fig, ax = plt.subplots(2,1,figsize=(20,10))

#check normality
#sm.qqplot(train_m, line='45')
#plt.show()

fig = sm.graphics.tsa.plot_acf(train_m, lags=32, ax=ax[0])
fig = sm.graphics.tsa.plot_pacf(train_m, lags=32, ax=ax[1])
plt.show()
p = acorr_ljungbox(train_m, lags=20)
print 'stotastic test, p-value is', p[1]

# select train_models
resDiff = sm.tsa.arma_order_select_ic(train_m, max_ar=3, max_ma=3, ic=['aic'], trend='c')
print('ARMA(p,q) =',resDiff['aic_min_order'],'is the best.')

arima = sm.tsa.statespace.SARIMAX(train_m,order=(2,0,1),seasonal_order=(0,0,0,0),enforce_stationarity=False, enforce_invertibility=False,).fit()
#print arima.summary()
res = arima.resid
fig,ax=plt.subplots(2, 1, figsize=(15,8))
fig = sm.graphics.tsa.plot_acf(res, lags=32, ax=ax[0])
fig = sm.graphics.tsa.plot_acf(res, lags=32, ax=ax[1])
plt.show()

from sklearn.metrics import mean_squared_error
pred = arima.predict(train_size,len(m))[1:]

print('mse is {}'.format(mean_squared_error(test_m, pred)))

'''
pd.DataFrame({'test':test_m*train_m_std+train_m_mean, 'pred':pred}).plot()
plt.axhline(y=train_m_mean-2*train_m_std, color='blue', linestyle='-')
plt.axhline(y=train_m_mean+2*train_m_std, color='red', linestyle='-')
plt.show()
'''
pd.DataFrame({'test':test_m, 'pred':pred}).plot()
plt.show()
