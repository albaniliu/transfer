#!/bin/bash

cur_dir=$(dirname $0)

python $cur_dir/fourban_daily.py 100 | sort > $cur_dir/da_ban.log

python $cur_dir/zhen_ban_daily.py > $cur_dir/zhen.log

mysql -uroot -pliuzhao2010 stock -e "select distinct stock_id from daily" > $cur_dir/stock_id.dat

python $cur_dir/report.py > /mnt/xvdb/log/report_log_`date +\%F` 2>&1
