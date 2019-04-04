#!/bin/bash

startdate=`date +%Y-%m-%d`
enddate=`date +%Y-%m-%d`

if [ $# == 0 ];
then
  echo "input start_date"
  exit 1
elif [ $# == 1 ];
then
  startdate=`date -d "$1" +%Y-%m-%d`
else
  startdate=`date -d "$1" +%Y-%m-%d`
  enddate=`date -d "$2" +%Y-%m-%d`
fi

#echo $startdate
#echo $enddate
temp_date=$startdate

while [[ $temp_date < $enddate  ]]
do
    echo 'makeup data for ' $temp_date
    temp_date=`date -d "+1 day $temp_date" +%Y-%m-%d`
    ~/quant/analyse/getdata/ali_rsync.sh $temp_date
    ~/quant/analyse/getdata/ali_rsync_night.sh $temp_date
done
