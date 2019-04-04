import time
start_sec = time.time()
import matplotlib.pyplot as plt
from market_snapshot import *

f = open()

c1 = 'NI1903'
c2 = 'NI1901'

for line in f:
  shot=MarketSnapshot()
  if shot.construct(line) == True:
    
