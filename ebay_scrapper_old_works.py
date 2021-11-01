import scrapy
import csv
from scrapy.http.request import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup as bs4

#for my_print()
from colorama import init
from termcolor import colored
init()

from scrapy.http import HtmlResponse

#these are used  in get_queries() and get_query()
first_chunk = 'https://www.ebay.es/sch/i.html?_from=R40&_nkw='
last_chunk = '&_sacat=0&rt=nc&LH_BIN=1'

def my_print(text, color='green', mode='normal',**id):
    ''' red,green,yellow,blue // mode="lines" to print a list line by line in BLUE"'''
    
    if mode == 'normal':
        if color == 'red':
            print(colored(id, 'white','on_red'))
            print(colored(text, 'white','on_red'))        

        elif color == 'green':
            print(colored(id, 'white','on_green'),sep="\n")
            print(colored(text, 'white','on_green'),sep="\n")

        elif color == 'yellow':
            print(colored(id, 'blue','on_yellow'))
            print(colored(text, 'blue','on_yellow'))

        elif color == 'blue':
            print(colored(id, 'white','on_blue'))
            print(colored(text, 'white','on_blue'))

    elif mode=='lines':
        
        for item in text:
            print(colored(item, 'white','on_blue'))

def get_queries():
    """this takes a file named queries.csv and creates url's to search
    by the scrapper"""
    import csv

    all_queries = []
    
    global first_chunk
    global last_chunk 

    with open('short_queries.csv') as queries_csv:
        reader = csv.reader(queries_csv)
        for row in reader:
            query = row[0]
            query = query.replace(' ','+')
            print(query)
            url = first_chunk + query + last_chunk
            all_queries.append(url)

        print("----------------------")
        for row in all_queries:
            print(row)

        return all_queries


#####################              #####################
#####################    CRAWLER   #####################

class EbaySpiderSpider(CrawlSpider):

    name = 'ebay-spider'

    def start_requests(self):
        # Forma de configurar el USER AGENT en scrapy
        custom_settings = {
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
        }

        # rules = (
        #     Rule(LinkExtractor(restrict_xpaths='//h3[@class="lvtitle"]/a'), callback='parse'),# product links from vendor articles
        #     Rule(LinkExtractor(restrict_xpaths='//div[@class="s-item__image"]/a'), callback='parse'), #product links from ebay search serps results
        #     # Rule(LinkExtractor(restrict_xpaths="//a[@class='pagination__button pagination__next-button']"),callback='parse_tem',),
        # )
    
        allowed_domains = ['www.ebay.es']
        start_urls = get_queries()
        # ['https://www.ebay.es/itm/194207335467?hash=item2d37a8c42b%3Ag%3AguUAAOSw42FgzIP%7E&LH_BIN=1',
        # 'https://www.ebay.es/itm/313519730655?_trkparms=ispr%3D1&hash=item48ff3b6fdf:g:myQAAOSwADxgsNiR&amdata=enc%3AAQAGAAACkPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSB0Xm7k0guzAysaIMfJcbBJmXtVrMUrraCYejHPgiSnRM%252BcPEn4Ba%252FuaUTbl8lT7%252B0FzuQp9fq1%252BaEqI2GrIZ1yCEupo1LkC5Ps%252BjuOFeB2r2Lsx7Tgv6Xg8BGes%252FnYBqR1RvF2IKifEADmNXYARhz%252FPvoIf6Px%252BwdX1qR4FoFyo9pOvOcft26y4wXr3gmafDfdBAIpLYfb3shPeSwpihBZ1aHpZnOVYQs0UcdzNaEr5ymWjQ%252FmSuEuT%252FPI5w4B9TmRM0Ew0XAkT0ZkkCZ88tRSJWxjxHJhnNirYeg5QwOP5SDD2v%252BNlW13CRXzykrdrjpIBSPuDwLFrHCd2bX8QYO9b%252F3DfRqzoIGh8CGedzBX%252BwjbV48W8GEVRPzMlL1AuS4ThusuiQXwKEmNr6IJ2XIX60sxsfPGjGObDeBY88m4z5iWpQ19iSgzU9lJWK0KyneBTKdr8QbUB87P%252FvcrCXYYPtOaXrZxl8Rb%252BVIIl60zujQt0tQO9wZTI8KzUfe108y9PcALaVB7PPmclqJq7S5cNh1XM7TPyVHXAFbTlDs0QyArAa6O8v98Ocagb01cS9PoKC90cI27Omkc0RHb8wN3ufBdGuTj5CnJPRc2dLh3EfCDuJOLrfVYVnPOhDMbWJngGWvjmvsRLGlcEVRkl7U%252BY4wzigH0VsR%252FvxMppiXtm0Sv64NEjLLN1JrH1ldDlcxT2r0%252FFS5ZNWcyEq8vY6WvQmJxwMXS1qAGCZ%252Bj12qEPDSeYqrltk8oVv7wRsLl%252FhdpBEKx3A%252BmeERLrHq9B2hKM0RMi4yfKxdICZQQwIFodjL6GJxFcA3w9luZp8vWPm%7Campid%3APL_CLK%7Cclp%3A2334524',
        # 'https://www.ebay.es/itm/143583232314?_trkparms=ispr%3D1&hash=item216e3a413a:g:WGIAAOSwKU1emitb&amdata=enc%3AAQAGAAACkPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsS9d9gBrkNbRQtRn8MVXnYkiJFMm7AxianpWr3Y8yHSWFpKEIfZIOHY7uKPFLdtlfps%252Ffb38sXWfveRXTH%252F7LSmsuktN12xJkLewPieBhWqktIYrSYl%252Ffg40LXhhHKcTHVmDfmoO9AyGJLWb3lTOeP2nMflV%252BA%252FjAGo%252F7ZiAJnyco02PkYfwuc6RDiut4K6lP7x66NmfxVyVqnvm9WxRO3y7JHH1eHAP88w33s6qmV28ey76jcJN1dfRuid24PlfLYVI2xnPbukV0S6V5uPp1KNhdhrW9rkH2pX%252FeV83JY%252B%252FSUtLrdKhCexCn8%252FsG%252FHCF6N6uWZp1kwgTCrcVHMh6GNi63Rp8j58wYxrFIvP8%252BDLKmUg73P7LI1N2529np8yZvbjIRVTL%252BlAYaEHVBwQJgJoZWNj%252Bop1QlgHlr0YaDLTiz491iMeyp8arD3chGIzpdU%252BXd6rSZO%252F3aLKV%252BoFHnrgs2ohVjEeS1EkYQ%252B9SHHcuVie4%252BcLDinCYjWwRMm7vUKblFrT2jvE6%252FIHF1gaN5yqhz3Ju4ycEHTGtgMado0Rhb24rQc%252BHizwzaciSL%252B9%252BdiOFVBFZpxbZgpgPCgrEMR1mnCPaDPZ4mwtsu7okZiVELnwzF1nI6%252B3je9Zqr55Wn6jCV1aaxKTvqIrtXU00%252BII8wnkhckQPoYba7qbkd1e4zZ8KoloHbgZjEVK8kINC7KWVBQH2P2FV0BVouZsjWe8G1nBlY32YRY273Axu1%252FkLoQhm708T5Y9x4HDtt7OkTrF1IsURuR32YREgslaefSM5OyMECfsBmWNPsPZ5LCw0KTWT8%252B5X36XrqbjdCGFgR%7Campid%3APL_CLK%7Cclp%3A2334524,'
        # ]
  

        download_delay = 2 # Already set in settings.py


        # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
        # rules = (
        #     Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
        #         LinkExtractor(
        #             allow=r'/itm/' # Si la URL contiene este patron, haz un requerimiento a esa URL
        #         ), follow=True, callback="parse"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
        # )

    

        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.serp, meta={'start_url':start_url})

    #ebay serp with prod links
    def serp(self,response):
        
        start_url = response.meta["start_url"]
        #my_print(response.text)

        prods_url = response.xpath('//div[@class="s-item__image"]/a[1]/@href').extract()        
        for url in prods_url:
            yield Request(url=url, callback=self.parse, meta={'start_url':start_url})

    

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
            
            subcategory='' #define subcategory default value
            #if xpath contains platform then the product
            if category == "Consolasyvideojuegos":
                subcategory = response.xpath('//td[contains(text(),"Plataforma")]/following-sibling::td[1]/span/text()').extract_first()

            elif category == "Móviles y Smartphones":
                subcategory = response.xpath('//td[contains(text(),"Modèle") or contains(text(),"Modelo") or contains(text(),"Model")]').extract_first()
            
            return subcategory
            

        def get_payment_methods(response):

            div = response.xpath('id="payDet1"')


        def get_query_text(query):
            global first_chunk
            global last_chunk

            query = query.split(first_chunk)[1]
            query = query.split(last_chunk)[0]
            query = query.replace('+',' ')
            return query

        def get_specs(html_data):
            '''Takes html and convert it into a dict of specs key:value,
            like Brand: Samsung'''
            from bs4 import BeautifulSoup

            #clean html
            html_data = html_data.replace('\n','').replace('\t','')

            soup = BeautifulSoup(html_data,'lxml')
            raw_data = soup.find_all('td')
            data_list = []

            for item in raw_data:
                data_list.append(item.get_text())

            #create two lists and an index to identify later even and odds
            odd_keys = []
            even_values = []
            index = 1

            #create 2 lists one with all the keys and the other with all the values
            for item in data_list:
                item = item.strip()# delete white spaces
                if index % 2 == 0:
                    even_values.append(item)
                    index += 1
                else:
                    odd_keys.append(item)
                    index += 1

            #zip and dict the keys
            zip_obj = zip(odd_keys,even_values)
            specs = dict(zip_obj)
            return specs

        #this doesn't work well, in vscode viewer the csv looks fine
        #in excel csv viewer looks with bugs, strange breaklines
        def get_related_links(response):
            related_prod_list = []
            related_links = response.xpath('//li[@class="rtxt"]/parent::ul/li/a/@href').getall()#.extract_first()
            # my_print(len(related_prod_list))
            # for prod in related_links:
            #     related_prod_list.append(prod)
            return related_links

        def get_price(price):
            if price == None:    #notice is different convB..       
                price = response.xpath('//span[@id="convbidPrice"]/text()').get()
            
            if price == None:           #notice the id is conviD and conviN, the're differents
                price = response.xpath('//span[@id="convbinPrice"]/text()').get()

            if price == None:   #this is spanish EUR price if prod is from spain
                price = response.xpath('//span[@class="notranslate"]/text()').extract_first()

            if price == None:
                price = response.xpath('//span[@id="mm-saleDscPrc"]').get()

            if price == None:
                price = response.xpath('//span[@class="notranslate"]').get()

            if price == None:
                price = response.xpath('//span[@class="notranslate "]').get()

            if price == None:
                price = response.xpath('//span[@id="mm-saleDscPrc"]').get()
            return price

        def get_shipping_price():
            #if shipping_price == None:          
            try:
                shipping_price = response.xpath('//span[@id="convetedPriceId"]/text()').get()
            except:
                pass

            if shipping_price == None:
                shipping_price = response.xpath('//span[@id="fshippingCost"]/span/text()').get()

            return shipping_price

        #################   PARSE FUNCTION   ####################
        #this is the iframe with prod_description inside, to get it it's needed another request to get the info inside the iframe
        #scrape all the data and make another request to the iframe's url and pass all the scrapped data as meta.
        iframe_description_url = response.xpath('//div[@id="desc_wrapper_ctr"]/div/iframe/@src').get()
        
        #get query url from meta, use a function to get the query text from the origin url
        start_url = response.meta["start_url"]
        query = get_query_text(start_url)

        #miscelaneus prod data; All Except prod_description 
        variable_prod = response.xpath('//span[@id="sel-msku-variation"]').get()
        title = response.xpath('//h1[@itemprop="name"]/text()').extract_first()            
        returns = response.xpath('//span[@id="vi-ret-accrd-txt"]/text()').extract_first()
        ebay_article_id = response.xpath('//div[@id="descItemNumber"]/text()').extract_first()
        prod_url = response.url        
        category = get_category(response) #taking the last link in breadcrumbs        
        ebay_vendor = response.xpath('//span[@class="mbg-nw"]/text()').extract_first()
        product_state = response.xpath('//div[@id="vi-itm-cond"]/text()').extract_first()        
        #related_links = get_related_links(response) #not using because of a weird bug
        product_sold_out_text = response.xpath('//span[contains(text(),"Este artículo está agotado")]')        
        shipping_price= response.xpath('//span[@class="vi-fnf-ship-txt "]/strong/text()').get()
        #if the prod is not from Spain, the xpath for shippment changes
        #shipping_time = response.xpath('//span[@class="vi-acc-del-range"]/b/text()').extract_first()
        shipping_time = response.xpath('//span[@class="vi-del-ship-txt"]/strong[@class="vi-acc-del-range"]/text()').extract_first()
        # when prod is not in spain, this identifies if its shipped to spain or not
        served_area = response.xpath('//span[@itemprop="areaServed"]/text()').get()
        reviews = response.xpath('//div[@class="reviews"]/text()').extract_first()        
        seller_votes = response.xpath('//span[@class="mbg-l"]/a/text()').get()
        payment_methods = response.xpath('//div[@id="payDet1"]/div/img/@alt').getall()
        prod_specs_html = response.xpath('//div[@class="itemAttr"]/div/table').get()
        prod_specs_text = str(prod_specs_html) 
        prod_specs = get_specs(prod_specs_text)
        import_taxes = response.xpath('//span[@id="impchCost"]/text()').get()
        #this is to replace breaklines that excel don't decode well        
        try:
            reviews = reviews.replace('\n','')
        except:
            pass

        try:
            served_area = served_area.replace('\n','')
        except:
            pass

        #location = response.xpath('//div[@class="iti-eu-bld-gry "]/span/text()').extract()
        article_location = response.xpath('//span[@itemprop="availableAtOrFrom"]/text()').get()
        
        #depending on article location shows on price or another
        if 'España' not in article_location:
            pass
        
        if shipping_price == None:
            shipping_price = get_shipping_price()

        if shipping_time == None or '':
                shipping_time=response.xpath('//span[@class="vi-acc-del-range"]/b/text()').extract_first()

        #many prods are from UK, they show price in GBP and EUR, 
        # this tries first to take EUR prices with prods with both options        
        price = response.xpath('//span[@id="convbinPrice"]/text()').get()        
        if price == None or '':
            price = get_price(price) # there're a lot of alternatives, so I made a function
        
        # now call the iframe parser and give it all the info inside meta
        yield Request(url=iframe_description_url, callback=self.iframe, 
                    meta={  
                        'title':title,'price':price, 'query':query,
                        'shipping_time':shipping_time, 'variable_prod':variable_prod,
                        'returns':returns,'shipping_price':shipping_price,
                        'ebay_article_id':ebay_article_id,'prod_url':prod_url,
                        'ebay_vendor':ebay_vendor,'seller_votes':seller_votes,        
                        'category':category, 'payment_methods':payment_methods,
                        'product_state':product_state, 'product_sold_out_text':product_sold_out_text,
                        'served_area':served_area,'reviews':reviews, 'prod_specs':prod_specs,
                        'import_taxes':import_taxes,
                        })
        

    #this scrapes the prod description in iframe
    def iframe(self,response):

        
        #this is the prod descrption in the iframe
        prod_description = response.xpath('//body').extract() #extract to get the html, not the text with get()
        prod_description = str(prod_description)

        #get all data from meta
        title = response.meta['title']
        price = response.meta['price']
        query = response.meta['query']
        shipping_time = response.meta['shipping_time']
        variable_prod = response.meta['variable_prod']
        returns = response.meta['returns']
        shipping_price = response.meta['shipping_price']
        ebay_article_id = response.meta['ebay_article_id']
        prod_url = response.meta['prod_url']
        ebay_vendor = response.meta['ebay_vendor']
        seller_votes = response.meta['seller_votes']
        category = response.meta['category']
        payment_methods = response.meta['payment_methods']
        product_state = response.meta['product_state']
        prod_specs = response.meta['prod_specs']
        served_area = response.meta['served_area']
        reviews = response.meta['reviews']
        product_sold_out_text = response.meta['product_sold_out_text']
        import_taxes = response.meta['import_taxes']
        
        yield {'title':title,'price':price, 'query':query,
        'shipping_time':shipping_time, 'variable_prod':variable_prod,
        'returns':returns,'shipping_price':shipping_price,
        'ebay_article_id':ebay_article_id,'prod_url':prod_url,
        'ebay_vendor':ebay_vendor,'seller_votes':seller_votes,        
        'category':category, 'payment_methods':payment_methods,'prod_specs':prod_specs,
        'product_state':product_state, 'prod_description':prod_description,
        'served_area':served_area,'reviews':reviews,'product_sold_out_text':product_sold_out_text,
        'import_taxes':import_taxes,
        #'related_links':related_links,
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


