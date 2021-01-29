import requests

url = 'http://www.ypbooks.co.kr/'
html = requests.get(url)

print(html.status_code)
print(html.ok)