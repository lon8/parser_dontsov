import csv
from bs4 import BeautifulSoup
import requests

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

# with open('result.csv', 'w') as file:
#     wr = csv.writer(file)
#     wr.writerow((
#         "ID",
#         "Film Name",
#         "Date",
#         "Genres",
#         "Top Actors",
#         "Director",
#         "Writer",
#         "Creator (If writer isn't found)"
#         "Book",
#         "Budget",
#         "Gross US",
#         "Gross World",
#         "Rating",
#         "Votes"
#     ))

with open('num_voices.csv', 'r') as file:
    ids = [line.rstrip() for line in file]

for i in range(1533, 40001):
    film_id = ids[i-1]
    response = requests.get(f'https://pro.imdb.com/title/{film_id}', headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    name_and_date = soup.find('span', class_='a-size-extra-large').find('span', class_=False).text.split('(')
    filmname = name_and_date[0][:-1]
    try:
        date = ''.join([x for x in name_and_date[1] if x.isdigit()])
    except:
        date = 'NotFound'
    genres = soup.find('span', id='genres').text.split(', ') # list
    caster_list = []
    try:
        casters = soup.find('table', id='title_cast_sortable_table').find_all('tr', class_=False)
        
        for cast in casters:
            caster = cast.find('div', class_='a-section').find('span', class_='a-size-base-plus').text
            caster_list.append(caster)
        print('\n\n', caster_list, '\n\n') # caster_list[0 - 3]
    except:
        caster_list.append('NotFound')
    try:
        director = soup.find('div', id='director_summary').find('a', class_='a-size- a-align- a-link- ttip').text
    except:
        director = "NotFound"
    creator = 'NotFound'
    try:
        writer = soup.find('div', id='writer_summary').find('a', class_='a-size- a-align- a-link- ttip').text
        novel = soup.find('div', id='writer_summary').find('div', class_='a-fixed-left-grid-col a-col-right').find('span', class_='a-color-secondary').text
        novel = novel.split('"')[1::2]
    except:
        writer = 'NotFound'
        novel = 'NotFound'
        try:
            creator = soup.find('div', id='creator_summary').find('a', class_='a-size- a-align- a-link- ttip').text
        except:
            creator = 'NotFound'
    box_office = soup.find('div', id='box_office_summary')
    try:
        budget = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[0].text.replace(' ', '')
        gross_us = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[2].text.replace(' ', '')
        gross_world = box_office.find_all('div', class_='a-column a-span5 a-text-right a-span-last')[3].text.replace(' ', '')
    except:
        budget = "NotFound"
        gross_us = "NotFound"
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
            .replace('\n', '')
    except:
        rating = "NotFound"
        votes = "NotFound"
    
    with open('result.csv', 'a', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow((
            film_id,
            filmname,
            date,
            " | ".join(genres),
            " | ".join(caster_list[:4]),
            director,
            writer,
            creator,
            novel,
            budget,
            gross_us,
            gross_world,
            rating,
            votes
        ))
        # "ID",
        # "Film Name",
        # "Date",
        # "Genres",
        # "Top Actors",
        # "Director",
        # "Writer",
        # "Creator (If writer isn't found)"
        # "Book",
        # "Budget",
        # "Gross US",
        # "Gross World",
        # "Rating",
        # "Votes"


    print('\n\n','----> Номер ID:', i,'-----> ID: ', film_id, '\n\n')