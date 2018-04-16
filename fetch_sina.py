#!/usr/bin/python

import httplib
import MySQLdb
import time
import sys

def fetch():

  conn=httplib.HTTPConnection('hq.sinajs.cn')
  
  idDict = {}
  
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    exit(1)
  
  for i in range(10000, 10001):
    stock_id = "sh510300"
    conn.request('GET','/?list=' + stock_id)
    result = conn.getresponse()
    resultStatus = result.status
    if resultStatus != 200:
      print "Error sina server!"
      time.sleep(1)
      continue
    content = result.read()
    content = content.strip()
    kv = content.split("=")
    if len(kv[1]) < 10:
      continue
    idDict[i] = 1
    kv[1] = kv[1].replace('"', '')
    kv[1] = kv[1].replace(';', '')
#    print 'sz00' + str(i)[1:5] + " = " + kv[1]
    allCol = kv[1].split(",")
  
    value = [stock_id,allCol[0], allCol[1], allCol[2], allCol[3],
             allCol[4], allCol[5], allCol[6], allCol[7], allCol[8],
             allCol[9], allCol[10], allCol[11], allCol[12], allCol[13],
             allCol[14], allCol[15], allCol[16], allCol[17], allCol[18],
             allCol[19], allCol[20], allCol[21], allCol[22], allCol[23],
             allCol[24], allCol[25], allCol[26], allCol[27], allCol[28],
             allCol[29], allCol[30], allCol[31], allCol[32]]
    
    try:
      results = db_cur.execute("insert into shanghai(stock_id,name,open_price,yesterday_close_price,current_price, \
        highest_price, lowest_price, buy1_price_, sell1_price_, deal_total_quantity, \
        deal_total_money, buy1_quantity, buy1_price, buy2_quantity, buy2_price, \
        buy3_quantity, buy3_price, buy4_quantity, buy4_price, buy5_quantity, \
        buy5_price, sell1_quantity, sell1_price, sell2_quantity, sell2_price, \
        sell3_quantity, sell3_price, sell4_quantity, sell4_price, sell5_quantity, \
        sell5_price, date, time, unknown) \
        values(%s,%s,%s,%s,%s, \
        %s,%s,%s,%s,%s, \
        %s,%s,%s,%s,%s, \
        %s,%s,%s,%s,%s, \
        %s,%s,%s,%s,%s, \
        %s,%s,%s,%s,%s, \
        %s,%s,%s,%s)", value)
    except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])
  
  db_conn.commit()
  conn.close()
  db_cur.close()
  db_conn.close()
  

if __name__ == "__main__":
  last_time = "08-00"
  while last_time < "15-15":
    now_time = time.strftime("%H-%M")
    if now_time > "11-40" and now_time < "12-50":
      print now_time
      time.sleep(1)
      continue
    if now_time != last_time:
      print now_time
      last_time = now_time
      try:
        fetch()
      except:
        print "fetch error"
      sys.stdout.flush()

    time.sleep(1)
