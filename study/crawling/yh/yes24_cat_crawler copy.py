import requests
from bs4 import BeautifulSoup
import re
import pprint
import json

# 중간중간 비어있는 category number가 있음
# ==> 수정 필요 재귀함수에서 000 ~ 999 다 서치하도록 변경할 필요 있음

def find_child(tree, depth, index, path) :
    url = 'http://www.yes24.com/24/Category/Display/' + path + '%03d' % index
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    if not soup.find(text = re.compile('잘못된 전시분류입니다.')) :
        soup = BeautifulSoup(html.content, 'html.parser')
        temp_cat = {
            "code": path + '%03d' % index,
            "name": soup.find('h3', attrs={'class':'cateTit_txt'}).text,
            "children": []
        }
        tree.append(temp_cat)
        print(temp_cat['code'])
        #pprint.PrettyPrinter(indent = 4).pprint(cat_tree)
        find_child(temp_cat['children'], depth+1, 1, temp_cat['code'])
        find_child(tree, depth, index+1, path)


cat_tree = []
#find_child(cat_tree, 1, 1, '')

for i in range(10, 100, 2) : 
    cat_tree.append([])
    for j in range(1, 100) : 
        cat_tree[i].append([])
        for k in range(1, 100) :
            code = '%02d' % i + '%02d' % j + '%02d' % k
            url = 'https://www.ypbooks.co.kr/search.yp?catesearch=true&collection=books_kor&sortField=DATE&c3=' + code
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'html.parser')
            res_num = -1;
            try :
                res_num = int(soup.select('#searchresult > div.result > span.bookQuantity > strong')[0].text)
            except :
                pass
            
            if res_num != -1 :
                temp_cat = {
                    "code": code,
                    "name": soup.find('h3', attrs={'class':'cateTit_txt'}).text
                }
            print(res_num)

#with open('yes24_cat.json', 'w', encoding='UTF-8') as json_file :
    #json.dump(cat_tree, json_file)
    #json.dump(cat_tree, json_file, indent = 4, ensure_ascii = False)
