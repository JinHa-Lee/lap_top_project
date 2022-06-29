import requests


def naver_api_crawling():
    client_id = input('What is your client_id? \n')
    client_secret = input('What is your client_password? \n')
    url = 'https://openapi.naver.com/v1/search/shop.json?query=노트북&display=100'
    params = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    res = requests.get(url, headers=params)
    if res.status_code == 200:
        data = res.json()
    else:
        print("Error Code : ", res.status_code)
    return data


