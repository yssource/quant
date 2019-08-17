import numpy as np

class Order:
  def __init__(self):
    self.wrap_time=-1.0;
    self.contract=''
    self.price=-1.0
    self.size=1
    self.traded_size=1
    self.side=-1
    self.order_ref=''
    self.action = -1
    self.status = -1
    self.offset=-1
    self.tbd=''

  def construct(self, s):
    content = s.split(' ')
    if len(content) == 15 and '@' in s and '|' in s:
      #1551280899 465344 1543375009 365863 Order AP910 | 7748.000000@1 0 SELL AP0 new_order SubmitNew UNKNOWN_OFFSET null
      show_time_sec=int(content[0])
      show_time_usec=float('0.'+content[1])
      wrap_time_sec=int(content[2])
      wrap_time_usec=float('0.'+content[3])
      self.wrap_time = wrap_time_sec+round(wrap_time_usec,2)
      topic=content[4]
      self.contract=content[5]
      split_char=content[6]
      trade_info=content[7]
      ti = trade_info.split('@')
      self.price = float(ti[0])
      self.size = int(ti[1])
      self.traded_size=content[8]
      self.side=2 if content[9] == "SELL" else 1
      self.order_ref=content[10]
      self.action=content[11]
      status=content[12]
      offset=content[13]
      self.tbd=content[14]
      return True
    else:
      return False

  def Show(self, split_c=' '):
    show_str = ''
    show_str += str(self.wrap_time)
    show_str += split_c   
    show_str += str(self.contract)
    show_str += split_c   
    show_str += str(self.price)
    show_str += '@'
    show_str += str(self.size)
    show_str += split_c   
    show_str += str(self.traded_size)
    show_str += split_c   
    show_str += "BUY" if self.side == 1 else "SELL"
    show_str += split_c   
    show_str += self.action
    show_str += split_c   
    show_str += self.order_ref
    show_str += split_c   
    show_str += self.tbd
    print show_str
