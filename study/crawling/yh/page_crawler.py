import requests
from bs4 import BeautifulSoup

def get_book_info_from_page(c3, start_cnt, show_cnt) :
    '''
        가져와야 할 데이터 - 제목, 저자, 출판사, 출판일, 판매가, 쪽수, 키워드
        name, author, publisher, pub_date, price, pages, [tags]
    '''
    url = ' http://www.ypbooks.co.kr/search.yp?catesearch=true&collection=books_kor&sortField=DATE&c3=' + \
                c3 + '&startCnt=' + start_cnt + '&showCnt=' + show_cnt
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    res = []
    book_list = soup.select('#resultlist')
    for item in book_list : 
        try :
            info1 = item.select('#resultlist_cont>.recom>.info01')[0].text.split('|')
            temp_book_info = {
                'name': item.select('#resultlist_cont>.recom>dl')[0].select('dt>a')[0].text.strip(),
                'author': info1[0].strip(),
                'publisher': info1[1].strip(),
                'pub_date_str': info1[2].strip(),
                'pages': int(info1[3].strip().split('p')[0]),
                'price': int(item.select('#resultlist_cont>.recom>dl')[4].select('.price>.cost')[0].text.strip().replace(',', '')),
                'tags': []
            }

            for keyword in item.select('#resultlist_cont>.recom>.keyword>a') : 
                temp_book_info['tags'].append(keyword.text.strip())

            res.append(temp_book_info)
        except : 
            pass
        
    return res

def get_book_info_from_cat3(c3) : 
    res = []
    start_cnt = 0
    show_cnt = 100
    while True :
        print('search - c3:',c3,' / index (',str(start_cnt),'~',str(start_cnt + show_cnt),')')
        temp_book_list = get_book_info_from_page(c3, str(start_cnt), str(show_cnt))
        if len(temp_book_list) == 0 :
            break
        else :
            res += temp_book_list
            start_cnt += show_cnt
    return res

book_list = get_book_info_from_cat3('100101')
print(len(book_list))
