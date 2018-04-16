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
#print todaystr

def isBan(yesPrice, curPrice):
  hi = curPrice + 0.01
  return abs((hi - yesPrice) / yesPrice - 0.1) > abs((curPrice - yesPrice) / yesPrice - 0.1)

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    cur=conn.cursor()
    cur.execute('select distinct date from shenzhen where (stock_id = %s or stock_id = %s) and date <= %s order by date desc limit 3', ['sz000001', 'sz000002', todaystr])
    days = list(cur.fetchall())
    cur.execute('select distinct stock_id from shenzhen')
    results = cur.fetchall()
    for r in results:
      count = 0
      for daystr in days:
        count = count + 1
        cur.execute('select lowest_price,yesterday_close_price from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], daystr[0]])
        tmp = cur.fetchall()
        if len(tmp) < 1:
          break
        lowest_price = float(tmp[0][0])
        yesterday_close_price = float(tmp[0][1])
        if lowest_price == 0 :
          break
        if not isBan(yesterday_close_price, lowest_price):
          break
        if count == 3:
          print r[0]
    
    cur.execute('select distinct stock_id from chuangye')
    results = cur.fetchall()
    for r in results:
      count = 0
      for daystr in days:
        count = count + 1
        cur.execute('select lowest_price,yesterday_close_price from chuangye where stock_id = %s and date = %s order by time desc limit 1', [r[0], daystr[0]])
        tmp = cur.fetchall()
        if len(tmp) < 1:
          break 
        lowest_price = float(tmp[0][0])
        yesterday_close_price = float(tmp[0][1])
        if lowest_price == 0 :
          break
        if not isBan(yesterday_close_price, lowest_price):
          break
        if count == 3:
          print r[0]

    cur.execute('select distinct stock_id from shanghai')
    results = cur.fetchall()
    for r in results:
      count = 0
      for daystr in days:
        count = count + 1
        cur.execute('select lowest_price,yesterday_close_price from shanghai where stock_id = %s and date = %s order by time desc limit 1', [r[0], daystr[0]])
        tmp = cur.fetchall()
        if len(tmp) < 1:
          break
        lowest_price = float(tmp[0][0])
        yesterday_close_price = float(tmp[0][1])
        if lowest_price == 0 :
          break
        if not isBan(yesterday_close_price, lowest_price):
          break
        if count == 3:
          print r[0]

    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
