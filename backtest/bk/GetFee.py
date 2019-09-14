import pylibconfig2 as cfg
from get_main import GetContract
open_fee_rate = {}
close_today_fee_rate = {}
close_fee_rate = {}
deposit_rate = {}
contract_size = {}
min_price_move = {}
is_fixed_open_fee_rate = {}
is_fixed_close_today_fee_rate = {}
is_fixed_close_fee_rate = {}
open_fee ={}
close_today_fee = {}
close_fee={}

config_path = "/root/hft/config/backtest/contract.config"

def Read(config_path = config_path):
  setting = cfg.Config(open(config_path).read()).lookup('map')
  for s in setting:
    ticker = s.ticker
    print 'handling ' + ticker
    is_fixed_open_fee_rate[ticker] = bool(s.is_fixed_open_fee_rate)
    is_fixed_close_fee_rate[ticker] = bool(s.is_fixed_close_fee_rate)
    is_fixed_close_today_fee_rate[ticker] = bool(s.is_fixed_close_today_fee_rate)
    if is_fixed_open_fee_rate[ticker]:
      open_fee[ticker] = float(s.open_fee)
    else:
      open_fee_rate[ticker] = float(s.open_fee_rate)
    if is_fixed_close_fee_rate[ticker]:
      close_fee[ticker] = float(s.close_fee)
    else:
      close_fee_rate[ticker] = float(s.close_fee_rate)
    if is_fixed_close_today_fee_rate[ticker]:
      close_today_fee[ticker] = float(s.close_today_fee)
    else:
      close_today_fee_rate[ticker] = float(s.close_today_fee_rate)
    deposit_rate[ticker] = float(s.deposit_rate)
    contract_size[ticker] = int(s.contract_size)
    min_price_move[ticker] = float(s.min_price_move)

Read()

def Cal_Fee(ticker, price, size, flag):
  con = GetContract(ticker)
  if flag == "open":
    if is_fixed_open_fee_rate[con]:
      return open_fee[con]
    else:
      return price*size*contract_size[con]*open_fee_rate[con]
  elif flag == "close_today":
    if is_fixed_close_today_fee_rate[con]:
      return close_today_fee[con]
    else:
      return price*size*contract_size[con]*close_today_fee_rate[con]
  elif flag == "close":
    if is_fixed_close_fee_rate[con]:
      return close_fee[con]
    else:
      return price*size*contract_size[con]*close_fee_rate[con]
  else:
    print "wrong flag:" + flag + ", ignore this fee"
    return 0.0

def Cal_Fee_Point(ticker, price, flag):
  con = GetContract(ticker)
  d = contract_size[con]
  if flag == "open":
    if is_fixed_open_fee_rate[con]:
      return open_fee[con] / d
    else:
      return price*contract_size[con]*open_fee_rate[con]/d
  elif flag == "close_today":
    if is_fixed_close_today_fee_rate[con]:
      return close_today_fee[con]/d
    else:
      return price*contract_size[con]*close_today_fee_rate[con]/d
  elif flag == "close":
    if is_fixed_close_fee_rate[con]:
      return close_fee[con]/d
    else:
      return price*contract_size[con]*close_fee_rate[con]/d
  else:
    print "wrong flag:" + flag + ", ignore this fee"
    return 0.0
