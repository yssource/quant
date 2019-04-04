import os
import subprocess

def gf():
  s = os.getcwd().split('/')[1]
  return '/'+s+'/'

def get_quant():
  command = "cd ~; pwd"
  command_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  out = command_result.communicate()[0].split('\n')[0]
  remote_command = "cd ~; find . -name \"quant\""
  remote_command_result = subprocess.Popen(remote_command, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  remote_out = remote_command_result.communicate()[0].split('\n')[0]
  return out+'/'+remote_out

print get_quant()
