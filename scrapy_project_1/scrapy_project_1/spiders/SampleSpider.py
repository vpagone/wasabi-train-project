from itertools import zip_longest
import scrapy

from scrapy_project_1.items import MyItem
from urllib.parse import urljoin

class SampleSpider(scrapy.Spider):
    #name of spider
    name = 'sample'
    
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

        # if "login" in response.url or ("accedi" or "login") in response.text.lower():
        #     self.logger.warning("⚠️ Non sei autenticato! Sei nella pagina di login.")
        #     yield
        # elif "logout" in response.text.lower() or "ciao" in response.text.lower():
        #     self.logger.info("✅ Sei autenticato correttamente.")
        #     yield
        # else:
        #     self.logger.info("ℹ️ Stato di login incerto.")
        #     yield

        keyword_found = False
        for parent in response.xpath('//body//*[not(self::script) and not(self::style)]'):    #per ogni livello sottostante del body della pagina response
            tag_name = parent.xpath('name()').get()                                             #prende il TAG
            texts = parent.xpath('text()').getall()                                             #tutti i text
            #print(f"Parent= {parent}" ) 
            for text in texts:                                                                  #per ogni testo
                if text and text.strip():
                    for keyword in self.keywords:                                                   #se c'è la parola chiave
                        if keyword in text.lower():
                            item=MyItem()
                            item['url'] =  response.url
                            item['title'] = response.css('title::text').get()
                            item['meta_description'] = response.css('meta[name="description"]::attr(content)').get()
                            item['referer'] = response.request.headers.get('Referer', b'Nessun referrer').decode()    #'URL originale richiesto': response.request.url
                            item['tag'] = tag_name
                            item['keyword'] = keyword
                            item['text'] = text

                            #item['images'] = response.css('img::attr(data-img)').extract()
                            #item['prices'] = response.css('.p_price::text').extract()
                            #item['discounts'] = response.css('.prd_discount::text').extract()
                            yield item

                            keyword_found = True

        if ( keyword_found ):
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

