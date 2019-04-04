#!/bin/bash

s=`pwd`
prefix=${s%quant*}

mkdir $prefix"quant/data/Mid"
mkdir $prefix"quant/data/Ali"
mkdir $prefix"quant/data/kaggle"
mkdir $prefix"quant/data/normality"
mkdir $prefix"quant/data/timeseries"
mkdir $prefix"quant/data/contract"
