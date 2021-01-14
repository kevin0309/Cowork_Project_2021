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

    def get_connection(self, autocommit=True, timeout=10) :
        '''
            @param autocommit: (bool) MySQL autocommit 옵션
            @param timeout: (int) MySQL timeout 옵션
            @return (pymysql.connections.Connection) 커넥션 객체
        '''
        return pymysql.connect(
            user = PyMySQLUtil.USER,
            passwd = PyMySQLUtil.PASSWD,
            host = PyMySQLUtil.HOST,
            db = PyMySQLUtil.DB,
            port = PyMySQLUtil.PORT,
            charset = PyMySQLUtil.CHARSET,
            autocommit = autocommit,
            connect_timeout = timeout
        )

    # TODO: PreparedStatement 기능 구현?
    