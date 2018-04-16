#!/usr/bin/python

import MySQLdb
import time
import datetime
import sys

today = datetime.datetime.now()
today = today - datetime.timedelta(int(sys.argv[1]))
yesterday = today - datetime.timedelta(3)
before = today - datetime.timedelta(2)
todaystr = today.strftime('%Y-%m-%d')
yesterdaystr = yesterday.strftime('%Y-%m-%d')
beforestr = before.strftime('%Y-%m-%d')
print todaystr

stock_dict = {}

def buildDict():
  try:
      conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
      cur=conn.cursor()
      cur.execute('select distinct stock_id from shenzhen')
      results = cur.fetchall()
      for r in results:
        cur.execute('select stock_id,deal_total_quantity,current_price,date,time from shenzhen where stock_id = %s order by date desc, time desc limit 1', [r[0]])
        tmp = cur.fetchall()
        stock_dict[tmp[0][0]] = tmp[0][1]
    
      cur.close()
      conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def solve():
  try:
      conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='stock',port=3306)
      cur=conn.cursor()
      cur.execute('select distinct stock_id from shenzhen')
      results = cur.fetchall()
      for r in results:
        cur.execute('select deal_total_quantity,current_price from shenzhen where stock_id = %s and date = %s order by time desc limit 1', [r[0], yesterdaystr])
        ytmp = cur.fetchall()
        if len(ytmp) < 1:
          continue
        if ytmp[0][0] == 0:
          continue
        cur.execute('select stock_id, yesterday_close_price, current_price, deal_total_quantity, time from shenzhen where stock_id = %s and date = %s order by time', [r[0], todaystr])
        tmp = cur.fetchall()
        if len(tmp) < 1:
          continue
        k = len(tmp) - 1
        for i in range(17, len(tmp)-1):
          if tmp[i][1] == 0:
            continue
          if ((tmp[i][2] - tmp[i][1]) / tmp[i][1] < 0.0995):
            continue
          #if ((tmp[i][3] - tmp[i-1][3]) * 1.0 / ytmp[0][0] > 0.1 and
          #if ((tmp[i][3] - tmp[i-1][3]) * 1.0 / stock_dict[r[0]] > 0.1 and
          if ((tmp[i][3] - tmp[i-1][3]) * 1.0 / tmp[i][3] > 0.1 and
              (tmp[i][3] - tmp[i-1][3]) * 1.0 / tmp[i][3] > 0.1):
            print tmp[i][0] + " " + str(tmp[i][3] - tmp[i-1][3])
            print tmp[i+1]
    
      cur.close()
      conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == "__main__":
  buildDict()
  solve()

