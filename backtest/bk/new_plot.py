import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import get_cwd as gd

tick_list = ['AP905', 'AP910']
path = gd.get_quant()+'/data/Mid/'+str(tick_list)+'.csv'
df = pd.read_csv(path)

start = min(df['time'])
end = max(df['time'])
days = int((end-start)/(24*3600)+1)
start=time.strftime("%Y-%m-%d", time.localtime(start))
end=time.strftime("%Y-%m-%d", time.localtime(end))

# 16:00 is a sep
print start+' 8:00:00'
start_sep = time.mktime(time.strptime(start+' 08:00:00', "%Y-%m-%d %H:%M:%S"))
print start_sep
print days
sep = [start_sep+i*24*3600 for i in range(days+1)]
print sep

col = df.columns
for i in range(days):
  d = {c:-9.91 for c in col}
  d['time'] = sep[i]
  df.loc[df['time'].count()] = d

#df = df.sort_values('time')
#df['time'] = [time.strftime('%H:%M:%S', time.localtime(y)) for y in df['time']]
#df.time = pd.to_datetime(df.time, format='%H:%M:%S')
df=df.set_index('time')
df = df.sort_index()
df.index = pd.to_datetime(df.index, unit='s', utc=True).tz_convert('Asia/Shanghai')
a = df[tick_list[0]]-df[tick_list[1]]
m=a[~np.isnan(a)]
plt.plot(m)
plt.show()
