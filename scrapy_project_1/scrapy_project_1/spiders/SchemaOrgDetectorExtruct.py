import json

import json
from scrapy.selector import Selector
from scrapy_project_1.items import MyItem

import extruct
from w3lib.html import get_base_url

class StructuredDataExtractorExtruct:
    def __init__(self, response):
        self.response = response
        #self.selector = Selector(response)
 
    def extract_json_ld(self):

        base_url = get_base_url(self.response.text, self.response.url)
        dati = extruct.extract(self.response.text, base_url=base_url)

        json_ld = dati.get('json-ld', [])
        items = []
        for jason_ld_item in json_ld:
            #print(f"microdataItem.get('@type') = {microdataItem.get('itemtype')}" )
            #print(microdata)
            if jason_ld_item.get('@type') == 'Product':

                item = MyItem()

                item['url'] =  jason_ld_item['properties']['url']
                item['title'] = jason_ld_item['properties']['title']
                item['meta_description'] =  jason_ld_item['properties']['meta_description']
                item['name'] = jason_ld_item['properties']['name']
                item['price'] = jason_ld_item['properties']['price']
                item['productID'] = jason_ld_item['properties']['productID']
                item['sku'] = jason_ld_item['properties']['sku']
                item['detected'] = 'json-ld'
                # item['properties'] = TODO
                
                items.append(item)
                print(item)
        
        return items
 
    def extract_open_graph(self):
        meta_tags = self.response.xpath('//meta[starts-with(@property, "og:")]')
        return {
            tag.xpath('@property').get(): tag.xpath('@content').get()
            for tag in meta_tags if tag.xpath('@content').get()
        }
 
    def extract_microdata(self):

        base_url = get_base_url(self.response.text, self.response.url)
        dati = extruct.extract(self.response.text, base_url=base_url)

        microdata = dati.get('microdata', [])
        items = []
        for microdataItem in microdata:
            #print(f"microdataItem.get('@type') = {microdataItem.get('itemtype')}" )
            #print(microdata)
            if microdataItem.get('@type') == 'Product':

                item = MyItem()

                item['url'] =  microdataItem['properties']['url']
                item['title'] = microdataItem['properties']['title']
                item['meta_description'] =  microdataItem['properties']['meta_description']
                item['name'] = microdataItem['properties']['name']
                item['price'] = microdataItem['properties']['price']
                item['productID'] = microdataItem['properties']['productID']
                item['sku'] = microdataItem['properties']['sku']
                item['detected'] = 'microdata'
                # item['properties'] = TODO
                
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




