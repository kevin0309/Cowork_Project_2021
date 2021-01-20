import pymysql
import json

#host = 'cowork-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com' #cowork-rds
host = 'test-rds.c9acto1zciwv.ap-northeast-2.rds.amazonaws.com' #test-rds

# MySQL Connection 연결
conn = pymysql.connect(host=host, 
    user='root', password='qwer1234', db='Cowork', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

with open('./source/crawling/insert_book_category/data/yp_cat1.json', encoding='UTF-8') as cat1_json :
    cat1 = json.load(cat1_json)
    
    with open('./source/crawling/insert_book_category/data/yp_cat2.json', encoding='UTF-8') as cat2_json :
        cat2 = json.load(cat2_json)
        for cat2_code in cat2.keys() :
            parent_node = list(cat1.keys()).index(cat2_code[:2]) +2
            print('p:',parent_node,'code:',cat2_code)
            curs.execute("INSERT INTO book_category VALUES(NULL, '"+cat2_code+"', '"+cat2[cat2_code]+"', '"+str(parent_node)+"', sysdate());")




conn.commit()        
 
#     # 전체 rows
# for i in rows:
#     print (i)



# Connection 닫기
conn.close()