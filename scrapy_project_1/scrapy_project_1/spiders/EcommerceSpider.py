from itertools import zip_longest
import scrapy

from scrapy_project_1.items import MyItem
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class EcommerceSpider(scrapy.Spider):
    #name of spider
    name = 'ecommerce'
    
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

        for prodotto in response.xpath("//div[.//*[contains(text(), '€')]  or contains(text(), '$') or contains(text(), 'EUR') ]"):
            testo = " ".join(prodotto.xpath(".//text()").getall()).strip()
            print(testo)
            item=MyItem()
            item['url'] =  response.url
            item['text'] = testo
            yield item

        # for product in response.xpath("//div[contains(@class, 'product')]"):
        #     # Estrarre prezzo da ciascun blocco
        #     price = product.xpath(".//*[contains(text(), '€') or contains(text(), '$') or contains(text(), 'EUR')]/text()").get()
        #     #print(price)
        #     item=MyItem()
        #     item['url'] =  response.url
        #     #item['title'] = response.css('title::text').get()
        #     #item['title'] = product.xpath(".//*[contains(text(), 'title']/text()")
        #     #item['meta_description'] = response.css('meta[name="description"]::attr(content)').get()
        #     item['product'] = 'non lo so'
        #     item['price'] = price
        #     item['text'] = product.xpath(".//text()")
        #     yield item


        # keyword_found = False
        # if not any(p in response.text.lower() for p in ["prezzo", "price", "€", "$"]) :
        #     self.logger.info(f"La pagina {response.url} NON contiene nel testo le parole di interesse")
        #     yield

        # item=MyItem()
        # item['url'] =  response.url
        # item['title'] = response.css('title::text').get()
        # item['meta_description'] = response.css('meta[name="description"]::attr(content)').get()
          
        # soup = BeautifulSoup(response.text, 'html.parser')
        # testo = soup.get_text()
        # if any(p in testo for p in ["prezzo", "price", "€", "$"]) :
        #     item['text'] = testo
        #     yield item

        # keyword_found = True

        # if ( keyword_found ):
        #     for href in response.css('a::attr(href)').getall():
        #         if not href:
        #             continue
        #         href = href.strip()
        #         if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:') or href.startswith('tel:'):
        #             continue
        #         try:
        #             absolute_url = urljoin(response.url, href)
        #             yield scrapy.Request(absolute_url, callback=self.parse)
        #         except ValueError:
        #             self.logger.warning(f"URL malformato: {href}")
        # else:
        #      self.logger.info(f"La pagina {response.url} NON contiene nel testo le parole di interesse")

