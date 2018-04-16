#!/usr/bin/python
#coding: utf-8

import httplib
import MySQLdb
import time
import sys
import copy
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
import traceback
 

stock_dict = {}
quick_check_dict = {}

sender = 'aisonliu@163.com'
receiver = '65745070@qq.com'
subject = 'python email'
smtpserver = 'smtp.163.com'
username = 'aisonliu@163.com'
password = '312715451'


def buildDict():
  for line in sys.stdin:
    line = line.strip()
    sp = line.split(',')
    for stock in sp:
      quick_check_dict[stock] = line

def isBan(yesPrice, curPrice):
  hi = curPrice + 0.01
  return abs((hi - yesPrice) / yesPrice - 0.1) > abs((curPrice - yesPrice) / yesPrice - 0.1) and (curPrice - yesPrice) / yesPrice > 0.09

def quickCheck():
  conn=httplib.HTTPConnection('hq.sinajs.cn')
  stocks = ""
  stock_ids = quick_check_dict.keys()
  for i in range(0, len(stock_ids)):
    stocks = stocks + stock_ids[i] + ","
    if (i+1) % 900 == 0 or i == len(stock_ids) - 1:
      conn.request('GET','/?list=' + stocks)
      stocks = ""
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
        if (len(kv) < 2):
          continue
        if len(kv[1]) < 10:
          continue
        kv[1] = kv[1].replace('"', '')
        kv[1] = kv[1].replace(';', '')
        allCol = kv[1].split(",")
        stock_id = kv[0].split("_")[2]

        try:
          closed_price = float(allCol[2])
          cur_price = float(allCol[3])
          if closed_price == 0:
            continue
    
          cur_total_quantity = long(allCol[8])
          buy1_quantity = long(allCol[10]) / 100
          buy2_quantity = long(allCol[12]) / 100

          if (cur_price > 0 and closed_price > 0 and isBan(closed_price, cur_price)):
            subject =  stock_id + " " + allCol[0] + " " + quick_check_dict[stock_id]
            print subject
            sys.stdout.flush()
            quick_check_dict.pop(stock_id)

#            smtp = smtplib.SMTP()
#            smtp.connect('smtp.163.com')
#            smtp.login(username, password)
#            msg = MIMEText(subject,'plain','utf-8')
#            msg['Subject'] = Header(subject, 'utf-8')
#            msg['To'] = receiver
#            smtp.sendmail(sender, receiver, msg.as_string())
#            smtp.quit()
        except Exception,e:
          print traceback.format_exc()
          sys.stderr.write("send maill error. " + e + "\n")
 
  conn.close()


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
      sys.stdout.flush()
      sys.stderr.flush()
    try:  
      quickCheck()
    except Exception,e:
      sys.stderr.write("quick Check error %s\n" % e)
    time.sleep(3)
