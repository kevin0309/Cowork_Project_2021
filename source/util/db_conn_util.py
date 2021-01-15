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
    #__HOST = 'cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com' #cowork-rds
    __HOST = 'test-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com' #test-rds
    __DB = 'Cowork'
    __PORT = 3306
    __CHARSET = 'utf8'

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

    def execute_query(self, query, params=[]) : 
        '''
            @param query: (string) 실행시킬 쿼리문
            @param params: (list) 파라미터 배열
            @return (tuple) 쿼리 실행 결과
        '''
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close_conn() :
        '''
            객체 사용 후 마지막에 꼭 close 시킬것!
        '''
        self.conn.close()

    # TODO: PreparedStatement 기능 구현?

