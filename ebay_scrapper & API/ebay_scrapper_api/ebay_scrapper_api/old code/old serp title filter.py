s = query_title.split(' ') #split in words
    n = len(s)
    if n == 1: # when title is only one word
        if query_title in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r: #if filter returns true == no exc_kws present in serp_title
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}, query_title <{query_title}>')
            continue
    elif n == 2:
        #if all the words in query_title are present in serp_title...
        if s[0] in serp_title and s[1] in serp_title:
            #append only if there aren't any excluded kw in serp_title
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
        if s[0] in serp_title and s[1] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 3:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 4:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 5:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            print(r)
            if r:
                url_list.append(serp_link)
                print('appended', serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 6:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title and s[5] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 7:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title and s[5] in serp_title and s[6] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 8:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title and s[5] in serp_title and s[6] in serp_title and s[7] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 9:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title and s[5] in serp_title and s[6] in serp_title and s[7] in serp_title and s[8] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    elif n == 10:
        if s[0] in serp_title and s[1] in serp_title and s[2] in serp_title and s[3] in serp_title and s[4] in serp_title and s[5] in serp_title and s[6] in serp_title and s[7] in serp_title and s[8] in serp_title and s[9] in serp_title:
            r = excluded_kw_absence(serp_title, excluded_kws)
            if r:
                url_list.append(serp_link)
        else:
            print(f'no title match in this prod <{serp_title}>, query_title <{query_title}>')
            continue
    print('END  prod------------------------------------')
    
    # except Exception as e:
    #     print('EXCEPTION..................')
    #     errors_n += 1
    #     print('errors= ', errors_n)
    #     traceback.print_exc()
    #     print(e)
    #     continue
    
print('return len',len(url_list))
return url_list

