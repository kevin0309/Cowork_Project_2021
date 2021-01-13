import requests
from bs4 import BeautifulSoup

def get_list(catesearch, sortField, c3, starCnt, showCnt):
    count= 0
    url= "http://www.ypbooks.co.kr/search.yp?catesearch="+catesearch+"&sortField="+sortField+"&c3="+c3+"&startCnt="+starCnt+"&showCnt="+showCnt+""
    response= requests.get(url)
    if response.status_code == 200:
        html= response.text
        soup= BeautifulSoup(html, 'html.parser')    #soup 객채로 변환
        lists= soup.findAll("dl",{"class":"info01"})
        for i in lists:
            count+=1
            print(str(count)+"번째 책정보"+i.text)
        return 0
    else:
        return(response.status_code)
        
get_list("true","DATE","100101","0","1000")