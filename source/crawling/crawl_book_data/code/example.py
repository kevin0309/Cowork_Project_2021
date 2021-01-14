# @Author        : Kim SueHyun
# @Since         : 2021.01.14
# @Dependency    : 
# @Description   : 

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from pprint import pprint 

import page_crawler
from util import db_conn_util

class ExampleClass:
    def __init__(self):
        self.db= db_conn_util.PyMySQLUtil()
        self.crawler= page_crawler.PageCrawler()

    def select_category_code(self):
        '''
            DB에 연결하여 책 카테고리가 c3인 code와 category_seq를 반환하는 함수
            @return (tuple)책 카테고리 코드(category_seq, code)  
        '''
        # curs= self.conn.cursor()                                                 #Connection으로부터 Cursor를 생성
        # sql= "SELECT category_seq, code FROM book_category where char_length(code)=6"     #c3 category code SELECT
        # curs.execute(sql)
        # rows= curs.fetchall()
        # return rows
        sql= "SELECT category_seq, code FROM book_category where char_length(code)=6" 
        return self.db.execute_query(sql)
    
    def insert_book_info(self, book):
        '''
            get_page_crawler에서 반환한 책 정보를 DB에 저장하는 함수
        '''
        sql= "INSERT INTO book_info VALUES(NULL, '"+book['name']+"',NULL,'"+book['author']+"',)"


    def get_page_crawler(self):
        '''
            DB에서 가져온 c3 카테고리로 page_crawler를 호출하는 함수
            @return (list)책 정보(name, author, publisher, pub_date, price, pages, [tags])
        '''
        #TODO: 책 목록에서 최신 목록만 가져오는 필터링 필요
        #TODO: DB에 이미 저장된 책 정보인지 비교할 수 있는 함수 필요
        books= []
        c3_list= self.select_category_code()
        for c3 in c3_list: 
            books.append(self.crawler.get_book_info_from_cat3(c3[1]))
        return books

    def exp(self):
        '''
        '''
        books= self.get_page_crawler()
        for book in books:
            self.insert_book_info(book)

 


