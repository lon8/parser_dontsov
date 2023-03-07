import csv
import random
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
import threading
import queue

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


with open('text.csv') as file:
    idis = [line.rstrip() for line in file]

proxies = [
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},		
]

def make_request(idi):
    sleep(1)
    response = requests.get(f'https://pro.imdb.com/title/{idi}', headers=headers, proxies=random.choice(proxies))

    print('\n\n','-----> ID: ', idi, '\n\n')

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        type = soup.find('span', id='title_type').text.replace('\n', '')
    except:
        type = "NotFound"

    name_and_date = soup.find('span', class_='a-size-extra-large').find('span', class_=False).text.split('(')
    filmname = name_and_date[0][:-1]
    try:
        date = ''.join([x for x in name_and_date[-1] if x.isdigit()] or '-')
    except:
        date = 'NotFound'
    genres = []
    try:
        genres = soup.find('span', id='genres').text.split(', ')  # list
        if len(genres) == 2:
            genres[2] = 'NotFound'
        elif len(genres) == 1:
            genres[2] = 'NotFound'
            genres[1] = 'NotFound'
    except:
        for i in range(0, 3):
            genres.append('NotFound')
    caster_list = []
    try:
        casters = soup.find('table', id='title_cast_sortable_table').find_all('tr', class_=False)
        
        for cast in casters:
            caster = cast.find('div', class_='a-section').find('span', class_='a-size-base-plus').text
            caster_list.append(caster) # caster_list[0 - 3]
        caster_list = caster_list[:4]
        if len(caster_list) == 3:
            caster_list[3] == "NotFound"
        elif len(caster_list) == 2:
            caster_list[3] == "NotFound"
            caster_list[2] == "NotFound"
        elif len(caster_list) == 1:
            caster_list[3] == "NotFound"
            caster_list[2] == "NotFound"
            caster_list[1] == "NotFound"
        print('\n\n', caster_list, '\n\n')
    except:
        for i in range(1, 5):
            caster_list.append('NotFound')
    try:
        director = soup.find('div', id='director_summary').find('a', class_='a-size- a-align- a-link- ttip').text
    except:
        director = "NotFound"
    creator = 'NotFound'
    novel_str = ''
    try:
        spans_writer = soup.find('div', id='writer_summary').find_all('span', class_='a-color-secondary')
        for span_writer in spans_writer:
            s_w = span_writer.text
            if '"' in s_w:
                novel = s_w.split('"')[1::2]
                novel_str = ''.join(novel)
                break
            else:
                continue
    except:
        pass


    try:
        spans_creator = soup.find('div', id='creator_summary').find_all('span', class_='a-color-secondary')
        for span_creator in spans_creator:
            s_c = span_creator.text
            if '"' in s_c:
                novel = novel.s_c('"')[1::2]
                novel_str = ''.join(novel)
                break
            else:
                novel = "NotFound"
                continue
    except:
        pass


    try:
        writer = soup.find('div', id='writer_summary').find('a', class_='a-size- a-align- a-link- ttip').text
    except:
        writer = 'NotFound'
        try:
            creator = soup.find('div', id='creator_summary').find('a', class_='a-size- a-align- a-link- ttip').text
        except:
            creator = 'NotFound'
    box_office = soup.find('div', id='box_office_summary')
    try:
        budget = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[0].text.replace(' ', '')
    except:
        budget = "NotFound"
    try:
        gross_us = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[2].text.replace(' ', '')
    except:
        gross_us = "NotFound"
    try:
        gross_world = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[3].text.replace(' ', '')
    except:
        gross_world = "NotFound"
    try:
        box_rating = soup.find('div', id='rating_breakdown')

        rating = box_rating \
            .find('div', class_='a-fixed-right-grid-col a-col-left') \
            .find_all('span',class_='a-size-medium')[1] \
            .text \
            .replace('\n', '')
        
        votes = box_rating \
            .find('div', class_='a-fixed-right-grid-col a-col-left') \
            .find('span',class_="a-size-small a-color-secondary") \
            .text.split('|')[-1] \
            .replace(u'\xa0', u'') \
            .replace('\n', '') \
            .replace('votes', '') \
            .replace(' ', '')
    except:
        rating = "NotFound"
        votes = "NotFound"
    
    with open('result.csv', 'a', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow((
            idi,
            filmname,
            date,
            genres[0],
            genres[1],
            genres[2],
            caster_list[0],
            caster_list[1],
            caster_list[2],
            caster_list[3],
            director,
            writer,
            creator,
            novel_str,
            budget,
            gross_us,
            gross_world,
            rating,
            votes,
            type
        ))

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