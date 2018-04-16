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

today = datetime.datetime.now()
today = today - datetime.timedelta(int(sys.argv[1]))
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')
print todaystr

days = 3
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
    stock_id = stock_ids[i]

    try:
      db_cur.execute('select date,current_price,highest_price,lowest_price from daily where stock_id = %s and date <= %s order by date desc limit %s', [stock_id, todaystr, days+1])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    if len(results) < days:
      continue
    ok = True
    for j in range(1, len(results)):
      yes_price = float(results[j-1][1])
      today_price = float(results[j][1])
      lowest_price = float(results[j][3])
      if not isBan(yes_price,today_price):
        ok = False
        break
    if ok:
      yes_price = float(results[1][1])
      today_price = float(results[0][1])
      highest_price = float(results[0][2])
      if isBan(yes_price, today_price):
        print stock_id
      elif isBan(yes_price, highest_price):
        print stock_id + " mian"

  db_cur.close()
  db_conn.close()

 

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
