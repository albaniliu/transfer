#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import traceback

from xml.etree import ElementTree

execfile("/mnt/xvdb/scripts/send_mail.py")

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}
stock_count = {}
stock_high_count ={}
data_dict = {}

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
        stock_count[r[0]] = 0
        stock_high_count[r[0]] = 0.0

      cur.close()
      db_conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def fetch():
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
 
  stock_ids = yes_stock_dict.keys()
  txt = ""
  for i in range(0, len(stock_ids)):
#  for i in range(0, 1):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date,current_price,highest_price,lowest_price,open_price, yesterday_close_price from daily where stock_id = %s and date >= %s and date <= %s', [stock_id, sys.argv[1], sys.argv[2]])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    count = 0
    ok = False
    history_list = []
    for j in range(0, len(results)):
      day = results[j][0]
      today_price = float(results[j][1])
      highest_price = float(results[j][2])
      lowest_price = float(results[j][3])
      open_price = results[j][4]
      yes_price = float(results[j][5])
      if open_price < 0.1 or yes_price < 0.1:
        continue
      if not data_dict.has_key(day):
        data_dict[day] = {}
      dic = data_dict[day]
      if isBan(yes_price, open_price) or open_price / yes_price > 1.1:
        dic[stock_id] = (1.1, open_price, isBan(yes_price, today_price), highest_price)
      elif isBan(yes_price, highest_price):
        dic[stock_id] = (open_price / yes_price, open_price, isBan(yes_price, today_price), highest_price)
      else:
        dic[stock_id] = (1.0, open_price, isBan(yes_price, today_price), highest_price)
#      if not (today_price > 0) or not (open_price > 0):
#        continue
#      if (not isBan(yes_price, lowest_price) or count > 0) and isBan(yes_price, today_price):
#        count = count + 1
#        if count == 6:
#          ok = True
#          print day + " " + stock_id
#      else:
#        count = 0
#
#      if isBan(yes_price, today_price) and not isBan(yes_price, open_price):
#        history_list.append(True)
#      else:
#        history_list.append(False)
#      if len(history_list) > 2:
#        history_list.pop(0)
#      if j+1 == len(results) and isBan(yes_price, today_price) and today_price / lowest_price > 1.18:
#        txt = txt + "\n" + stock_id + " tian di ban"

  db_cur.close()
  db_conn.close()

  money = 1.0
  buy_price = 0.0
  buy_id = ''
  date_time = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
  can_buy = {}
  for i in range(0, 365):
    today = date_time + datetime.timedelta(days=i)
    today_str = today.strftime('%Y-%m-%d')
    if today.strftime('%Y-%m-%d') > sys.argv[2]:
      break
    if not data_dict.has_key(today_str):
      continue
    dic = data_dict[today_str]
    if len(buy_id) > 0:
      if dic.has_key(buy_id):
        sell_price = dic[buy_id]
        if sell_price > 0:
          money = money * sell_price[1] * 0.998 / buy_price
    buy_id = ''
    maxValue = (0.0, 0.0, False, 0.0)
    maxId = ''
    for k,v in dic.items():
      if v[0] != 1.1:
        if v[0] > maxValue[0] and can_buy.has_key(k) and can_buy[k]:
          maxId = k
          maxValue = v
      can_buy[k] = not v[2]
    buy_id = maxId
    buy_price = maxValue[3]
    print today_str + " " + maxId + " " + str(maxValue)
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
