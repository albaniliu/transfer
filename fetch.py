#!/usr/bin/python

import httplib
import MySQLdb
import time
import sys

execfile("/mnt/xvdb/scripts/send_mail.py")
execfile("/mnt/xvdb/scripts/base_util.py")

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}

def buildDict():
  try:
      conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
      cur=conn.cursor()
      cur.execute('select distinct stock_id from shenzhen')
      results = cur.fetchall()
      for r in results:
        yes_stock_dict[r[0]] = 1
      
      print len(yes_stock_dict)
      cur.close()
      conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == "__main__":
  buildDict()
  last_time = "08-00"
  while last_time < "15-15":
    now_time = time.strftime("%H-%M")
    if now_time > "11-40" and now_time < "12-50":
      time.sleep(1)
      continue
    if now_time != last_time:
      print now_time
      last_time = now_time
      try:
        fetch(yes_stock_dict, stock_dict, 'shenzhen', True)
      except Exception,e:
        sys.stderr.write("fetch error %s\n" % e)
      sys.stdout.flush()
      sys.stderr.flush()
      
    time.sleep(1)
