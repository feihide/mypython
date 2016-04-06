#-*- coding: utf-8 -*-
#encoding=utf-8
import time
import requests
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    headers = {'Accept-Encoding':'deflate, gzip',
        #'Cookie':'_sid=he5aruuo4l9b1u7s4920bceau1',
        'Accept':'text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, image/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-application/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5',
        'User-Agent':'Mozilla/5.0 (Android; U; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/18.0',
        'x-flash-version':'18,0,0,161',
        'Connection':'Keep-Alive',
        'Cache-Control':'no-cache',
        'Referer':'app:/assets/CardMain.swf',
        'Content-Type':'application/x-www-form-urlencoded'}
    cookies = {'_sid':'dslekktlpkin9hcv1ob974j7b1'}
    data = {'MapStageDetailId':178,'isManual':0} #174
    step = str(int(time.time())*10000000000)
    worship_url='http://s14.anqu.mysticalcard.com/mapstage.php?do=EditUserMapStages&v='+step+'&phpp=anqu&phpl=ZH_CN&pvc=1.7.0&pvb=2015-08-07%2013%3A44%3A02&platformtype=1'
    r = requests.post(worship_url ,data =data,cookies = cookies,headers=headers);
    if json.loads(r.text)['status']:
        print json.loads(r.text)['data']['Win'];
    else:
        print r.text
