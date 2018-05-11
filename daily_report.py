#!/usr/bin/python

import httplib
import time
import datetime
import sys

execfile("send_mail.py")
execfile("base_util.py")

stock_dict = {}
yes_stock_dict = {}
today = datetime.datetime.now()
todaystr = today.strftime('%Y-%m-%d')
print todaystr

def fetch():

  conn=httplib.HTTPConnection('qt.gtimg.cn')
  
  idDict = {}
  
  stock_ids = ''
  highBan = 0
  ban = 0
  tiandiBan = 0
  yiBan = 0
  content = ''

  prefixes = ['sz00', 'sz30', 'sh60']
  for i in range(10000, 19051):
    for prefix in prefixes:
      stock_ids = stock_ids + prefix + str(i)[1:5] + ","
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
        allCol = kv[1].split("~")
        stock_id = kv[0].split("_")[1]
        day = allCol[30][0:4] + '-' + allCol[30][4:6] + '-' + allCol[30][6:8]
        mtime = allCol[30][8:10] + ':' + allCol[30][10:12] + ':' + allCol[30][12:14]
      
        if day != todaystr:
          continue
        yester_close_price = float(allCol[4])
        current_price = float(allCol[3])
        highest_price = float(allCol[33])
        lowest_price = float(allCol[34])
        if current_price < 0.1:
          continue
        if isBan(yester_close_price, lowest_price):
          yiBan = yiBan + 1
        elif isBan(yester_close_price, current_price):
          ban = ban + 1
        elif isBan(yester_close_price, highest_price):
          highBan = highBan + 1
  
        if isBan(yester_close_price, current_price) and current_price / lowest_price > 1.8:
          content = content + stock_id + " tian di ban\n"
          
  #      value = [stock_id,allCol[1], allCol[5], allCol[4], allCol[3],
  #               allCol[33], allCol[34], allCol[9], allCol[19], allCol[6],
  #               allCol[37], allCol[10], allCol[9], allCol[12], allCol[11],
  #               allCol[14], allCol[13], allCol[16], allCol[15], allCol[18],
  #               allCol[17], allCol[20], allCol[19], allCol[22], allCol[21],
  #               allCol[24], allCol[23], allCol[26], allCol[25], allCol[28],
  #               allCol[27], day, mtime, allCol[0]]
  #      try:
  #        results = db_cur.execute("insert into daily(stock_id,name,open_price,yesterday_close_price,current_price, \
  #          highest_price, lowest_price, buy1_price_, sell1_price_, deal_total_quantity, \
  #          deal_total_money, buy1_quantity, buy1_price, buy2_quantity, buy2_price, \
  #          buy3_quantity, buy3_price, buy4_quantity, buy4_price, buy5_quantity, \
  #          buy5_price, sell1_quantity, sell1_price, sell2_quantity, sell2_price, \
  #          sell3_quantity, sell3_price, sell4_quantity, sell4_price, sell5_quantity, \
  #          sell5_price, date, time, unknown) \
  #          values(%s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s,%s, \
  #          %s,%s,%s,%s)", value)
  #      except MySQLdb.Error,e:
  #        sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
  #    
 
  content = content + "ban: " + str(ban)
  content = content + "\nhighBan: " + str(highBan)
  content = content + "\nyiBan: " + str(yiBan)
  print(content)
#  sendMail('daily report', content)
  conn.close()
 

 
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
