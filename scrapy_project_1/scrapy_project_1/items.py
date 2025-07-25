# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyProject1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    meta_description=scrapy.Field()
    referer=scrapy.Field()
    scraped_date=scrapy.Field()
    tag=scrapy.Field()
    keyword=scrapy.Field()
    text=scrapy.Field()
    images=scrapy.Field()
    price=scrapy.Field()
    discounts=scrapy.Field()
    detected=scrapy.Field()
    product=scrapy.Field()
    name=scrapy.Field()
    productID=scrapy.Field()
    sku=scrapy.Field()
    properties=scrapy.Field()
