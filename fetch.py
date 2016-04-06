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
        'Cookie':'_sid=04hteg0o0i8i889hfb13hbcij3',
        'Accept':'text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, image/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-application/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5',
        'User-Agent':'Mozilla/5.0 (Android; U; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/18.0',
        'x-flash-version':'18,0,0,161',
        'Connection':'Keep-Alive',
        'Cache-Control':'no-cache',
        'Referer':'app:/assets/CardMain.swf',
        'Content-Type':'application/x-www-form-urlencoded'}
    data = {'MapStageDetailId':164}
    step = str(int(time.time())*10000000000)
    for c in ['dslekktlpkin9hcv1ob974j7b1','he5aruuo4l9b1u7s4920bceau1']:
        worship_url='http://s14.anqu.mysticalcard.com/worship.php?do=Worship&v='+step+'&phpp=anqu&phpl=ZH_CN&pvc=1.7.0&pvb=2015-08-07%2013%3A44%3A02&platformtype=1'
        cookies = {'_sid':c}

        for i in [1,2,3]:
            data = {'Type':i}
            r = requests.post(worship_url,data=data ,cookies = cookies,headers=headers);
            print r.text
            case = json.loads(r.text)['status']


        sweep_url = 'http://s14.anqu.mysticalcard.com/dungeon.php?do=Sweep&v='+step+'&phpp=anqu&phpl=ZH_CN&pvc=1.7.0&pvb=2015-08-07%2013%3A44%3A02&platformtype=1'
        r = requests.post(sweep_url ,cookies = cookies,headers=headers);
        print r.text
        print c+'完成任务'
