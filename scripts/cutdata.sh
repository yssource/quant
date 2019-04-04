#!/bin/bash

dir=`pwd`

if [ $# -lt 1 ];
then
  echo "error: input contracts"
  exit 1
fi

contract=$1
 
for file in /root/quant/data/Ali/*; do
  echo $file
  rm $file/$contract
  cat $file/data.log | grep -E $contract > $file/$contract
  cat $file/data_night.log | grep -E $contract >> $file/$contract
done
