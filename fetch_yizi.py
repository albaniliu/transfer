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
from email.utils import COMMASPACE,formatdate
import traceback
 

execfile("/mnt/xvdb/scripts/send_mail.py")

stock_dict = {}
quick_check_dict = {}

def buildDict():
  for line in sys.stdin:
    line = line.strip()
    if line.startswith('sz') or line.startswith('sh'):
      quick_check_dict['s_' + line] = 1

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

def quickCheck():
  conn=httplib.HTTPConnection('qt.gtimg.cn')
  stocks = ""
  stock_ids = quick_check_dict.keys()
  for i in range(0, len(stock_ids)):
    stocks = stocks + stock_ids[i] + ","
    if (i+1) % 60 == 0 or i == len(stock_ids) - 1:
      conn.request('GET','/?q=' + stocks)
      stocks = ""
      result = conn.getresponse()
      resultStatus = result.status
      if resultStatus != 200:
        sys.stderr.write("Error tencent server!\n")
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
        allCol = kv[1].split("~")
        stock_id = kv[0].split("_")[2]

        try:
          cur_price = float(allCol[3])
          zhang = float(allCol[5])
          if cur_price <= 0:
            continue

          cur_total_quantity = long(allCol[6])

          if (zhang < 9.5):
            quick_check_dict.pop('s_' + stock_id)
            subject =  stock_id[2:] + " " + allCol[1] + " " + str(zhang) + "%"
            print subject
            sys.stdout.flush()
            sendMail(subject, 'yizi')
            continue
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
    time.sleep(10)
