#!/usr/bin/python

import MySQLdb
import time
import datetime
import sys

today = datetime.datetime.now()
today = today - datetime.timedelta(int(sys.argv[1]))
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')
print todaystr

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], todaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      today_deal = long(tmp[0][0])
      today_open_price = float(tmp[0][1])
      today_current_price = float(tmp[0][2])
      yesterday_close_price = float(tmp[0][3])
      if today_deal == 0 :
        continue
    
      cur.execute('select deal_total_quantity,current_price from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], yesterdaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      yesterday_deal = long(tmp[0][0])
      yesterday_current_price = tmp[0][1]
      if ((today_current_price - yesterday_current_price)/ yesterday_close_price < -0.11):
        print r[0] 

    cur.execute('select distinct stock_id from shanghai')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price from shanghai where stock_id = %s and date = %s order by time desc limit 1', [r[0], todaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      today_deal = long(tmp[0][0])
      today_open_price = float(tmp[0][1])
      today_current_price = float(tmp[0][2])
      yesterday_close_price = float(tmp[0][3])
      if today_deal == 0 :
        continue
    
      cur.execute('select deal_total_quantity,current_price from shanghai where stock_id = %s and date = %s order by time desc limit 1', [r[0], yesterdaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      yesterday_deal = long(tmp[0][0])
      yesterday_current_price = tmp[0][1]
      if ((today_current_price - yesterday_current_price)/ yesterday_close_price < -0.11):
        print r[0] 
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
