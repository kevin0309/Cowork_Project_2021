# @Author        : Kim Suehyun
# @Since         : 2021.01.21
# @Dependency    : 
# @Description   : 영풍문고 책 카테고리 테이블 초기화

import json
import sys
sys.path.append('./source')
from util import db_conn_util

class KyoboCatInit :
    def __init__(self) :
        '''
            self.file_path -> cat1,2,3 json파일 경로 확인!
            @return (void)
        '''
        self.db = db_conn_util.PyMySQLUtil()
        self.file_path = {
            "cat1": './source/crawling/kyobobook/insert_book_category/data/kyobo_cat1.json',
        }

    def __insert_cat_1(self) :
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
                #sql = "INSERT INTO book_category VALUES(NULL,%s,%s,1,sysdate())"
                #self.db.execute_query(sql, (code, name))

    def __insert_cat_2(self) :



test= KyoboCatInit()
test.insert_cat_1()