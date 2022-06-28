import requests
import pprint

client_id = ''
client_secret = ""

url = 'https://openapi.naver.com/v1/search/shop.json?query=노트북&display=100'
params = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}

res = requests.get(url, headers=params)

if res.status_code == 200:
    data = res.json()
    pprint.pprint(data)
else:
    print("Error Code : ",res.status_code)
