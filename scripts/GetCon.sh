#!/bin/bash

date=`date --rfc-3339=date`
python ~/quant/analyse/getticksize/caldata.py $date
