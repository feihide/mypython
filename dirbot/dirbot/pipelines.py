#coding=utf-8
from scrapy.exceptions import DropItem

from scrapy import signals

import json
import codecs
from collections import OrderedDict
import sqlite3
import time

import pdb
import jpush as jpush

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""
    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')
        # try:
        #     conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='self_db',port=3306)
        #     self.cur=conn.cursor()
        # except MySQLdb.Error,e:
        #          print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        self.cx = sqlite3.connect("/python/db/test.db")
        self.cu=self.cx.cursor()
        # self.cu.execute("create table fetch (id integer primary key autoincrement, name varchar(200) ,url varchar(255) ,ctime integer  default 0  )")
    # put all words in lowercase
    words_to_filter = ['9100','iphone','birdy','brompton','works','cervelo','dogma','rapha','team sky','tarmac','assos','colnago','kask','supersix','super six','tikit','air','madone','zipp']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            #print unicode(item['name']).lower()
            if unicode(word) in unicode(item['name']).lower():
                if item['domain']:
                    item['url'][0] = item['domain'] +"/"+ item['url'][0]
                # line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
                # self.file.write(line)
                # insert = [null,item['name'][0],item['url'][0], time.time()];
                # self.cur.execute('insert into test values(%d,%s,%s,%d)',value)
                #pdb.set_trace()
                self.cu.execute("select * from fetch where  url=  '"+item['url'][0]+"'")
                #pdb.set_trace()
                r = self.cu.fetchone()

                if r == None:

                    #print  item['name'][0]
                    t = [item['name'][0],item['url'][0], int(time.time())];
                    self.cu.execute("insert into fetch (name,url,ctime) values (?,?,?)", t)
                    self.cx.commit()
                    _jpush = jpush.JPush('8a4d4ac5c14856cb59df9c84', '4be8bd02e575ee5d16d8b8cd')
                    push = _jpush.create_push()
                    push.audience = jpush.all_
                    # device = _jpush.create_device()
                    # device.get_aliasuser('30B414C0D1BE414C8DCEEDE3627B43A7','ios');

                    ios_msg = jpush.ios(alert="Fetch有新的数据!", badge="+1", sound="a.caf", extras={'k1':'v1'})
                    push.notification = jpush.notification(alert="fetch notify!", android= None, ios=ios_msg)
                    push.options = {"time_to_live":86400, "sendno":12345,"apns_production":False}
                    push.platform = jpush.platform("ios")
                    push.send()

                else :
                    print u'已存在';
                return item
            else:
                None
                #raise DropItem(" NOT Contains forbidden word: %s" % word)
    def spider_closed(self, spider):
                self.cx.commit()
                self.cx.close
                # conn.commit()
                # cur.close()
                # conn.close()
                #self.file.close()
