#!/usr/bin/python

import httplib
import MySQLdb
import time
import sys

from xml.etree import ElementTree

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}

def buildDict():
  yes_stock_dict[sys.argv[1]] = 1
#  try:
#      db_conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
#      cur=db_conn.cursor()
#      cur.execute('select distinct stock_id from chuangye')
#      results = cur.fetchall()
#      for r in results:
#        yes_stock_dict[r[0]] = 1
#
#      cur.close()
#      db_conn.close()
#  except MySQLdb.Error,e:
#       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def fetch():

  quick_check_dict.clear()
  conn=httplib.HTTPConnection('stock2.finance.sina.com.cn')
#  try:
#    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
#    db_cur = db_conn.cursor()
#  except MySQLdb.Error,e:
#    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
#    exit(1)
 
  stocks = ""
  stock_ids = yes_stock_dict.keys()
  for i in range(0, len(stock_ids)):
    conn.request('GET','/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=' + stock_ids[i])
    result = conn.getresponse()
    resultStatus = result.status
    if resultStatus != 200:
      sys.stderr.write("Error sina server!\n")
      time.sleep(1)
      continue

    stock_id = stock_ids[i]
    contents = result.read()
    lst = contents.split(']')
    for r in lst:
      if len(r) < 2:
        continue
      line =  r[2:]
      line = line.replace('"', '')
      print line
#    lst_node = root.getiterator("content")
#    for node in lst_node:
#      print node

#      value = [stock_id, node.get('o'), node.get('c'), node.get('h'), node.get('l'),
#               node.get('v') + '00', node.get('d'), '15:00:00']
#      try:
#        results = db_cur.execute("insert into daily(stock_id,open_price,current_price, \
#          highest_price, lowest_price, deal_total_quantity, date, time) \
#          values(%s,%s,%s,%s,%s, \
#          %s,%s,%s)", value)
#      except MySQLdb.Error,e:
#        sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
#    db_conn.commit()
 
  conn.close()
#  db_cur.close()
#  db_conn.close()
 

if __name__ == "__main__":
  buildDict()
  last_time = "08-00"
  while last_time < "15-15":
    now_time = time.strftime("%H-%M")
    if now_time > "11-40" and now_time < "12-50":
      time.sleep(1)
      continue
    if now_time != last_time:
      last_time = now_time
      try:
        fetch()
      except Exception,e:
        sys.stderr.write("fetch error %s\n" % e)
      sys.stdout.flush()
      sys.stderr.flush()

    time.sleep(1)
