from pyramid.arima import auto_arima
import self_input as si
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

date,mode = si.init()

target_list = ['ni1905', 'ni1903']

file_path = '/root/quant/data/Mid/'+target_list[0]+target_list[1]+'_'+date+mode+'_mid.npy'
print file_path
m = np.load(file_path)
train_ratio = 0.9
train_size = int(len(m)*0.9)
train = m[0:train_size]
valid = m[train_size:]

model = auto_arima(train, trace=True, error_action='ignore', suppress_warnings=True)
model.fit(train)
print model

forecast = model.predict(n_periods=len(valid))
forecast = pd.DataFrame(forecast,columns=['Prediction'])

#plot the predictions for validation set
plt.plot(train, label='Train')
plt.plot(valid, label='Valid')
plt.plot(forecast, label='Prediction')
plt.show()
