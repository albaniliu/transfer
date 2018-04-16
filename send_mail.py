#coding: utf-8

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
  

def sendMail(subject, body):
  sender = 'aisonliu@163.com'
  receiver = 'aisonliu@163.com'
  smtpserver = 'smtp.163.com'
  username = 'aisonliu@163.com'
  password = '312715451'

  msg = MIMEText(body,'plain','utf-8')
  msg['Subject'] = Header(subject, 'utf-8')  
  msg['To'] = receiver
  
  smtp = smtplib.SMTP()
  smtp.connect('smtp.163.com')  
  smtp.login(username, password)  
  smtp.sendmail(sender, receiver, msg.as_string())  
  smtp.quit()  
