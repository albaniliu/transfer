#!/usr/bin/python
#coding: utf-8

import httplib
import MySQLdb
import time
import sys
import copy
import smtplib  
  
num = 20
buy = False
buyDown = False
lastV = 0.0
total = 0.0
money = 1.0
mashDict = {}
first = True
count = 0.0
current = 0.0
lastDate = '0000-00-00'

mash = open(sys.argv[1])
for line in mash.readlines():
  line = line.strip()
  if line.startswith('buy') or line.startswith('sell'):
    sp = line.split(' ')
    mashDict[sp[1]] = sp[0]

for num in range(1101, 1508):
  if (num-1) % 100 < 12:
    if not first:
      if buy:
        count = count + current - lastV
        print "exchange sell:" + lastDate + "," + str(current)
        print count
      else:
        count = count - current + lastV
        print "exchange buy:" + lastDate + "," + str(current)
        print count
    for line in open('if/if' + str(num)).readlines():
      line = line.strip()
      sp = line.split(',')
      current = float(sp[4])
      if sp[0] < lastDate:
        continue
      if sp[0] == lastDate:
        lastV = current
        continue

      lastDate = sp[0]
      if mashDict.has_key(sp[0]):
        if mashDict[sp[0]].startswith('buy'):
          if not first:
            count = count + lastV - float(sp[4])
            print "buy:" + sp[0] + "," + sp[4]
            print count
          lastV = float(sp[4])
          buy = True
          first = False
        else:
          if not first:
            count = count + float(sp[4]) - lastV
            print "sell:" + sp[0] + "," + sp[4]
            print count
          lastV = float(sp[4])
          buy = False
          first = False
if buy:
  count = count + current - lastV
  print "sell:" + lastDate + "," + str(current)
else:
  count = count - current + lastV
  print "buy:" + lastDate + "," + str(current)
print "total: " +  str(count)

