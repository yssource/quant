#!/bin/bash

date=$1
#server=$2
if [[ $# < 1 ]];
then
  date=`date +"%Y-%m-%d" -d "-1day"`
fi
echo $date
chmod 600 ~/quant/key/ali_key
rsync -avz --rsh='ssh -p 22 -i ~/quant/key/ali_key' root@101.132.173.17:/running/$date/log/data_night.log.gz .
if [ $? -ne 0 ]; then
    echo $date" failed"
    exit 1
fi

mkdir ~/quant/data
mkdir ~/quant/data/Ali
mkdir ~/quant/data/Ali/$date

mv data_night.log.gz ~/quant/data/Ali/$date

gunzip -f -n ~/quant/data/Ali/$date/data_night.log.gz
