#!/usr/bin/python

import MySQLdb
import time
import datetime

today = datetime.datetime.now()
today = today - datetime.timedelta(1)
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')
print todaystr
print yesterdaystr

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='stock',port=3306)
    cur=conn.cursor()
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
      if ((today_current_price - yesterday_close_price)/ yesterday_close_price > 0.0995):
        continue
      
      cur.execute('select deal_total_quantity,current_price from shanghai where stock_id = %s and date = %s order by time desc limit 1', [r[0], yesterdaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      yesterday_deal = long(tmp[0][0])
      yesterday_current_price = tmp[0][1]
      if yesterday_deal == 0 :
        continue
      if today_deal > yesterday_deal * 2.0 and today_current_price > today_open_price :
        print r[0] + ", " + str(today_deal) + ", " + str(yesterday_deal)
    
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
