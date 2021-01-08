### Required Packages Installation
# conda install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

from pprint import pprint

url = 'https://www.youtube.com/'
html = requests.get(url)
# async 요청에 대해서 처리할 수 없음 
# ==> 데이터를 async요청으로 받아오는 페이지일 경우 데이터를 뽑아내지 못함
# ==> 일반적으로 정적 웹페이지에만 사용 가능 (데이터가 포함된 api에 바로 요청할 수 있다면 사용가능)
soup = BeautifulSoup(html.content, 'html.parser')

#pprint(soup.prettify())

for link in soup.find_all('a') :
    pprint(link.get('href'))