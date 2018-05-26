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
stock_count = {}
stock_high_count ={}

today = datetime.datetime.now()
before = today - datetime.timedelta(100)
beforestr = before.strftime('%Y-%m-%d')

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

def buildDict():
  try:
      db_conn=MySQLdb.connect(host='localhost',user='root',passwd='LIUzhao2010!',db='stock',port=3306)
      cur=db_conn.cursor()
      cur.execute('select distinct stock_id from daily')
      results = cur.fetchall()
      for r in results:
        yes_stock_dict[r[0]] = 1
        stock_count[r[0]] = 0
        stock_high_count[r[0]] = 0

      cur.close()
      db_conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def fetch():
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='LIUzhao2010!',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
 
  stock_ids = yes_stock_dict.keys()
  for i in range(0, len(stock_ids)):
#  for i in range(0, 1):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date,current_price,highest_price,lowest_price from daily where stock_id = %s and date > %s', [stock_id, beforestr])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    for j in range(1, len(results)):
      yes_price = float(results[j-1][1])
      today_price = float(results[j][1])
      highest_price = float(results[j][2])
      lowest_price = float(results[j][3])
      if lowest_price == highest_price:
        continue 
      if isBan(yes_price,today_price):
        stock_count[stock_id] = stock_count[stock_id] + 1
      if isBan(yes_price, highest_price):
        stock_high_count[stock_id] = stock_high_count[stock_id] + 1

  db_cur.close()
  db_conn.close()

  for stock in stock_high_count.keys():
   if stock_high_count[stock] > 0:
     print stock + " " + str(stock_count[stock] * 1.0 / stock_high_count[stock]) + " " + str(stock_count[stock]) + "/" + str(stock_high_count[stock])

 

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
