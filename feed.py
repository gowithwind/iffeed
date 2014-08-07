import requests
import hashlib
import json,smtplib
import os
from setting import *
import random
body='''From: %s
To: %s
Subject:%s

%s
'''
base=os.path.join(os.path.dirname(__file__),'static/')
print base
def notify(content):
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    msg=body%(fro,to,'New feeds :%s '%random.random(),content+str(random.random()))
    smtp.sendmail(fro, to, msg) 
    smtp.close()
    print msg
def fetch(feed):
    url=feed[0]
    r=requests.get(url)
    content=r.content
    url_hex=hashlib.md5(url).hexdigest()
    new=hashlib.md5(content).hexdigest()
    #simple code for record old content
    old=''
    try:
        with open(base+url_hex,'r') as f:old=f.read()
    except:
        old=''
    if old!=new:
        with open(base+url_hex,'w') as f:f.write(new)
        return True
    else:
        return False
def list():
    r=requests.get(feed_url)
    content=r.text
    feeds=json.loads(content)
    result=[]
    for feed in feeds:
        try:
            if fetch(feed):result.append(feed[1])
        except:
            print 'error'
    if result:
        notify('\n'.join(result))
if __name__ == '__main__':
    list()
