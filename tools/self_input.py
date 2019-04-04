import time
import sys

def init():
  date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  mode = ''
  if len(sys.argv) == 2:
    date = sys.argv[1]
  if len(sys.argv) == 3:
    date = sys.argv[1]
    mode = sys.argv[2]
  return date,mode
