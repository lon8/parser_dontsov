import csv
import random
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
import threading
import queue
import pandas as pd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'ubid-main=132-4642849-1346340; signup-offer-territory=WW; _gcl_au=1.1.166086762.1677573559; signup-offer-term=B073C6VV42; signup-offer-duration=year; _uetsid=7ccad020b74211ed9d6aa962b4d8f7e5; _uetvid=7ccb0db0b74211eda5aad75799f116bf; session-id=144-2309239-3684200; x-main=e2R4xua1iS16MO1XgCmi6CfGg7Ba2ea4LHrY7W3gU7nmkgdEaWhMmGyRO0FCGjN7; at-main=Atza|IwEBIKdRPEqS0RpptofdZ5qE1IfufPpF09hLANRhMALNK_R7eNVcDoquMLkFUS9iqfNjDNdPVLgxNVA2OT05TWQCReC4GBVQULR6hlit24hemCLw_y9lbRJCLaJEgr5La383AADJcgVKTYhIAW-lOyc8k34R4HB5-rw8x4SoKndWKPYru2jbU9E0ljqbbL0I1WFu5R6fAJfd0a-wYkm1rnUXF5V9xhUZDlGMoxpbwRyGGLR6OA; sess-at-main="GkGfpIHiFZaMIRBEc2SFpr66dxgXpB0e+bNjC/CFOBg="; uu=eyJpZCI6InV1NDY5M2U3MDVjMjJhNGVkOGJkZGUiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfSwidWMiOiJ1cjE2Mjc4NTY0OCJ9; session-id-time=2082787201l; csm-hit=tb:1909E010XQTT3HERXB1H+s-D37HC9EE92HH39F4NFET|1677580366500&t:1677580366500&adb:adblk_yes; session-token=tKRGQNjjk/S6GyHpHqq/m7kD93/YW6lOvoHrd7pgsilpJDcDy2lTXv0olLhhsTHZ1DpPd/dKAwdgHi+5jK8xevR3lVdRbtk7mNc0cntIoL3UV6uh295uJsswAuCdqd5Cuc/OTvurqg2mbMNFjz6bzXB43rK4/BPxbMPrTab+Aydefrs8uHxX9xjXlP1ebz1amVOD78egAxnN3sHFiZ/JF00v4+qmZ8RIeDVpbZCuk7ftE1xjD9uKeZimmy4q/cfibojbvY+SNmk',    'Referer': 'https://pro.imdb.com/?rf=cons_nb_hm&ref_=cons_nb_hm',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.996 (beta) Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

with open('text.csv', 'r', encoding='utf-8') as file:
    idis = [line.rstrip() for line in file]

print(1)

proxies = [
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},		
]

def make_request(idi):
    sleep(1)
    response = requests.get(f'https://pro.imdb.com/title/{idi}/details', headers=headers) #, proxies=random.choice(proxies)

    print('\n\n','-----> ID: ', idi, '\n\n')

    soup = BeautifulSoup(response.text, 'lxml')
    div = []
    try:
        div = soup.find('div', id='release_details').find('td').text.split(', ')
    except:
        div.append("NotFound")
    div_f = ','.join(div)
    
    with open('result_countries.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((
            idi, div_f
        ))
    
    print('Done!')

def worker(q):
    while True:
        idi = q.get()
        make_request(idi)
        q.task_done()

concurrent_requests = 15
q = queue.Queue()
for idi in idis:
    q.put(idi)

threads = []
for i in range(concurrent_requests):
    thread = threading.Thread(target=worker, args=(q,))
    threads.append(thread)
    thread.start()

q.join()

for thread in threads:
    thread.join()