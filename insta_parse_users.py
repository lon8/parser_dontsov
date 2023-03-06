import random
from bs4 import BeautifulSoup
import requests
from fp.fp import FreeProxy

headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'referer': 'https://www.instagram.com/perspectiva.ru/followers/',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-asbd-id': '198387',
    'x-csrftoken': 'OJYNRyYFCvroxEPkNikmBqGo56oOnI3K',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2B8GGn7gJyKajZzlUyYtir0LYhUAhYplym5Ga-yB7qZR6Y',
    'x-requested-with': 'XMLHttpRequest',
}

proxies = [
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},		
]

usernames = []

first_request = requests.get('https://www.instagram.com/api/v1/friendships/451169625/followers/?count=50&max_id=QVFBUEJ2QmZhTzhWYmJUa1VvZ1FPSzMtN0pzc2kwNTBUOHdwZXAzSElzVkUtY0tnSExHajNGczJISW5lbThGOWhydnN3em1OUW9xYUtMYmFBRTVVbzB0SA==',headers=headers, proxies=random.choice(proxies))

first_data = first_request.json()
#157 546
first_users_data = first_data['users']

for item in first_users_data:
    usernames.append(item['username'])

with open('text.txt', 'w', encoding='utf-8') as file:
    for user in usernames:
        file.write("%s\n" % user)
usernames.clear()

max_id = first_data['next_max_id']

for i in range(1, 3199):
    
    req = requests.get(f'https://www.instagram.com/api/v1/friendships/451169625/followers/?count=50&max_id={max_id}',headers=headers, proxies=random.choice(proxies))

    data = req.json()

    users_data = data['users']

    for item in users_data:
        usernames.append(item['username'])
    
    max_id = data['next_max_id']
    print('\n\n', '-----> Успешно записали пользователей. MAX_ID ===> ', max_id, '\n\n')

    with open('users.txt', 'a', encoding='utf-8') as file:
        for item in usernames:
            file.write("%s\n" % item)

print(1)