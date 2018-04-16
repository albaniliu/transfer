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
yes_stock_dict = {}
quick_check_dict = {}

def buildDict():
  for line in sys.stdin:
    line = line.strip()
    if line.startswith('sz') or line.startswith('sh'):
      yes_stock_dict[line] = 1
      quick_check_dict[line] = 1

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

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
          sell1_price = float(allCol[7])
          buy1_price = float(allCol[6])
          if closed_price == 0:
            continue
    
          if cur_price < 0.001:
            cur_price = sell1_price

          cur_total_quantity = long(allCol[8]) / 100
          buy1_quantity = long(allCol[10]) / 100
          buy2_quantity = long(allCol[12]) / 100
          if (allCol[31] < '09:24:50' and buy1_quantity * 2 > buy2_quantity):
            subject = "yizi1 " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
            print subject
            sys.stdout.flush()
            quick_check_dict.pop(stock_id)

            txt = str(buy1_quantity) + '     ' + str(buy2_quantity)
            sendMail(subject, txt)
            continue


          if (allCol[31] < '09:24:50'  and buy1_price > 0 and closed_price > 0 and not isBan(closed_price, buy1_price)):
            subject =  "yizi2 " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
            print subject
            sys.stdout.flush()
            quick_check_dict.pop(stock_id)

            sendMail(subject, 'yizi')
            continue

          if (allCol[31] > '09:25:50'  and cur_price > 0 and closed_price > 0 and not isBan(closed_price, cur_price)):
            subject =  "yizi3 " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
            print subject
            sys.stdout.flush()
            quick_check_dict.pop(stock_id)

            sendMail(subject, 'yizi')
            continue

          if (allCol[31] > '09:31:30' and allCol[31] < '14:57:00' and cur_price > 0 and closed_price > 0 and buy1_quantity > 0 and cur_total_quantity * 2 > buy1_quantity):
            #quick_check_dict.pop(stock_id)
            if not stock_dict.has_key(stock_id):
              subject =  "yizi4 " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
              print subject
              sys.stdout.flush()
              sendMail(subject, 'yizi')
            stock_dict[stock_id] = 1

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
