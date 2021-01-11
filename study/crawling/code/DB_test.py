import pymysql
import json


# MySQL Connection 연결
conn = pymysql.connect(host='cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com', user='root', password='qwer1234', db='Cowork', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

with open("./doc/yp_cat1.json", encoding="UTF-8") as json_file:
    json_data= json.load(json_file)
    json_string= json_data.keys() #book_category.code
    for code in json_string:
        name = json_data[code] #book_category.name
        # SQL문 실행
        sql = "INSERT INTO book_category VALUES(NULL,'"+code+"','"+name+"',1,sysdate())"
        curs.execute(sql)
        # 데이타 Fetch
        rows = curs.fetchall()

conn.commit()        
 
#     # 전체 rows
# for i in rows:
#     print (i)



# Connection 닫기
conn.close()