import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup as bs4

from scrapy.http import HtmlResponse




class EbaySpiderSpider(CrawlSpider):

    name = 'ebay-spider'
     # Forma de configurar el USER AGENT en scrapy

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }


    allowed_domains = ['www.ebay.es']
    start_urls = ["https://www.ebay.es/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=juegatodo&_ipg=100&rt=nc"]
    #https://www.ebay.es/itm/113725810645?hash=item1a7a9627d5:g:OEAAAOSwyahgd-lz
    #https://www.ebay.es/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=juegatodo&_ipg=100&rt=nc
    #url = "https://www.ebay.es/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=juegatodo&_ipg=100&rt=nc"
    #one item
    #  "https://www.ebay.es/itm/265164474000?hash=item3dbd08c690:g:EOwAAOSwtGdgo51K"

    custom_settings = {"FEEDS":{"results.json":{"format":"json"}}}


    download_delay = 0.25


    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    # rules = (
    #     Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
    #         LinkExtractor(
    #             allow=r'/itm/' # Si la URL contiene este patron, haz un requerimiento a esa URL
    #         ), follow=True, callback="parse"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    # )

    rules = (
    Rule(LinkExtractor(restrict_xpaths='//h3[@class="lvtitle"]/a'), callback='parse'),
    # Rule(LinkExtractor(restrict_xpaths="//a[@class='pagination__button pagination__next-button']"),callback='parse_tem',),
)


    # response = HtmlResponse(url=start_urls, body=body)
    # sel = Selector(response=response)

    # prod_links = sel.xpath('//h3[@class="lvtitle"]/a')
    # print("----------------------PROD Links-----",prod_links)



    def parse(self, response):

        def get_category(breadcrumbs):
            from bs4 import BeautifulSoup as bs4
            #breadcrumbs = "<li class=\"vi-VR-brumblnkLst vi-VR-brumb-hasNoPrdlnks\" id=\"vi-VR-brumb-lnkLst\">\n\t\t\t<ul role=\"list\" aria-label=\"En la categoría: \" itemscope=\"\" itemtype=\"https://schema.org/BreadcrumbList\">\n\t\t\t\t\t<li role=\"listitem\" itemprop=\"itemListElement\" itemscope=\"\" itemtype=\"https://schema.org/ListItem\" class=\"bc-w\">\n\t\t\t\t\t\t\t\t\t<a itemprop=\"item\" _sp=\"p2047675.l2706\" href=\"https://www.ebay.es/b/Consolas-y-videojuegos-/1249\" class=\"thrd\">\n\t\t\t\t\t\t\t\t\t\t<span itemprop=\"name\">Consolas y videojuegos</span>\n\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t<meta itemprop=\"position\" content=\"1\">\n\t\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t\t<li aria-hidden=\"true\">&gt;</li>\n\t\t\t\t\t\t\t\t<li role=\"listitem\" itemprop=\"itemListElement\" itemscope=\"\" itemtype=\"https://schema.org/ListItem\" class=\"bc-w\">\n\t\t\t\t\t\t\t\t\t<a itemprop=\"item\" _sp=\"p2047675.l2706\" href=\"https://www.ebay.es/b/Videojuegos-/139973\" class=\"scnd\">\n\t\t\t\t\t\t\t\t\t\t<span itemprop=\"name\">Videojuegos</span>\n\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t<meta itemprop=\"position\" content=\"2\">\n\t\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t\t<li>&gt;</li>\n\t\t\t\t\t\t<li itemprop=\"itemListElement\" itemscope=\"\" itemtype=\"https://schema.org/ListItem\" class=\"bc-w\">\n\t\t\t\t\t\t\t<a itemprop=\"item\" _sp=\"p2047675.l2644\" href=\"https://www.ebay.es/p/25031842995\" title=\"Ver más Days Gone (Sony PlayStation 4, 2019)\">\n\t\t\t\t\t\t\t\t<span itemprop=\"name\">Ver más Days Gone (Sony PlayStation 4, 2019)</span>\n\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t<meta itemprop=\"position\" content=\"1\">\n\t\t\t\t\t\t</li>\n\t\t\t\t\t</ul>\n\t\t\t</li>"
            try:
                #extract html
                breadcrumbs = response.xpath('//ul[@id="bc"]/li[4]').extract_first()
                
                #parse html
                soup = bs4(breadcrumbs, 'html.parser')
                
                #find all the links
                raw = soup.find_all('a')[-2] #-2 because it's allways the penultimate a
                link = raw.get('href')
                
                #take only text, avoid https:/....
                category_name = link.split('/')[-2] #split using '/' and take only the text of the link
                category_name = category_name.replace('-','')
                return category_name

            except Exception as e:
                print(e)
                

            
        def get_subcategory(response, category):
            ''' Assing subcat based on category, if category is phone, seek for model
            if category is games seek for platform '''
            
            #if xpath contains platform then the product
            if category == "Consolasyvideojuegos":
                subcategory = response.xpath('//td[contains(text(),"Plataforma")]/following-sibling::td[1]/span/text()').extract_first()

            elif category == "Móviles y Smartphones":
                subcategory = response.xpath('//td[contains(text(),"Modèle") or contains(text(),"Modelo") or contains(text(),"Model")]').extract_first()
            
            return subcategory


        
        def get_payment_methods(response):

            div = response.xpath('id="payDet1"')
        
        
        #################   PARSE FUNCTION   ####################

        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)

        

        #item = ItemLoader(EbayProduct(), sel) # Instancio mi ITEM con el selector en donde estan los datos para llenarlo
        # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector "pregunta"
        # item.add_xpath(' ', '//div[@itemprop="itemCondition"]/text()')
        title = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        
        #shipping_price = response.xpath('//span[@id="fshippingCost"]/span/text()').extract_first()
        shipping_price= response.xpath('//span[@class="vi-fnf-ship-txt "]/strong/text()').extract_first()

        #shipping_time = response.xpath('//span[@class="vi-acc-del-range"]/b/text()').extract_first()
        shipping_time = response.xpath('//span[@class="vi-del-ship-txt"]/strong[@class="vi-acc-del-range"]').extract()
        
        returns = response.xpath('//span[@id="vi-ret-accrd-txt"]/text()').extract_first()
        ebay_article_id = response.xpath('//div[@id="descItemNumber"]/text()').extract_first()
        prod_url = response.url
        price = response.xpath('//span[@class="notranslate"]/@content').extract_first()    
        category = get_category(response) #taking the last link in breadcrumbs
        subcategory = get_subcategory(response, category) # subcat is assigned based on category

        ebay_vendor = response.xpath('//span[@class="mbg-nw"]/text()').extract_first()
        product_state = response.xpath('//div[@id="vi-itm-cond"]/text()').extract_first()
        

        related_products = response.xpath('//li[@class="rtxt"]/parent::ul').extract_first()
        reviews = response.xpath('//div[@class="reviews"]').extract_first()
        product_sold_out_text = response.xpath('//span[contains(text(),"Este artículo está agotado")]')

        #supported_payment_methods = get_payment_methods(response)        

        yield { 'title':title,'price':price, 'shipping_time':shipping_time,
        'shipping_price':shipping_price,'returns':returns,
        'ebay_article_id':ebay_article_id,'prod_url':prod_url,
        'related_products' :related_products, 'ebay_vendor':ebay_vendor,
        'reviews': reviews, 'category':category, 'subcategory':subcategory,
        'product_state':product_state, 'product_sold_out_text':product_sold_out_text,
         }


 # item.add_xpath('warranty', '')
        # item.add_xpath('num_availables','')
        # item.add_xpath('','')

        # item.add_xpath('score', './/div[@class="kVNDLtqL"]/span/text()',
        # MapCompose(self.quitarDolar))
        # # Utilizo Map Compose con funciones anonimas
        # # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        # item.add_xpath('descripcion', '//div[@class="ui_column  "]//div[@class="cPQsENeY"]//text()', # //text() nos permite obtener el texto de todos los hijos
        # MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
