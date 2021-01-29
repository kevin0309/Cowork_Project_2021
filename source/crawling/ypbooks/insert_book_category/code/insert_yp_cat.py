# @Author        : Park YuHyeon
# @Since         : 2021.01.20
# @Dependency    : 
# @Description   : 영풍문고 책 카테고리 테이블 초기화

import json
import sys
sys.path.append('./source')
from util import db_conn_util

class YpCatInit :
    def __init__(self) :
        '''
            self.data_path -> cat1,2,3 json파일 경로 확인!
            @return (void)
        '''
        self.db = db_conn_util.PyMySQLUtil()
        self.data_path = {
            "cat1": './source/crawling/ypbooks/insert_book_category/data/yp_cat1.json',
            "cat2": './source/crawling/ypbooks/insert_book_category/data/yp_cat2.json',
            "cat3": './source/crawling/ypbooks/insert_book_category/data/yp_cat3.json'
        }

    def __insert_cat_1(self) :
        '''
            카테고리 레벨1을 테이블에 삽입하는 메서드
            @return (void)
        '''
        with open(self.data_path["cat1"], encoding="UTF-8") as json_file:
            cat1 = json.load(json_file)
            print('insert category level 1')
            for code in cat1.keys():
                name = cat1[code]
                sql = "INSERT INTO book_category VALUES(NULL,%s,%s,1,sysdate())"
                self.db.execute_query(sql, (code, name))

    def __insert_cat_2(self):
        '''
            카테고리 레벨2을 테이블에 삽입하는 메서드
            @return (void)
        '''
        with open(self.data_path["cat1"], encoding="UTF-8") as cat1_json:
            cat1 = json.load(cat1_json)
            with open(self.data_path["cat2"], encoding="UTF-8") as cat2_json:
                cat2 = json.load(cat2_json)
                print('insert category level 2')
                for code in cat2.keys() :
                    name = cat2[code]
                    parent_code = list(cat1.keys()).index(code[:2]) + 2 # root node index
                    sql = "INSERT INTO book_category VALUES(NULL,%s,%s,%s,sysdate())"
                    self.db.execute_query(sql, (code, name, parent_code))
    
    def __insert_cat_3(self):
        '''
            카테고리 레벨3을 테이블에 삽입하는 메서드
            @return (void)
        '''
        with open(self.data_path["cat2"], encoding="UTF-8") as cat2_json:
            cat2 = json.load(cat2_json)
            with open(self.data_path["cat3"], encoding="UTF-8") as cat3_json:
                cat3 = json.load(cat3_json)
                print('insert category level 3')
                for code in cat3.keys() :
                    name = cat3[code]
                    parent_code = list(cat2.keys()).index(code[:4]) + 26 # (root node + cat 1) index
                    sql = "INSERT INTO book_category VALUES(NULL,%s,%s,%s,sysdate())"
                    self.db.execute_query(sql, (code, name, parent_code))

    def __init_table(self):
        '''
            1. 테이블 내용 삭제
            2. 테이블 auto_increment 초기화
            3. 루트노드 삽입
            @return (void)
        '''
        print('delete remaining records')
        sql = "DELETE FROM book_category"
        self.db.execute_query(sql)  # 테이블에 있던 전체 레코드 삭제
        print('init auto_increment')
        sql = "ALTER TABLE book_category AUTO_INCREMENT = 1"
        self.db.execute_query(sql)  # 테이블 AUTO_INCREMENT 초기화
        print('insert root node')
        sql = "INSERT INTO book_category VALUES(NULL,'1','국내도서',1,sysdate())"
        self.db.execute_query(sql)  # root 노드 삽입

    def run(self):
        '''
            전체 카테고리 입력작업 시작 메서드
            @return (void)
        '''
        self.__init_table()
        self.__insert_cat_1()
        self.__insert_cat_2()
        self.__insert_cat_3()
    
test = YpCatInit()
test.run()
