# @Author        : Park YuHyeon
# @Since         : 2021.01.14
# @Dependency    : pymysql
# @Description   : MySQL 유틸
# 1. get_connection : DB 커넥션을 받아오는 함수

import pymysql

class PyMySQLUtil :
    USER = 'root'
    PASSWD = 'qwer1234'
    HOST = 'cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com'
    DB = 'Cowork'
    PORT = 3306
    CHARSET = 'utf8'

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
            user = PyMySQLUtil.USER,
            passwd = PyMySQLUtil.PASSWD,
            host = PyMySQLUtil.HOST,
            db = PyMySQLUtil.DB,
            port = PyMySQLUtil.PORT,
            charset = PyMySQLUtil.CHARSET,
            autocommit = autocommit,
            connect_timeout = timeout
        )

        return self.conn

    def excute_query(self, query) : 
        '''
            @param query: (string) 실행시킬 쿼리문
            @return (tuple) 쿼리 실행 결과
        '''
        cursor = self.conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return res

    def close_conn() :
        '''
            객체 사용 후 마지막에 꼭 close 시킬것!
        '''
        self.conn.close()

    # TODO: PreparedStatement 기능 구현?
    