import json

import json
from scrapy.selector import Selector
#from ..items import MyIte  
from scrapy_project_1.items import MyItem

import extruct
from w3lib.html import get_base_url

class StructuredDataExtractor:
    def __init__(self, response):
        self.response = response
        #self.selector = Selector(response)
 
    def extract_json_ld(self):

        #print("--------------- extract_json_ld")
        scripts = self.response.xpath('//script[@type="application/ld+json"]/text()').getall()

        item_trovati = []

        for script in scripts:
            try:
                data = json.loads(script)

                # Verifica se � un grafo o un oggetto singolo
                elements = data.get('@graph', [data]) if isinstance(data, dict) else data
                
                # print("+++++++++++")
                # print(elements)
                # print("+++++++++++")

                for el in elements:
                    # print("+++++++++++")
                    # print(el)
                    # print("+++++++++++")
                    if isinstance(el, dict) and el.get('@type') == 'Product':
                        #print(type(el.get('offers')))
                        price = None
                        p = el.get('offers', {})[0].get('price')
                        hp = el.get('offers', {})[0].get('highPrice')
                        lp = el.get('offers', {})[0].get('lowPrice')
                        if p is not None:
                            price = p
                        elif hp is not None:
                            price = hp
                        else:
                            price = lp

                        item = MyItem()

                        item['url'] =  self.response.url
                        item['title'] = self.response.css('title::text').get()
                        item['meta_description'] = self.response.css('meta[name="description"]::attr(content)').get()
                        item['name'] = el.get('name'),
                        #'brand': el.get('brand', {}).get('name') if isinstance(el.get('brand'), dict) else el.get('brand'),
                        item['price'] = price
                        item['productID'] = el.get('productID')
                        item['sku'] = el.get('sku')
                        item['detected'] = 'json ld'

                        print(item)

                        item_trovati.append(item)

            except Exception:
                continue

        return item_trovati
 
    def extract_open_graph(self):
        meta_tags = self.response.xpath('//meta[starts-with(@property, "og:")]')
        return {
            tag.xpath('@property').get(): tag.xpath('@content').get()
            for tag in meta_tags if tag.xpath('@content').get()
        }
 
    # def extract_microdata(self):

    #     base_url = get_base_url(self.response.text, self.response.url)
    #     dati = extruct.extract(self.response.text, base_url=base_url)

    #     microdata = dati.get('microdata', [])
    #     items = []
    #     for microdataItem in microdata:
    #         #print(f"microdataItem.get('@type') = {microdataItem.get('itemtype')}" )
    #         #print(microdata)
    #         if microdataItem.get('@type') == 'Product':

    #             item = MyItem()

    #             item['url'] =  microdataItem['properties']['url']
    #             item['title'] = microdataItem['properties']['title']
    #             item['meta_description'] =  microdataItem['properties']['meta_description']
    #             item['name'] = microdataItem['properties']['name']
    #             item['price'] = microdataItem['properties']['price']
    #             item['productID'] = microdataItem['properties']['productID']
    #             item['sku'] = microdataItem['properties']['sku']
    #             item['detected'] = 'microdata'
                
    #             items.append(item)
    #             print(item)

    #     return items
    
    def extract_microdata(self):

        # Trova tutti i contenitori di oggetti Product
        products = self.response.xpath('//div[@itemscope and @itemtype="https://schema.org/Product"]')

        items = []
        for product in products:

                item = MyItem()

                item['url']              = product.xpath('.//*[@itemprop="url"]/@href | .//*[@itemprop="url"]/text()').get()
                item['title']            = product.xpath('.//*[@itemprop="title"]/text()').get()
                item['meta_description'] = product.xpath('.//*[@itemprop="meta_description"]/text()').get()
                item['name']             = product.xpath('.//*[@itemprop="name"]/text()').get()
                item['price']            = product.xpath('.//*[@itemprop="price"]/text()').get()
                item['sku']              = product.xpath('.//*[@itemprop="sku"]/text()').get()
                item['productID']        = product.xpath('.//*[@itemprop="productID"]/text()').get(),
                #item['brand']            = product.xpath('.//*[@itemprop="brand"]//*[@itemprop="name"]/text() | .//*[@itemprop="brand"]/text()').get()
                #item['description']      = product.xpath('.//*[@itemprop="description"]/text()').get()
                item['detected']         = 'microdata-xpath'

                items.append(item)
                print(item)

        return items
 
    def get_items(self):

        items = []

        if ( len(self.extract_json_ld()) != 0 ):
            items.extend(self.extract_json_ld())

        if ( self.extract_microdata() ):
            items.extend(self.extract_microdata())

        # microdata = self.extract_microdata()
        # if microdata:
        #     return 'microdata', microdata
        # opengraph = self.extract_open_graph()
        # if opengraph:
        #     return 'open-graph', opengraph

#        if ( len(items) == 0):
#            self.logger.info(f"url {self.response} NO items found.")

        return items

    def detect_structured_data(self):
        """Detect structured data formats in the response."""
        detected = {}

        # Schema.org - Microdata
        if self.response.xpath('//*[@itemtype[contains(., "schema.org")]]'):
            detected["schema_microdata"] = True

        # Schema.org - RDFa
        if self.response.xpath('//*[@vocab[contains(., "schema.org")]]'):
            detected["schema_rdfa"] = True

        # Schema.org - JSON-LD
        json_ld_blocks = self.response.xpath('//script[@type="application/ld+json"]/text()').getall()
        for block in json_ld_blocks:
            try:
                data = json.loads(block)
                contexts = []
                if isinstance(data, dict):
                    contexts = [data.get("@context")]
                elif isinstance(data, list):
                    contexts = [item.get("@context") for item in data if isinstance(item, dict)]
                if any("schema.org" in str(ctx) for ctx in contexts if ctx):
                    detected["schema_jsonld"] = True
                    break
            except Exception:
                continue

        # Open Graph
        if self.response.xpath('//meta[starts-with(@property, "og:")]'):
            detected["open_graph"] = True

        # Twitter Cards
        if self.response.xpath('//meta[starts-with(@name, "twitter:")]'):
            detected["twitter_card"] = True

        # Dublin Core
        if self.response.xpath('//meta[starts-with(@name, "DC.")]'):
            detected["dublin_core"] = True

        # Microformats (very heuristic)
        if self.response.xpath('//*[contains(@class, "h-card") or contains(@class, "h-entry")]'):
            detected["microformats"] = True

        return detected if detected else None


class SchemaOrgDetectorMixin:
    def detect_structured_data(self, response):
        """Detect structured data formats in the response."""
        detected = {}

        # Schema.org - Microdata
        if response.xpath('//*[@itemtype[contains(., "schema.org")]]'):
            detected["schema_microdata"] = True

        # Schema.org - RDFa
        if response.xpath('//*[@vocab[contains(., "schema.org")]]'):
            detected["schema_rdfa"] = True

        # Schema.org - JSON-LD
        json_ld_blocks = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        for block in json_ld_blocks:
            try:
                data = json.loads(block)
                contexts = []
                if isinstance(data, dict):
                    contexts = [data.get("@context")]
                elif isinstance(data, list):
                    contexts = [item.get("@context") for item in data if isinstance(item, dict)]
                if any("schema.org" in str(ctx) for ctx in contexts if ctx):
                    detected["schema_jsonld"] = True
                    break
            except Exception:
                continue

        # Open Graph
        if response.xpath('//meta[starts-with(@property, "og:")]'):
            detected["open_graph"] = True

        # Twitter Cards
        if response.xpath('//meta[starts-with(@name, "twitter:")]'):
            detected["twitter_card"] = True

        # Dublin Core
        if response.xpath('//meta[starts-with(@name, "DC.")]'):
            detected["dublin_core"] = True

        # Microformats (very heuristic)
        if response.xpath('//*[contains(@class, "h-card") or contains(@class, "h-entry")]'):
            detected["microformats"] = True

        return detected if detected else None




