#!/usr/bin/python

import MySQLdb
import time
import datetime

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')
print todaystr

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select stock_id, yesterday_close_price, current_price, deal_total_quantity from shenzhen where stock_id = %s and date = %s order by time', [r[0], todaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      for i in range(17, len(tmp)):
        if tmp[i][1] == 0:
          continue
        if ((tmp[i][2] - tmp[i][1]) / tmp[i][1] < 0.05):
          continue
        if ((tmp[i][2] - tmp[i-5][2]) / tmp[i][1] > 0.05 and
            (tmp[i][2] - tmp[i-1][2]) / tmp[i][1] > 0.01):
          print tmp[i-1]
          print tmp[i]
#        if ((tmp[i][2] - tmp[i-1][2]) / tmp[i][1] > 0.02 and 
#            (tmp[i-1][2] - tmp[i-2][2]) / tmp[i][1] > 0.02 ): 
#          print tmp[i-1]
#          print tmp[i]
      
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
