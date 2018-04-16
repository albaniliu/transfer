#!/usr/bin/python

import MySQLdb
import time
import datetime
import sys

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(1)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

def solve(table):
  try:
      conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
      cur=conn.cursor()
  
      cur.execute('select distinct stock_id from ' + table)
      results = cur.fetchall()
      for r in results:
        #print r[0]
        #print today
        count = 0
        cur.execute('select deal_total_quantity,open_price,current_price ,yesterday_close_price,lowest_price,highest_price,date,time from ' + table + ' where stock_id = %s and date >= %s and date <= %s', [r[0], sys.argv[1], sys.argv[2]])
        tmp = cur.fetchall()
        if len(tmp) < 1:
          continue
  
        buy = False
        printed = False
        txt = ''
        for j in range(0, len(tmp)):
          today_deal = long(tmp[j][0])
          open_price = float(tmp[j][1])
          current_price = float(tmp[j][2])
          yes_price = float(tmp[j][3])
          lowest_price = float(tmp[j][4])
          highest_price = float(tmp[j][5])
          date = tmp[j][6]
          time = tmp[j][7]
          if count == 0:
            if not buy and time < '10:00:00' and lowest_price > yes_price and isBan(yes_price, highest_price) and open_price < highest_price:
              buy = True
              txt = time

          if today_deal == 0:
            continue
  
          if buy and time >= '15:00:00':
            if isBan(yes_price, current_price):
              print date + " " + txt + " " + r[0] + " yes" 
            else:
              print date + " " + txt + " " + r[0] + " no"
              
            buy = False
  
          if j == len(tmp) - 1:
            continue
          next_date = tmp[j+1][6]
  
          if date == next_date:
            continue
  
          if isBan(yes_price, current_price):
          #if isBan(yes_price, current_price) and not isBan(yes_price, lowest_price):
            count = count + 1
          else:
            count = 0
  
  
  
      cur.close()
      conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#solve('shenzhen')
#solve('chuangye')
solve('shanghai')
