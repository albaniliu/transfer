#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import traceback

from xml.etree import ElementTree

stock_date = {}
date_stock = {}
yes_stock_dict = {}

def isBan(yesPrice, curPrice):
  if yesPrice > 0 and curPrice > 0:
    hi = curPrice + 0.01
    return abs((hi - yesPrice) / yesPrice - 0.1) > abs((curPrice - yesPrice) / yesPrice - 0.1)
  return False

def buildDict():
  try:
      db_conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
      cur=db_conn.cursor()
      cur.execute('select distinct stock_id from daily')
      results = cur.fetchall()
      for r in results:
        yes_stock_dict[r[0]] = 1

      cur.close()
      db_conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

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
  for i in range(0, len(stock_ids)):
#  for i in range(1000, 1001):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date, lowest_price, current_price, open_price, highest_price from daily where stock_id = %s and date >= %s and date <= %s', [stock_id, '2015-01-01', '2016-01-01'])
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
      if isBan(yes_price,current_price) and not isBan(yes_price, lowest_price):
        if not stock_date.has_key(stock_id):
          l = []
          stock_date[stock_id] = l
        stock_date[stock_id].append(day)
        if not date_stock.has_key(day):
          l = []
          date_stock[day] = l
        date_stock[day].append(stock_id)
          

  db_cur.close()
  db_conn.close()

  stocks = sorted(stock_date.keys())
  for stock_id in stocks:
    if len(stock_date[stock_id]) < 5:
      continue
    stock_count = {}
    for day in stock_date[stock_id]:
      ss = date_stock[day]
      for nstock_id in ss:
        if nstock_id != stock_id:
          if stock_count.has_key(nstock_id):
            stock_count[nstock_id] = stock_count[nstock_id] + 1
          else:
            stock_count[nstock_id] = 1
    maxNum = 0
    maxStock = ''
    for stock in stock_count:
      if stock_count[stock] > maxNum:
        maxNum = stock_count[stock]
        maxStock = stock
    if maxNum * 1.0 / len(stock_date[stock_id]) > 0.8:
      print stock_id + ": " + str(len(stock_date[stock_id]))
      print maxStock + ": " + str(maxNum)
      print ""

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
