import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from bs4 import BeautifulSoup


class EbayProduct(scrapy.Item):

    title = Field()
    prod_state = Field()
    price = Field()
    description = Field()
    url = Field()
    shipping_price = Field()
    shipping_day = Field()
    warranty = Field()
    num_availables = Field()
    article_num = Field()
    vendor = Field()

class EbaySpiderSpider(CrawlSpider):
    
    name = 'ebay-spider'
     # Forma de configurar el USER AGENT en scrapy
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    } 


    allowed_domains = ['www.ebay.es']
    start_urls = ["https://www.ebay.es/itm/113725810645?hash=item1a7a9627d5:g:OEAAAOSwyahgd-lz"]
    #https://www.ebay.es/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=juegatodo&_ipg=100&rt=nc
    #url = "https://www.ebay.es/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=juegatodo&_ipg=100&rt=nc"
    #one item
    #  "https://www.ebay.es/itm/265164474000?hash=item3dbd08c690:g:EOwAAOSwtGdgo51K"
            
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/itm/' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )
    
    
    def something():
        pass

    def parse(self, response):
        
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
        
        products = sel.xpath('//h3/a')
        prod_count = 0       

        item = ItemLoader(EbayProduct(), sel) # Instancio mi ITEM con el selector en donde estan los datos para llenarlo

        # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector "pregunta"
        item.add_xpath('title', '//h1[@itemprop="name"]/text()')
        item.add_xpath('prod_state ', '//div[@itemprop="itemCondition"]/text()') 
        item.add_xpath('price', '//span[@class="nontransalte"]').get_attribute("content") 
        #item.add_xpath('description', '') 
        #item.add_xpath('url', '') 
        url = response.url
        item.add_xpath('shipping', '') 
        item.add_xpath('shipping_day','')
        item.add_xpath('warranty', '') 
        item.add_xpath('num_availables','')
        item.add_xpath('article_num','')
        
        item.add_xpath('score', './/div[@class="kVNDLtqL"]/span/text()',
        MapCompose(self.quitarDolar))
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('descripcion', '//div[@class="ui_column  "]//div[@class="cPQsENeY"]//text()', # //text() nos permite obtener el texto de todos los hijos
        MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))

        prod_count += 1
        print(prod_count)

        yield item.load_item() # Hago Yield de la informacion para que se escriban los datos en el archivo