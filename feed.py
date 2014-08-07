import requests
import hashlib
import json,smtplib
from setting import *
body='''From: %s
To: %s
Subject:%s

%s
'''

def notify(content):
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    msg=body%(fro,to,'New feeds : '+content[0:10],content)
    smtp.sendmail(fro, to, msg) 
    smtp.close()
    print msg
def fetch(feed):
    url=feed[0]
    r=requests.get(url)
    content=r.content
    url_hex=hashlib.md5(url).hexdigest()
    hex=hashlib.md5(content).hexdigest()
    #simple code for record old content
    try:
        with open('static/'+url_hex,'r') as f:old=f.read()
        if old!=hex:return True
    except:
        return True
    with open('static/'+url_hex,'w') as f:f.write(hex)
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