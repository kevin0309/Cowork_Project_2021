### Required Packages Installation
# selenium 3은 파이썬 3.9 이상의 최신버전에서 동작하지 않음
# conda install selenium
#
# 사용할 브라우저의 webdriver 파일 필요 ==> 크롬 87버전용 파일 첨부 chromedriver.exe

# 데탑에 설치된 웹 브라우저 어플리케이션의 드라이버를 사용해 브라우저 직접 조작 가능
# ==> 동적 웹페이지 렌더링 가능

from selenium import webdriver

from pprint import pprint

# 브라우저용 webdriver 로딩

# 에러 로그 발생 ==> USB: usb_device_handle_win.cc:1020 Failed to read descriptor from node connection: 시스템에 부착된 장치가 작동하지 않습니다. (0x1F)
# 에러 로그 방지용 코드
# wd_options = webdriver.ChromeOptions()
# wd_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# wd = webdriver.Chrome('chromedriver.exe', options=wd_options)

# 일반적인 코드
wd = webdriver.Chrome('chromedriver.exe')
wd.implicitly_wait(3)

wd.get('https://www.youtube.com/')

wd.implicitly_wait(3)

# 렌더링 완료된 페이지에서 해당 js 코드를 실행시켜 렌더링 완료된 html 소스 가져오기
html = wd.execute_script("return document.documentElement.outerHTML")

pprint(html)