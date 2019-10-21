#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONPATH=/root/quant/tools:/root/lib-hft/lib/cpp_py:/root/quant/tools/common

/root/anaconda2/bin/python /root/quant/report/PT_report.py > /root/PT_report.log  2>&1
