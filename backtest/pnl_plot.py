# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import zmq
import sys
import struct
import numpy as np
import copy
import pylibconfig2 as cfg


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("ipc://order_pub")
socket.setsockopt(zmq.SUBSCRIBE,'')

pnl = {}
pos = {}
avgcost = {}
realtime_pnl ={}

'''
send_context = zmq.Context()
send_socket = send_context.socket(zmq.PUB)
send_socket.bind("ipc://exchange_info")

def SendReply(side, contract, order_ref, price, size):
  reason=''
  exchange_info=struct.pack("i32s32sid64si", 5, contract, order_ref, size, price, reason, side)
  send_socket.send(exchange_info)
'''

day_file = ""
config_path= ''
cfg_str= ''
legend= ''

def CfgSetting(path):
  f=open(path)
  setting=cfg.Config(f.read())
  f.close()
  return "range_width:" + str(setting.lookup('strategy')[0].max_holding_sec)

while True:
  response = socket.recv();
  tv_sec, tv_usec, contract,price,size,traded_size,side,order_ref,action,status,offset,tbd,res=struct.unpack("2Q32sd3i32s3i128s784s",response)
  contract=contract.split('\0')[0]
  if contract == 'day_end':
    continue
  tbd=tbd.split('\0')[0]
  order_ref=order_ref.split('\0')[0]
  if action == 5: # config file path
    if contract == 'data_path':
      day_file = tbd
      continue
    if contract == 'config_path':
      config_path = tbd;
      cfg_str = CfgSetting(config_path)
      continue
    if contract == 'plot':
      #plt.legend(loc='upper left')
      #plt.show()
      continue
    if contract == 'legend':
      legend = tbd
      continue
    if contract == 'backtest_end':
      pos.clear()
      pnl.clear()
      avgcost.clear()
      rm = copy.deepcopy(realtime_pnl)
      realtime_list = sorted(realtime_pnl.items())
      np.save("rm_"+cfg_str+'.npy', rm)
      plt.plot([r[0] for r in realtime_list], [r[1][0] for r in realtime_list], label=legend)
      plt.legend(loc='upper left')
      plt.pause(0.1)
      realtime_pnl.clear()
      continue
    continue
    
    '''
    for r in realtime_pnl:
      plt.annotate(r[1][1], xy=(r[0],r[1][0]), xytext=(r[0], r[1][0]-0.1), arrowprops=dict(facecolor='black', shrink=0.5))
    '''
    
  print("%s order %s traded %d@%lf side:%d" %(contract, order_ref, size, price, side))
  #SendReply(side, contract, order_ref, price, size)
  #print("contract:%s price:%f size:%d traded_size:%d side:%d order_ref:%s action:%d status:%d offset:%d tbd:%s" % (contract,price,size,traded_size,side,order_ref,action,status,offset,tbd))
  true_size = (size if side == 1 else -size)
  if not pos.has_key(contract):
    pos[contract] = 0
    avgcost[contract] = 0.0
    pnl[contract] = 0
  pos[contract] += true_size
  is_close = (pos[contract]*true_size <= 0)
  #print contract + str(is_close)
  pnl[contract] += (true_size*(avgcost[contract]-price) if is_close else 0.0) # only update pnl if close traded
  avgcost[contract] += (price-avgcost[contract])*true_size/pos[contract] if not is_close else 0.0 # only update avgcost if open traded
  if pos[contract] == 0:
    avgcost[contract] = 0.0
  if is_close:
    realtime_pnl[tv_sec] = (np.array(pnl.values()).sum(), contract)
