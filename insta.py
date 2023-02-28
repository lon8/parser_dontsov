import requests
import json 
import argparse
import requests

headers = {
    'authority': 'www.instagram.com',
    'accept': '/',
    'accept-language': 'ru,en;q=0.9',
    'cookie': 'ig_did=1C4022FF-7A8E-4284-8E77-339CD0133C49; ig_nrcb=1; mid=Y-0f4QAEAAGiw6H49NfQLhs-6DNl; datr=xh_tY01Vm9xrn-6jpbOb5o-l; csrftoken=W0DvgBvoygAIjgwaI5YEZ2CbhNvzK9pU; ds_user_id=16417251805; shbid="18126\05416417251805\0541708020678:01f7b0d1f58876ffbf92d8edcd7a005404de77b5459e0300e795ddc8bfd1c30b8b7c2049"; shbts="1676484678\05416417251805\0541708020678:01f769166d68a80c08d8ff26d4ff318a3ad4d4ea935d0d5ea8249ce8a668e2cb3751924e"; sessionid=16417251805%3AGuiTtpdbbSQ1Ta%3A14%3AAYeEwMLeptP8nYDMKZDIA6_MP0SL0aAGzA02ULqp3w; rur="NCG\05416417251805\0541708025413:01f7e7d342800a6f3ff2a6402d17f1bc7a3156fb03006bc831603613d2fae6e4d494883b"',
    'referer': 'https://www.instagram.com/ger_man204/',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0.2; SM-G530H Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36 YandexSearch/5.40',
    'x-asbd-id': '198387',
    'x-csrftoken': 'W0DvgBvoygAIjgwaI5YEZ2CbhNvzK9pU',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2B8GGn7gJyKajZzlUyYtir0LYhUAhYplym5Ga-yB7qZY1a',
    'x-requested-with': 'XMLHttpRequest',
}


def parce_data(username:str):
    params = {
        'username': f'{username}',
    }

    response = requests.get(
        'https://www.instagram.com/api/v1/users/web_profile_info/',
        params=params,
        headers=headers,
    )

    data = response.json()

    return data['data']['user']['full_name'], data['data']['user']['biography_with_entities']['raw_text']


parser = argparse.ArgumentParser(description='Instagram info parser v0.1')

parser.add_argument('filters', type=str, help='Path to filters file')
parser.add_argument('hrefs', type=str, help='Path to input hrefs file')
parser.add_argument('output', type=str, help='Path to output hrefs file')
args = parser.parse_args()

file = open(args.filters, encoding="utf8")
filters = file.readlines()
file.close()

file = open(args.hrefs)
hrefs = file.readlines()
file.close()


def cleaner(format_text):
    for ch in ['\n', '\t', ' ']:
        if ch in format_text:
            format_text = format_text.replace(ch, "")

    return format_text


validated = []

for h in hrefs:
    user = cleaner(h.replace("https://www.instagram.com/", '').replace('/', ''))
    for parsed in parce_data(user):
        for validator in filters:
            if validator.lower().replace('\n', '') in parsed.lower():
                validated.append(cleaner(h))


file = open(args.output, 'w')
file.writelines(line + '\n' for line in validated)
file.close()