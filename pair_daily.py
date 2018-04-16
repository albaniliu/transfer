#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import traceback

from xml.etree import ElementTree

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}
day_list_dict = {}
day_count_dict = {}

def isBan(yesPrice, curPrice):
  if yesPrice > 0 and curPrice > 0:
    hi = curPrice + 0.01
    return abs((hi - yesPrice) / yesPrice - 0.1) > abs((curPrice - yesPrice) / yesPrice - 0.1)
  return False

def fetch():
  day_count = {}
  stock_num = {}
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
 
  stock_ids = yes_stock_dict.keys()
  money = 1.0
  buy = False
  last_value = 0.0
  for i in range(0, 1):
    stock_id = sys.argv[1]
    stock_id2 = sys.argv[2]
    try:
      db_cur.execute('select date, lowest_price, current_price, open_price, highest_price from daily where stock_id = %s and date >= %s and date <= %s', [stock_id, '2015-04-01', '2016-01-01'])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    lian_ban_count = 0
    for j in range(1, len(results)):
      if (results[j-1][0] == results[j][0]):
        print "error, date: " + results[j][0] + " stock: " + stock_id
        sys.exit(1)
      day = results[j][0]
      yes_price = float(results[j-1][2])
      lowest_price = float(results[j][1])
      current_price = results[j][2]
      open_price = results[j][3]
      highest_price = results[j][4]

      if buy:
        buy = False
        try:
          db_cur.execute('select date, lowest_price, current_price, open_price, highest_price from daily where stock_id = %s and date = %s', [stock_id2, day])
        except MySQLdb.Error,e:
          sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
        stock2 = db_cur.fetchall()
        if len(stock2) > 0:
          money = money * stock2[0][3] / last_value
          print day + " " + str(money)

      if isBan(yes_price,highest_price):
        if stock_id.startswith('sh'):
          try:
            db_cur.execute('select current_price, time from shanghai where stock_id = %s and date = %s and time > %s order by time', [stock_id, day, '09:26:00'])
          except MySQLdb.Error,e:
            sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
        elif stock_id.startswith('sz3'):
          try:
            db_cur.execute('select current_price, time from chuangye where stock_id = %s and date = %s and time > %s order by time', [stock_id, day, '09:26:00'])
          except MySQLdb.Error,e:
            sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
        else:
          try:
            db_cur.execute('select current_price, time from shenzhen where stock_id = %s and date = %s and time > %s order by time', [stock_id, day, '09:26:00'])
          except MySQLdb.Error,e:
            sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
        


        dailyDetail = db_cur.fetchall()
        if len(dailyDetail) < 100:
          continue
        for detail in dailyDetail:
          if isBan(yes_price, detail[0]):
            if stock_id2.startswith('sh'):
              try:
                db_cur.execute('select current_price, yesterday_close_price, time from shanghai where stock_id = %s and date = %s and time >= %s order by time', [stock_id2, day, detail[1]])
              except MySQLdb.Error,e:
                sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
            elif stock_id.startswith('sz3'):
              try:
                db_cur.execute('select current_price, yesterday_close_price, time from chuangye where stock_id = %s and date = %s and time > %s order by time', [stock_id2, day, detail[1]])
              except MySQLdb.Error,e:
                sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
            else:
              try:
                db_cur.execute('select current_price, yesterday_close_price, time from shenzhen where stock_id = %s and date = %s and time > %s order by time', [stock_id2, day, detail[1]])
              except MySQLdb.Error,e:
                sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
            stock2 = db_cur.fetchall()
            if len(stock2) < 1:
              break
            if not isBan(stock2[0][1], stock2[0][0]):
              buy = True
              last_value = stock2[0][0]
            break

  db_cur.close()
  db_conn.close()

if __name__ == "__main__":
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
