# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from collections import OrderedDict

import datetime

class ScrapyProject1Pipeline:
    def process_item(self, item, spider):
        return item

class AddScrapedDatePipeline:
    def process_item(self, item, spider):

        ordered = OrderedDict()

        current_utc_datetime = datetime.datetime.utcnow()
        ordered['scraped_date'] = current_utc_datetime.isoformat()

        ordered['url']              = item.get('url')
        ordered['title']            = str(item.get('title')).replace('\n', '')
        ordered['detected']         = item.get('detected') 
        ordered['meta_description'] = str(item.get('meta_description')).replace('\n', '')
        ordered['referer']          = item.get('referer')
        ordered['tag']              = item.get('tag')
        ordered['keyword']          = item.get('keyword')
        ordered['text']             = str(item.get('text')).replace('\n', '')
        #ordered['images'] = item.get('images')
        ordered['product'] = item.get('product')
        ordered['price'] = item.get('price')
        #ordered['discounts'] = item.get('discounts')
        ordered['properties'] = item.get('properties')

        return ordered
