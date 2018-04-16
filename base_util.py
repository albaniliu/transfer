
def dieBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  low = yesPrice * 0.9
  return low - curPrice < 0.005 and low - curPrice > -0.006

def isBan(yesPrice, curPrice):
  if yesPrice == 0:
    return False
  hi = yesPrice * 1.1
  return curPrice - hi < 0.006 and curPrice - hi > -0.005

def diffDate(one, two):
  date_time_one = datetime.datetime.strptime(one,'%Y-%m-%d')
  date_time_two = datetime.datetime.strptime(two,'%Y-%m-%d')
  return (date_time_two - date_time_one).days

def fetch(yes_stock_dict, has_printed_dict, table_name, is_stock_db):

  conn=httplib.HTTPConnection('hq.sinajs.cn')
  
  try:
    db_conn = MySQLdb.connect(host='localhost',user='root',passwd='liuzhao2010',db='stock',port=3306)
    db_cur = db_conn.cursor()
  except MySQLdb.Error,e:
    sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
    exit(1)
 
  stocks = ""
  stock_ids = yes_stock_dict.keys()
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
      contents = result.read().split("\n")
      for content in contents:
        content = content.strip().decode('GBK').encode("utf-8")
        kv = content.split("=")
        if (len(kv) < 2):
          continue
        if len(kv[1]) < 10:
          continue
        kv[1] = kv[1].replace('"', '')
        kv[1] = kv[1].replace(';', '')
        allCol = kv[1].split(",")
        stock_id = kv[0].split("_")[2]

        if is_stock_db:
          value = [stock_id,allCol[0], allCol[1], allCol[2], allCol[3],
                   allCol[4], allCol[5], allCol[6], allCol[7], allCol[8],
                   allCol[9], allCol[10], allCol[11], allCol[12], allCol[13],
                   allCol[14], allCol[15], allCol[16], allCol[17], allCol[18],
                   allCol[19], allCol[20], allCol[21], allCol[22], allCol[23],
                   allCol[24], allCol[25], allCol[26], allCol[27], allCol[28],
                   allCol[29], allCol[30], allCol[31], allCol[32]]
          try:
            results = db_cur.execute("insert into " + table_name + "(stock_id,name,open_price,yesterday_close_price,current_price, \
              highest_price, lowest_price, buy1_price_, sell1_price_, deal_total_quantity, \
              deal_total_money, buy1_quantity, buy1_price, buy2_quantity, buy2_price, \
              buy3_quantity, buy3_price, buy4_quantity, buy4_price, buy5_quantity, \
              buy5_price, sell1_quantity, sell1_price, sell2_quantity, sell2_price, \
              sell3_quantity, sell3_price, sell4_quantity, sell4_price, sell5_quantity, \
              sell5_price, date, time, unknown) \
              values(%s,%s,%s,%s,%s, \
              %s,%s,%s,%s,%s, \
              %s,%s,%s,%s,%s, \
              %s,%s,%s,%s,%s, \
              %s,%s,%s,%s,%s, \
              %s,%s,%s,%s,%s, \
              %s,%s,%s,%s)", value)
          except MySQLdb.Error,e:
            sys.stderr.write("Mysql Error %d: %s\n" % (e.args[0], e.args[1]))
      
        try:
          closed_price = float(allCol[2])
          cur_price = float(allCol[3])
          highest_price = float(allCol[4])
          lowest_price = float(allCol[5])
          time = allCol[31]
          if closed_price == 0:
            continue

#          if (time < '10:00:00' and not has_printed_dict.has_key(stock_id) and lowest_price > 0 and cur_price > 0 and closed_price > 0 and not isBan(closed_price, lowest_price) and ( cur_price - closed_price) / closed_price > 0.07):
#            subject =  "daban " + stock_id + " " + allCol[0] + " " + str((cur_price - closed_price) * 100 / closed_price) + "%"
#            print subject
#            has_printed_dict[stock_id] = 1

        except Exception,e:
          sys.stderr.write(e + "\n")

 
  db_conn.commit()
  conn.close()
  db_cur.close()
  db_conn.close()
