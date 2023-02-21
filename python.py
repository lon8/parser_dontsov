import requests
from bs4 import BeautifulSoup
import datetime
import csv

today_time = f'parse_{datetime.datetime.today()}.csv'

with open(today_time, 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow((
        "Товар",
        "1-ый раздел",
        "2-ой раздел",
        "3-ий раздел",
        "4-ый раздел",
        "5-ый раздел",
        "6-ой раздел",
        "Название",
        "Артикул",
        "Доставка",
        "Цена",
        "Фотографии"
    ))

for page in range(1, 29):
    req = requests.get(f'https://carbon.pro/usd/new-products/page/{page}/?wpp-filter-brend')
    soup = BeautifulSoup(req.text, 'lxml')
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
    blocks = soup.find_all('div', class_='col-xl-4 col-lg-4 col-md-6 col-sm-12 wpp-grid-item')
    for block in blocks:
        description = ''
        pictures_hrefs = []
        name = block.find('h4', class_="grid-headline-icon").text
        try:
            price = block.find('p', style="margin-bottom: 5px;").text
        except:
            price = "None"
        delivery_time = block.find('p', class_="wpp-br-time-p").text
        product = block.find('a')['href']

        req_product = requests.get(product)
        soup_product = BeautifulSoup(req_product.text, 'lxml')
        pictures = soup_product.find_all('picture')
        for picture in pictures:
            picture_href = picture.find('img')["src"]
            pictures_hrefs.append(picture_href)

        sections = soup_product.find('ul', class_='breadcrumb breadcrumb--overflow responsive-gutter section-padding-small') \
            .find_all('li')
        section_1 = sections[1].text
        section_2 = sections[2].text
        try:
            section_3 = sections[3].text
        except:
            section_3 = ' '
        try:
            section_4 = sections[4].text
        except:
            section_4 = ' '
        try:
            section_5 = sections[5].text
        except:
            section_5 = ' '
        try:
            section_6 = sections[6].text
        except:
            section_6 = ' '

        article = soup_product.find('p', class_='cart-item-number wpp_scu').text


        with open(today_time, 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                product,
                section_1,
                section_2,
                section_3,
                section_4,
                section_5,
                section_6,
                name,
                article,
                delivery_time,
                price,
                ';\n'.join(pictures_hrefs)
            ))
        print(page)