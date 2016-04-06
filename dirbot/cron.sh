#! /bin/sh

export PATH=$PATH:/usr/local/bin

cd /python/dirbot
nohup scrapy crawl 77bike
nohup scrapy crawl dongfanghong
nohup scrapy crawl cb
nohup scrapy crawl bh
nohup scrapy crawl ok
