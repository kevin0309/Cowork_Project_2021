# @Author        : Kim Suehyun
# @Since         : 2021.01.21
# @Dependency    : 
# @Description   : 교보문고 책 카테고리 크롤링

import requests
from bs4 import BeautifulSoup
import json

class KyoboCatCrawler :
    def __init__(self):
        '''
            file_path-> 생성한 json파일 저장 경로
        '''
        self.__file_path = {
            "cat2": './source/crawling/kyobobook/insert_book_category/data/kyobo_cat2.json',
            "cat3": './source/crawling/kyobobook/insert_book_category/data/kyobo_cat3.json'
        }

    def get_cat_from_page(self, pcode):
        '''
            @param pcode: (string)부모 카테고리 코드
        '''
        url= "http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?linkClass="+pcode+"&mallGb=KOR&orderClick=JAR"
        html= requests.get(url)

        if html.status_code==200:
            soup= BeautifulSoup(html.content, 'html.parser')
            res= []
            if len(pcode)==2:   #pcode가 cat1인 경우 cat2 크롤링 
                index=2 
                file_path= self.__file_path["cat2"]
            elif len(pcode)==4: #pcode가 cat2인 경우 cat3 크롤링
                index=3
                file_path= self.__file_path["cat3"]
            else:
                pass
            cat_list= soup.select('.location_zone')[index].select('.list_zone>ul>li')
            for cat in cat_list:
                cat_dict= {
                    'name': cat.text,
                    'code': cat.find('a').attrs['href'].split('linkClass=')[1].split('&')[0]
                }
                res.append(cat_dict)
        #json 파일로 저장
        with open(file_path, 'w', encoding='utf-8') as make_file:
            '''
                ensure_ascii=False 문자 그대로 출력
                indent="\t"        문자열 들여쓰기에 \t 사용
            '''
            json.dump(res, make_file, ensure_ascii=False, indent="\t")  

test= KyoboCatCrawler()
test.get_cat_from_page("0103")