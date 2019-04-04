#!/bin/sh
if [ $# == 2 ]; then
    datebeg=$1
    dateend=$2
else
    echo "请输入开始时间和结束日期，格式为2017-04-04"
    exit 1
fi

beg_s=`date -d "$datebeg" +%s`
end_s=`date -d "$dateend" +%s`

echo "处理时间范围：$beg_s 至 $end_s"

while [ "$beg_s" -le "$end_s" ];do
    day=`date -d @$beg_s +"%Y-%m-%d"`;
    echo "当前日期：$day"
    beg_s=$((beg_s+86400));
    if [ ! -f "~/quant/data/Ali/$day/data.log.gz" ];
    then
      /root/quant/analyse/getdata/ali_rsync.sh $day
    fi
    if [ ! -f "~/quant/data/Ali/$day/data_night.log.gz" ];
    then
      /root/quant/analyse/getdata/ali_rsync_night.sh $day
    fi
    #if [ ! -f "~/quant/data/Ali/$day/data_night.log.gz" -a ! -f "~/quant/data/Ali/$day/data.log.gz" ];
    if [ "`ls -A ~/quant/data/Ali/$day`" = "" ];
    then
      rm -rf ~/quant/data/Ali/$day
    fi
done

echo "日期全部处理完成"
