#!/usr/bin/python
#coding: utf-8

import httplib
import MySQLdb
import time
import datetime
import sys
import copy
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
from email.utils import COMMASPACE,formatdate
import traceback
 
execfile("/mnt/xvdb/scripts/send_mail.py")

today = datetime.datetime.now()
todaystr = today.strftime('%Y-%m-%d')

stock_dict = {}
quick_check_dict = {}
quick_check_dict_bak = {}

last_quantity = {}
last_minute = time.strftime("%H-%M")

def dieBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  low = yesPrice * 0.9
  return low - curPrice < 0.005 and low - curPrice > -0.006

def fetchStock(stocks):
  conn=httplib.HTTPConnection('hq.sinajs.cn')
  while True:
    conn.request('GET','/?list=' + stocks)
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
        if closed_price == 0:
          continue
  
        cur_total_quantity = long(allCol[8])
        buy1_quantity = long(allCol[10]) / 100
        buy2_quantity = long(allCol[12]) / 100
        if dieBan(closed_price, sell1_price):
#          quick_check_dict[stock_id] = 1
          quick_check_dict_bak[stock_id] = 1
          print stock_id
  
      except Exception,e:
        print traceback.format_exc()
        sys.stderr.write("fetch stock error. " + e + "\n")

    quick_check_dict = copy.deepcopy(quick_check_dict_bak)
    if len(quick_check_dict) > 20:
      sys.exit()
    break
 
  conn.close()

  

def buildDict():
  try:
    daban_file = open('/mnt/xvdb/scripts/stock_id.dat')
    count = 0
    stocks = ""
    for line in daban_file.readlines():
      line = line.strip()
      if line.startswith('sz') or line.startswith('sh'):
        count = count + 1
        stocks = stocks + line + ","
        if count % 900 == 0:
          fetchStock(stocks)
          stocks = ""
    if len(stocks) > 1:
      fetchStock(stocks)
      stocks = ""
  except Exception,e:
    print traceback.format_exc()
    sys.stderr.write("buildDict error. " + e + "\n")


def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

def quickCheck():
  global last_minute
  global quick_check_dict
  conn=httplib.HTTPConnection('hq.sinajs.cn')
  stocks = ""
  stock_ids = quick_check_dict.keys()
  cur_minute = time.strftime("%H-%M")
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
          if closed_price == 0:
            continue
    
          if cur_price < 0.001:
            cur_price = sell1_price

          cur_total_quantity = long(allCol[8])
          sell1_quantity = long(allCol[20])
          cur_time = allCol[31]

          if (cur_time < '09:25:00' and ((not dieBan(closed_price, sell1_price) or sell1_quantity > 1000000 ))) or (cur_time >= '14:57:00' and cur_time <= '15:00:00' and stock_id.startswith('sz') and sell1_quantity * 1.0 / cur_total_quantity > 0.2) or (last_quantity.has_key(stock_id) and last_quantity[stock_id] > 0 and cur_total_quantity * 1.0 / last_quantity[stock_id] > 1.1):
            subject = "dieban " + stock_id + " " + allCol[0] + " " + str((sell1_price - closed_price) * 100 / closed_price) + "%"
            txt = ""
            print subject
            sys.stdout.flush()
            last_quantity[stock_id] = cur_total_quantity
            quick_check_dict.pop(stock_id)

#            sendMail(subject, txt)
          if cur_minute != last_minute:
            #print stock_id + " " + cur_time
            last_quantity[stock_id] = cur_total_quantity
        except Exception,e:
          print traceback.format_exc()
          sys.stderr.write("send maill error. " + e + "\n")

  if cur_minute != last_minute:
    last_minute = cur_minute
#    print cur_minute + " liu"
    quick_check_dict = copy.deepcopy(quick_check_dict_bak)
#    print quick_check_dict
 
  conn.close()


if __name__ == "__main__":
  time.sleep(2)

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
    time.sleep(5)
