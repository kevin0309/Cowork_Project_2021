import pymysql

conn = pymysql.connect(
    user = 'root',
    passwd = 'qwer1234',
    host = 'cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com',
    db = 'Cowork',
    port = 3306,
    charset = 'utf8'
)

c = conn.cursor()
c.execute('show tables')
result = c.fetchall()
print(result)
c.close()