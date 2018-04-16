#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import traceback

from xml.etree import ElementTree

execfile("/mnt/xvdb/scripts/base_util.py")

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}
day_list_dict = {}
day_count_dict = {}

#today = datetime.datetime.now()
#today = today - datetime.timedelta(int(sys.argv[1]))
#yesterday = today - datetime.timedelta(1)
#before = today - datetime.timedelta(2)
#todaystr = today.strftime('%Y-%m-%d')
#yesterdaystr = yesterday.strftime('%Y-%m-%d')
#beforestr = before.strftime('%Y-%m-%d')
#print todaystr

print sys.argv[1]

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
      db_cur.execute('select date, lowest_price, current_price, open_price, highest_price from daily where stock_id = %s and date >= %s and date <= %s', [stock_id,  sys.argv[1], sys.argv[2]])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    lian_ban_count = 0
    max_lian_ban = 0
    buy = 0.0
    sell = 0.0
    ok = False
    for j in range(1, len(results) - 1):
      if (results[j-1][0] == results[j][0]):
        print "error, date: " + results[j][0] + " stock: " + stock_id
        sys.exit(1)
      day = results[j][0]
      yes_price = float(results[j-1][2])
      lowest_price = float(results[j][1])
      current_price = results[j][2]
      open_price = results[j][3]
      highest_price = results[j][4]
      tomr_price = results[j+1][3]
      if not (open_price > 0):
        continue
      if open_price > 0 and buy > 0:
        sell = current_price
        money = money * sell / buy
        buy = 0.0
        sell = 0.0
      #if dieBan(yes_price, open_price) and not dieBan(yes_price, highest_price):
      #if dieBan(yes_price, open_price) and not dieBan(yes_price, highest_price) and not day_count_dict.has_key(day):
      if dieBan(yes_price, current_price) and tomr_price > current_price:
        buy = open_price
        day_count_dict[day] = 1
        print day + " " + stock_id + " yes"

  db_cur.close()
  db_conn.close()
  print money

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
