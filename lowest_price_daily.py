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

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')

num_stock = 5

def buildDict():
  try:
      db_conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
      cur=db_conn.cursor()
      cur.execute('select distinct stock_id  from daily where stock_id like "s%"')
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
  
  print sys.argv[1]
  sys.stdout.flush()
  sys.stderr.flush()
  date_time = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
  stock_ids = yes_stock_dict.keys()
  start_money = 1000000.0
  start_shangzhen = 0.0
  money = start_money
  stock_map = {}
  all_stock_map = {}
  stock_price_map = {}
  stock_number_map = {}
  last_month = '0'
  for i in range(0, 365 * 18 + 5):
    date_time = date_time + datetime.timedelta(days=1)
    buy = 0.0
    need_buy = False
    sell = 0.0
    if date_time.strftime('%m') == last_month or int(date_time.strftime('%m')) % 2 == 1:
      continue

    try:
      db_cur.execute('select date,stock_id, current_price, open_price from daily where date = %s order by current_price', [date_time.strftime('%Y-%m-%d')])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    lian_ban_count = 0
    stock_map.clear()
    for j in range(0, len(results)):
      if (j > 0 and results[j-1][1] == results[j][1]):
        print "error, date: " + results[j][0] + " stock: " + stock_id
        sys.exit(1)
      stock_id = results[j][1]
      if not (stock_id.startswith('sh6') or stock_id.startswith('sz3') or stock_id.startswith('sz0') or stock_id == 'sh000001'):
        continue
      current_price = results[j][2]
      open_price = results[j][3]
      
      if open_price == 0.0:
        continue

      if date_time.strftime('%m') != last_month and len(stock_map) < num_stock:
        stock_map[stock_id] = open_price
      all_stock_map[stock_id] = open_price
        
    if len(stock_map) == num_stock:
#      print date_time.strftime('%Y-%m-%d')
      last_month = date_time.strftime('%m')
#      money = money + 5000
      for st_id in stock_price_map.keys():
         #if not stock_map.has_key(st_id):
           money = money + all_stock_map[st_id] * stock_number_map[st_id] * 1.0
           del stock_price_map[st_id]
           del stock_number_map[st_id]
#           print st_id
      for st_id in stock_map.keys():
         if not stock_price_map.has_key(st_id):
           div = len(stock_map) - len(stock_price_map)
           if div == 0:
             print len(stock_price_map)
             break
           stock_price_map[st_id] = stock_map[st_id]
           stock_number_map[st_id] = int(money / div / stock_map[st_id] / 100) * 100
           money = money - stock_number_map[st_id] * stock_price_map[st_id]
      res = money
      for st_id in stock_price_map.keys():
        res = res + all_stock_map[st_id] * stock_number_map[st_id]
#      if start_shangzhen == 0.0:
#        start_shangzhen = all_stock_map['sh000001']
      print date_time.strftime('%Y-%m-%d') + " " + str(res / start_money)
#        + " " + str(all_stock_map['sh000001'] / start_shangzhen)
      sys.stdout.flush()
      sys.stderr.flush()


  db_cur.close()
  db_conn.close()

if __name__ == "__main__":
#  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
