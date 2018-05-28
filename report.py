#!/usr/bin/python

import httplib
import MySQLdb
import time
import datetime
import sys
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
from email.utils import COMMASPACE,formatdate
import traceback

from xml.etree import ElementTree

execfile("./send_mail.py")
execfile("./base_util.py")

stock_dict = {}
yes_stock_dict = {}
quick_check_dict = {}
stock_count = {}
stock_high_count ={}

today = datetime.datetime.now()
if len(sys.argv) > 1:
  today = today - datetime.timedelta(int(sys.argv[1]))
todaystr = today.strftime('%Y-%m-%d')
before = today - datetime.timedelta(90)
beforestr = before.strftime('%Y-%m-%d')
print todaystr


def buildDict():
  try:
      db_conn=MySQLdb.connect(host='localhost',user='root',passwd='LIUzhao2010!',db='stock',port=3306)
      cur=db_conn.cursor()
      cur.execute('select distinct stock_id from daily where date = %s', [todaystr])
      results = cur.fetchall()
      for r in results:
        yes_stock_dict[r[0]] = 1
        stock_count[r[0]] = 0
        stock_high_count[r[0]] = 0

      cur.close()
      db_conn.close()
  except MySQLdb.Error,e:
       print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def fetch():
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='LIUzhao2010!',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
 
  stock_ids = yes_stock_dict.keys()
  total_num = 0
  ban_num = 0
  high_ban_num = 0
  low_ban_num = 0
  die_ban_num = 0
  low_die_ban_num = 0

  yi_zi_file = open('./yi_zi.log', 'w')
  for i in range(0, len(stock_ids)):
    stock_id = stock_ids[i]
    try:
      db_cur.execute('select date,current_price,highest_price,lowest_price,yesterday_close_price,deal_total_quantity from daily where stock_id = %s and date = %s order by time desc limit 1', [stock_id, todaystr])
    except MySQLdb.Error,e:
      sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    results = db_cur.fetchall()
    
    if not results[0][5] > 0 :
      continue
    total_num = total_num + 1
    today_price = float(results[0][1])
    highest_price = float(results[0][2])
    lowest_price = float(results[0][3])
    yes_price = float(results[0][4])
    if isBan(yes_price,today_price):
      ban_num = ban_num + 1
    if dieBan(yes_price, today_price):
      die_ban_num = die_ban_num + 1
    if isBan(yes_price,highest_price):
      high_ban_num = high_ban_num + 1
    if isBan(yes_price,lowest_price):
      low_ban_num = low_ban_num + 1
      yi_zi_file.write(stock_id + '\n')
    if dieBan(yes_price,lowest_price):
      low_die_ban_num = low_die_ban_num + 1

  db_cur.close()
  db_conn.close()

  subject = "daily report"
  txt = "total num: " + str(total_num) + "\n"
  txt = txt + "zhang ting: " + str(ban_num - low_ban_num) + "\n"
  txt = txt + "high zhang ting: " + str(high_ban_num - ban_num) + "\n"
  txt = txt + "low zhang ting: " + str(low_ban_num) + "\n"
  txt = txt + "die ting: " + str(die_ban_num) + "\n"
  txt = txt + "low die ting: " + str(low_die_ban_num) + "\n"

  daban_file = open('./da_ban.log')
  txt = txt + "da ban: " + str(len(daban_file.readlines())) + "\n"
  
  # yiban log
  txt = txt + "==================\nyi ban log:\n"
  yiban_log_file = open('./log/fetch_yiban_' + todaystr)
  for line in yiban_log_file.readlines():
    line = line.strip()
    if line.find('%') > 0:
      txt = txt + line + '\n'
  print txt

  sendMail(subject, txt)
  yi_zi_file.close()
  daban_file.close()
  yiban_log_file.close()
 

if __name__ == "__main__":
  buildDict()
  try:
    fetch()
  except Exception,e:
    sys.stderr.write("fetch error %s\n" % e)
    traceback.print_exc()
  sys.stdout.flush()
  sys.stderr.flush()
