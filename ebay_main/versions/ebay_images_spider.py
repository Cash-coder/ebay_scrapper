import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from time import sleep
import sys
from termcolor import colored

import re #used in to clean data in above yield
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from shutil import which

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy import Spider
from scrapy.http import Request

# for logging()
import logging

#for my_print()
from colorama import init
from termcolor import colored
init()

#for extract_urls()
import csv



#type xp if you want target by xpath, css taget by css, id = css/xpath identifier
def my_click(id, type='xp'):
    '''Uses action chains to click
    requiered xpath, type=css to use css, web_element...'''

    

    from selenium.common.exceptions import TimeoutException

    if type == 'xp':
        wait = WebDriverWait(driver,12)
        target = wait.until(
        EC.element_to_be_clickable((By.XPATH, id)))

        try:
            #target.click()
            actions = ActionChains(driver)
            actions.move_to_element(target).click().perform()
        # except TimeoutException as e:
        #     print("THIS IS TIMEOUT EXCEPTION")
        #     print(e)
        except Exception as e:
            print(e)
            

    elif type == 'css':
        wait = WebDriverWait(driver,12)
        target = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, id)))

    
    elif type == 'web_element':
        
        #using the raw web element passed in args(id) as target
        target = id

        try:
            #target.click()            
            actions = ActionChains(driver)
            actions.move_to_element(target).click().perform()
        # except TimeoutException as e:
        #     print("THIS IS TIMEOUT EXCEPTION")
        #     print(e)
        except Exception as e:
            print(e)



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
            

        

def get_big_images(self):

    big_images_list = []

    images = self.driver.find_elements_by_xpath('//td[@class="tdThumb"]/div/img')

    for image in images:

        my_click(self,type='web_element',id=image)
        my_print('imageclicked-------')
        #big_img = image.get_attribute('src')
        sleep(3)
        big_img = self.driver.find_element_by_xpath('//img[@id="icImg"]').get_attribute('src')
        big_images_list.append(big_img)
        #big_images_list.append("///////")
        #my_print(text=big_images_list, mode='lines')

        #avoid the repeated images
        set_images = set(big_images_list)

        my_print(self.driver.current_url)
        my_print(set_images, mode='lines')                        

        #my_print(big_images_list,id="complete list")

    return set_images


################################### SPIDER ##############################

class EbaySpiderSpider(scrapy.Spider):

    name = 'ebay-spider'
    allowed_domains = ['www.ebay.es']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'

    def start_requests(self):


        try:

            driver_path = "/home/kv/Desktop/python_scripts/chromedriver_linux64/chromedriver"

            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920, 1200")

            self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
            self.driver.set_window_size(1920, 1080)
                
            self.driver.get('https://www.ebay.es/itm/262888132565?_trkparms=aid%3D1110018%26algo%3DHOMESPLICE.COMPLISTINGS%26ao%3D1%26asc%3D20201210111452%26meid%3D9c42c5aba058431482e069d71c6c773b%26pid%3D101196%26rk%3D2%26rkt%3D12%26sd%3D324091464922%26itm%3D262888132565%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DItemStripV101HighAdFeeWithCompV3Ranker&_trksid=p2047675.c101196.m2219&amdata=cksum%3A2628881325659c42c5aba058431482e069d71c6c773b%7Cenc%3AAQAFAAACALehJB2Y4Sxk5yFg7R9UN9SEMYfbLRHrkt3mNsnT%252FM28j2dPZ89SmFybiDgERsrN8ZtqCigSi%252FkaIMmBDn3cN9VXhqQLiwKg3gB8sPF5UuXiXSZIbo6VtjTJll6mKHQYzf0M1uWGARluXuZzRXs35cEnkdTyxkDjCTqmLj4pc8%252BR%252BTO2y10YxGU0p1%252Fe496JzMXY5OBEx6KKSaC8uFlh6p55wvq27DrXkqYNb6ucl4mRUyLCSbM6jhIq%252BmbVzSKaPuK8lHRSIciOkmUZwGt6tncrfTZe6UtaeEcVkSXf%252BNJ23z%252Bdb8ur85boLLgHgUX6%252BuwL1Egs1E2a%252FgUQULqI4oYr4F36oyNugMMCAI%252F%252B%252FF5u3kG0RDqfvJEU1%252Bzmmoi9PtzaEOQVz9Bx8JkPgNgHpXFGii8J2SMCLO0AOpQk8o9kZyj4%252By8sjaZnPHfn0BVmfmXN5J06njuXk3A3kz2%252B8BFJnZkiUGO52wsFoQYkzX%252BKpdhEPucn8DmAfacerf%252FVbDIO2FgtkuMgfYmmY8vFK6PGRO8KDOEt1OCw5veF3ED52h%252BBj2CdQnOwNVruH3oLSLrLz5%252FEXnliEKBk%252B%252Fg7JdW8%252BTbfJufMzyRgbtPsqmIYL7JmKO1vGbKDqTIT%252FwWoxzcxg7XGtnJSMKoaHMzba0k1r%252BHGNS97jnsWMn%252BKoXs1%7Campid%3APL_CLK%7Cclp%3A2047675')
            
            self.driver.get(self.driver.current_url)
            sleep(2)
            self.driver.refresh()
            # imphone muchas img    https://www.ebay.es/itm/384050938155?_trkparms=ispr%3D1&hash=item596b38412b:g:wtkAAOSw3dBgWIOi&amdata=enc%3AAQAFAAACcBaobrjLl8XobRIiIML1V4Imu%252Fn%252BzU5L90Z278x5ickkxFtV7J5P58ubuVigtBH%252Fez6nI8344IQJbEEo6Kw5kcVecp0ElSr0up7jJsTy8K2IUcfqCG0ePHzA0DraC2ZWA6Pr%252FYqjI%252FBemx4kjhqSmQF6c2rjQbIJXYB%252BGdklg9%252BUT%252BD1aWYkQGDw4WJlPg1Xk%252FW49a418CsXnd5m%252FhHG0APKvtLVTNP1pW%252FAkGCLg4fn3ilgOBEGBh%252Fiu6jlC1P7yYVXZBf7tO2xAm9cnroKXIyM80MBlz1xmwu%252F0mZhbcktb3PVnMi9p6zGlNGBxVGYaWJYLvliMaPkhN1vOpUdgcGluFT%252BsLtMngeO65%252B9WVAiwvjOppuovoB8FOlC7Dc6LFldtkPQtZ2%252Brg7vvAaTHushk7iVkNNQV3M3V3qHiyLJjQiNsUwwg6K8nK%252BjwDsNjcnUVurGZu4bRIfti7wSOmshEyG4P1RjsGXyrya9sJ0m%252Bsoj6IxEY1ir2S2iUkJOzQJJ3rQ1PgoEAyA8yPvw%252Bp6Nb%252FemI87o9IXZcteDhhl6bgGLAM%252FBqNPc9%252BSIFFdugjLBJ3n%252BofdIgZddlXLob1QtL5U8E6hwvICz%252FGS4OW0rJdGi86Oj5xBfHse2VNZ4vRTSdJLonAFP8ZYMBmW2ZQbn2Q1OLSXcyIDVZ44BM1K1t2dqhkU5YOklx7iFLx5yhMXU%252FwOPtYb8JPpRR2VbPNexOOKLMh9qd1yHOlwDBLjQXby4rdewg%252FTZGWgrxJqbkNpmw4mIgyzVIoRLjUKfFg2w0o5wWepGOcO%252F6GJHV6fcr9Y7akcPQ6osmzkp%252BQMZnA%253D%253D%7Ccksum%3A384050938155a4f946db713641c1a5983c0d2c31d9a6%7Campid%3APL_CLK%7Cclp%3A2334524
            #tv   https://www.ebay.es/itm/324091464922?_trkparms=5373%3A5000010670%7C5374%3AElectr%F3nica%7C5079%3A5000010670
            #sporte https://www.ebay.es/itm/263157205383?_trkparms=aid%3D1110018%26algo%3DHOMESPLICE.COMPLISTINGS%26ao%3D1%26asc%3D20201210111452%26meid%3D4395a5e635d24b49acc403a4cb4995ac%26pid%3D101196%26rk%3D6%26rkt%3D12%26sd%3D324091464922%26itm%3D263157205383%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DItemStripV101HighAdFeeWithCompV3Ranker&_trksid=p2047675.c101196.m2219&amdata=cksum%3A2631572053834395a5e635d24b49acc403a4cb4995ac%7Cenc%3AAQAFAAACAF77T3tAFAwEEN692tBUU2TI820Hazh6M0m7pEe4V0w0DjKxWqr4643VfbXwWQ3QTRGylI7RRrUzwD463kjnR1ZWeFwHEzNEz4i7JeCMZ%252FbaXQbD7WBaxrzJXpCoZWIh4IcJTurI4PHQarMVKt5T91B3cJEb7x21qp1vsLaKYwIM%252FqitqAQ%252FEqJowczCKWis2VjTo7JUy2HKGpt62dRPcRcyLWUV%252BAjnY%252BIiXLrzVnnGamPLaX5lp7N5mX8MEnS%252Bw9lVUTLFikKeCSqHffthNzx3cdoqyqG9eaQQg9ntwxy1N8qO9pUjY8fXBbWQizrNJiGZbHTr1qPl2bzDMkIbmyv0vcqZ5GND%252FEk6pWLdAjwJL85j8tcF%252BtvUrSf95pS7J2fXbcE1HIeyli%252BEz8vJFUmz8zdeNHAR7qC7uE6IPVK4rcm8BERR23Q3cRUF2RGsGx3%252FzhwCjwvCGi3qYxyZITLzzNd6VGbns2wC1yrY5PH%252F0RubaZ98UhQYMOPxPZrsq5DFnkq0WLODzbL0rMSZTWAr39O0VXSUIAFd5AhOg9%252B6ttmMSMakef6DEbLRNL3jhTlFEAAtOsTfBLECOMN4hFWovSrnK8xxbc4vyQC8%252F55WKJNk5Nwcysac8nX8RHCH3M2xI0niYqX8cA7D%252BNQqczTHgvM4iUWf0cTA90g9E%252BnN%7Campid%3APL_CLK%7Cclp%3A2047675&epid=6034106535            

            #cookies agreement
            #my_click(self,'//div[@class="gdpr-banner-actions"]/button')

            #thumbnails = self.driver.find_elements_by_xpath('//td[@class="tdThumb"]/div/img')

            big_images_set = get_big_images(self)

            url = self.driver.current_url
            yield Request(url=url, callback=self.parse, meta={'images': big_images_set})

            # prods = self.driver.find_elements_by_xpath('//a[contains(text(),"Comprar ahora")]')
            # my_print(text=len(prods),color='red')

            # for prod in prods:

            #     url = prod.get_attribute('href')
            #     my_print(text=url,color='blue')

            #     yield SeleniumRequest(url=url,meta={"url": url}, callback=self.parse)

        ############### MAIN EXCEPT #####################

        except Exception as e:
            my_print(e,color='red')


        finally:
            sleep(5)
            #self.driver.close()



    def parse(self, response):
        
        big_images_set = response.meta.get('images')
        
        yield{
            'images':big_images_set
        }
