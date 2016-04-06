from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class MySpider(Spider):
    name = "cb"

    allowed_domains = ["bbs.chinabike.net"]
    start_urls = [
        "http://bbs.chinabike.net/forum-35-1.html"
    ]
    def getUrl(self):
        print self.allowed_domains[0]
        return 'http://'+self.allowed_domains[0]+'/';

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
