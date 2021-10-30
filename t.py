from requests_html import HTMLSession
from selenium.webdriver.common.by import By


session = HTMLSession()
response = session.get('https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2047675.m570.l1313&_nkw=iphone+11&_sacat=0')

# serp_prods = response.find_element(By.XPATH, '//li[@class="s-item s-item__pl-on-bottom"]')
serp_prods = response.html.xpath('//li[@class="s-item s-item__pl-on-bottom"]')

for p in serp_prods:
    print(p.text)
    


    text = p.text.split('\n')
    serp_title = text[0]
    
    #get serp price
    flag = 0
    for line in text:
        # used 'EUR' to get price, there's also 'EUR' in shipping cost, prod price is always firts, so use a flag to capture only the first
        if 'EUR' in line and flag == 0:
            serp_price = line.split(' ')[0]
            flag += 1
            #150,45 -> 150
            if ',' in serp_price:
                serp_price = serp_price.split(',')[0]
                print('---------', serp_price)
    print('\n')
