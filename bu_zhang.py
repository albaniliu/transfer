#!/usr/bin/python

import MySQLdb
import time
import datetime
import sys

start = sys.argv[1]
end = sys.argv[2]

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      cur.execute('select yesterday_close_price,deal_total_quantity from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], start])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      if tmp[0][1] == 0:
        continue
      start_close_price = float(tmp[0][0])
      cur.execute('select yesterday_close_price,deal_total_quantity from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], end])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      if tmp[0][1] == 0:
        continue
      end_close_price = float(tmp[0][0])
      print r[0]  + " " + str((end_close_price - start_close_price) / start_close_price)

    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
