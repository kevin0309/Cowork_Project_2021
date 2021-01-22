#@Author        : Park YuHyeon
#@Since         : 2021.01.12
#@Dependency    : requests, BeautifulSoup4(4.9.3)
#@Description   : DB에 저장된 book_category.code값으로 영풍문고 사이트에 있는 국내도서 책 정보를 list로 반환하는 코드

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

import http_error

class PageCrawler :
    __book_name_blacklist = [
        #'.', '사용안함'
    ]

    def __get_book_info_from_page(self, cat_code, page_num, per_page) :
        '''
            @param cat_code : (string)책 카테고리 코드
            @param start_cnt: (int)시작 인덱스
            @param show_cnt : (int)간격
            @return 책 정보
        '''
        self.prev_page_num = page_num
        url = 'http://www.kyobobook.co.kr/categoryRenewal/categoryTab.laf'
        param = {
            'targetPage': str(page_num),
            'mallGb': 'KOR',
            'serviceGb': '',
            'cateDivYn': '',
            'pageNumber': str(self.prev_page_num),
            'priceVal': '',
            'perPage': str(per_page),
            'paramEjkGb': 'KOR',
            'excelYn': 'N',
            'sendEjkGb': '',
            'sendBarcode': '',
            'seeOverTn': '',
            'sortColumn': 'near_date',
            'linkClass': cat_code,
            'changeViewType': 'detail',
            'menuCode': '003',
            'cateGb': 'tab',
            'link6flag': '',
            'loginYN': 'N'
        }
        html = requests.post(url, data=param)

        if not (html.status_code == 200 and html.ok) :
            raise http_error.HTTPError('Page unavailable', url)

        soup = BeautifulSoup(html.content, 'html.parser')   #soup객체로 변환
        res = []
        book_list = soup.select('#frmList>ul>.id_detailli .info_area')
        print(len(book_list))
        for item in book_list:
            try:
                print('---------------------')
                temp_book_info = {
                    'name': item.select('.detail .title strong')[0].text.strip(),
                    'author': item.select('.detail .pub_info>.author')[0].text.strip(),
                    'publisher': item.select('.detail .pub_info>.publication')[0].text.strip(),
                    'pub_date_str': item.select('.detail .pub_info>.publication')[1].text.strip(),
                    'page': -1,
                    'price': -1
                }

                img_url = item.select('.cover_wrap .cover>a>span>img')[0].get('src')
                if img_url == 'http://image.kyobobook.co.kr/newimages/apps/b2c/product/19adult_m.gif':
                    temp_book_info['img_url'] = ''
                    temp_book_info['is_adult'] = 'Y'
                else:
                    temp_book_info['img_url'] = img_url
                    temp_book_info['is_adult'] = 'N'

                try:
                    temp_book_info['pub_date'] = datetime.strptime(temp_book_info["pub_date_str"],"%Y.%m.%d")
                except:
                    temp_book_info['pub_date'] = datetime.strptime(temp_book_info["pub_date_str"],"%Y.%m")
                
                if not self.__validate_book_info(temp_book_info) :  # 책 정보 필터링
                    raise ValueError()

                res.append(temp_book_info)
                # print(temp_book_info['name'])
                # print(temp_book_info['author'])
                # print(temp_book_info['publisher'])
                # print(temp_book_info['pub_date'])
                # print(temp_book_info['page'])
                # print(temp_book_info['price'])
                # print(temp_book_info['img_url'])
                # print(temp_book_info['is_adult'])
            except Exception as e:
                pass
        print(len(res))
        return res

    def __validate_book_info(self, book) : 
        '''
            책 정보의 유효성을 검증하는 메서드
            1. 출판일이 지정한 날짜 범위 내에 있는지
            2. 책 제목이 적절한지 (PageCrawler.__book_name_blacklist 참고)
            @param book: (dictionary) 책 정보 객체
            @return (bool) 문제 없다면 True 반환
        '''
        #기준일 사이의 출판일을 갖는 도서는 필터링
        if book['pub_date'] < self.start_date or book['pub_date'] > self.end_date  :
            return False

        #책 제목으로 필터링
        for name in PageCrawler.__book_name_blacklist : 
            if book['name'] == name :
                return False

        return True


    def get_book_info_from_cat(self, cat_code, fixed_pub_date_start, fixed_pub_date_end) : 
        '''
            @param cat_code: (string)책 카테고리 코드
            @param fixed_pub_date_start: (datetime)크롤링 할 데이터를 필터링하는 기준일
            @param fixed_pub_date_end: (datetime)크롤링 할 데이터를 필터링하는 기준일
            @return (list)책 정보
        '''
        res = []
        page_num = 1
        per_page = 20
        self.start_date = fixed_pub_date_start
        self.end_date = fixed_pub_date_end

        while True :
            print('search - cat:', cat_code, ' / index (',str((page_num - 1) * per_page),'~',str(page_num * per_page),')')
            self.prev_page_num = 1
            temp_book_list = self.__get_book_info_from_page(cat_code, page_num, per_page)
            if len(temp_book_list) == 0 :   #범위 내에 책이 없는 경우 break
                break
            else :
                res += temp_book_list
                page_num += 1
        return res


fixed_pub_date_start = datetime.strptime('1000.01.01', '%Y.%m.%d')
fixed_pub_date_end = datetime.strptime('2021.01.21 23:59:59', '%Y.%m.%d %H:%M:%S')
crawler = PageCrawler()
print(crawler.get_book_info_from_cat('010101', fixed_pub_date_start, fixed_pub_date_end))
