import json

import json
from scrapy.selector import Selector
from scrapy_project_1.items import MyItem

class StructuredDataExtractor:
    def __init__(self, response):
        self.response = response
        #self.selector = Selector(response)
 
    def extract_json_ld(self):

        scripts = self.response.xpath('//script[@type="application/ld+json"]/text()').getall()

        item_trovati = []

        for script in scripts:
            try:
                data = json.loads(script)

                # Verifica se è un grafo o un oggetto singolo
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

                        print(item)

                        item_trovati.append(item)

            except Exception:
                continue

        return item_trovati
 
    def extract_open_graph(self):
        meta_tags = self.selector.xpath('//meta[starts-with(@property, "og:")]')
        return {
            tag.xpath('@property').get(): tag.xpath('@content').get()
            for tag in meta_tags if tag.xpath('@content').get()
        }
 
    def extract_microdata(self):
        items = []
        for tag in self.selector.xpath('//*[@itemscope]'):
            itemtype = tag.xpath('@itemtype').get()
            itemprops = tag.xpath('.//*[@itemprop]')
            props = {
                p.xpath('@itemprop').get(): p.xpath('string(.)').get()
                for p in itemprops
            }
            items.append({
                'itemtype': itemtype,
                'properties': props
            })
        return items
 
    def get_items(self):

        items = self.extract_json_ld()
        if items:
            return items

        # microdata = self.extract_microdata()
        # if microdata:
        #     return 'microdata', microdata
        # opengraph = self.extract_open_graph()
        # if opengraph:
        #     return 'open-graph', opengraph
        return []

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




