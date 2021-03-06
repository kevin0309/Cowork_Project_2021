#@Author        : Park YuHyeon
#@Since         : 2021.01.12
#@Dependency    : requests, BeautifulSoup4
#@Description   : DB에 저장된 book_category.code값으로 영풍문고 사이트에 있는 국내도서 책 정보를 list로 반환하는 코드

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

class PageCrawler :
    def __get_book_info_from_page(self, c3, start_cnt, show_cnt, fixed_pub_date_start, fixed_pub_date_end) :
        '''
            @param c3       : (string)책 카테고리 코드
            @param start_cnt: (int)시작 인덱스
            @param show_cnt : (int)간격
            @param fixed_pub_date_start : (datetime)크롤링 할 데이터를 필터링하는 기준일
            @param fixed_pub_date_end   : (datetime)크롤링 할 데이터를 필터링하는 기준일
            @return 책 정보
        '''
        url = 'http://www.ypbooks.co.kr/search.yp?catesearch=true&collection=books_kor&sortField=DATE&c3=' + \
                    c3 + '&startCnt=' + start_cnt + '&showCnt=' + show_cnt
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        res = []    
        book_list = soup.select('#resultlist')  #soup객체로 변환
        #가져와야 할 데이터 - 제목, 저자, 출판사, 출판일, 판매가, 쪽수, 키워드
        #name, author, publisher, pub_date, price, pages, [tags]
        for item in book_list : 
            try :
                info1 = item.select('#resultlist_cont>.recom>.info01')[0].text.split('|')
                img_url = item.select('#resultlist_thum>#book_img>img')[0].get('src') \
                    if item.select('#resultlist_thum>#book_img>img')[0].get('src') != '/ypbooks/images/empty70x100.gif' else ''
                
                temp_book_info = {               
                    'name': item.select('#resultlist_cont>.recom>dl')[0].select('dt>a')[0].text.strip(),    
                    'author': info1[0].strip(),                                                            
                    'publisher': info1[1].strip(),
                    'pub_date_str': info1[2].strip(),
                    'pages': int(info1[3].strip().split('p')[0]),
                    'price': int(item.select('#resultlist_cont>.recom>dl')[4].select('.price>.cost')[0].text.strip().replace(',', '')),
                    'img_url': img_url,
                    'tags': []  
                }
                
                temp_book_info['pub_date']= datetime.strptime(temp_book_info["pub_date_str"],"%Y.%m.%d")   #string->datetime 자료형 변환

                if temp_book_info['pub_date'] < fixed_pub_date_start or \
                    temp_book_info['pub_date'] > fixed_pub_date_end  : #기준일 이전의 출판일을 갖는 도서는 필터링
                    raise ValueError()

                for keyword in item.select('#resultlist_cont>.recom>.keyword>a') : 
                    temp_book_info['tags'].append(keyword.text.strip())

                res.append(temp_book_info)
            except Exception as e : #책 정보가 생략되어 있는 경우 예외처리
                pass
            
        return res


    def get_book_info_from_cat3(self, c3, fixed_pub_date_start, fixed_pub_date_end) : 
        '''
            @param c3: (string)책 카테고리 코드
            @param fixed_pub_date_start: (datetime)크롤링 할 데이터를 필터링하는 기준일
            @param fixed_pub_date_end: (datetime)크롤링 할 데이터를 필터링하는 기준일
            @return (list)책 정보
        '''
        res = []
        start_cnt = 0
        show_cnt = 100
        while True :
            print('search - c3:',c3,' / index (',str(start_cnt),'~',str(start_cnt + show_cnt),')')
            temp_book_list = self.__get_book_info_from_page(c3, str(start_cnt), str(show_cnt), \
                fixed_pub_date_start, fixed_pub_date_end)
            if len(temp_book_list) == 0 :   #범위 내에 책이 없는 경우 break
                break
            else :
                res += temp_book_list
                start_cnt += show_cnt
        return res

