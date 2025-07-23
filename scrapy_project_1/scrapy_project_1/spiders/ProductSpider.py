from itertools import zip_longest
import scrapy

from scrapy_project_1.items import MyItem
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .SchemaOrgDetectorMixin import StructuredDataExtractor

class ProductSpider(scrapy.Spider):
    #name of spider
    name = 'product_detector'
    
    custom_settings = {
#        'FEED_URI' : 'RISULTATI.csv',
        'ROBOTSTXT_OBEY' : False,               #IGNORA IL ROBORT.TXT
        'HTTPERROR_ALLOWED_CODES' : [403]       #IGNORA IL FORBIDDEN   
    }

    def __init__(self, urls=None, keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []
        self.keywords = [k.lower() for k in keywords.split(',')] if keywords else []

    def parse(self, response):

        self.logger.info(f"User-Agent usato: {response.request.headers.get('User-Agent')}")

        # URL finale (dopo eventuali redirect)
        self.logger.info(f"URL di risposta: {response.url}")

        # Status code
        self.logger.info(f"Status HTTP: {response.status}")

        sd = StructuredDataExtractor(response)
        fmt, items = sd.get_best_format()
 
        self.logger.info(f"✅ Detected format: {fmt}")
 
        if fmt == 'json-ld':
            for item in items:
                # print(item['@graph'])
                # print('------------------------')
                # if item.get('@type') == 'Product':
                #     print("+++++++++++++++++++Io sono qui")
                #     yield {
                #     # myitem=MyItem()
                #     # myitem['url'] =  response.url
                #     # myitem['product'] = item.get('name')
                #     # myitem['price'] = item.get('offers', {}).get('price')
                #         'name': item.get('name'),
                #         'price': item.get('offers', {}).get('price'),
                #         'currency': item.get('offers', {}).get('priceCurrency'),
                #         'image': item.get('image')
                #     #yield myitem
                #     }
                #     nome=item.get('name')
                #     prezzo=item.get('offers', {}).get('price')
                #     sconto=item.get('offers', {}).get('priceCurrency')
                #print(response.url)
                print(item)
                myitem=MyItem()
                myitem['url'] = response.url
                myitem['product'] = item.get('name')
                myitem['url'] =  response.url
                myitem['price'] = item.get('price')
                yield myitem

        elif fmt == 'open-graph':
            yield {
                'name': data.get('og:title'),
                'image': data.get('og:image'),
                'description': data.get('og:description')
            }
 
        elif fmt == 'microdata':
            for item in data:
                if 'Product' in (item.get('itemtype') or ''):
                    yield item['properties']
 
        else:
            self.logger.warning("❌ No structured data found.")

        for href in response.css('a::attr(href)').getall():
            if not href:
                continue
            href = href.strip()
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:') or href.startswith('tel:'):
                continue
            try:
                absolute_url = urljoin(response.url, href)
                yield scrapy.Request(absolute_url, callback=self.parse)
            except ValueError:
                self.logger.warning(f"URL malformato: {href}")
