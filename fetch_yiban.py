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
zhen_dict = {}


def buildDict():
  zhen_file = open('/mnt/xvdb/scripts/zhen.log')
  for line in zhen_file.readlines():
    line = line.strip()
    sp = line.split(' ')
    zhen_dict[sp[0]] = line
  try:
    daban_file = open('/mnt/xvdb/scripts/stock_id.dat')
    count = 0
    stocks = ""
    for line in daban_file.readlines():
      line = line.strip()
      if line.startswith('sz') or line.startswith('sh'):
        quick_check_dict['s_' + line] = 1
    print len(quick_check_dict)
    yes_file = open('/mnt/xvdb/scripts/stock_id.yes')
    count = 0
    stocks = ""
    for line in yes_file.readlines():
      line = line.strip()
      if line.startswith('sz') or line.startswith('sh'):
        sp = line.split(",")
        if int(sp[1]) == 1:
          stock_dict[sp[0]] = 1
    print len(stock_dict)
  except Exception,e:
    print traceback.format_exc()
    sys.stderr.write("buildDict error. " + e + "\n")

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
          #closed_price = float(allCol[4])
          cur_price = float(allCol[3])
          #highest_price = float(allCol[33])
          #lowest_price = float(allCol[34])
          zhang = float(allCol[5])
          if cur_price <= 0:
            continue
          yes_stock_dict[stock_id] = 1
#          if (cur_price > 0 and closed_price > 0 and lowest_price > closed_price and not isBan(closed_price, lowest_price) and ( highest_price - closed_price) / closed_price > 0.07):
          if zhang > 7:
            subject = stock_id[2:] + " " + allCol[1] + " " + str(zhang) + "%"
            #subject = stock_id[2:] + " " + allCol[1]
#            txt = ""
            if not stock_dict.has_key(stock_id):
              subject = subject + " NO"
            print subject
            if zhen_dict.has_key(stock_id):
              print zhen_dict[stock_id]
#              txt = zhen_dict[stock_id]
            else:
              print "-1"
#              txt = "-1"
            sys.stdout.flush()
            sys.stderr.flush()
            quick_check_dict.pop('s_' + stock_id)

#            sendMail(subject, txt)
        except Exception,e:
          print traceback.format_exc()
          sys.stderr.write("send maill error. " + e + "\n")
 
  conn.close()


if __name__ == "__main__":
  buildDict()

  last_time = "08-00"
  while last_time < "10-01":
    now_time = time.strftime("%H-%M")
    if now_time != last_time:
      print now_time
      last_time = now_time
      sys.stdout.flush()
      sys.stderr.flush()
    try:  
      quickCheck()
    except Exception,e:
      sys.stderr.write("quick Check error %s\n" % e)
    time.sleep(20)

  f = open('/mnt/xvdb/scripts/stock_id.yes', 'w')
  for key,value in yes_stock_dict.items():
    f.write(key + "," + str(value) + "\n")
