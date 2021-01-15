# @Author        : Kim SueHyun
# @Since         : 2021.01.14
# @Dependency    : 
# @Description   : 영풍문고 책 정보 크롤링 모듈

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from datetime import datetime

import page_crawler
from util import db_conn_util

class CrawlingModule:
    def __init__(self):
        self.db= db_conn_util.PyMySQLUtil()
        self.crawler= page_crawler.PageCrawler()

    def select_category_code(self):
        '''
            DB에 연결하여 책 카테고리가 c3인 code와 category_seq를 반환하는 함수
            @return (tuple)책 카테고리 코드(category_seq, code)  
        '''
        sql= "SELECT category_seq, code FROM book_category where char_length(code)=6" 
        return self.db.execute_query(sql)
    
    def insert_book_info(self, c3, books):  
        '''
            get_page_crawler에서 반환한 책 정보를 DB에 저장하는 함수
        '''
        category_seq= c3[0]
        for book in books:  #book의 keys: name, author, publisher, pub_date, price, pages, [tags]
            name= book["name"]
            author= book["author"]
            publisher= book["publisher"]
            pub_date_str= book["pub_date_str"]  
            price= book["price"] 
            pages= book["pages"] 
            tags= book["tags"] #list
            
            sql= "INSERT INTO book_info VALUES(NULL, '"+name+"',NULL,'"+author+"','"+publisher+"',timestamp(date_format('"+pub_date_str+\
            "','%Y.%m.%d')),"+str(category_seq)+","+str(price)+","+str(pages)+",sysdate())"                      # book_info 테이블에 책 정보 삽입
            self.db.execute_query(sql)
            sql1= "SELECT book_seq from book_info order by book_seq desc limit 1"                   # book_info 테이블에 가장 최근에 입력된 row의 book_seq 조회               
            book_seq= self.db.execute_query(sql1)

            for tag in tags:
                sql2= "INSERT INTO book_tags VALUES(NULL, "+str(book_seq[0][0])+",'"+tag+"',sysdate())"   # book_tags 테이블에 태그 삽입
                self.db.execute_query(sql2)
        print(category_seq, datetime.now()) #카테고리별 종료시간 출력
               

    def get_page_crawler(self):
        '''
            DB에서 가져온 c3 카테고리로 page_crawler를 호출하는 함수
        '''
        # TODO: 책 목록에서 최신 목록만 가져오는 필터링 필요
        # TODO: DB에 이미 저장된 책 정보인지 비교할 수 있는 함수 필요
        c3_list= self.select_category_code()
        for c3 in c3_list:  #c3의 구성: (category_seq,code)
            code= c3[1]
            books= self.crawler.get_book_info_from_cat3(code)
            self.insert_book_info(c3, books)



test= CrawlingModule()
test.get_page_crawler()