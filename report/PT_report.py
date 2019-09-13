# -*- coding: UTF-8 -*-
from EmailWorker import *
from Reader import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import subprocess
from exchangeinfo import *
from Trader import *
import datetime

def LoadShot(mid_file, mid_map, mid_time_map, single_map, up_bound_map, down_bound_map, mean_map):
  r = Reader()
  r.load_shot_file(mid_file)
  for i in range(r.get_shotsize()):
    shot = r.read_bshot(i)
    ticker = shot.ticker
    mid = shot.last_trade
    up = shot.asks[0]
    down = shot.bids[0]
    mean_up = shot.asks[2]
    mean_down = shot.bids[2]
    mean = (mean_up+mean_down)/2
    time = shot.time
    if ticker not in mid_map:
      mid_map[ticker] = [mid]
      mid_time_map[ticker] = {time:mid}
      single_map[ticker] = [(shot.bids[3], shot.asks[3])]
      up_bound_map[ticker] = [up]
      down_bound_map[ticker] = [down]
      mean_map[ticker] = [mean]
      continue
    up_bound_map[ticker].append(up)
    down_bound_map[ticker].append(down)
    mean_map[ticker].append(mean)
    mid_map[ticker].append(mid)
    mid_time_map[ticker][time] = mid
    single_map[ticker].append((shot.bids[3], shot.asks[3]))

def SaveSpreadPng(mid_map, mid_time_map, png_path):
  tickers = mid_time_map.keys()
  ksize = len(tickers)
  ncol, nrow = int(math.sqrt(ksize)), int(math.sqrt(ksize))+1
  width = int(math.sqrt(ksize)) + 1 
  height = int(math.sqrt(ksize)) +1
  fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(10,8))
  count = 0
  for t in tickers:
    if count % (ncol*nrow) == 0 and count > 0:
      fig.tight_layout()
      fig.savefig('spread_move@%d' %(t, str(count)))
      fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=(10,8))
    this_ax = ax[int(count/ncol)%nrow, count%ncol]
    items = mid_time_map[t].items()
    items = sorted(items, key=lambda x:x[0])
    #plt.plot([i[0] for i in items], [i[1] for i in items])
    this_ax.plot(mid_map[t], label='mid')
    this_ax.plot(up_bound_map[t], label='up')
    this_ax.plot(down_bound_map[t], label='down')
    this_ax.plot(mean_map[t], label='mean')
    this_ax.set_title('%s\'s spread move' % (t))
    this_ax.grid()
    this_ax.legend()
    count += 1
  plt.tight_layout()
  plt.savefig(png_path)

def TradeReport(date_prefix, trade_path, cancel_path):
  trader = Trader()
  command = 'cat '+date_prefix+'log/order.log | grep Filled > ' +  trade_path +'; cat '+ date_prefix + 'log/order_night.log | grep Filled >> ' + trade_path
  command_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  command = 'cat '+date_prefix+'log/order.log | grep Cancelled > '+ cancel_path +'; cat '+date_prefix+'log/order_night.log | grep Cancelled >> '+ cancel_path
  command_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  with open(trade_path) as f:
    ei = ExchangeInfo()
    for l in f:
      ei.construct(l)
      trader.RegisterOneTrade(ei.contract, int(ei.trade_size) if ei.side == 0 else -int(ei.trade_size), float(ei.trade_price))
  df = trader.GenDFReport()
  #trader.Summary()
  df.insert(len(df.columns), 'cancelled', 0)
  with open(cancel_path) as f:
    ei = ExchangeInfo()
    for l in f:
      ei.construct(l)
      df.loc[ei.contract, 'cancelled'] = df.loc[ei.contract, 'cancelled'] + 1
  return df, trader.GenStratReport()

def GenVolReport(mid_map, single_map):
  caler = CALER('/root/hft/config/contract/contract.config')
  v = {}
  i_rate = 0.2
  col = [str((i+1)*i_rate*100)+'%' for i in range(int(1/i_rate))]
  col.append('oneround_fee(estimated)')
  for k in mid_map:
    main_ticker, hedge_ticker = k.split('|')
    mid = mid_map[k]
    increment = int(len(mid)*i_rate)
    v[k] = [np.std(mid[i*increment:(i+1)*increment-1]) for i in range(int(1/i_rate))]
    main_mean, hedge_mean = np.mean([p[0] for p in single_map[k]]), np.mean([p[1] for p in single_map[k]])
    main_fee = caler.CalFeePoint(main_ticker, main_mean, 1, main_mean, 1, GetCon(main_ticker) in no_today)
    hedge_fee = caler.CalFeePoint(hedge_ticker, hedge_mean, 1, hedge_mean, 1, GetCon(hedge_ticker) in no_today)
    v[k].append(main_fee.open_fee_point+main_fee.close_fee_point+hedge_fee.open_fee_point+hedge_fee.close_fee_point)
  rdf = pd.DataFrame(v).T
  rdf.columns = col
  for k in rdf:
    for c in rdf[k].keys():
      if isinstance(rdf[k][c], float):
        rdf[k][c] = round(rdf[k][c], 1)
  return rdf

def GenBTReport(bt_file_path):
  r = Reader()
  t = Trader()
  r.load_order_file(bt_file_path)
  for i in range(r.get_ordersize()):
    o = r.read_border(i)
    if o.price > 0 and abs(o.size) > 0:
      t.RegisterOneTrade(o.contract, o.size if o.side==1 else -o.size, o.price)
  return t.GenDFReport(), t.GenStratReport()

if __name__ == '__main__':
  mid_map = {}
  mid_time_map = {}
  single_map = {}
  up_bound_map = {}
  down_bound_map = {}
  mean_map = {}
  EM = EmailWorker(recv_mail="huangxy17@fudan.edu.cn;839507834@qq.com")
  date_prefix = '/today/'
  LoadShot(date_prefix+'mid.dat', mid_map, mid_time_map, single_map, up_bound_map, down_bound_map, mean_map)
  strat_keys = mid_map.keys()
  png_path = date_prefix+'spread_move.png'
  SaveSpreadPng(mid_map, mid_time_map, png_path)
  trade_df, strat_df = TradeReport(date_prefix, date_prefix+'filled', date_prefix+'cancelled')
  vol_df = GenVolReport(mid_map, single_map)
  bt_df, bt_strat_df = GenBTReport(date_prefix+'order_backtest.dat')
  EM.SendHtml(subject='PT_Report on %s'%(datetime.date.today().strftime("%d/%m/%Y")), content = render_template('PT_report.html', trade_df=trade_df, strat_df=strat_df, vol_df=vol_df, bt_df=bt_df, bt_strat_df=bt_strat_df), png_list=[png_path])
