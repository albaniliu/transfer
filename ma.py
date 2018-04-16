#!/usr/bin/python
#coding: utf-8

import httplib
import MySQLdb
import time
import sys
import copy
import smtplib  
  
lst = []
num = 20
buy = False
lastV = 0.0
total = 0.0
money = 10000.0

for line in sys.stdin:
  line = line.strip()
  if len(lst) == num:
    count = 0.0
    s = 0.0
    for l in lst:
      sp = l.split(',')
      count = count + float(sp[4])
    avg = count / num
    for l in lst:
      sp = l.split(',')
      s = s + pow(float(sp[4]) - avg, 2)
    s = s / num
    sp = line.split(',')
    if not buy:
      if float(sp[4]) > avg:
        buy = True
        lastV = float(sp[4])
        print "buy:" + sp[0] + "," + sp[4] + "," + str(s)
    else:
      if float(sp[4]) < avg:
        buy = False
        money = money * float(sp[4]) / lastV
        total = total + float(sp[4]) - lastV
        print "sell:" + sp[0] + "," + sp[4] + "," + str(s)
        print money
    lst.pop(0)
  lst.append(line)
print total
