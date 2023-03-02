import random
from bs4 import BeautifulSoup
import requests
from fp.fp import FreeProxy

def recurse_request():
    try:
        req = requests.get(f'https://www.instagram.com/api/v1/friendships/451169625/followers/?count=50&max_id={max_id}', headers=headers, proxies=proxies)
        return req
    except:
        recurse_request()

proxy_list = []
for i in range (1, 16):
    try:
        proxy = FreeProxy(https=True, elite=True).get()
        proxy_list.append(proxy)
    except: break

headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'cookie': 'ig_did=1C4022FF-7A8E-4284-8E77-339CD0133C49; ig_nrcb=1; mid=Y-0f4QAEAAGiw6H49NfQLhs-6DNl; datr=xh_tY01Vm9xrn-6jpbOb5o-l; shbid="18126\\05416417251805\\0541709071917:01f788b5f1ecba153fa7839881b9746e2abe9413b16f31963a2fd2da413eb3f9a6369a1e"; shbts="1677535917\\05416417251805\\0541709071917:01f7c56ac90549c6de33b05b76bfb74049e7ee881d7ace95407b5964a3d5193c86e75ab9"; csrftoken=OJYNRyYFCvroxEPkNikmBqGo56oOnI3K; ds_user_id=16417251805; sessionid=16417251805%3AdVbrlA1Bj9VPsp%3A5%3AAYdlXSQWFSUUhgHF3TMMQjiQJpi4vrObfXiv9--0NQ; rur="CLN\\05416417251805\\0541709148609:01f79174cdcc16f02ba0a99d00effb0c67c2ea15b948c1661d94cfa9caa831687361df64"',
    'referer': 'https://www.instagram.com/perspectiva.ru/followers/',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.996 (beta) Yowser/2.5 Safari/537.36',
    'x-asbd-id': '198387',
    'x-csrftoken': 'OJYNRyYFCvroxEPkNikmBqGo56oOnI3K',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2B8GGn7gJyKajZzlUyYtir0LYhUAhYplym5Ga-yB7qZdEI',
    'x-requested-with': 'XMLHttpRequest',
}


proxies = {
    "https": random.choice(proxy_list)
}

usernames = []

first_request = requests.get('https://www.instagram.com/api/v1/friendships/451169625/followers/?count=50&max_id=QVFBUEJ2QmZhTzhWYmJUa1VvZ1FPSzMtN0pzc2kwNTBUOHdwZXAzSElzVkUtY0tnSExHajNGczJISW5lbThGOWhydnN3em1OUW9xYUtMYmFBRTVVbzB0SA==', headers=headers, proxies=proxies)

first_data = first_request.json()

first_users_data = first_data['users']

for item in first_users_data:
    usernames.append(item['username'])

max_id = first_data['next_max_id']

for i in range(1, 3199):

    proxies = {
    "https": random.choice(proxy_list)
    }
    
    req = recurse_request()

    data = req.json()

    users_data = data['users']

    for item in users_data:
        usernames.append(item['username'])
    
    max_id = data['next_max_id']
    print('\n\n', '-----> Успешно записали пользователей. MAX_ID ===> ', max_id, '\n\n')

with open('users.txt', 'w', encoding='utf-8') as file:
    for item in usernames:
        file.write("%s\n" % item)

print(1)