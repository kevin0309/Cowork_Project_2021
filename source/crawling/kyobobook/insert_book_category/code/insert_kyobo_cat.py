# @Author        : Kim Suehyun
# @Since         : 2021.01.21
# @Dependency    : 
# @Description   : 영풍문고 책 카테고리 테이블 초기화

import json
import sys
sys.path.append('./source')
from util import db_conn_util
import crawl_kyobo_cat

class KyoboCatInit :
    def __init__(self) :
        '''
            @return (void)
        '''
        self.db = db_conn_util.PyMySQLUtil()
        self.file_path = {
            "cat1": './source/crawling/kyobobook/insert_book_category/data/kyobo_cat1.json',
        }

    def insert_root(self):
        '''
            루트 카테고리를 테이블에 삽입하는 메서드
            @return (void)
        '''
        sql= "INSERT INTO book_category VALUES(NULL,1,'국내도서',1,sysdate())"
        self.db.execute_query(sql)

    def insert_cat_1(self):
        '''
            카테고리 레벨1을 테이블에 삽입하는 메서드
            @return (void)
        '''
        with open(self.file_path["cat1"], encoding="UTF-8") as json_file:
            cat1 = json.load(json_file)
            print('insert category level 1')
            for category in cat1:
                name= category['name']
                code= category['code']
                sql = "INSERT INTO book_category VALUES(NULL,%s,%s,1,sysdate())"
                self.db.execute_query(sql, (code, name))

    def insert_cat_2(self):
        '''
            카테고리 레벨2을 테이블에 삽입하는 메서드
            @return (void)
        '''
        sql= "SELECT category_seq FROM book_category WHERE char_length(code)=2"
        self.__cat_1_list= self.db.execute_query(sql)
        
prog= KyoboCatInit()
prog.insert_cat_1()