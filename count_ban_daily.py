#!/usr/bin/python

import httplib
import MySQLdb
import time
import sys
import traceback

from xml.etree import ElementTree

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}

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
  for i in range(0, len(stock_ids)):
#  for i in range(0, 1):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date,current_price,highest_price from daily where stock_id = %s', stock_id)
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    if (stock_num.has_key(results[0][0])):
      stock_num[results[0][0]] = stock_num[results[0][0]] + 1
    else:
      stock_num[results[0][0]] = 1
    
    for j in range(1, len(results)):
      yes_price = float(results[j-1][1])
      today_price = float(results[j][1])
      highest_price = float(results[j][2])
      if isBan(yes_price,today_price):
        if (day_count.has_key(results[j][0])):
          day_count[results[j][0]] = day_count[results[j][0]] + 1
        else:
          day_count[results[j][0]] = 1
      else:
        if (not day_count.has_key(results[j][0])):
          day_count[results[j][0]] = 0

  db_cur.close()
  db_conn.close()

  num = stock_num[sorted(stock_num.keys())[0]]
  days = sorted(day_count.keys())
  for day in days:
   if stock_num.has_key(day):
     num = num + stock_num[day]
   print day + " " + str(day_count[day]) +  " " + str(num)

 

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
