from lxml import html
import requests

from requests_html import HTMLSession
from selenium.webdriver.common.by import By




def myfilter(query_title, serp_titles, excluded_kws):
    #filter by title, split query in words, if all words in serp_title, append the serp_link to filtered_urls
    s = query_title.split(' ') #split in words
    n = len(s) 

    filtered_urls = []
    for serp_title in serp_titles:
        if n == 1: # title is only one word
            if query_title in serp_title and excluded_kws not in serp_title:
                filtered_urls.append(serp_link)
            else:
                print(f'no title match in this prod <{serp_title}, query_title <{query_title}>')
                continue
        elif n == 2:
            if s[0] in serp_title and s[1] in serp_title:
                if any(item in s for item in excluded_kws) == False:
                    print(f'cathed excluded! {serp_title}')
                    continue
                filtered_urls.append(serp_title)
                # for kw in excluded_kws: # if exluded the is some kw in serp_title -> continue
                #     print(kw)
                    # if kw not in serp_title:
                    
                    
                    #     print(f'kw {kw}, serp_title:{serp_title}, query_title{query_title}')
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue
        elif n == 3:
            if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title:
                filtered_urls.append(serp_link)
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue                        
        elif n == 4:
            if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title:
                filtered_urls.append(serp_link)
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue  
        return filtered_urls                      

query_title = 'iphone 12'
serp_titles = 'iphone 12 pro', 'iphone 12 max', 'iphone 12'
serp_link = 'urlheree'
excluded_kws = ['pro', 'max']

print(myfilter(query_title, serp_titles, excluded_kws))

list_A = ['iphone', '12']

list_B = ['pro', 'max']

check = any(item in list_A for item in list_B)

# print(check)