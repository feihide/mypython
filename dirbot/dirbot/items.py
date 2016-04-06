from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    domain = Field()
    url = Field()
