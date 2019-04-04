#Embedded file name: /root/quant/backtest/online_pnl_plot.py
import matplotlib.pyplot as plt
import zmq
import sys
import struct
import numpy as np
import copy
import pylibconfig2 as cfg
from order import *
from get_main import GetContract
action_map = {'Uninited': 0,
 'new_order': 1,
 'replace_order': 2,
 'cancel_order': 3,
 'query_pos': 4,
 'plaintext': 5}
pnl = {}
pos = {}
avgcost = {}
realtime_pnl = {}
day_file = ''
config_path = ''
cfg_str = ''
hedge =''
open_fee_rate = {}
close_today_rate = {}
close_rate = {}
deposit_rate = {}
contract_size = {}
min_price_move = {}
temp_fee = {}

fee = {}

'''
print(GetContract('I1903'))
print(GetContract('asd'))
sys.exit(1)
'''

def CfgSetting(path):
    f = open(path)
    setting = cfg.Config(f.read())
    f.close()
    return 'holding time:' + str(setting.lookup('strategy')[0].max_holding_sec)

def GetHedge(path):
    f = open(path)
    setting = cfg.Config(f.read())
    f.close()
    #print [setting.lookup('strategy')[i].pairs[1] for i in range(len(setting.lookup('strategy')))]
    return [setting.lookup('strategy')[i].pairs[1] for i in range(len(setting.lookup('strategy')))]

def HandleContractConfig(path):
    f = open(path)
    setting = cfg.Config(f.read()).lookup('map')
    for s in setting:
      ticker = s.ticker
      deposit_rate[ticker] = float(s.deposit_rate)
      open_fee_rate[ticker] = float(s.open_fee_rate)
      close_today_rate[ticker] = float(s.close_today_fee_rate)
      close_rate[ticker] = float(s.close_fee_rate)
      contract_size[ticker] = int(s.contract_size)
      min_price_move[ticker] = float(s.min_price_move)

def plot_pnl(path = '/root/hft/build/bin/backtest_record'):
  f = open(path)
  for line in f:
      o = Order()
      if o.construct(line) == True:
          action = action_map[o.action]
          tv_sec = int(o.wrap_time)
          contract = o.contract
          price = o.price
          size = o.size
          traded_size = o.traded_size
          order_ref = o.order_ref
          tbd = o.tbd
          side = o.side
          if action == 5:
              if contract == 'data_path':
                  day_file = tbd
              if contract == 'param_config_path':
                  config_path = tbd.split('\n')[0]
                  cfg_str = CfgSetting(config_path)
                  hedge = GetHedge(config_path)
              if contract == 'contract_config_path':
                  contract_config_path = tbd.split('\n')[0]
                  HandleContractConfig(contract_config_path)
              if contract == 'plot':
                  print 'plot'
                  plt.show()
              if contract == 'backtest_end':
                  pos.clear()
                  pnl.clear()
                  avgcost.clear()
                  rm = copy.deepcopy(realtime_pnl)
                  realtime_list = sorted(realtime_pnl.items(), key=lambda x: x[0])
                  np.save('rm_' + cfg_str + '.npy', rm)
                  #plt.plot([ r[0] for r in realtime_list ], [ r[1][0] for r in realtime_list ], label=cfg_str)
                  plt.plot([ r[1][0] for r in realtime_list ], label=cfg_str)
                  plt.legend(loc='upper left')
                  plt.savefig(cfg_str + '.jpg')
                  plt.title('pnl curve')
                  print realtime_pnl
                  realtime_pnl.clear()
              continue
          '''
          print '%d %s order %s traded %d@%lf side:%d' % (tv_sec,
           contract,
           order_ref,
           size,
           price,
           side)
          '''
          true_size = size if side == 1 else -size
          if not pos.has_key(contract):
              pos[contract] = 0
              avgcost[contract] = 0.0
              pnl[contract] = 0
          pos[contract] += true_size
          is_close = pos[contract] * true_size <= 0
          con = GetContract(contract)
          if is_close == True:
              this_pnl = true_size * (avgcost[contract] - price) * contract_size[con]
              this_fee = size*(price*close_rate[con] + avgcost[contract]*open_fee_rate[con])*contract_size[con]
              pnl[contract] += this_pnl
              pnl[contract] -= this_fee
              if pos[contract] == 0:
                  avgcost[contract] = 0.0
              if contract in hedge:
                realtime_pnl[tv_sec] = (np.array(pnl.values()).sum(), contract)
          else:
              avgcost[contract] = abs((avgcost[contract] * (pos[contract] - true_size) + price * true_size) / pos[contract])


if __name__ == '__main__':
    plot_pnl()
