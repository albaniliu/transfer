#!/usr/bin/python

import MySQLdb
import time
import datetime
import sys

#today = datetime.datetime.now()
#today = today - datetime.timedelta(int(sys.argv[1]))
#yesterday = today - datetime.timedelta(1)
#before = today - datetime.timedelta(2)
#todaystr = today.strftime('%Y-%m-%d')
#yesterdaystr = yesterday.strftime('%Y-%m-%d')
#beforestr = before.strftime('%Y-%m-%d')
#print todaystr

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      dpDate = {}
      cur.execute('select deal_total_quantity,open_price, current_price, yesterday_close_price, date, lowest_price from shenzhen where stock_id = %s order by time desc', [r[0]])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      count = 0
      for v in tmp:
        if dpDate.has_key(v[4]):
          continue
        dpDate[v[4]] = 1
        today_deal = long(v[0])
        today_open_price = float(v[1])
        today_current_price = float(v[2])
        yesterday_close_price = float(v[3])
        if today_deal == 0 :
          continue
        if v[2] == v[5]:
          continue
        if ((today_current_price - yesterday_close_price)/ yesterday_close_price > 0.0995):
          count = count + 1
      print r[0] + " " + str(count)
    

    cur.execute('select distinct stock_id from shanghai')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      dpDate = {}
      cur.execute('select deal_total_quantity,open_price, current_price, yesterday_close_price, date, lowest_price from shanghai where stock_id = %s order by time desc', [r[0]])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      count = 0
      for v in tmp:
        if dpDate.has_key(v[4]):
          continue
        dpDate[v[4]] = 1
        today_deal = long(v[0])
        today_open_price = float(v[1])
        today_current_price = float(v[2])
        yesterday_close_price = float(v[3])
        if today_deal == 0 :
          continue
        if v[2] == v[5]:
          continue
        if ((today_current_price - yesterday_close_price)/ yesterday_close_price > 0.0995):
          count = count + 1
      print r[0] + " " + str(count)

    cur.execute('select distinct stock_id from chuangye')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      dpDate = {}
      cur.execute('select deal_total_quantity,open_price, current_price, yesterday_close_price, date, lowest_price from chuangye where stock_id = %s order by time desc', [r[0]])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      count = 0
      for v in tmp:
        if dpDate.has_key(v[4]):
          continue
        dpDate[v[4]] = 1
        today_deal = long(v[0])
        today_open_price = float(v[1])
        today_current_price = float(v[2])
        yesterday_close_price = float(v[3])
        if today_deal == 0 :
          continue
        if v[2] == v[5]:
          continue
        if ((today_current_price - yesterday_close_price)/ yesterday_close_price > 0.0995):
          count = count + 1
      print r[0] + " " + str(count)

    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
