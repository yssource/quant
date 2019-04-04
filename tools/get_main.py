import numpy as np
import sys
import os
import get_cwd as gc
import datetime

today = datetime.date.today()

#path_prefix = os.getcwd().split('quant')[0]
path_prefix = gc.gf()

#mean_spread_map = np.load(path_prefix+'quant/data/contract/mean_spread_map_'+'.npy').tolist()
def GetContract(ticker):
  count = 0
  for c in ticker:
    if not c.isdigit():
      count += 1
  return ticker[:count]

def get_main(tick, lag=0, topn=2):
  date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
  while not os.path.exists(path_prefix+'quant/data/contract/'+date+'/main_map'+'.npy'):
    date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
    lag += 1
  print "get " + str(date) +'\'s main'
  main_map = np.load(path_prefix+'quant/data/contract/'+date+'/main_map'+'.npy').tolist()
  if topn > 10:
    print 'cant get top10 contract!'
    sys.exit(1)
  print 'return ' + str(date) + '\'s ticker'
  return main_map[tick][0:topn]

def get_tick(lag=0):
  date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
  while not os.path.exists(path_prefix+'quant/data/contract/'+date+'/tick_list'+'.npy'):
    date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
    lag += 1
  print "get " + str(date) +'\'s main'
  tick_list = np.load(path_prefix+'quant/data/contract/'+date+'/tick_list'+'.npy').tolist()
  print 'return ' + str(date) + '\'s ticker'
  return tick_list

def get_ticker(lag=0):
  date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
  while not os.path.exists(path_prefix+'quant/data/contract/'+date+'/ticker_list'+'.npy'):
    date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
    lag += 1
  print "get " + str(date) +'\'s main'
  ticker_list = np.load(path_prefix+'quant/data/contract/'+date+'/ticker_list'+'.npy').tolist()
  print 'return ' + str(date) + '\'s ticker'
  return ticker_list

def get_tickmap(lag=0):
  date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
  while not os.path.exists(path_prefix+'quant/data/contract/'+date+'/tick_size_map_'+'.npy'):
    date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
    lag += 1
  print "get " + str(date) +'\'s main'
  tick_size_map = np.load(path_prefix+'quant/data/contract/'+date+'/tick_size_map_'+'.npy').tolist()
  print 'return ' + str(date) + '\'s ticker'
  return tick_size_map

def get_volumemap(lag=0):
  date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
  while not os.path.exists(path_prefix+'quant/data/contract/'+date+'/volume_map_'+'.npy'):
    date = str((today - datetime.timedelta(days=lag)).strftime('%Y-%m-%d'))
    lag += 1
  print "get " + str(date) +'\'s main'
  volume_map = np.load(path_prefix+'quant/data/contract/'+date+'/volume_map_'+'.npy').tolist()
  print 'return ' + str(date) + '\'s ticker'
  return volume_map
