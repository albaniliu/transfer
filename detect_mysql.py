#!/usr/bin/python

import MySQLdb
import time
import datetime

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='product',port=3306)
    cur=conn.cursor()
    cur.execute('select product_id, price, description from product where partner_type != 4')
    count = 0
    while True:
      result = cur.fetchone()
      if result == None:
        break
      if result[1] == '':
        print result[0] + " price is null"
      if result[2] == '':
        print result[0] + " description is null"
      count += 1
      if count % 1000 == 0:
        print count
    
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
