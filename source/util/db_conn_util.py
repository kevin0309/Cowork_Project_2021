# @Author        : Park YuHyeon
# @Since         : 2021.01.14
# @Dependency    : pymysql
# @Description   : MySQL 유틸
# 1. get_connection : DB 커넥션을 받아오는 함수

import pymysql
import re
from datetime import datetime as dt

class PyMySQLUtil :
    __USER = 'root'
    __PASSWD = 'qwer1234'
    __HOST = 'cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com'
    __DB = 'Cowork'
    __PORT = 3306
    __CHARSET = 'utf8'

    __PARAM_REGEXP_PREFIX = '#{'
    __PARAM_REGEXP_SUFFIX = '}'

    def __init__(self, set_conn=True) : 
        if set_conn :
            self.conn = self.get_connection()

    def get_connection(self, autocommit=True, timeout=10) :
        '''
            @param autocommit: (bool) MySQL autocommit 옵션
            @param timeout: (int) MySQL timeout 옵션
            @return (pymysql.connections.Connection) 커넥션 객체
        '''
        self.conn = pymysql.connect(
            user = PyMySQLUtil.__USER,
            passwd = PyMySQLUtil.__PASSWD,
            host = PyMySQLUtil.__HOST,
            db = PyMySQLUtil.__DB,
            port = PyMySQLUtil.__PORT,
            charset = PyMySQLUtil.__CHARSET,
            autocommit = autocommit,
            connect_timeout = timeout
        )

        return self.conn

    def execute_query(self, query, params={}) : 
        '''
            @param query: (string) 실행시킬 쿼리문 #{parameter key}를 사용하여 파라미터 세팅 가능
            @param params: (dictionary) {"key": "value", "key2": "value2" ....} 파라미터의 key, value pair를 갖는 객체
            @return (tuple) 쿼리 실행 결과
        '''
        query_param_keys = self.__analyze_query(query)
        missing_keys = self.__match_params(query_param_keys, params)

        if len(missing_keys) == 0 :
            excute_query = self.__generate_query_str(query, query_param_keys, params)
            cursor = self.conn.cursor()
            cursor.execute(excute_query)
            res = cursor.fetchall()
            return res
        else :
            raise ValueError('쿼리에 지정한 파라미터가 params에 정의되지 않았습니다.', missing_keys)

    def __analyze_query(self, query) :
        '''
            쿼리문에 파라미터가 지정되어있는지 먼저 확인하는 함수
            @param query: (string) 분석할 쿼리문
            @return (list) 지정되어있는 파라미터들의 키값의 배열
        '''
        prefix_len = len(PyMySQLUtil.__PARAM_REGEXP_PREFIX)
        suffix_len = len(PyMySQLUtil.__PARAM_REGEXP_SUFFIX)
        regexp_str = PyMySQLUtil.__PARAM_REGEXP_PREFIX + '[^<]+' + PyMySQLUtil.__PARAM_REGEXP_SUFFIX
        regexp = re.compile(regexp_str)
        param_keys = regexp.findall(query)

        for i in range(len(param_keys)) : 
            param_keys[i] = param_keys[i][prefix_len:len(param_keys[i])-suffix_len]   # 내용부분 추출

        return param_keys

    def __match_params(self, param_keys, params) :
        '''
            쿼리문에 지정된 파라미터의 키가 사용자가 params로 넘겨준 파라미터에 존재하는지 확인하는 함수
            @param param_keys (list) 확인할 파라미터 키 배열
            @param params (dictionary) 파라미터가 존재하는지 확인할 객체 
            @return (list) 존재하지 않는 키값(string)을 배열로 만들어 반환
        '''
        missing_keys = []

        for key in param_keys :
            try :
                params[key]
            except KeyError :
                missing_keys.append(key)                

        return missing_keys

    def __generate_query_str(self, query, param_keys, params) :
        '''
            최종적으로 execute 시킬 쿼리문을 생성하는 함수
            @param query: (string) 처음 입력받은 쿼리문
            @param param_keys: (list) 세팅해야 할 파라미터 키값 목록
            @param params: (dictionary) 파라미터 값 저장 객체
            @return (string) 실행시킬 쿼리
        '''
        for key in param_keys :
            target = PyMySQLUtil.__PARAM_REGEXP_PREFIX + key + PyMySQLUtil.__PARAM_REGEXP_SUFFIX
            value_str = ''
            
            if str(type(params[key])) == "<class 'int'>" :
                value_str = self.__get_int_value(params[key])
            elif str(type(params[key])) == "<class 'float'>" :
                value_str = self.__get_float_value(params[key])
            elif str(type(params[key])) == "<class 'str'>" :
                value_str = self.__get_str_value(params[key])
            elif str(type(params[key])) == "<class 'datetime.datetime'>" :
                value_str = self.__get_datetime_value(params[key])
            else :
                value_str = self.__get_etc_value(params[key])

            query = query.replace(target, value_str)
        return query

    def __get_int_value(self, value) :
        return str(value)
        
    def __get_float_value(self, value) :
        return str(value)
        
    def __get_str_value(self, value) :
        res = value.replace('"', '""')
        res = '"' + res + '"'
        return res
        
    def __get_datetime_value(self, value) :
        res = 'timestamp(date_format("'+value.strftime("%Y.%m.%d %H:%M:%S")+'", "%Y.%m.%d %H:%M:%S")'
        return res
        
    def __get_etc_value(self, value) :
        return str(value)


    def close_conn() :
        '''
            객체 사용 후 마지막에 꼭 close 시킬것!
        '''
        self.conn.close()

    # TODO: PreparedStatement 기능 구현?
    
p = PyMySQLUtil()
sql = 'select * from book_info where book_seq > #{seq} and publisher = #{pub} limit 1'
res = p.execute_query(sql, {"seq": 10, "pub": "동아출판"})
print(res)