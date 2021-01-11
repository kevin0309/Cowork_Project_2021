import requests
from bs4 import BeautifulSoup
import re
import pprint
import json

cat_tree = []
tree_depth = 1

def find_child(tree, depth, index, path) :
    url = 'http://www.yes24.com/24/Category/Display/' + path + '%03d' % index
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    if not soup.find(text = re.compile('잘못된 전시분류입니다.')) :
        soup = BeautifulSoup(html.content, 'html.parser')
        category_str = path + '%03d' % index
        cat = {
            "code": path + '%03d' % index,
            "name": soup.find('h3', attrs={'class':'cateTit_txt'}).text,
            "children": []
        }
        tree.append(cat)
        print(cat['code'])
        #pprint.PrettyPrinter(indent = 4).pprint(cat_tree)
        find_child(cat['children'], depth+1, 1, path + '%03d' % index)
        find_child(tree, depth, index+1, path)
    
find_child(cat_tree, 1, 1, '')
with open('yes24_cat.json', 'w', encoding='UTF-8') as json_file :
    #json.dump(cat_tree, json_file)
    json.dump(cat_tree, json_file, indent = 4, ensure_ascii = False)
