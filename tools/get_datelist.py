import datetime

def get(lag=20):
  today = datetime.date.today()
  date_list = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(lag, 0, -1)] 
  return date_list

def gettoday():
  today = datetime.date.today()
  return str(today)
