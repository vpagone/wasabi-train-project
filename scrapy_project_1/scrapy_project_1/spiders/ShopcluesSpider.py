from itertools import zip_longest
import scrapy

from scrapy_project_1.items import MyItem
from urllib.parse import urljoin

class ShopcluesSpider(scrapy.Spider):
    #name of spider
    name = 'shopclues'

    #list of allowed domains
    #allowed_domains = ['www.shopclues.com/mobiles-featured-store-4g-smartphone.html']
    #allowed_domains = ['www.chrono24.com']
    #starting url
    #start_urls = ['http://www.shopclues.com/mobiles-featured-store-4g-smartphone.html/']
    #start_urls = ['https://www.chrono24.com/rolex/index.htm']
    #start_urls = ['https://mementoitalia.com/']
    # start_urls=[
    #             'https://www.chrono24.com/',
    #             'https://www.orologicalamai.com/',
    #             'https://www.watchelegance.it/',
    #             'https://baltic-watches.com/en',
    #             'https://www.patek.com/en/',
    #             'https://www.chlw.it/',
    #             'https://www.zodiacwatches.com/en-us/',
    #             'https://www.piretti.it/',
    #             'https://www.swatch.com/it-it/',
    #             'https://ruzzaorologi.com/',
    #             ]
    #location of csv file
    
    custom_settings = {
#        'FEED_URI' : 'RISULTATI.csv',
        'ROBOTSTXT_OBEY' : False,               #IGNORA IL ROBORT.TXT
        'HTTPERROR_ALLOWED_CODES' : [403]       #IGNORA IL FORBIDDEN   
    }

    #headers = {
    #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    #   'Accept-Language': 'it-IT,it;q=0.9'
    # }

    def __init__(self, urls=None, keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []
        self.keywords = [k.lower() for k in keywords.split(',')] if keywords else []

    def parse(self, response):

        self.logger.info(f"User-Agent usato: {response.request.headers.get('User-Agent')}")

        # URL finale (dopo eventuali redirect)
        self.logger.info(f"URL di risposta: {response.url}")

        # URL originale richiesto
 #       self.logger.info(f"URL della richiesta originale: {response.request.url}")

        # Referrer (se presente)
 #       referrer = response.request.headers.get('Referer', b'Nessun referrer').decode()
 #       self.logger.info(f"Referrer: {referrer}")

        # Status code
        self.logger.info(f"Status HTTP: {response.status}")

        page_text = response.text.lower()
        if any(keyword in page_text for keyword in self.keywords):
            item=MyItem()
            item['url'] =  response.url
            item['title'] = response.css('title::text').get()
            item['meta_description'] = response.css('meta[name="description"]::attr(content)').get()
             #'URL originale richiesto': response.request.url,
            item['referer'] = response.request.headers.get('Referer', b'Nessun referrer').decode()
            yield item

            # for href in response.css('a::attr(href)').getall():
            #    yield response.follow(href, callback=self.parse)

            # for href in response.css('a::attr(href)').getall():
            #     if href and not href.startswith('#'):
            #         absolute_url = urljoin(response.url, href)
            #         yield scrapy.Request(absolute_url, callback=self.parse)
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
        else:
            self.logger.info(f"La pagina {response.url} NON contiene nel testo le parole di interesse")

        #Extract product information
#        titles = response.css('img::attr(title)').extract
#        images = response.css('img::attr(data-img)').extract()
#        prices = response.css('.p_price::text').extract()
#        discounts = response.css('.prd_discount::text').extract()

#        self.logger.info(f"Titles: {titles}")
#        self.logger.info(f"Images: {images}")
#        self.logger.info(f"Prices: {prices}")
#        self.logger.info(f"Discounts: {discounts}")

#        for item in zip_longest(titles,prices,images,discounts,fillvalue=None):
#            scraped_info = {
#                'url' : response.url,
#                'title' : item[0],
#                'price' : item[1],
#                'image_urls' : [item[2]], #Set's the url for scrapy to download images
#                'discount' : item[3]
#            }
#            yield scraped_info

        # scraped_info = {
        #     'url' : response.url
        # }

        #yield scraped_info


    # def parse_linked_page(self, response):
    #     # Estrai altri dati dalle pagine collegate
    #     yield {
    #         'url': response.url,
    #         #'heading': response.css('a::attr(href)').get(),
    #     }