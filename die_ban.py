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

def dieBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  low = yesPrice * 0.9
  return low - curPrice < 0.005 and low - curPrice > -0.006

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price,lowest_price,sell1_quantity,sell1_price from shenzhen where stock_id = %s and date = %s and time > "09:20:00" and time < "09:25:00"', [r[0], todaystr])
      tmps = cur.fetchall()
      if len(tmps) < 1:
        continue
      today_deal_1 = long(tmps[0][0])
      today_open_price = float(tmps[0][1])
      today_current_price = float(tmps[0][2])
      yesterday_close_price = float(tmps[0][3])
      today_lowest_price = float(tmps[0][4])
      sell1_price_1 = float(tmps[0][6])
      if not dieBan(yesterday_close_price, sell1_price_1):
        continue
      for tmp in tmps:
        today_deal = long(tmp[0])
        today_open_price = float(tmp[1])
        today_current_price = float(tmp[2])
        yesterday_close_price = float(tmp[3])
        today_lowest_price = float(tmp[4])
        sell1_price = float(tmp[6])
        sell1_quantity = long(tmp[5])
        if not dieBan(yesterday_close_price, sell1_price) or sell1_quantity > 1000000:
          print r[0] 
          break
    
    cur.execute('select distinct stock_id from chuangye')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price,lowest_price,sell1_quantity,sell1_price from chuangye where stock_id = %s and date = %s and time > "09:20:00" and time < "09:25:00"', [r[0], todaystr])
      tmps = cur.fetchall()
      if len(tmps) < 1:
        continue
      today_deal_1 = long(tmps[0][0])
      today_open_price = float(tmps[0][1])
      today_current_price = float(tmps[0][2])
      yesterday_close_price = float(tmps[0][3])
      today_lowest_price = float(tmps[0][4])
      sell1_price_1 = float(tmps[0][6])
      if not dieBan(yesterday_close_price, sell1_price_1):
        continue
      for tmp in tmps:
        today_deal = long(tmp[0])
        today_open_price = float(tmp[1])
        today_current_price = float(tmp[2])
        yesterday_close_price = float(tmp[3])
        today_lowest_price = float(tmp[4])
        sell1_price = float(tmp[6])
        sell1_quantity = long(tmp[5])
        if not dieBan(yesterday_close_price, sell1_price) or sell1_quantity > 1000000:
          print r[0] 
          break

    cur.execute('select distinct stock_id from shanghai')
    results = cur.fetchall()
    for r in results:
      #print r[0]
      #print today
      cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price,lowest_price,sell1_quantity,sell1_price from shanghai where stock_id = %s and date = %s and time > "09:20:00" and time < "09:25:00"', [r[0], todaystr])
      tmps = cur.fetchall()
      if len(tmps) < 1:
        continue
      today_deal_1 = long(tmps[0][0])
      today_open_price = float(tmps[0][1])
      today_current_price = float(tmps[0][2])
      yesterday_close_price = float(tmps[0][3])
      today_lowest_price = float(tmps[0][4])
      sell1_price_1 = float(tmps[0][6])
      if not dieBan(yesterday_close_price, sell1_price_1):
        continue
      for tmp in tmps:
        today_deal = long(tmp[0])
        today_open_price = float(tmp[1])
        today_current_price = float(tmp[2])
        yesterday_close_price = float(tmp[3])
        today_lowest_price = float(tmp[4])
        sell1_price = float(tmp[6])
        sell1_quantity = long(tmp[5])
        if not dieBan(yesterday_close_price, sell1_price) or sell1_quantity > 1000000:
          print r[0] 
          break

    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
