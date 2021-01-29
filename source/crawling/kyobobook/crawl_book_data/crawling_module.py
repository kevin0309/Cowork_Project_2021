# @Author        : Kim SueHyun
# @Since         : 2021.01.14
# @Dependency    : 
# @Description   : 영풍문고 책 정보 크롤링 모듈

import os
import sys
sys.path.append('./source')
from datetime import datetime
import threading

import page_crawler
import http_error
from util import db_conn_util

class CrawlingModule:
    def __init__(self):
        self.db= db_conn_util.PyMySQLUtil()

    def __select_category_code(self):
        '''
            DB에 연결하여 책 카테고리가 c3인 code와 category_seq를 반환하는 함수
            @return (tuple)책 카테고리 코드(category_seq, code)  
        '''
        #sql= "SELECT category_seq, code FROM book_category where char_length(code)=6"
        sql= "select category_seq, code from book_category where category_seq not in (select distinct category_seq from book_info) and category_seq >= 236;"
        return self.db.execute_query(sql)
    
    def __insert_book_info(self, category_seq, books, t_index):  
        '''
            get_page_crawler에서 반환한 책 정보를 DB에 저장하는 함수
            @param category_seq: (int) C3 카테고리 seq
            @param books: (list) 책 정보 객체가 담긴 리스트
            @return (void)
        '''
        for book in books:  #book의 keys: name, author, publisher, pub_date, price, pages, [tags]
            name= book["name"]
            author= book["author"]
            publisher= book["publisher"]
            pub_date= book["pub_date"] #datetime
            price= book["price"] 
            pages= book["pages"] 
            img_url = book["img_url"]
            tags= book["tags"] #list

            sql= "INSERT INTO book_info VALUES(NULL,%s,NULL,%s,%s,%s,%s,%s,%s,%s,sysdate())"    #book_info 테이블에 책 정보 삽입
            book_seq= self.db_conn_list[t_index].execute_query(sql, (name, author, publisher, pub_date, category_seq, price, pages, img_url))

            sql1= "SELECT book_seq from book_info order by book_seq desc limit 1"   #book_info 테이블에 가장 최근에 입력된 row의 book_seq 조회               
            book_seq= self.db_conn_list[t_index].execute_query(sql1)

            for tag in tags:
                sql2= "INSERT INTO book_tags VALUES(NULL, %s, %s,sysdate())"        #book_tags 테이블에 태그 삽입
                self.db_conn_list[t_index].execute_query(sql2, (book_seq[0][0],tag))

        print(category_seq, datetime.now()) #카테고리별 종료시간 출력
               
    def get_page_crawler(self, thread_cnt, fixed_pub_date_start, fixed_pub_date_end):
        '''
            DB에서 가져온 c3 카테고리로 page_crawler를 호출하는 함수
            @param thread_cnt: (int)동시에 진행할 크롤링 쓰레드 개수
            @param fixed_pub_date_start: (datetime) 크롤링 할 데이터를 필터링하는 기준일
            @param fixed_pub_date_end: (datetime) 크롤링 할 데이터를 필터링하는 기준일
            @return (void)
        '''
        self.__start_date = fixed_pub_date_start
        self.__end_date = fixed_pub_date_end
        self.__category_list= self.__select_category_code()
        self.__next_category_cnt = 0
        self.__error_category_list = []
        self.lock = threading.Lock()

        self.db_conn_list = []
        thread_list = []
        for i in range(thread_cnt) :    #쓰레드 생성
            self.db_conn_list.append(db_conn_util.PyMySQLUtil())
            temp_thread = threading.Thread(target=self.__crawl_next, args=(i,))
            temp_thread.daemon = True
            temp_thread.start()
            thread_list.append(temp_thread)

        for t in thread_list:           #쓰레드 종료까지 대기
            t.join()

        for i in range(thread_cnt) :    #쓰레드 종료 후 db 연결 종료
            self.db_conn_list[i].close_conn()
        self.db.close_conn()

        print('페이지 오류로 실행되지 못한 카테고리 리스트')
        print(self.__error_category_list)
        print(len(self.__error_category_list))

    def __crawl_next(self, t_index) :
        '''
            쓰레드에서 실행할 재귀함수
            다음 작업할 카테고리를 조회하여 크롤링한다
            @return (void)
        '''
        self.lock.acquire()
        if self.__next_category_cnt >= len(self.__category_list) :
            self.lock.release()
            return
        category_seq= self.__category_list[self.__next_category_cnt][0]
        code = self.__category_list[self.__next_category_cnt][1]
        print(t_index,'thread start -', code, category_seq)
        self.__next_category_cnt += 1
        self.lock.release()

        try : 
            books= page_crawler.PageCrawler().get_book_info_from_cat3(code, self.__start_date, self.__end_date)
            self.__insert_book_info(category_seq, books, t_index)
        except :
            print('page error occured -', code, category_seq)
            self.lock.acquire()
            self.__error_category_list.append([category_seq, code])
            self.lock.release()

        self.__crawl_next(t_index)

test= CrawlingModule()
fixed_pub_date_start = datetime.strptime('1000.01.01', '%Y.%m.%d')
fixed_pub_date_end = datetime.strptime('2021.01.21 23:59:59', '%Y.%m.%d %H:%M:%S')
#fixed_pub_date_end = datetime.datetime.combine(datetime.date(2021, 1, 16), datetime.time(23, 59, 59))
test.get_page_crawler(5, fixed_pub_date_start, fixed_pub_date_end)

