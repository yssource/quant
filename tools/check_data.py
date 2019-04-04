import pandas as pd
import numpy as np
from market_snapshot import *
import sys

tick = 'IC1906'
if len(sys.argv) >= 2:
  tick=sys.argv[1]

s=set()
f = open('data.log')
count = 0
for line in f:
  shot = MarketSnapshot()
  if shot.construct(line) == True:
    if shot.ticker == tick:
      count += 1
      s.add(round(shot.time, 1))

print 'construct '+str(count)
print 'set_len '+str(len(s))
