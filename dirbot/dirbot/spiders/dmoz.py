from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class MySpider(Spider):
    name = "77bike"
    allowed_domains = ["bbs.77bike.com"]
    start_urls = [
        "http://bbs.77bike.com/thread.php?fid=12&page=1"
    ]
    def getUrl(self):
        print self.allowed_domains[0]
        return 'http://'+self.allowed_domains[0];

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//td[@class="subject"]')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a[@class="subject_t f14"]/text()').extract()
            item['url'] = site.xpath('a[@class="subject_t f14"]/@href').extract()
            item['domain'] = self.getUrl()
            #item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items
