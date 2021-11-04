from lxml import html
import requests

from requests_html import HTMLSession
from selenium.webdriver.common.by import By




def myfilter(query_title, serp_titles, excluded_kws):
    
    def excluded_kw_absence(serp_title, excluded_kw):
        '''workaround to exclude kw, iphone 12 pro != iphone 12 // if excluded kw in serp_title: continue'''
        flag = 0 
        
        for kw in excluded_kws:
            if kw in serp_title:
                flag +=1 # exc kw found in serp_title
        
        if flag == 0 :
            return True # any exc kw in title
        elif flag != 0:
            return False #some exc kw in title

    #filter by title, split query in words, if all words in serp_title, append the serp_link to filtered_urls
    s = query_title.split(' ') #split in words
    n = len(s) 

    filtered_urls = []
    print('serp_titles',serp_titles)
    for serp_title in serp_titles:
        print('serp_title',serp_title)
       
        ##########
        if n == 2:    
            #if all the words in query_title are present in serp_title...
            if s[0] in serp_title and s[1] in serp_title:
                #workaround to exclude kw, iphone 12 pro != iphone 12 // if excluded kw in serp_title: continue
                # flag = 0
                # for kw in excluded_kws:
                    # if kw in serp_title:
                        # flag +=1
                # #if there aren't any excluded kw in serp_title, append to list
                # if flag == 0:
                r = excluded_kw_absence(serp_title, excluded_kws)
                if r:
                    filtered_urls.append(serp_title)
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue
        #############
        elif n == 3:
            if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title:
                filtered_urls.append(serp_title)
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue                        
        elif n == 4:
            if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title:
                filtered_urls.append(serp_title)
            else:
                print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
                continue  
    return filtered_urls                      

# query_title = 'iphone 12'
# serp_titles = ['iphone 12 pro', 'iphone 12 max', 'iphone 12 pro max', 'iphone 12']
# serp_link = 'urlheree'

query_title = 'iphone 12'
serp_titles = ['samsung j3','iphone 12 pro', 'iphone 12 max', 'iphone 12']
excluded_kws = ['pro', 'max']

filtered_urls = myfilter(query_title, serp_titles, excluded_kws)
print(filtered_urls)




# check = any(item in list_A for item in list_B)


# for serp_title in serp_titles:
#     if serp_title in query_title:
#         break
#     else:
#         print(e)

#####################
# s = query_title.split(' ') #split in words
# filtered_urls = []

# for serp_title in serp_titles:
#     #if all the words in query_title are present in serp_title...
#     if s[0] in serp_title and s[1] in serp_title:
#         #workaround to exclude kw, iphone 12 pro != iphone 12 // if excluded kw in serp_title: continue
#         flag = 0
#         for kw in excluded_kws:
#             if kw in serp_title:
#                 flag +=1
#         #if there aren't any excluded kw in serp_title, append to list
#         if flag == 0:
#             filtered_urls.append(serp_title)
#     else:
#         print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
#         continue


# for e in filtered_urls: 
#     print(e)