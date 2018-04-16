#!/bin/bash

for ((i=1;i<=512;i++));
do 
#  day=`date -d "-${i} days" +%F`
  python three_ban_daily.py $i >> my.log;
done
