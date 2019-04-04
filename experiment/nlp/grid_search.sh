#!/bin/bash

learning_rate_list=('0.1' '0.05' '0.01' '0.001')
lstm_size_list=('10' '30' '50' '100')

cd /home/canl/quant/experiment/nlp
for lr in ${learning_rate_list[@]};do
  for lsl in ${lstm_size_list[@]};do
    python news_pred.py $lsl $lr > $lsl$lr.txt
  done
done
