# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt
import test_stationarity

df = pd.read_csv('/root/quant/data/time_series/AirPassengers.csv', encoding='utf-8', index_col='date')

df.index = pd.to_datetime(df.index)  # 将字符串索引转换成时间索引
ts = df['x']  # 生成pd.Series对象
# 查看数据格式

ts_log = np.log(ts)
#test_stationarity.draw_ts(ts_log)

#test_stationarity.draw_trend(ts_log, 12)
#print ts_log

'''
diff_12 = ts_log.diff(12)
diff_12.dropna(inplace=True)
diff_12_1 = diff_12.diff(1)
diff_12_1.dropna(inplace=True)
print test_stationarity.testStationarity(diff_12_1)
'''

rol_mean = ts_log.rolling(window=12).mean()
rol_mean.dropna(inplace=True)
ts_diff_1 = rol_mean.diff(1)
ts_diff_1.dropna(inplace=True)
print test_stationarity.testStationarity(ts_diff_1)

ts_diff_2 = ts_diff_1.diff(1)
ts_diff_2.dropna(inplace=True)
print test_stationarity.testStationarity(ts_diff_2)

#test_stationarity.draw_acf_pacf(ts_diff_2)

from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa import arima_model
model = ARMA(ts_diff_2, order=(1, 1)) 
result_arma = model.fit( disp=-1, method='css')

predict_ts = result_arma.predict()
# 一阶差分还原
diff_shift_ts = ts_diff_1.shift(1)
diff_recover_1 = predict_ts.add(diff_shift_ts)
# 再次一阶差分还原
rol_shift_ts = rol_mean.shift(1)
diff_recover = diff_recover_1.add(rol_shift_ts)
# 移动平均还原
rol_sum = ts_log.rolling(window=11).sum()
rol_recover = diff_recover*12 - rol_sum.shift(1)
# 对数还原
log_recover = np.exp(rol_recover)
log_recover.dropna(inplace=True)

print log_recover

ts = ts[log_recover.index]  # 过滤没有预测的记录
plt.figure(facecolor='white')
log_recover.plot(color='blue', label='Predict')
ts.plot(color='red', label='Original')
plt.legend(loc='best')
plt.title('RMSE: %.4f'% np.sqrt(sum((log_recover-ts)**2)/ts.size))
plt.show()

print test_stationarity.proper_model(ts_log)

print model.forecast()
