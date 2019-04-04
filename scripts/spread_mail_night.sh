#!/bin/bash

yes_date=`date -d "1 day ago" +"%Y-%m-%d"`
sh /root/quant/analyse/getdata/ali_rsync_night.sh $yes_date

python /root/quant/analyse/spread_analyse/snapshot_spread.py $yes_date _night
