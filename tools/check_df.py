import numpy as np
import pandas as pd

tick = 'IC1906'
if len(sys.argv) >= 2:
  tick=sys.argv[1]

time_end=1543474902
df=pd.read_csv('/root/quant/data/Mid/[\'IC1903\', \'IC1906\'].csv')

df=df.sort_values('time')
df=df[df['time'] < time_end]

d=df[tick]
real=d[~np.isnan(d)]
print 'df len is ' + str(len(real))
