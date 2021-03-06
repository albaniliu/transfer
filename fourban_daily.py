#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import traceback

from xml.etree import ElementTree

execfile("./send_mail.py")

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}
stock_count = {}
stock_high_count ={}

today = datetime.datetime.now()
before = today - datetime.timedelta(int(sys.argv[1]))
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
        stock_high_count[r[0]] = 0.0

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
  txt = ""
  for i in range(0, len(stock_ids)):
#  for i in range(0, 1):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date,current_price,highest_price,lowest_price,open_price,yesterday_close_price from daily where stock_id = %s and date > %s', [stock_id, beforestr])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    count = 0
    ok = False
    history_list = []
    for j in range(0, len(results)):
      yes_price = float(results[j][5])
      today_price = float(results[j][1])
      highest_price = float(results[j][2])
      lowest_price = float(results[j][3])
      open_price = results[j][4]
      day = results[j][0]
      if not (today_price > 0) or not (open_price > 0):
        continue
      if (not isBan(yes_price, lowest_price) or count > 0) and isBan(yes_price, today_price):
        count = count + 1
#        if ok and count < 4:
#          ok = False
        if count == 3:
          ok = True
          #print day + " " + stock_id
      else:
        count = 0

      if isBan(yes_price, today_price) and not isBan(yes_price, open_price):
        history_list.append(True)
      else:
        history_list.append(False)
      if len(history_list) > 2:
        history_list.pop(0)
      if j+1 == len(results) and isBan(yes_price, today_price) and today_price / lowest_price > 1.18:
        txt = txt + "\n" + stock_id + " tian di ban"
    if ok or count == 2:
      print stock_id
      if count == 2:
        txt = txt + "\n" + stock_id
      if count == 4:
        txt = txt + "\n" + stock_id + " 4 ban"
    #elif len(history_list) == 2 and history_list[0] and not history_list[1]:
    #  print 'a'
    #  print stock_id

  db_cur.close()
  db_conn.close()
  sendMail("2 ban report", txt)

 

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
