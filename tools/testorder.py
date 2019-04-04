from order import *

o=Order()
s='1551281134 275398 1551159678 462071 Order AP905 | 11380.000000@1 0 SELL AP1505 new_order SubmitNew UNKNOWN_OFFSET null'
print o.construct(s)
o.Show()
