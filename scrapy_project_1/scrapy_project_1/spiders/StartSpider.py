﻿from itertools import zip_longest
import scrapy

#from items import MyItem

from urllib.parse import urljoin
#from bs4 import BeautifulSoup
#from .SchemaOrgDetectorMixin import SchemaOrgDetectorMixin
#from .SchemaOrgDetectorMixin import StructuredDataExtractor
from .SchemaOrgDetectorXPath import StructuredDataExtractorXPath
from .SchemaOrgDetectorExtruct import StructuredDataExtractorExtruct

#class DetectSpider(scrapy.Spider, SchemaOrgDetectorMixin):
class TestSpider(scrapy.Spider):
    #name of spider
    name = 'startspider'
    
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

        sd = StructuredDataExtractorXPath(response)
#        structured = sd.detect_structured_data()
#        print (f"{response.url} --- {structured} ")

        items =  sd.get_items()
        for item in items:
            yield item

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


