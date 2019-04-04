import wget, tarfile
import os
import gzip
import time
import sys
import pandas as pd
import numpy as np

start_time = time.time()

url_prefix = 'https://s3.amazonaws.com/wanlitech-data/polled/1s/'
url_mid = '/SFITF/'
url_post = '.top.gz'

print "input contract:"
product = raw_input()

print "input start_date:"
start_date = raw_input()

print "input period:"
period = int(raw_input())

#product = 'NIK9'
#start_date = '20181015'
#period = 5

retry_times = 10

out_file = product + start_date + '@' + str(period)
if os.path.exists(out_file):
  os.remove(out_file)

#of = open(out_file, 'w+')

columns = 'time bid_price ask_price bid_size ask_size last_price volume\n'
column_list = columns.strip('\n').split(' ')

df = pd.DataFrame()
temp_file = 'temp.gz'
for i in range(period):
  if os.path.exists(temp_file):
    os.remove(temp_file)
  date = int(start_date) + i
  url = url_prefix + str(date) + url_mid + product + url_post
  fail = True
  for j in range(retry_times):
    try:
      file_name = wget.download(url, out=temp_file)
      if os.path.getsize(file_name) < 1000:
        print "\nno data in " + str(date)
        os.remove(file_name)
      else:
        fail = False
    except Exception as inst:
      print("had exception on wget: ", inst)
      if os.path.exists(temp_file):
        os.remove(temp_file)
      if j == retry_times-1:
        print 'download ' + str(date) + " failed"
        #of.close()
        os.remove(out_file)
        sys.exit(1)
      continue
    break
  if fail == False:
    g = gzip.GzipFile(temp_file)
    temp_df = pd.read_csv(g, sep=' ', names=column_list)
    df = df.append(temp_df)
    #of.write(g.read())

if os.path.exists(temp_file):
  os.remove(temp_file)

df['ticker'] = [product]*len(df)
column_list.insert(0, 'ticker')
print column_list
df = df.reindex(columns = column_list)
df = df[df['bid_price'] > 0]
print df.head()

df.to_csv(out_file, sep=' ', quoting = False, index=False)
#of.close()

print '\nrunning time ' + str(time.time()-start_time)
