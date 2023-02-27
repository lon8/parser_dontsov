import requests
import datetime
from bs4 import BeautifulSoup

req = requests.get('https://v01.ru/auto/search/k015479xs/?brand_title=GATES&extra%5Bwf_b%5D%5B0%5D=GATES%2FDATI&extra%5Bwf_b%5D%5B1%5D=GATES+%2F+KETNER&extra%5Bwf_b%5D%5B2%5D=GATES+RUBBER+COMPANY&extra%5Bwf_b%5D%5B3%5D=GATES+USA&extra%5Bwf_b%5D%5B4%5D=GATES+ВОДЯНЫЕ+НАСОСЫ&extra%5Bwf_b%5D%5B5%5D=GATES+ИНСТРУМЕНТЫ&extra%5Bwf_b%5D%5B6%5D=GATES+ПАТРУБКИ&extra%5Bwf_b%5D%5B7%5D=GATES+РЕМНИ&extra%5Bwf_b%5D%5B8%5D=GATES+РОЛИКИ&extra%5Bwf_b%5D%5B9%5D=GATES+ТЕРМОСТАТЫ&extra%5Bwf_b%5D%5B10%5D=GATES-AU&extra%5Bwf_b%5D%5B11%5D=GATES-BR&extra%5Bwf_b%5D%5B12%5D=GATES-SEA&extra%5Bwf_b%5D%5B13%5D=GATES1&extra%5Bwf_b%5D%5B14%5D=GATES')

soup = BeautifulSoup(req.text, 'lxml')


dates = soup.find_all('div', class_='icon_info fas fa-home toolttip-fade')
dates_of_issue = {}
today = datetime.datetime.today()
count = 1
for date in dates:
    data = date.get('title').replace('\n                            ', '').replace('\n                        ', '')
    datasoup = BeautifulSoup(data, 'lxml')
    src = datasoup.find_all('tr')[0].find('b').text
    final_data = datetime.datetime.strptime(src, "%H:%M %d.%m.%Y")
    dates_of_issue[count] = final_data
    count += 1
final_data_issue = {k: v for k, v in sorted(dates_of_issue.items(), key=lambda item: item[1])}
print(1)