#!/bin/bash


pp
if [ $? -ne 0 ]; then
    echo "fail"
else
    echo "success"
fi
exit 1

if [ ! -f "/root/data.log.1" -o ! -f "/root/data.log.bk" ];
then
  echo "not"
else
  echo "yes"
fi
