#!/bin/bash

date=`date --rfc-3339=date`
sh /root/quant/analyse/getdata/ali_rsync.sh

python /root/quant/analyse/spread_analyse/snapshot_spread.py $date
