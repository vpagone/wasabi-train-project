import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class GenericSpiderOld(scrapy.Spider):
    name = "generic_spider_old"

    def __init__(self, urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []

    def parse(self, response):
        yield {
            'url': response.url,
            'titolo': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get()
        }

class GenericSpider(scrapy.Spider):
    name = "generic_spider"

    def __init__(self, urls=None, keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []
        self.keywords = [k.lower() for k in keywords.split(',')] if keywords else []

  
    def parseOld(self, response):
        page_text = response.text.lower()

        # ✅ Verifica se almeno una parola chiave è presente nel testo della pagina
        if any(keyword in page_text for keyword in self.keywords):
            yield {
                'url': response.url,
                'titolo': response.css('title::text').get(),
                'meta_description': response.css('meta[name="description"]::attr(content)').get()
            }
            # 🔄 Continua a seguire i link
            for href in response.css('a::attr(href)').getall():
                r = response.follow(href, callback=self.parse)
                if ( r is not None ):
                    yield r
        else:
            self.mylogger.info(f"❌ Esclusa (no match): {response.url}")
            yield None

    def parse(self, response):
            author_page_links = response.css(".author + a")
            yield from response.follow_all(author_page_links, self.parse_author)

            pagination_links = response.css("li.next a")
            yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),



        }



#def run_spider(urls,keywords):
#    process = CrawlerProcess(get_project_settings())
#    process.crawl(GenericSpider, urls=urls, keywords=keywords)
#    process.start()
 