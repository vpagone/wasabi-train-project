from itertools import zip_longest
import scrapy

from scrapy_project_1.items import MyItem
from urllib.parse import urljoin

class LoginSpider(scrapy.Spider):
    #name of spider
    name = 'login'
    
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

        if "login" in response.url or ("accedi" or "login") in response.text.lower():
            self.logger.warning("⚠️ Non sei autenticato! Sei nella pagina di login.")
        elif "logout" in response.text.lower() or "ciao" in response.text.lower():
            self.logger.info("✅ Sei autenticato correttamente.")
        else:
            self.logger.info("ℹ️ Stato di login incerto.")


        # Inserisci i nomi dei campi corretti dal form
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'email': 'admin@example.com',
                'password': 'password',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if "logout" in response.text.lower():
            self.logger.info("Login riuscito!")
            self.logger.info("Contenuto area riservata:")
            print(response.text[:500])
        else:
            self.logger.warning("Login fallito!")



