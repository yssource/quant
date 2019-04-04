#coding=utf8
import os
import pandas as pd
import datetime
import json
import numpy as np
import sys
from gensim.models import word2vec

data_map = {}  # contract: pandas(index = date, columns=[news,price,label])

freq = 5

news_path = '/home/canl/quant/data/stocknet-dataset/tweet/preprocessed/'
price_path = '/home/canl/quant/data/stocknet-dataset/price/raw/'
contract_list = os.listdir(news_path)
columns = ['date','news']#, 'price', 'label']
#price_columns = ['date', 'movement percent', 'open price', 'high price', 'low price', 'close price', "volume"]
price_columns = ['date', 'open price', 'high price', 'low price', 'close price', 'adjust close price', 'volume']
news_set = []

#pricefile_path = price_path+'AAPL'+'.txt'
#price_df = pd.read_csv(pricefile_path, sep='\t', header=None, names=price_columns)

for contract in contract_list:
  df_content = []
  date_list = sorted(os.listdir(news_path+contract))
  start_date = date_list[0]
  end_date = date_list[-1]
  pricefile_path = price_path+contract+'.csv'
  price_df = pd.read_csv(pricefile_path, sep=',', header=None, names=price_columns)
  open_day = list(price_df['date'])
  #print open_day
  #print price_df.head()
  #sys.exit(1)
  #print start_date + '-' + end_date
  period_start_list = pd.date_range(start_date, end_date,freq=str(freq)+'D')
  for period_start in period_start_list:
    date_index_fill = False
    this_content = []
    #this_content.append(period_start.date().strftime('%Y-%m-%d'))
    init_date_index = period_start.date().strftime('%Y-%m-%d')
    file_date_list = []
    period_news_list = {}
    for i in range(freq):
      #file_date_list.append(news_path+contract+'/'+(period_start.date()+datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    #for d in file_date_list:  # date_file list
      d = news_path+contract+'/'+(period_start.date()+datetime.timedelta(days=i)).strftime('%Y-%m-%d')
      #print d
      if not os.path.exists(d):
        period_news_list[i] = []  # get this freq period all news as [[[]]]
        continue
      #date = period_start.date().strftime('%Y-%m-%d')
      date = (period_start.date()+datetime.timedelta(days=i)).strftime('%Y-%m-%d')
      if not date_index_fill:
        if date in open_day:
          this_content.append(date)
          date_index_fill = True
      day_news = []
      f = open(d)
      for line in f:
        j = json.loads(line)
        day_news.append(j['text'])
        news_set.append(j['text'])
        #day_news[d] = j['text']
      #period_news_list.append(day_news)  # get this freq period all news as [[[]]]
      period_news_list[i] = day_news  # get this freq period all news as [[[]]]
    if not date_index_fill:
      this_content.append(init_date_index)
      # add to last's news
      if len(df_content) > 0:
        max_key = sorted(df_content[-1][-1].keys())[-1]
        for k in period_news_list.keys():
          df_content[-1][-1][k+max_key+1] = period_news_list[k]
    this_content.append(period_news_list)
    df_content.append(this_content)
  #print df_content
  df = pd.DataFrame(df_content, columns=columns)
  final_df = pd.merge(df, price_df)
  price_list = final_df['close price']
  tomw_price = price_list[1:]
  last_price = price_list[:-1]
  diff_list = (np.array(tomw_price, dtype=float)-np.array(last_price, dtype=float))
  diff_percent = diff_list/np.array(last_price, dtype=float)*100
  diff_percent = np.append(diff_percent, [-101])
  class_label_list = []
  for j in range(len(diff_percent)):
    if diff_percent[j] > 0.55:
      class_label_list.append(2)
    elif diff_percent[j] < -0.5:
      class_label_list.append(0)
    else:
      class_label_list.append(1)
  #print diff_percent
  
  final_df['label'] = diff_percent
  final_df['class_label'] = class_label_list
  data_map[contract] = final_df

print data_map['AAPL']["close price"]
np.save('/home/canl/quant/data/stocknet-dataset/data_map',data_map)
np.save('/home/canl/quant/data/stocknet-dataset/news_set',news_set)

w2v_embd_size = 50
model = word2vec.Word2Vec(news_set, hs=1,min_count=1,window=3,size=w2v_embd_size)
model.save('/home/canl/quant/data/stocknet-dataset/news_word2vec.model')
np.save('/home/canl/quant/data/stocknet-dataset/w2v_embd_size', w2v_embd_size)
