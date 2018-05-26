#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys

stock_dict = {}
yes_stock_dict = {}
today = datetime.datetime.now()
todaystr = today.strftime('%Y-%m-%d')
print todaystr

def fetch():

  conn=httplib.HTTPConnection('qt.gtimg.cn')
  
  idDict = {}
  
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='LIUzhao2010!',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
  
  stock_ids = ''
  for i in range(10000, 12001):
    stock_ids = stock_ids + "sz30" + str(i)[1:5] + ","
    if i % 50 != 0:
      continue
    conn.request('GET','/?q=' + stock_ids)
    stock_ids = ''
    result = conn.getresponse()
    resultStatus = result.status
    if resultStatus != 200:
      sys.stderr.write("Error sina server!\n")
      time.sleep(1)
      continue
    contents = result.read().decode('GBK').encode("utf-8").split("\n")
    for content in contents:
      content = content.strip()
      kv = content.split("=")
      if len(kv) < 2 or len(kv[1]) < 10:
        continue
      idDict[i] = 1
      kv[1] = kv[1].replace('"', '')
      kv[1] = kv[1].replace(';', '')
  #    print 'sz00' + str(i)[1:5] + " = " + kv[1]
      allCol = kv[1].split("~")
      stock_id = kv[0].split("_")[1]
      day = allCol[30][0:4] + '-' + allCol[30][4:6] + '-' + allCol[30][6:8]
      mtime = allCol[30][8:10] + ':' + allCol[30][10:12] + ':' + allCol[30][12:14]
    
      if day != todaystr:
        continue
      value = [stock_id,allCol[1], allCol[5], allCol[4], allCol[3],
               allCol[33], allCol[34], allCol[9], allCol[19], allCol[6],
               allCol[37], allCol[10], allCol[9], allCol[12], allCol[11],
               allCol[14], allCol[13], allCol[16], allCol[15], allCol[18],
               allCol[17], allCol[20], allCol[19], allCol[22], allCol[21],
               allCol[24], allCol[23], allCol[26], allCol[25], allCol[28],
               allCol[27], day, mtime, allCol[0]]
      try:
        results = db_cur.execute("insert into daily(stock_id,name,open_price,yesterday_close_price,current_price, \
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
        sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    
 
  db_conn.commit()
  conn.close()
  db_cur.close()
  db_conn.close()
 

 
if __name__ == "__main__":
  last_time = "08-00"
  if last_time < "15-15":
    now_time = time.strftime("%H-%M")
    if now_time != last_time:
      print now_time
      last_time = now_time
      try:
        fetch()
      except Exception,e:
        sys.stderr.write("fetch error %s\n" % e)
      sys.stderr.flush()
  
    time.sleep(1)
