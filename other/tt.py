from lxml import html
import requests

from requests_html import HTMLSession
from selenium.webdriver.common.by import By

print('started program')
session = HTMLSession()
print('got session')
# response = session.get('https://www.ebay.es/sch/15032/i.html?_from=R40&_nkw=iphone+11&LH_TitleDesc=0')
response = session.get('https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2499334.m570.l2632&_nkw=camara+digital&_sacat=31388')
# response = session.get('https://stackoverflow.com/questions/53459924/how-to-scrape-a-web-site-using-python-requests-and-xpath')
print('got response')
print(response.text)



# response = requests.get('https://www.ebay.es/sch/15032/i.html?_from=R40&_nkw=iphone+11&LH_TitleDesc=0')
# tree = html.fromstring(response.content)  
# serp_prods = tree.xpath('//li[@class="s-item s-item__pl-on-bottom"]')
# print(serp_prods)

# serp_prods = response.find_element(By.XPATH, '//li[@class="s-item s-item__pl-on-bottom"]')
# serp_prods = response.html.xpath('//li[@class="s-item s-item__pl-on-bottom"]')
print('got serp_prods')

def filter_price_title(serp_prods, query_title, query_price):
    print('executing...')

    #this is the output return
    filtered_prods_urls = []

    for prod in serp_prods:
        print(prod.text)
        prod_url = prod.find('a')
        print('--------', prod_url)
        
        text = prod.text.split('\n')
        serp_title = text[0]
        
        # #get serp price
        # flag = 0
        # for line in text:
        #     # used 'EUR' to get price, there's also 'EUR' in shipping cost, prod price is always firts, so use a flag to capture only the first
        #     if 'EUR' in line and flag == 0:
        #         serp_price = line.split(' ')[0]
        #         flag += 1
        #         #150,45 -> 150
        #         if ',' in serp_price:
        #             serp_price = serp_price.split(',')[0]
        #             print('---------', serp_price)
        # print('\n')

        flag = 0
        for line in text:
            line = line.lower()
            
            #avoid auctions, 
            if 'puja' or 'pujas' in line:
                break #continue with the outer loop
            
            #get the price
            # used 'EUR' to get price, there's also 'EUR' in shipping cost, prod price is always firts, so use a flag to capture only the first
            if 'EUR' in line and flag == 0:
                serp_price = line.split(' ')[0]
                flag += 1
                #150,45 -> 150
                if ',' in serp_price:
                    serp_price = serp_price.split(',')[0]
                    
                    #if the prod serp price is lower than target price (query_price), continue to next prod // FI: no iphone 12 costs less than 300€
                    if query_price > serp_price :
                        break
        
        ####################
        serp_title = text[0]

        #split the item into words, to search standalone words in the titles instead only one string
        s = serp_title.split(' ')
        n = len(s)
        #n_t = len(attribute_p) # attribute len FI: Sky blue == len 2

        # if n == 1:
        #     if serp_title in title and attribute_p in title :
        #         entry = select(p,title,query)
        #         data_list.append(entry) # list of dicts that contains accepted query, title, link

        #     else:
        #         print('not found in get_MATCHED entrys:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #         print('-----------')
        #         ##write_no_results(query)

        # elif n == 2:
        #     if attribute_p in title and s[0] in title and s[1] in title:
        #         entry = select(p,title,query)
        #         data_list.append(entry) # list of dicts that contains accepted query, title, link

        #     else:   
        #         print('not found in get_MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #         print('-----------')    
        #         #write_no_results(query)    

        # elif n == 3:    
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title:
        #         entry = select(p,title,query)
        #         data_list.append(entry)     # list of dicts that contains accepted query, title, link

        #     else:   
        #         print('not found in get_    MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #         #write_no_results(query)    
        #         print('-----------')    
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title and s[3] in title:
        # elif n == 4:    

        #         entry = select(p,title,query)
        #         data_list.append(entry)     # list of dicts that contains accepted query, title, link
        #         print('not found in get_    MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #     else:   
        #         #write_no_results(query)    
        #         print('-----------')    
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title and s[3] in title and s[4] in title:
        # elif n == 5:    

        #         entry = select(p,title,query)
        #         data_list.append(entry)     # list of dicts that contains accepted query, title, link
        #         print('not found in get_    MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #     else:   

        #         print('-----------')    
        #         #write_no_results(query)    elif n == 6:

        #         entry = select(p,title,query)
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title and s[3] in title and s[4] in title  and s[5] in title:
        #     else:
        #         data_list.append(entry) # list of dicts that contains accepted query, title, link
        #         print('-----------')
        #         print('not found in get_MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        # elif n == 7:
        #         #write_no_results(query)
        #         entry = select(p,title,query)
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title and s[3] in title and s[4] in title  and s[5] in title  and s[6] in title in title:
        #     else:
        #         data_list.append(entry) # list of dicts that contains accepted query, title, link
        #         print('-----------')
        #         print('not found in get_MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        # elif n == 8:
        #         #write_no_results(query)
        #         entry = select(p,title,query)
        #     if attribute_p in title and s[0] in title and s[1] in title and s[2] in title and s[3] in title and s[4] in title  and s[5] in title  and s[6] in title and s[7] in title:
        #         #return(data_list) # list of dicts that contains accepted query, title, link
        #         data_list.append(entry)
        #         print('not found in get_MATCHED data:','---','query: ', query,'-----','prod_title:',title,'---', 'item: ',serp_title,'---','attr: ',attribute_p,)
        #     else:
        #         ##write_no_results(query)
        #     print('-----------')


# query_category = response.meta['query_category']
query_title = 'iphone 12'
query_price = 350

#get product  webelements from ebay serps
# serp_prods = response.xpath('//li[@class="s-item s-item__pl-on-bottom"]')

#return url list of products that pass title, price not auction price
filtered_prods = filter_price_title(serp_prods, query_title, query_price)