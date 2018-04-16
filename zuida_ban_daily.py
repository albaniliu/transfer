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

def transferDay(strDay):
  sp = strDay.split('-')
  return datetime.date(int(sp[0]), int(sp[1]), int(sp[2]))

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
  startDay = transferDay(sys.argv[1])
  endDay = transferDay(sys.argv[2])
   
  while startDay <= endDay:
    startDay = startDay + datetime.timedelta(days = 1)
    try:
      db_cur.execute('select date, lowest_price, current_price, open_price, highest_price, stock_id, yesterday_close_price from daily where date = %s', [startDay])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    if len(results) == 0:
      continue
    curResult = results[0]
    maxGap = 0.0
    
    lian_ban_count = 0
    max_lian_ban = 0
    buy = 0.0
    sell = 0.0
    yes_price = 0.0
    ok = False
    nxt = False
    buy_day = ""
    for j in range(0, len(results)):
      day = results[j][0]
      lowest_price = float(results[j][1])
      current_price = results[j][2]
      open_price = results[j][3]
      highest_price = results[j][4]
      stock_id = results[j][5]
      yes_price = results[j][6]

      if not current_price > 0:
        continue

#      if buy > 0 and not ok and open_price > 0:
#        sell = open_price
#        money = money * 0.998 * sell / buy
#        buy = 0.0
#        sell = 0.0
#        print money
#
#      if ok and buy < 0.1:
#        buy = open_price
#        ok = False
#        buy_day = day
#      if nxt and isBan(yes_price, current_price):
#        ok = True
##        print day + " " + stock_id
#      else:
#        ok = False
#
#      nxt = False
#      
      #if open_price == lowest_price and isBan(yes_price, current_price) and dieBan(yes_price, open_price):
      if isBan(yes_price, current_price) and current_price / lowest_price > maxGap:
        maxGap = current_price / lowest_price
        curResult = results[j]
        nxt = True
        ok = True

    if maxGap > 0:
      day = results[j][0]
      lowest_price = float(curResult[1])
      current_price = curResult[2]
      open_price = curResult[3]
      highest_price = curResult[4]
      stock_id = curResult[5]
      yes_price = curResult[6]
      print(day + " " + stock_id)




  db_cur.close()
  db_conn.close()
#  print money

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
