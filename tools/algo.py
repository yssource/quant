import numpy as np
import pandas as pd

def GetSlipWindowMax(nums, k):
  if len(nums) <= 1 or k==1:
      return nums
  v = []
  temp = []
  for i, num in enumerate(nums):
      if len(temp) == 0:
          temp.append(i)
          v.append(num)
          continue
      if i - temp[0] >= k:
          del temp[0]
      for t in reversed(temp):
          if num > nums[t]:
              temp.pop()
          else:
              break
      temp.append(i)
      v.append(nums[temp[0]])
  return v

def rolled(df, n, cut_tail = True):
  roll = np.reshape(np.hstack([df.shift(-i).values for i in range(n)]), (len(df), n, -1))
  return roll[:-n] if cut_tail else roll

def rolled2(df, n, cut_tail = True):
  k = range(df.columns.nlevels)
  _k = [i - len(k) for i in k]
  myroll = pd.concat([df.shift(i).stack(level=k) for i in range(n)],
    axis=1, keys=range(n)).unstack(level=_k)
  return [np.transpose(row.unstack(0).values).tolist() for i, row in myroll.iterrows()]
