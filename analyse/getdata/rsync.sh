#!/bin/bash

date=$1
server=$2
if [[ $# < 2 ]];
then
  echo 'use default settings'
  date=`date +%Y%m%d`
  server='jefferson'
fi
echo $date
s='cat ~/'$server'/run/'$date'/backend/market_data.log | grep SFIT > ~/market_data.log'
echo $s
ssh  -i /root/nanshan_backup ec2-user@54.178.131.85 $s
rsync -avz --rsh='ssh -p 22 -i /root/nanshan_backup' ec2-user@54.178.131.85:~/market_data.log .
