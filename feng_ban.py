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

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    
    dbname = "chuangye"
    cur.execute('select distinct stock_id from ' + dbname)
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price,lowest_price, highest_price, time from ' + dbname + ' where stock_id = %s and date = %s and time > "09:26:00"', [r[0], todaystr])
      tmp = cur.fetchall()
      if len(tmp) < 1:
        continue
      ban = False
      OK = False
      for result in tmp:
        today_current_price = float(result[2])
        yesterday_close_price = float(result[3])
        lowest_price = float(result[4])
        if isBan(yesterday_close_price, lowest_price):
          OK = False
          break
        if result[6] < '10:00:00' and isBan(yesterday_close_price, today_current_price):
          ban = True
          OK = True
        elif ban and not isBan(yesterday_close_price, today_current_price):
          OK = False
          break
      if OK:
        print r[0]

    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
