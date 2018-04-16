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

numDay = 20

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
 
  stock_id = sys.argv[1]
  try:
    db_cur.execute('select date, lowest_price, current_price, open_price, highest_price from daily where stock_id = %s', [stock_id])
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
  results = db_cur.fetchall()
  
  buy = False
  money = 1.0
  lastValue = 0.0
  for j in range(numDay, len(results)):
    if (results[j-1][0] == results[j][0]):
      print "error, date: " + results[j-k][0] + " stock: " + stock_id
      sys.exit(1)
    total = 0.0
    for k in range(0,numDay):
      total = total + results[j-k][2]
    avg = total / numDay
    if j == len(results) - 1:
      print "avg: " + str(avg)
    current_price = results[j][2]
    if not buy:
      if current_price > avg:
        buy = True
        lastValue = current_price
        print "buy: " + results[j][0] + " " + str(current_price)
    else:
      if current_price < avg:
        buy = False
        money = money * current_price / lastValue
        print "sell: " + results[j][0] + " " + str(current_price)
        print money

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
