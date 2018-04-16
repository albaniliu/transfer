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
  daban_file = open('/mnt/xvdb/scripts/da_ban.log')
  for line in daban_file.readlines():
    line = line.strip()
    if line.startswith('sz') or line.startswith('sh'):
      yes_stock_dict[line] = 1
      quick_check_dict[line] = 1
#      if zhen_dict.has_key(line):
#        txt = zhen_dict[line]
#        sp = txt.split(' ')
#        if len(sp) > 2:
#          real_ban = float(sp[1])
#          if real_ban < 0.79:
#            continue
#          yes_stock_dict[line] = 1
#          quick_check_dict[line] = 1
#        else:
#          continue

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
          if closed_price == 0:
            continue
    
          cur_total_quantity = long(allCol[8])
          buy1_quantity = long(allCol[10]) / 100
          buy2_quantity = long(allCol[12]) / 100

          if (cur_price > 0 and closed_price > 0 and ( cur_price - closed_price) / closed_price > 0.07):
            subject =  "daban " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
            txt = ""
            print subject
            if zhen_dict.has_key(stock_id):
              print zhen_dict[stock_id]
              txt = zhen_dict[stock_id]
            else:
              print "0"
              txt = "0"
            sys.stdout.flush()
            quick_check_dict.pop(stock_id)

            sendMail(subject, txt)
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
    time.sleep(15)
