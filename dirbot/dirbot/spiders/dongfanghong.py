from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class MySpider(Spider):
    name = "dongfanghong"

    allowed_domains = ["www.dongfanghong.com.cn"]
    start_urls = [
        "http://www.dongfanghong.com.cn/bbs/forum.php?mod=forumdisplay&fid=11"
    ]
    def getUrl(self):
        print self.allowed_domains[0]
        return 'http://'+self.allowed_domains[0]+'/bbs';

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//th[@class="new"]')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a[@class="s xst"]/text()').extract()
            item['url'] = site.xpath('a[@class="s xst"]/@href').extract()
            item['domain'] = self.getUrl()
            #item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            #print item
            items.append(item)

        return items
