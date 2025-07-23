import scrapy

class EcommerceSpiderByImg(scrapy.Spider):
    #name of spider
    name = 'ecommercebyimg'

    #list of allowed domains
    #allowed_domains = ['www.shopclues.com/mobiles-featured-store-4g-smartphone.html']
    #starting url
    #start_urls = ['http://www.shopclues.com/mobiles-featured-store-4g-smartphone.html/']
    #location of csv file
    custom_settings = {
        'FEED_URI' : 'tmp/ecommerce.csv'
    }
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def __init__(self, urls=None, keywords=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []
        self.keywords = [k.lower() for k in keywords.split(',')] if keywords else []

    def parse(self, response):

        print("++++++++++++++++++++++++++++++++++++++ qui")

        page_text = response.text.lower()

        # ✅ Verifica se almeno una parola chiave è presente nel testo della pagina
        if any(keyword in page_text for keyword in self.keywords):

            print("-------------------------------- qui")

            #Extract product information
            titles = response.css('img::attr(title)').extract()
            images = response.css('img::attr(data-img)').extract()
            prices = response.css('.p_price::text').extract()
            discounts = response.css('.prd_discount::text').extract()

            for item in zip(titles,prices,images,discounts):
                scraped_info = {
                    'title' : item[0],
                    'price' : item[1],
                    'image_urls' : item[2], #Set's the url for scrapy to download images
                    'discount' : item[3]
                }
                yield scraped_info

            next_page = response.css("li.next a::attr(href)").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

