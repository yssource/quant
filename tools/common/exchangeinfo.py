class ExchangeInfo:
  def __init__(self):
    self.type = -1;
    self.ticker = 'c';
    self.order_ref = 'or';
    self.trade_size = -1;
    self.trade_price = -1.0;
    self.reason = '';
    self.side = -1;
    self.time_str = '-1'
    type_list = ['Uninited','Acc','Rej','Cancelled','CancelRej',
    'Filled','Pfilled','Position','Unknown']
    self.side_int = {"BUY":0, 'SELL':1}
    self.int_side = {0:"BUY", 1:'SELL'}
    self.type_int = {type_list[i]:i for i in range(len(type_list))}
    self.int_type = {i:type_list[i] for i in range(len(type_list))}

  def construct(self, l):
    if l[-1] == '\n':
      l = l[:-1]
    c = l.split(' ')
    if len(c) != 9:
      return False
    self.time_str = c[0]+'.'+c[1][0:2]
    self.order_ref = c[3]
    ps = c[5].split('@')
    self.trade_price = ps[0]
    self.trade_size = ps[1]
    self.type = self.type_int[c[6]]
    self.ticker = c[7]
    self.side = self.side_int[c[8]]
    return True

  def Show(self):
    show_str = ''
    split_c = ' '
    ts = self.time_str.split('.')
    time_sec = ts[0]
    time_usec = ts[1]+'0000'
    show_str += time_sec + split_c + time_usec +split_c
    show_str += 'exchangeinfo' + split_c
    show_str += self.order_ref + split_c
    show_str += '|' + split_c
    show_str += self.trade_price + '@'+self.trade_size + split_c
    show_str += self.int_type[self.type] + split_c
    show_str += self.ticker+split_c
    show_str += self.int_side[self.side]
    print(show_str)
    return show_str

if __name__ == '__main__':
  with open('/today/filled') as f:
    for l in f:
      ei = ExchangeInfo()
      ei.construct(l)
      ei.Show()
